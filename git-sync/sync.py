import os
import json
from git import Repo
from datetime import datetime

def update_remote_url(repo_path, username, token):
    """
    Update the remote URL to include GitHub username and personal access token for authentication.
    """
    repo = Repo(repo_path)
    
    # If there are no remotes, do not proceed with updating the URL.
    if len(repo.remotes) == 0:
        print(f"No remotes found in the repository at {repo_path}. Skipping remote URL update.")
        return

    origin = repo.remotes.origin
    new_url = f"https://{username}:{token}@github.com/{username}/{repo.remotes.origin.url.split('/')[-1]}"
    origin.set_url(new_url)

def sync_folder(folder_config, push_changes=True):
    folder = os.path.expanduser(folder_config["folder_to_sync"])
    repo_url = folder_config["repo_url"]
    branch = folder_config["branch"]
    commit_message_template = folder_config["commit_message"]
    username = folder_config["username"]
    token = folder_config["token"]  # Fetch the personal access token from the config

    # Initialize or open Git repo
    if not os.path.exists(os.path.join(folder, ".git")):
        print(f"Initializing repository at {folder}...")
        Repo.init(folder)

    repo = Repo(folder)

    # Only update remote URL if push_changes is True (no need to do this if we're not pushing)
    if push_changes:
        update_remote_url(folder, username, token)

    # Commit and (optionally) push changes
    if repo.is_dirty(untracked_files=True):
        repo.git.add(A=True)
        commit_message = commit_message_template.format(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        repo.index.commit(commit_message)
        if push_changes:
            origin = repo.remotes.origin
            origin.push(branch)
        else:
            print(f"Changes committed to {folder}, but not pushed to the remote repository.")

