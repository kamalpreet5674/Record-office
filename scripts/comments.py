"""Comments on our recent videos: list new ones, and post a reply.

  python scripts/comments.py --hours 24 [--videos 10]
  python scripts/comments.py reply --parent <comment id> --text "..."

Prints JSON: one item per top-level comment newer than --hours on our latest --videos uploads,
with video title, link, author, text, likes, time, and whether we already replied.
`reply` needs the youtube.force-ssl permission (run get_youtube_token.py again after 23 Nov 2026).
"""
import argparse
import datetime as dt
import json
import sys

from yt_common import youtube


def reply(parent, text):
    try:
        r = youtube().comments().insert(part="snippet", body={
            "snippet": {"parentId": parent, "textOriginal": text}}).execute()
    except Exception as e:
        if "insufficient" in str(e).lower() or "403" in str(e):
            sys.exit("No permission to reply yet: run get_youtube_token.py again and update YT_REFRESH_TOKEN.")
        raise
    print("replied:", r["id"])


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "reply":
        rp = argparse.ArgumentParser()
        rp.add_argument("cmd")
        rp.add_argument("--parent", required=True)
        rp.add_argument("--text", required=True)
        r = rp.parse_args()
        return reply(r.parent, r.text)
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
            out.append({"id": t["id"], "video": title, "link": f"https://www.youtube.com/watch?v={vid}&lc={t['id']}",
                        "author": c.get("authorDisplayName"), "text": c.get("textDisplay"),
                        "likes": c.get("likeCount", 0), "at": c["publishedAt"], "we_replied": replied})
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
