#!/bin/bash

STATE_DIR="$HOME/.local/state"
API_KEY_FILE="$STATE_DIR/steamgriddb_apikey"

# Ensure state directory exists
mkdir -p "$STATE_DIR"

# Clear screen for a clean UI look
clear

# Display header with styling
echo "#############################################"
echo "#          SteamGridDB API Key Setup       #"
echo "#############################################"
echo ""
echo "Welcome to the SteamGridDB API Key Setup Wizard!"
echo ""
echo "To continue, please follow the instructions below to obtain your SteamGridDB API key."
echo ""

# Check if the API key file exists
if [ -f "$API_KEY_FILE" ]; then
  echo "An existing SteamGridDB API key was found."
  echo "Do you want to update the existing key? (y/n)"
  read -r choice

  if [[ "$choice" =~ ^[Yy]$ ]]; then
    echo "Updating API key..."
    # Prompt user to input the new API key
    while true; do
      echo "Please paste your new SteamGridDB API key below: "
      read -r API_KEY
      if [ -z "$API_KEY" ]; then
        echo "Error: API key cannot be empty. Please try again."
      else
        break
      fi
    done
    echo "$API_KEY" >"$API_KEY_FILE"
    echo ""
    echo "**********************************************"
    echo "            API Key Updated Successfully!     "
    echo "**********************************************"
  else
    echo "Keeping the existing API key. No changes were made."
    exit 0
  fi
else
  # Step-by-step tutorial in a UI-style for new users
  echo "Step 1: Open your web browser and go to the SteamGridDB website:"
  echo "       https://www.steamgriddb.com/"
  echo ""
  echo "Step 2: If you don't have an account, click 'Sign Up' in the top right corner."
  echo "       If you already have an account, click 'Log In' to access your profile."
  echo ""
  echo "Step 3: After logging in, click your profile icon in the top-right corner and select 'Account'."
  echo ""
  echo "Step 4: On the Account page, navigate to the 'API' tab."
  echo ""
  echo "Step 5: Click on 'Create API Key' to generate a new API key."
  echo ""
  echo "Step 6: Copy the generated API key to your clipboard."
  echo ""
  echo "Step 7: Paste the API key below when prompted."
  echo ""

  # User prompt to input API key
  while true; do
    echo "--------------------------------------------------"
    echo "Please paste your SteamGridDB API key below: "
    read -r API_KEY
    echo "--------------------------------------------------"
    if [ -z "$API_KEY" ]; then
      echo "Error: API key cannot be empty. Please try again."
    else
      break
    fi
  done

  # Save the API key to the file
  echo "$API_KEY" >"$API_KEY_FILE"

  # Success message with UI-style notification
  echo ""
  echo "**********************************************"
  echo "            API Key Saved Successfully!      "
  echo "**********************************************"
  echo ""
fi
