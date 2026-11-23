#!/bin/bash
# Cloud environment setup script: installs video tools once per session.
set -e
if ! command -v ffmpeg >/dev/null; then
  (apt-get update && apt-get install -y ffmpeg fonts-dejavu fonts-noto-core) >/dev/null 2>&1 || true
fi
pip install -q google-api-python-client google-auth google-auth-oauthlib requests Pillow playwright gdown
python -m playwright install --with-deps chromium >/dev/null 2>&1 || true
