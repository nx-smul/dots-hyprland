import os

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# Define the path to the colors file and the output file
colors_file_path = os.path.expanduser('~/.cache/wal/colors')
output_file_path = os.path.expanduser('~/.cache/wal/colors-hypr.conf')

# Debugging information
print(f"Colors file path: {colors_file_path}")
print(f"Output file path: {output_file_path}")

# Check if the colors file exists
if not os.path.isfile(colors_file_path):
    raise FileNotFoundError(f"The colors file does not exist at {colors_file_path}")

# Read the colors from the colors file
with open(colors_file_path, 'r') as colors_file:
    colors = colors_file.read().splitlines()

# Ensure there are enough colors in the colors file
if len(colors) < 16:
    raise ValueError("The colors file does not contain enough colors.")

# Convert hex colors to RGB and store them in a dictionary
hex_colors = {f"color{i+1}": colors[i][1:] for i in range(16)}
rgb_colors = {f"color{i+1}": hex_to_rgb(colors[i]) for i in range(16)}

# Create the content for the colors-hypr.conf file
config_content = ""

for i in range(16):
    hex_color = hex_colors[f"color{i+1}"]
    rgb_color = rgb_colors[f"color{i+1}"]
    config_content += f"$color{i+1} = {hex_color}\n"
    config_content += f"$color-hyprlock{i+1} = rgb({rgb_color[0]}, {rgb_color[1]}, {rgb_color[2]})\n"

# Write the content to the output file
with open(output_file_path, 'w') as output_file:
    output_file.write(config_content)

print(f"colors-hypr.conf has been created at {output_file_path}")

