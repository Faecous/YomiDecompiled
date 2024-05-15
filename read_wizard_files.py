import os
import json

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

# Function to read file content
def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Read all wizard files and store their contents in a dictionary
wizard_files_content = {}
for file_path in wizard_files:
    full_path = os.path.join(os.getcwd(), file_path)
    if os.path.exists(full_path):
        wizard_files_content[file_path] = read_file(full_path)
    else:
        wizard_files_content[file_path] = None

# Save the contents to a JSON file
with open("wizard_files_content.json", "w") as json_file:
    json.dump(wizard_files_content, json_file, indent=4)

print("Finished reading wizard files. Contents saved to wizard_files_content.json")
