import os
import json
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .sync import sync_folder

class SyncHandler(FileSystemEventHandler):
    def __init__(self, folder_config):
        super().__init__()
        self.folder_config = folder_config

    def on_any_event(self, event):
        if not event.is_directory:
            # Skip files inside the .git directory and other irrelevant files
            if '.git' in event.src_path or event.src_path.endswith(('.lock', 'config', 'HEAD', 'index.lock')):
                return  # Ignore changes in .git directory files

            print(f"Change detected in {self.folder_config['folder_to_sync']}: {event.src_path}")
            sync_folder(self.folder_config)

def monitor_folders(config):
    observers = []
    for folder_config in config["folders"]:
        observer = Observer()
        folder_path = os.path.expanduser(folder_config["folder_to_sync"])
        observer.schedule(SyncHandler(folder_config), folder_path, recursive=True)
        observers.append(observer)

    try:
        print("Starting folder monitoring...")
        for observer in observers:
            observer.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping folder monitoring...")
        for observer in observers:
            observer.stop()
    for observer in observers:
        observer.join()

