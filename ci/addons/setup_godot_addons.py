#!/usr/bin/env python3
from collections import namedtuple
import subprocess
import sys
import os
from pathlib import Path

# Add the parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from globals.logger import Logger
logger = Logger(False)


SUBMODULES_FOLDER = ".submodules"

Submodule = namedtuple('submodule', ['url', 'path', 'sparse_folder', 'branch'])

def main():

    # Step out of ci/ folder
    os.chdir("../..")

    repo_urls = [
        Submodule("git@github.com:bitwes/Gut.git",                                      "gut",                          "addons/gut",                           "main"),
        Submodule("git@github.com:GDQuest/GDScript-formatter.git",                      "script_formatter",             "addons/GDQuest_GDScript_formatter",    "main"),
        Submodule("git@github.com:CodeNameTwister/Godot-IDE-Extension.git",             "_Godot-IDE_",                  "addons/_Godot-IDE_",                   "main"),
        Submodule("git@github.com:anthonyec/godot_little_camera_preview.git",           "camera_preview",               "addons/anthonyec.camera_preview",      "main"),
        Submodule("git@github.com:bbbscarter/GodotRuntimeDebugTools.git",               "runtime_debug_tools",          "addons/runtime_debug_tools",           "master"),
        Submodule("git@github.com:don-tnowe/godot-resources-as-sheets-plugin.git",      "resources_spreadsheet_view",   "addons/resources_spreadsheet_view",    "master"),
    ]
    
    try:
        for repo in repo_urls:
            add_submodule_with_sparse_checkout(repo.url, repo.path, repo.sparse_folder, repo.branch)
            create_symbolic_links(repo.path, repo.sparse_folder)
            logger.print_success(f"Submodule {repo.path} configured\n")
    except Exception as e:
        logger.print_error(f"{e}")


def run_command(cmd, capture_output=True, cwd=None):
    """Run shell command and return result."""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            cwd=cwd, 
            capture_output=capture_output,
            text=True,
            check=True
        )
        return result.stdout.strip() if capture_output else ""
    except subprocess.CalledProcessError as e:
        Logger.print_error(f"Command failed: {cmd}")
        Logger.print_error(f"{e.stderr}")
        raise


def add_submodule_with_sparse_checkout(repo_url, submodule_path=None, sparse_folder="addons", branch="main"):
    """
    Add git submodule to .submodule/ folder. Setup sparse-checkout for {sparse_folder}.
    
    Args:
        repo_url (str): Git repository URL
        submodule_path (str): Path where submodule should be added (default: "{repo_name}")
        sparse_folder (str): Folder to checkout (default: "addons")
        branch (str): Branch to checkout (default: main)
    """

    if submodule_path is None:
        submodule_path = Path(repo_url).stem
    submodule_path = SUBMODULES_FOLDER + "/" + submodule_path

    logger.print_log(f"Adding submodule {repo_url} to {submodule_path}")
    
    # Get current directory for later restoration
    original_dir = Path.cwd()
    # Sparce file path is located in parent repository's .git folder
    sparse_checkout_file = Path(f".git/modules/{submodule_path}/info/sparse-checkout").resolve()

    try:
        # Add submodule
        run_command(f"git submodule add --force -b {branch} {repo_url} {submodule_path}")
        
        # Initialize submodule
        run_command(f"git submodule update --init {submodule_path}")
        

        # Configure sparse checkout in submodule
        submodule_dir = Path(submodule_path)
        
        # Navigate to submodule directory
        os.chdir(submodule_dir)
    
        # Enable sparse checkout
        run_command("git sparse-checkout init --cone")
        

        with open(sparse_checkout_file, 'w') as f:
            f.write(f"/{sparse_folder}/\n")
            # Hack to remove all items in root directory (it causes warning that disables scaning)
            f.write(f"!\n")
        
        run_command("git sparse-checkout reapply")
    finally:
        # Return to parent directory
        os.chdir(original_dir)


def create_symbolic_links(path, sparse_folder):
    src_path = Path(f"{SUBMODULES_FOLDER}/{path}/{sparse_folder}").absolute()
    dest_path = Path(f"addons/{path}").absolute()

    if not Path("addons").absolute().exists():
        os.mkdir("addons")

    # Remove existing link or file if it exists
    if dest_path.exists() or dest_path.is_symlink():
        logger.print_debug(f"Removing existing path: {dest_path}", 6)
        os.remove(dest_path)

    # Ensure the source exists
    if not src_path.exists():
        logger.print_error(f"Source path does not exist: {src_path}", 6)
        return

    # Create symbolic link
    try:
        logger.print_log(f"Linking {src_path} to {dest_path}", 6)
        os.symlink(src_path, dest_path)
    except OSError as e:
        raise


if __name__ == "__main__":
    main()