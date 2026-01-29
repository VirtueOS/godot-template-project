# Overview
This repository provides automation for basic Godot project initialization functions, including:
- Installing addons as git submodules
- Adding git hooks
- Setting up project settings

# Key Features

## Python Integration
Installs Python, as most CI scripts in the repository are written in Python.

## Addon Management
Installs specified addons as Git submodules in a designated directory.  

**Current issue with addons:** Addons in the Godot AssetLib are structured as full Godot projects. If added directly as submodules, this would result in the entire project being downloaded, with the addon nested under addons/addon_name/addons/addon_name. This can cause compilation errors (e.g., when using preload(path))  

**Solution:** Instead, all addons are added as submodules to the .submodules folder. Then only addon folder is sparce-checkouted. From there, symbolic links are created for each addon, pointing to the addons/addon_name directory  

## Project Settings
setup_project_settings.gd is editor script, adapted from [TheDuriel](https://gist.github.com/TheDuriel/4507f6f81ebe4ed0bc082c0e3c220049)

## System Requirements
Developed for Windows

# TODO
- Evaluate replacing Python scripts with GDScript for tighter integration with the Godot editor.
