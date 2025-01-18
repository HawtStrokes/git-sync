# git-sync

## Overview

`git-sync` is a simple Python-based tool that automatically syncs files from a specified folder to a Git repository. It monitors the folder for changes and commits and pushes those changes to a remote Git repository, ensuring that your files are always backed up in version control. This tool can be configured to run as a service, providing seamless synchronization for your files.

## Features

- Syncs files from a local folder to a remote Git repository.
- Watches for changes in the folder and automatically commits and pushes them.
- Supports configuration through a `config.json` file.
- Excludes unnecessary Git files (like `.git/config`, `.git/HEAD`) from triggering syncs.
- Can be run as a background service for continuous monitoring.

## Requirements

- Python 3.x
- Required Python packages (listed in `requirements.txt`)

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/git-sync.git
   ```

2. Navigate into the project directory:

   ```
   cd git-sync
   ```

3. Set up a virtual environment (optional but recommended):

   ```
   python3 -m venv venv
   source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
   ```

4. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

5. Create a `config.json` file with the following structure:

   ```json
   {
     "folders": [
       {
         "folder_to_sync": "/path/to/your/folder",
         "repo_url": "https://github.com/yourusername/yourrepo.git",
         "branch": "main",
         "commit_message": "Auto commit at {timestamp}"
       }
     ]
   }
   ```

   - `folder_to_sync`: Path to the folder you want to sync.
   - `repo_url`: URL of the Git repository to push the changes.
   - `branch`: Git branch to push changes to.
   - `commit_message`: Template for the commit message (supports `{timestamp}` for the current time).

## Usage

1. Run the sync process:

   ```
   python -m git_sync
   ```

   This will start the monitoring of the specified folders and sync changes to the Git repository.

2. To run the script as a service, you can set up a systemd service (for Linux) or use other appropriate methods depending on your operating system.

### Explanation:

- `git_sync/`: Contains the main code for the project.
  - `__init__.py`: Makes the folder a package.
  - `__main__.py`: The entry point of the application.
  - `sync.py`: Handles the syncing logic (commit and push).
  - `watcher.py`: Monitors the folder for changes.
  
- `requirements.txt`: Lists the required Python packages.
- `config.json`: Configuration file to specify the folders to sync and other settings.
- `.gitignore`: Specifies which files and directories should be ignored by Git.
- `README.md`: Documentation for the project.

## Configuration

The configuration for `git-sync` is stored in the `config.json` file. You can add multiple folders to sync by adding them to the `folders` array. For each folder, provide the `folder_to_sync`, `repo_url`, `branch`, and `commit_message`.

### Example `config.json`:

```json
{
  "folders": [
    {
      "folder_to_sync": "/home/user/Documents/myproject",
      "repo_url": "https://github.com/yourusername/myproject.git",
      "branch": "main",
      "commit_message": "Auto commit at {timestamp}"
    }
  ]
}
```

## Excluding Files

By default, `git-sync` excludes changes in Git-related files (e.g., `.git/config`, `.git/HEAD`, etc.). This is done to prevent unnecessary commits and pushes related to internal Git files.

You can modify this behavior by editing the `watcher.py` file if you need to include or exclude specific files.

