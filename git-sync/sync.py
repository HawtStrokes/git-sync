import os
import json
from git import Repo
from datetime import datetime
import fnmatch

def update_remote_url(repo_path, username, token):
    """
    Update the remote URL to include GitHub username and personal access token for authentication.
    """
    repo = Repo(repo_path)
    if len(repo.remotes) == 0:
        print(f"No remotes found in the repository at {repo_path}. Skipping remote URL update.")
        return

    origin = repo.remotes.origin
    new_url = f"https://{username}:{token}@github.com/{username}/{repo.remotes.origin.url.split('/')[-1]}"
    origin.set_url(new_url)

def should_track_file(file_path, tracked_files):
    """
    Check if a file matches any of the tracked files or patterns.
    """
    for pattern in tracked_files:
        if fnmatch.fnmatch(file_path, pattern):
            return True
    return False

def sync_folder(folder_config, push_changes=True):
    folder = os.path.expanduser(folder_config["folder_to_sync"])
    repo_url = folder_config["repo_url"]
    branch = folder_config["branch"]
    commit_message_template = folder_config["commit_message"]
    username = folder_config["username"]
    token = folder_config["token"]
    tracked_files = folder_config.get("tracked_files", [])  # Get tracked files list

    # Initialize or open Git repo
    if not os.path.exists(os.path.join(folder, ".git")):
        print(f"Initializing repository at {folder}...")
        Repo.init(folder)

    repo = Repo(folder)

    # Only update remote URL if push_changes is True (no need to do this if we're not pushing)
    if push_changes:
        update_remote_url(folder, username, token)

    # Collect the files to commit (only those that are tracked)
    tracked_changes = []
    for file_path in repo.untracked_files:
        if should_track_file(file_path, tracked_files):
            tracked_changes.append(file_path)
    for item in repo.index.diff(None):  # Iterating through staged changes
        if should_track_file(item.a_path, tracked_files):
            tracked_changes.append(item.a_path)

    # Commit and (optionally) push changes
    if tracked_changes:
        repo.git.add(tracked_changes)
        commit_message = commit_message_template.format(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        repo.index.commit(commit_message)
        if push_changes:
            origin = repo.remotes.origin
            origin.push(branch)
        else:
            print(f"Changes committed to {folder}, but not pushed to the remote repository.")
    else:
        print("No tracked changes detected.")

