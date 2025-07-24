import os
import sys
import zipfile
import shutil
from os import path


def absolute_path(path : str) -> str:
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), path)

ZIPFILE_FILENAME = absolute_path("geode-v2.0.0_withAllMods.zip")
ASSETS_LOCATION = absolute_path("geode-v2.0.0_withAllMods")

if __name__ == "__main__":

    input("WARNING: This WILL replace your config file for LATER VERSIONS OF GEODE! Please only run this script on GDPSes where you DON'T plan to use later versions.\nPRESS ENTER TO CONTINUE.> ")

try:
        if not os.path.exists(ASSETS_LOCATION):
            print("Folder with 2.204 Geode and all mods included has not been unzipped. Unzipping geode-v2.0.0_withAllMods.zip...")
            with zipfile.ZipFile(ZIPFILE_FILENAME, 'r') as zip_file:
                zip_file.extractall(ASSETS_LOCATION)
            
        installation_path = input("\nEnter the path for your Geometry Dash installation's equivalent to \"GeometryDash.exe\". It will be renamed for GDPSes.> ").strip()
        if not installation_path.endswith(".exe"):
            raise Exception("ERROR! You must select a .exe file within a Geometry Dash installation folder!")

        GAME_NAME = os.path.basename(installation_path).removesuffix(".exe")
        GAME_PATH = os.path.dirname(installation_path)
        GAME_APPDATA_PATH = os.path.join(os.environ['LOCALAPPDATA'], GAME_NAME)
        SAVED_JSON_PATH = os.path.join(GAME_APPDATA_PATH, "geode\\mods\\geode.loader\\saved.json")

        print(f"Copying 2.204 geode's assets to {GAME_PATH}...")
        for file_name in os.listdir(ASSETS_LOCATION):
            og_path = os.path.join(ASSETS_LOCATION, file_name)
            final_path = os.path.join(GAME_PATH, file_name)

            if os.path.isdir(og_path):
                if os.path.exists(final_path):
                    shutil.rmtree(final_path)
                shutil.copytree(og_path, final_path)
            else:
                if os.path.exists(final_path):
                    os.remove(final_path)
                shutil.copy(og_path, final_path)

        print(f"Successfully installed 2.204 Geode.")


        savedjson_template = absolute_path("config_templates/saved_onlyDependencies.json")
        answer = input("""\nWould you like to install geode with RECOMMENDED mods ENABLED? Otherwise only common dependencies that mods rely on will be enabled. (y/n)> """)
        if "y" in answer:
            savedjson_template = absolute_path("config_templates/saved_recommendedMods.json")

        if not os.path.exists(GAME_APPDATA_PATH):
            raise Exception(f"ERROR! Your game's AppData folder was not created yet! Please launch and exit the game so {GAME_APPDATA_PATH} can be created.")
        else:
            if os.path.exists(os.path.dirname(SAVED_JSON_PATH)):
                shutil.rmtree(os.path.dirname(SAVED_JSON_PATH))
            os.makedirs(os.path.dirname(SAVED_JSON_PATH))

        print(f"Replacing {SAVED_JSON_PATH} with {savedjson_template}...")
        if os.path.exists(SAVED_JSON_PATH):
            os.remove(SAVED_JSON_PATH)
        shutil.copy(savedjson_template, SAVED_JSON_PATH)

        input("\nDONE! Press enter to exit. ")
except Exception as e:
    print(f"An error occured!\n{e}")
    input("Press enter to continue. ")