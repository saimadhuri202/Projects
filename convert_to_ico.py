from PIL import Image

# Path to your JPG file
jpg_path = "bluenotepad.jpg"

# Path where the ICO file will be saved
ico_path = "bluenotepad.ico"

# Load the image
img = Image.open(jpg_path)

# Convert and save as ICO (multiple sizes for Windows compatibility)
img.save(ico_path, format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])

print(f"Icon saved as: {ico_path}")
