"""Upload a Short to YouTube.

  python scripts/youtube_upload.py --file videos/<dir>/final/short.mp4 --meta videos/<dir>/seo/upload.json

upload.json:
{
  "title": "...",
  "description": "...",
  "tags": ["..."],
  "privacy": "private",            # private | unlisted | public
  "publish_at": null,              # e.g. "2026-11-23T08:00:00Z" (needs privacy=private, after Google's app audit)
  "category_id": "27",             # 27 = Education
  "synthetic": false,              # true if realistic AI imagery of real people/events was used
  "language": "hi"
}
Prints the video id and link and writes it into upload.json as "video_id".
"""
import argparse
import json

from googleapiclient.http import MediaFileUpload

from yt_common import youtube


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True)
    ap.add_argument("--meta", required=True)
    a = ap.parse_args()
    m = json.load(open(a.meta, encoding="utf-8"))
    status = {"privacyStatus": m.get("privacy", "private"), "selfDeclaredMadeForKids": False,
              "containsSyntheticMedia": bool(m.get("synthetic", False))}
    if m.get("publish_at"):
        status["privacyStatus"] = "private"
        status["publishAt"] = m["publish_at"]
    body = {
        "snippet": {"title": m["title"][:100], "description": m["description"][:5000],
                    "tags": m.get("tags", []), "categoryId": m.get("category_id", "27"),
                    "defaultLanguage": m.get("language", "hi"),
                    "defaultAudioLanguage": m.get("language", "hi")},
        "status": status,
    }
    req = youtube().videos().insert(part="snippet,status", body=body,
                                    media_body=MediaFileUpload(a.file, chunksize=8 * 1024 * 1024, resumable=True))
    resp = None
    while resp is None:
        prog, resp = req.next_chunk()
        if prog:
            print(f"uploaded {int(prog.progress() * 100)}%")
    vid = resp["id"]
    m["video_id"] = vid
    json.dump(m, open(a.meta, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"Done: https://youtube.com/shorts/{vid}  (status: {resp['status']['privacyStatus']})")


if __name__ == "__main__":
    main()
