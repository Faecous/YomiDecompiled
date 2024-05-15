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
        "variables": [],
        "functions": [],
        "classes": []
    }

    extends_pattern = re.compile(r'extends\s+(\w+)')
    variable_pattern = re.compile(r'(var|const)\s+(\w+)\s*=\s*(.+)')
    function_pattern = re.compile(r'func\s+(\w+)\s*\((.*?)\)')
    class_pattern = re.compile(r'class\s+(\w+)')

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
            file_info["variables"].append({
                "name": var_name,
                "type": var_type,
                "value": var_value,
                "scope": "local",  # GDScript doesn't have explicit global variables, usually inferred from context
                "defined_at": line_number,
                "used_at": [],  # This would need more sophisticated analysis
                "references": []  # This would need cross-file analysis
            })

        # Check for functions
        function_match = function_pattern.match(line)
        if function_match:
            func_name = function_match.group(1)
            params = function_match.group(2).split(',') if function_match.group(2) else []
            file_info["functions"].append({
                "name": func_name,
                "return_type": "void",  # GDScript doesn't have explicit return types
                "scope": "local",  # GDScript doesn't have explicit global functions, usually inferred from context
                "defined_at": line_number,
                "parameters": [{"name": param.strip().split(":")[0], "type": param.strip().split(":")[1] if ":" in param else "unknown"} for param in params],
                "used_at": [],  # This would need more sophisticated analysis
                "references": []  # This would need cross-file analysis
            })

        # Check for classes
        class_match = class_pattern.match(line)
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
    "characters/wizard/CharacterState.gd",
    "characters/wizard/EnergyBomb.gd",
    "characters/wizard/FlameWave.gd",
    "characters/wizard/Landing.gd",
    "characters/wizard/Launch.gd",
    "characters/wizard/Wizard.gd",
    "characters/wizard/WizardExtra.gd",
    "characters/wizard/WizardPlayerInfo.gd",
    "characters/wizard/ZephyrThrow.gd",
    "characters/wizard/ActionUiData/GeyserActionUIData.gd",
    "characters/wizard/ActionUiData/MissileFormActionUIData.gd",
    "characters/wizard/projectiles/OrbDart.gd",
    "characters/wizard/projectiles/SparkBomb.gd",
    "characters/wizard/projectiles/VileClutch.gd",
    "characters/wizard/projectiles/orb/Orb.gd",
    "characters/wizard/projectiles/orb/OrbLightning.gd",
    "characters/wizard/projectiles/orb/states/Default.gd",
    "characters/wizard/projectiles/orb/states/LightningDefault.gd",
    "characters/wizard/projectiles/orb/states/Sword.gd",
    "characters/wizard/projectiles/states/FlameWaveDefault.gd",
    "characters/wizard/projectiles/states/MagicDartDefault.gd",
    "characters/wizard/projectiles/states/OrbDartDefault.gd",
    "characters/wizard/projectiles/states/SparkBombDefault.gd",
    "characters/wizard/projectiles/states/SparkBombExplode.gd",
    "characters/wizard/projectiles/states/VileClutchDefault.gd",
    "characters/wizard/projectiles/telekinesis/BombDefault.gd",
    "characters/wizard/projectiles/telekinesis/BoulderFling.gd",
    "characters/wizard/projectiles/telekinesis/Default.gd",
    "characters/wizard/projectiles/telekinesis/TelekinesisBomb.gd",
    "characters/wizard/projectiles/telekinesis/TelekinesisBoulder.gd",
    "characters/wizard/projectiles/telekinesis/TelekinesisFruit.gd",
    "characters/wizard/states/CatchWind.gd",
    "characters/wizard/states/Combust.gd",
    "characters/wizard/states/ConfusingTouch.gd",
    "characters/wizard/states/ConjurePebble.gd",
    "characters/wizard/states/ConjureStorm.gd",
    "characters/wizard/states/ConjureWeapon.gd",
    "characters/wizard/states/Geyser.gd",
    "characters/wizard/states/IceSpikeGround.gd",
    "characters/wizard/states/Liftoff.gd",
    "characters/wizard/states/LockOrb.gd",
    "characters/wizard/states/MagicMissile.gd",
    "characters/wizard/states/MagmaBolt.gd",
    "characters/wizard/states/ManaStrike.gd",
    "characters/wizard/states/Orb.gd",
    "characters/wizard/states/OrbPush.gd",
    "characters/wizard/states/OrbTeleport.gd",
    "characters/wizard/states/OrbTether.gd",
    "characters/wizard/states/Sandstorm.gd",
    "characters/wizard/states/Taunt.gd",
    "characters/wizard/states/VileClutch.gd",
    "characters/wizard/states/WizardState.gd"
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
