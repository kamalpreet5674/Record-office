"""Run ONCE on your own computer to log in to YouTube and get the refresh token.

    pip install google-auth-oauthlib
    python get_youtube_token.py path/to/client_secret.json

A browser opens, you pick the channel's Google account and allow access.
The script prints a refresh token. Copy it into the cloud environment secret
YT_REFRESH_TOKEN (never paste it in a chat).
"""
import sys

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/youtube.force-ssl",      # reply to comments
    "https://www.googleapis.com/auth/yt-analytics.readonly",  # audit: retention, subscribers
]

if len(sys.argv) != 2:
    sys.exit("Usage: python get_youtube_token.py client_secret.json")

flow = InstalledAppFlow.from_client_secrets_file(sys.argv[1], SCOPES)
creds = flow.run_local_server(port=0, access_type="offline", prompt="consent")
print("\nYT_REFRESH_TOKEN =", creds.refresh_token)
print("Client ID       =", creds.client_id)
print("\nSave these three values as environment secrets: YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN")
