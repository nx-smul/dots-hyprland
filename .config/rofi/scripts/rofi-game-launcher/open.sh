#!/usr/bin/env bash

# Open a Rofi game menu whose entries are all installed Steam games

SCRIPT_DIR="$(dirname "$(realpath "$0")")"

GAME_LAUNCHER_CACHE="$HOME/.cache/rofi-game-launcher"
APP_PATH="$HOME/.local/share/applications/rofi-game-launcher"

# Check if python-vdf is installed by attempting to import it in Python
check_python_vdf() {
  python3 -c "import vdf" &>/dev/null
  if [ $? -ne 0 ]; then
    if [ -t 1 ]; then
      # If running in a terminal, print the message
      echo "python-vdf package not found. Please install it using your package manager"
    else
      # If not running in a terminal, show a notification
      notify-send "Steam Game Launcher" "python-vdf package not found. Please install it using your package manager"
    fi
    exit 1 # Exit the script if python-vdf is not installed
  fi
}

# Function to open launcher
launcher-open() {
  # Update entries in the background
  "$SCRIPT_DIR/update-entries.sh" -q &

  # Temporarily link then unlink the *.desktop files to the directory
  # where rofi looks for them to avoid having them appear when using
  # rofi normally
  if [ ! -e "$APP_PATH" ]; then
    ln -s "$GAME_LAUNCHER_CACHE/applications" "$APP_PATH"
  fi

  rofi -show drun \
    -theme games \
    -drun-categories SteamLibrary \
    -cache-dir "$GAME_LAUNCHER_CACHE"

  if [ -h "$APP_PATH" ]; then
    rm "$APP_PATH"
  fi

  # Emulate most recently used history by resetting the count
  # to 0 for each application
  sed -i -e 's/^1/0/' "$GAME_LAUNCHER_CACHE/rofi3.druncache"
}

# Get workspace width
workspace-width() {
  hyprctl monitors -j | jq '.[] | select(.focused == true) | .width'
}

# Set environment variables for Rofi
export ROFI_GAME_LAUNCHER_N_ENTRIES=$(($(workspace-width) / 220))
export ROFI_GAME_LAUNCHER_HEIGHT=360

# Check if python-vdf is installed before proceeding
check_python_vdf

# Open the launcher
launcher-open
