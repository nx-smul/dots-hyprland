import re
import os

# Define the file path for the configuration file
config_file = os.path.expanduser("~/.config/hypr/custom/general.conf")

# Function to read the current opacity values from the file
def read_opacity():
    with open(config_file, "r") as file:
        lines = file.readlines()

    active_opacity = None
    inactive_opacity = None

    for line in lines:
        if match := re.match(r"^\s*active_opacity\s*=\s*(\d*\.?\d+)\s*$", line):
            active_opacity = float(match.group(1))
        elif match := re.match(r"^\s*inactive_opacity\s*=\s*(\d*\.?\d+)\s*$", line):
            inactive_opacity = float(match.group(1))

    return active_opacity, inactive_opacity

# Function to write the opacity values to the file
def write_opacity(active_opacity, inactive_opacity):
    with open(config_file, "r") as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if re.match(r"^\s*active_opacity\s*=\s*.*$", line):
            lines[i] = f"    active_opacity = {active_opacity}\n"
        elif re.match(r"^\s*inactive_opacity\s*=\s*.*$", line):
            lines[i] = f"    inactive_opacity = {inactive_opacity}\n"

    with open(config_file, "w") as file:
        file.writelines(lines)

# Function to toggle opacity values
def toggle_opacity():
    active_opacity, inactive_opacity = read_opacity()

    if active_opacity == 1 and inactive_opacity == 1:
        active_opacity = 0.85
        inactive_opacity = 0.80
    else:
        active_opacity = 1
        inactive_opacity = 1

    write_opacity(active_opacity, inactive_opacity)

    # Print the applied opacity values
    print(f"Active opacity set to: {active_opacity}")
    print(f"Inactive opacity set to: {inactive_opacity}")

# Execute the toggle function
toggle_opacity()

print("Opacity values have been toggled.")

