"""Download the owner's own assets (music, sfx, clips, logo) from a shared Google Drive folder.

  python scripts/sync_assets.py

Needs secret DRIVE_ASSETS_URL (folder shared as "Anyone with the link: Viewer").
Files land in library/ (git-ignored). Runs at the start of every Phase B run; existing files are skipped.
"""
import os
import sys

try:
    import gdown
except ImportError:
    sys.exit("pip install gdown")

url = os.environ.get("DRIVE_ASSETS_URL")
if not url:
    print("DRIVE_ASSETS_URL not set; skipping owner assets")
    sys.exit(0)
os.makedirs("library", exist_ok=True)
gdown.download_folder(url=url, output="library", quiet=True, resume=True)
for root, _, files in os.walk("library"):
    for f in files:
        print(os.path.join(root, f))
