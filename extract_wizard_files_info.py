import os
import json
import re

def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.readlines()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []

def extract_info(file_path):
    content = read_file(file_path)
    if not content:
        return None

    file_info = {
        "extends": None,
        "global_variables": [],
        "functions": [],
        "classes": [],
        "nodes": [],
        "script_references": [],
        "resources": []
    }

    extends_pattern = re.compile(r'extends\s+(\w+)')
    variable_pattern = re.compile(r'(var|const)\s+(\w+)\s*=\s*(.+)')
    function_pattern = re.compile(r'func\s+(\w+)\s*\((.*?)\)')
    class_pattern = re.compile(r'class\s+(\w+)')
    node_pattern = re.compile(r'\[node\s+name="(\w+)"\s+type="(\w+)"')
    script_ref_pattern = re.compile(r'script\s*=\s*ExtResource\s*\(\s*path="([^"]+)"')
    resource_pattern = re.compile(r'\[resource\s+type="(\w+)"\s+id="(\d+)"')

    current_function = None

    for line_number, line in enumerate(content, start=1):
        # Check for extends
        extends_match = extends_pattern.match(line)
        if extends_match:
            file_info["extends"] = extends_match.group(1)

        # Check for variables
        variable_match = variable_pattern.match(line)
        if variable_match:
            var_type = variable_match.group(1)
            var_name = variable_match.group(2)
            var_value = variable_match.group(3)
            variable_info = {
                "name": var_name,
                "type": var_type,
                "value": var_value,
                "defined_at": line_number,
                "used_at_lines": [],
                "used_in_functions": []
            }
            if current_function:
                current_function["local_variables"].append(variable_info)
            else:
                file_info["global_variables"].append(variable_info)

        # Check for functions
        function_match = function_pattern.match(line)
        if function_match:
            func_name = function_match.group(1)
            params = function_match.group(2).split(',') if function_match.group(2) else []
            current_function = {
                "name": func_name,
                "return_type": "void",
                "defined_at": line_number,
                "parameters": [{"name": param.strip().split(":")[0], "type": param.strip().split(":")[1] if ":" in param else "unknown"} for param in params],
                "local_variables": [],
                "used_variables": []
            }
            file_info["functions"].append(current_function)

        # Check for classes
        class_match = class_pattern.match(line)
        if class_match:
            class_name = class_match.group(1)
            file_info["classes"].append({
                "name": class_name,
                "defined_at": line_number,
                "methods": [],
                "variables": []
            })

        # Check for nodes in .tscn files
        node_match = node_pattern.match(line)
        if node_match:
            node_name = node_match.group(1)
            node_type = node_match.group(2)
            file_info["nodes"].append({
                "name": node_name,
                "type": node_type,
                "defined_at": line_number
            })

        # Check for script references in .tscn files
        script_ref_match = script_ref_pattern.match(line)
        if script_ref_match:
            script_path = script_ref_match.group(1)
            file_info["script_references"].append({
                "path": script_path,
                "referenced_at": line_number
            })

        # Check for resources in .tres files
        resource_match = resource_pattern.match(line)
        if resource_match:
            resource_type = resource_match.group(1)
            resource_id = resource_match.group(2)
            file_info["resources"].append({
                "type": resource_type,
                "id": resource_id,
                "defined_at": line_number
            })

        # Track variable usage
        for variable in file_info["global_variables"]:
            if variable["name"] in line:
                variable["used_at_lines"].append(line_number)
                if current_function:
                    variable["used_in_functions"].append(current_function["name"])
                    current_function["used_variables"].append({
                        "name": variable["name"],
                        "used_at_lines": [line_number]
                    })

        if current_function:
            for variable in current_function["local_variables"]:
                if variable["name"] in line:
                    variable["used_at_lines"].append(line_number)

    return file_info

def collect_files(structure, current_path=""):
    files = []
    print(f"Current path: {current_path}, Structure: {structure}")  # Debugging print
    for file in structure.get("script_files", []):
        if file.endswith(('.gd', '.tscn', '.tres')):
            files.append(os.path.join(current_path, file))
    for subdir, substructure in structure.get("subdirectories", {}).items():
        files.extend(collect_files(substructure, os.path.join(current_path, subdir)))
    return files

# Load the JSON structure
with open('repo_structure.json', 'r') as file:
    repo_structure = json.load(file)

# Find the wizard section within the JSON structure
wizard_structure = repo_structure
wizard_key = 'wizard'

# Traverse to find the wizard key in the structure
def find_wizard_structure(structure):
    for key, value in structure.items():
        if key == wizard_key:
            return value
        if isinstance(value, dict):
            result = find_wizard_structure(value)
            if result:
                return result
    return None

wizard_structure = find_wizard_structure(repo_structure)
if not wizard_structure:
    print(f"Error: Could not find the '{wizard_key}' key in the JSON structure")
else:
    print(f"Found wizard structure: {wizard_structure}")  # Debugging print

# Extract wizard files from the JSON structure
wizard_files = collect_files(wizard_structure)
print("Collected wizard files:", wizard_files)  # Debugging print

# Read all wizard files and store their extracted information in a dictionary
wizard_files_info = {}
repo_root = os.path.join(os.getcwd(), 'characters', 'wizard')

for file_path in wizard_files:
    full_path = os.path.join(repo_root, file_path)
    if os.path.exists(full_path):
        print(f"Reading {full_path}")  # Debugging print
        wizard_files_info[file_path] = extract_info(full_path)
    else:
        print(f"File not found: {full_path}")  # Debugging print
        wizard_files_info[file_path] = None

# Save the extracted information to a JSON file
with open("wizard_files_info.json", "w") as json_file:
    json.dump(wizard_files_info, json_file, indent=4)

print("Finished extracting information from wizard files. Data saved to wizard_files_info.json")
