import Crime_Catcher.Analyze.analyze as img_stuff
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
ASSETS_DIR = BASE_DIR / "evidence"

test_image = ASSETS_DIR / "image.jpg"
  
   # If file doesn't exist, we create a dummy one just so the code doesn't crash
if not os.path.exists(test_image):
   print(f"Please put an image named '{test_image}' in this folder to test.")
else:
       img_stuff.analyze_img(test_image)