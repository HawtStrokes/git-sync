# git_sync/__main__.py
from .sync import sync_folder
from .watcher import monitor_folders
import json
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Git Sync Project")
    parser.add_argument('--no-push', action='store_true', help="Disable pushing changes to remote repository")
    args = parser.parse_args()
    return args

def main():
    args = parse_arguments()
    push_changes = not args.no_push
    # Load configuration
    with open('config.json', "r") as f:
        config = json.load(f)
    # Start monitoring and syncing folders
    monitor_folders(config, push_changes=push_changes)

if __name__ == "__main__":
    main()

