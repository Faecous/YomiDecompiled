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
        "variables": [],
        "functions": [],
        "classes": []
    }

    variable_pattern = re.compile(r'var\s+(\w+)\s*:\s*(\w+)?')
    function_pattern = re.compile(r'func\s+(\w+)\s*\((.*?)\)\s*:\s*(\w+)?')
    class_pattern = re.compile(r'class\s+(\w+)')

    for line_number, line in enumerate(content, start=1):
        # Check for variables
        variable_match = variable_pattern.search(line)
        if variable_match:
            var_name = variable_match.group(1)
            var_type = variable_match.group(2) if variable_match.group(2) else "unknown"
            file_info["variables"].append({
                "name": var_name,
                "type": var_type,
                "scope": "local",  # GDScript doesn't have explicit global variables, usually inferred from context
                "defined_at": line_number,
                "used_at": [],  # This would need more sophisticated analysis
                "references": []  # This would need cross-file analysis
            })

        # Check for functions
        function_match = function_pattern.search(line)
        if function_match:
            func_name = function_match.group(1)
            params = function_match.group(2).split(',') if function_match.group(2) else []
            return_type = function_match.group(3) if function_match.group(3) else "void"
            file_info["functions"].append({
                "name": func_name,
                "return_type": return_type,
                "scope": "local",  # GDScript doesn't have explicit global functions, usually inferred from context
                "defined_at": line_number,
                "parameters": [{"name": param.strip().split(":")[0], "type": param.strip().split(":")[1] if ":" in param else "unknown"} for param in params],
                "used_at": [],  # This would need more sophisticated analysis
                "references": []  # This would need cross-file analysis
            })

        # Check for classes
        class_match = class_pattern.search(line)
        if class_match:
            class_name = class_match.group(1)
            file_info["classes"].append({
                "name": class_name,
                "defined_at": line_number,
                "methods": [],  # Methods would be filled in by further analysis
                "variables": []  # Class variables would be filled in by further analysis
            })

    return file_info

# List of files related to the wizard character
wizard_files = [
    "wizard/CharacterState.gd",
    "wizard/EnergyBomb.gd",
    "wizard/FlameWave.gd",
    "wizard/Landing.gd",
    "wizard/Launch.gd",
    "wizard/Wizard.gd",
    "wizard/WizardExtra.gd",
    "wizard/WizardPlayerInfo.gd",
    "wizard/ZephyrThrow.gd",
    "wizard/ActionUiData/GeyserActionUIData.gd",
    "wizard/ActionUiData/MissileFormActionUIData.gd",
    "wizard/projectiles/OrbDart.gd",
    "wizard/projectiles/SparkBomb.gd",
    "wizard/projectiles/VileClutch.gd",
    "wizard/projectiles/orb/Orb.gd",
    "wizard/projectiles/orb/OrbLightning.gd",
    "wizard/projectiles/orb/states/Default.gd",
    "wizard/projectiles/orb/states/LightningDefault.gd",
    "wizard/projectiles/orb/states/Sword.gd",
    "wizard/projectiles/states/FlameWaveDefault.gd",
    "wizard/projectiles/states/MagicDartDefault.gd",
    "wizard/projectiles/states/OrbDartDefault.gd",
    "wizard/projectiles/states/SparkBombDefault.gd",
    "wizard/projectiles/states/SparkBombExplode.gd",
    "wizard/projectiles/states/VileClutchDefault.gd",
    "wizard/projectiles/telekinesis/BombDefault.gd",
    "wizard/projectiles/telekinesis/BoulderFling.gd",
    "wizard/projectiles/telekinesis/Default.gd",
    "wizard/projectiles/telekinesis/TelekinesisBomb.gd",
    "wizard/projectiles/telekinesis/TelekinesisBoulder.gd",
    "wizard/projectiles/telekinesis/TelekinesisFruit.gd",
    "wizard/states/CatchWind.gd",
    "wizard/states/Combust.gd",
    "wizard/states/ConfusingTouch.gd",
    "wizard/states/ConjurePebble.gd",
    "wizard/states/ConjureStorm.gd",
    "wizard/states/ConjureWeapon.gd",
    "wizard/states/Geyser.gd",
    "wizard/states/IceSpikeGround.gd",
    "wizard/states/Liftoff.gd",
    "wizard/states/LockOrb.gd",
    "wizard/states/MagicMissile.gd",
    "wizard/states/MagmaBolt.gd",
    "wizard/states/ManaStrike.gd",
    "wizard/states/Orb.gd",
    "wizard/states/OrbPush.gd",
    "wizard/states/OrbTeleport.gd",
    "wizard/states/OrbTether.gd",
    "wizard/states/Sandstorm.gd",
    "wizard/states/Taunt.gd",
    "wizard/states/VileClutch.gd",
    "wizard/states/WizardState.gd"
]

# Read all wizard files and store their extracted information in a dictionary
wizard_files_info = {}
for file_path in wizard_files:
    full_path = os.path.join(os.getcwd(), file_path)
    if os.path.exists(full_path):
        print(f"Reading {full_path}")
        wizard_files_info[file_path] = extract_info(full_path)
    else:
        print(f"File not found: {full_path}")
        wizard_files_info[file_path] = None

# Save the extracted information to a JSON file
with open("wizard_files_info.json", "w") as json_file:
    json.dump(wizard_files_info, json_file, indent=4)

print("Finished extracting information from wizard files. Data saved to wizard_files_info.json")

   
