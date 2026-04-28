import os
import zipfile
import urllib.request

# URL of the small English Vosk model
VOSK_URL = "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
MODEL_DIR = "model"
ZIP_FILE = "vosk_model.zip"

# Download the zip file
print("Downloading Vosk model...")
urllib.request.urlretrieve(VOSK_URL, ZIP_FILE)
print("Download complete!")

# Create model directory if not exists
os.makedirs(MODEL_DIR, exist_ok=True)

# Extract the zip file
print("Extracting model...")
with zipfile.ZipFile(ZIP_FILE, 'r') as zip_ref:
    zip_ref.extractall(MODEL_DIR)

# Remove the zip file
os.remove(ZIP_FILE)

print("Vosk model is ready in the 'model' folder!")
