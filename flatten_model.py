import os
import shutil

model_parent = "model/vosk-model-small-en-us-0.15"
target_model = "model"

# Move all files/folders up one level
for item in os.listdir(model_parent):
    s = os.path.join(model_parent, item)
    d = os.path.join(target_model, item)
    shutil.move(s, d)

# Remove the now-empty nested folder
os.rmdir(model_parent)

print("Model folder flattened successfully!")
