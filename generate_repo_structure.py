import os
import json

def get_script_files(directory):
    script_files = []
    subdirectories = {}
    
    for entry in os.scandir(directory):
        if entry.is_file() and entry.name.endswith(('.gd', '.tres')):
            script_files.append(entry.name)
        elif entry.is_dir():
            subdir_path = os.path.join(directory, entry.name)
            subdirectories[entry.name] = get_script_files(subdir_path)
    
    return {
        "script_files": script_files,
        "subdirectories": subdirectories
    }

# Assuming the script is in the root directory of the repo
repo_path = os.path.dirname(os.path.abspath(__file__))
repo_structure = get_script_files(repo_path)

with open("repo_structure.json", "w") as json_file:
    json.dump(repo_structure, json_file, indent=4)
