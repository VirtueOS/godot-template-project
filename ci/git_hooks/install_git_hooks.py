import os
import shutil
import sys

# Add the parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from globals.logger import Logger
logger = Logger(False)


def main():
    # Get the project path (two levels up from this script's location)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_path = os.path.normpath(os.path.join(script_dir, '..', '..'))
    
    # Define source and destination directories
    source_dir = os.path.join(project_path, 'ci', 'git_hooks', 'hooks')
    dest_dir = os.path.join(project_path, '.git', 'hooks')
    
    # Check if source directory exists
    if not os.path.exists(source_dir):
        logger.print_error(f"Source directory not found: {source_dir}")
        sys.exit(1)
    
    # Check if destination directory exists
    if not os.path.exists(dest_dir):
        logger.print_error(f"Destination directory not found: {dest_dir}")
        sys.exit(1)
    
    try:
        
        logger.print_log(f"Copying hooks from {source_dir} to {dest_dir}")
        # Copy all files from source to destination
        for filename in os.listdir(source_dir):
            source_file = os.path.join(source_dir, filename)
            dest_file = os.path.join(dest_dir, filename)
            
            if os.path.isfile(source_file):
                shutil.copy2(source_file, dest_file)
                logger.print_log(f"Copied: {filename}", 6)
        
        logger.print_success("Hooks copied successfully!")
        
    except Exception as e:
        logger.print_error(f"Failed to copy hooks: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()