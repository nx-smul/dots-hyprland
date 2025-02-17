#!/bin/bash

# Define color variables
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
RESET='\033[0m'

STATE_DIR="$HOME/.local/state"
API_KEY_FILE="$STATE_DIR/steamgriddb_apikey"

# Function to simulate typing animation
typing_animation() {
  text="$1"
  delay=0.03 # Reduced delay for faster animation
  for ((i = 0; i < ${#text}; i++)); do
    echo -n "${text:i:1}"
    sleep $delay
  done
  echo
}

# Function to add API key to the file
add_api_key() {
  # Show instructions to the user without animation for specific lines
  echo ""
  echo -e "${CYAN}Follow these steps to collect a new API key:${RESET}"

  # These lines do not have animation
  echo "1. Open your web browser and go to the SteamGridDB website: https://www.steamgriddb.com/"
  echo "2. If you don't have an account, click 'Sign Up' in the top right corner. Otherwise, log in."
  echo "3. After logging in, click your profile icon in the top-right corner and select 'Account'."
  echo "4. On the Account page, go to the 'API' tab."
  echo "5. Click 'Create API Key' to generate your new API key."
  echo "6. Copy the generated API key to your clipboard."
  echo ""

  # Create the directory if it doesn't exist
  mkdir -p "$STATE_DIR"

  # Prompt user to input the API key
  while true; do
    echo -e "${BLUE}Please paste your SteamGridDB API key below: ${RESET}"
    read -r API_KEY
    if [ -z "$API_KEY" ]; then
      echo -e "${RED}Error: API key cannot be empty. Please try again.${RESET}"
    else
      break
    fi
  done

  # Save the API key to the file
  echo "$API_KEY" >"$API_KEY_FILE"

  # Success message with UI-style notification
  echo ""
  echo -e "${GREEN}**********************************************"
  echo -e "            API Key Saved Successfully!      "
  echo -e "**********************************************${RESET}"
}

# Function to check and update API key
check_and_update_api_key() {
  # Check if the API key file exists
  if [ -f "$API_KEY_FILE" ]; then
    echo -e "${YELLOW}An existing SteamGridDB API key was found.${RESET}"
    echo "Do you want to update the existing key? (y/N)"
    read -r choice

    if [[ "$choice" =~ ^[Yy]$ ]]; then
      echo -e "${CYAN}Updating API key...${RESET}"
      # Call add_api_key function to prompt for and save the new API key
      add_api_key
    else
      echo -e "${CYAN}Keeping the existing API key. No changes were made.${RESET}"
      exit 0
    fi
  else
    # If the file doesn't exist, call add_api_key function to prompt the user for a new API key
    typing_animation "It seems like there is no existing API key. Let's add a new one."
    echo ""
    add_api_key
  fi
}

# Ensure state directory exists
mkdir -p "$STATE_DIR"

# Clear screen for a clean UI look
clear

# Display header
echo -e "${CYAN}#############################################"
echo -e "#          ${GREEN}SteamGridDB API Key Setup${CYAN}       #"
echo -e "#############################################${RESET}"
echo ""

typing_animation "Welcome to the SteamGridDB API Key Setup Wizard!"
echo ""

# Call the API key checking and updating function
check_and_update_api_key
