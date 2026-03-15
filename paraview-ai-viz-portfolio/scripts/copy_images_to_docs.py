"""
Copy rendered images from output/ to docs/images/ for GitHub Pages.
Run after generating all visualizations.
"""
import shutil
import os

PROJ_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(PROJ_DIR, "output")
DST = os.path.join(PROJ_DIR, "docs", "images")

os.makedirs(DST, exist_ok=True)

copied = 0
for f in os.listdir(SRC):
    if f.endswith(".png"):
        shutil.copy2(os.path.join(SRC, f), os.path.join(DST, f))
        print(f"  Copied: {f}")
        copied += 1

print(f"\n{copied} image(s) copied to docs/images/")
