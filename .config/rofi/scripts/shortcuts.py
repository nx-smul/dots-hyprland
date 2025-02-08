#!/usr/bin/env python3

import vdf
import sys
import os
import glob
import requests
import shutil

# API key and Base URL for SteamGridDB
CONFIG_DIR = os.path.expanduser("~/.config")
STATE_DIR = os.path.expanduser("~/.local/state")
SteamGridDB_API = os.path.join(STATE_DIR, "steamgriddb_apikey")
STEAM_APP_ID_FILE = os.path.join(STATE_DIR, "steamAPP_id")  # Changed the file name to steamAPP_id
BASE_URL = "https://www.steamgriddb.com/api/v2"
ADD_API = os.path.join(CONFIG_DIR, "rofi", "add_steamgridDB_api.sh")

# Check if running in a terminal
def is_running_in_terminal():
    return os.isatty(sys.stdin.fileno())

# Load API key from file
def load_api_key():
    if os.path.exists(SteamGridDB_API):
        with open(SteamGridDB_API, 'r') as f:
            for line in f:
                if line.strip():
                    return line.strip()  # Return the first non-empty line
    return None

# If API key is missing
def api_key_not_found(shortcuts=None):
    API_KEY = load_api_key()
    notification_message = f"API key not found. To add your API key, run {ADD_API}"

    # Check if API_KEY is missing
    if not API_KEY:
        # Only check for notifications if the 'shortcuts' data exists and is not empty
        if shortcuts and 'shortcuts' in shortcuts and shortcuts['shortcuts']:
            if not is_running_in_terminal():
                os.system(f'notify-send "SteamGridDB" "To add non-steam games run {ADD_API} and add api key."')

        # Send terminal message and exit if running in terminal
        if is_running_in_terminal():
            print(notification_message)
            sys.exit()

# Load processed app IDs from file
def load_processed_app_ids():
    processed_app_ids = set()
    if os.path.exists(STEAM_APP_ID_FILE):
        with open(STEAM_APP_ID_FILE, 'r') as f:
            for line in f:
                if line.strip().isdigit():
                    processed_app_ids.add(int(line.strip()))
    return processed_app_ids

# Save processed app IDs to file
def save_processed_app_ids(app_ids):
    os.makedirs(STATE_DIR, exist_ok=True)
    with open(STEAM_APP_ID_FILE, 'w') as f:  # Use 'w' to overwrite the file
        for app_id in app_ids:
            f.write(f"{app_id}\n")

# Main script logic
def main():
    force = '--force' in sys.argv

    # Load the API key directly here instead of calling get_api_key
    API_KEY = load_api_key()

    # If the API key is missing, notify the user and exit
    api_key_not_found()

    def find_shortcuts_vdf():
        steam_root = os.path.expanduser("~/.local/share/Steam")
        pattern = os.path.join(steam_root, "userdata/*/config/shortcuts.vdf")
        files = glob.glob(pattern)
        if files:
            return files[0]
        else:
            sys.exit("Error: No shortcuts.vdf file found")

    def search_images_by_name(name):
        headers = {
            "Authorization": f"Bearer {API_KEY}"
        }
        url = f"{BASE_URL}/search/autocomplete/{name}"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()["data"]
            if data:
                return data[0]["id"]
        return None

    def fetch_image(app_id, image_type):
        headers = {
            "Authorization": f"Bearer {API_KEY}"
        }
        url = f"{BASE_URL}/{image_type}/game/{app_id}"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()["data"]
            if data:
                return data[0]["url"]
        return None

    def download_image(url, dest_path):
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(dest_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return True
        return False

    def create_library_cache(app_id, original_app_id, name, exe, force=False):
        steam_root = os.path.expanduser("~/.local/share/Steam")
        cache_dir = os.path.join(steam_root, f"appcache/librarycache/{original_app_id}")  # Use original app_id

        # Check if cache directory exists and if not, proceed to create it
        if not force and os.path.exists(cache_dir):
            print(f"Appcache folder already exists for app_id: {original_app_id}. Skipping image download.\n")
            print("To overwrite appcache folders use --force flag")  # Separate message with a newline
            return  # Skip image download if the folder exists and force is not enabled

        # If cache directory does not exist, create the folder and download images
        os.makedirs(cache_dir, exist_ok=True)

        image_types = {
            "grids": "library_600x900.jpg",
            "heroes": "library_hero.jpg",
            "logos": "logo.png"  # Keeping the default name for logos
        }

        for image_type, file_name in image_types.items():
            image_url = fetch_image(app_id, image_type)
            if image_url:
                dest_path = os.path.join(cache_dir, file_name)
                if download_image(image_url, dest_path):
                    print(f"{image_type.capitalize()} image downloaded for {name} (app_id: {original_app_id})")
                    print(f"Image saved at: {dest_path}")
                else:
                    print(f"Failed to download {image_type.capitalize()} image for {name} (app_id: {original_app_id})")
            else:
                print(f"No {image_type.capitalize()} image found for {name} (app_id: {original_app_id})")

    def delete_library_cache(app_id):
        steam_root = os.path.expanduser("~/.local/share/Steam")
        cache_dir = os.path.join(steam_root, f"appcache/librarycache/{app_id}")
        if os.path.exists(cache_dir):
            shutil.rmtree(cache_dir)
            print(f"Library cache deleted for app_id: {app_id}")
        else:
            print(f"No library cache found for app_id: {app_id}")

    def parse_shortcuts(file_path, force=False):
        processed_app_ids = load_processed_app_ids()
        new_app_ids = set()

        # Check if the file is empty, but do not send any notification or terminal output for it
        if os.path.getsize(file_path) == 0:
            print(f"{file_path} is empty. No shortcuts to process.")
            sys.exit(0)  # Exit if the file is empty

        with open(file_path, 'rb') as f:
            shortcuts = vdf.binary_load(f)

            # Call api_key_not_found() to send the notification when no API key is found
            api_key_not_found(shortcuts)

            if 'shortcuts' not in shortcuts or not shortcuts['shortcuts']:
                print(f"No shortcuts found in {file_path}. Exiting...")
                sys.exit(0)  # Exit if there are no shortcuts

            for shortcut in shortcuts['shortcuts'].values():
                try:
                    original_app_id = abs(shortcut['appid'])  # Use abs() to remove negative sign
                    name = shortcut['AppName']
                    exe = shortcut['Exe']
                    print(f"Processing {name} (original_app_id: {original_app_id})...")
                    
                    steam_id = search_images_by_name(name)
                    if steam_id:
                        create_library_cache(steam_id, original_app_id, name, exe, force)  # Create library cache with original app_id
                        new_app_ids.add(original_app_id)  # Track new app IDs using the original app_id
                    else:
                        print(f"SteamGridDB ID not found for {name} (original_app_id: {original_app_id})")
                    # print(f"{original_app_id},{name},{exe}")
                except KeyError as e:
                    print(f"KeyError: {e} not found in {shortcut}")
        # Save new app IDs to file
        save_processed_app_ids(new_app_ids)
 
        # Delete library cache folders for processed shortcuts that no longer exist
        for app_id in processed_app_ids:
            if app_id not in new_app_ids:
                delete_library_cache(app_id)

    if len(sys.argv) < 2:
        file_path = find_shortcuts_vdf()
    else:
        file_path = sys.argv[1]
    
    print(f"Processing games from: {file_path}")
    parse_shortcuts(file_path, force)

if __name__ == '__main__':
    main()

