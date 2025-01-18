# git_sync/__main__.py
from .sync import sync_folder
from .watcher import monitor_folders
import json

def main():
    # Load configuration
    with open("config.json", "r") as f:
        config = json.load(f)

    # Start monitoring and syncing folders
    monitor_folders(config)

if __name__ == "__main__":
    main()

