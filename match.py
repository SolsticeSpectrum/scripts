from PIL import Image, ImageChops
import os

# Folder containing the images
folder_path = "sequence"

# Load the reference image
reference_image_path = os.path.join(folder_path, "frame00001.png")
reference_image = Image.open(reference_image_path)

# Initialize the next matching image path
next_matching_image_path = None

# Loop through all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".png") and filename != "frame00001.png":
        # Load the current image
        current_image_path = os.path.join(folder_path, filename)
        current_image = Image.open(current_image_path)

        # Compare images pixel by pixel
        diff = ImageChops.difference(reference_image, current_image)

        # If the images are identical (pixel-perfect match), save the path and break
        if not diff.getbbox():
            next_matching_image_path = current_image_path
            break

# Print the path to the next matching image
if next_matching_image_path:
    print("Next matching image:", next_matching_image_path)
else:
    print("No matching image found.")
