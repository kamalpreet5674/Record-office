"""New comments on our recent videos, so Claude can draft replies for the owner.

  python scripts/comments.py --hours 24 [--videos 10]

Prints JSON: one item per top-level comment newer than --hours on our latest --videos uploads,
with video title, link, author, text, likes, time, and whether we already replied.
Read-only (the token cannot post comments; the owner replies from the YouTube app).
"""
import argparse
import datetime as dt
import json

from yt_common import youtube


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hours", type=int, default=24)
    ap.add_argument("--videos", type=int, default=10)
    a = ap.parse_args()
    yt = youtube()
    ch = yt.channels().list(part="contentDetails,id", mine=True).execute()["items"][0]
    uploads = ch["contentDetails"]["relatedPlaylists"]["uploads"]
    items = yt.playlistItems().list(part="snippet", playlistId=uploads, maxResults=a.videos).execute()["items"]
    since = dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=a.hours)
    out = []
    for it in items:
        vid, title = it["snippet"]["resourceId"]["videoId"], it["snippet"]["title"]
        try:
            res = yt.commentThreads().list(part="snippet,replies", videoId=vid, maxResults=50,
                                           order="time", textFormat="plainText").execute()
        except Exception as e:  # comments off, or private video
            continue
        for t in res.get("items", []):
            c = t["snippet"]["topLevelComment"]["snippet"]
            when = dt.datetime.fromisoformat(c["publishedAt"].replace("Z", "+00:00"))
            if when < since:
                continue
            replied = any(r["snippet"].get("authorChannelId", {}).get("value") == ch["id"]
                          for r in (t.get("replies") or {}).get("comments", []))
            out.append({"video": title, "link": f"https://www.youtube.com/watch?v={vid}&lc={t['id']}",
                        "author": c.get("authorDisplayName"), "text": c.get("textDisplay"),
                        "likes": c.get("likeCount", 0), "at": c["publishedAt"], "we_replied": replied})
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
