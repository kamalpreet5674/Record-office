"""Trend + competitor research with the YouTube Data API (cheap calls only).

  python scripts/yt_research.py --competitors config/competitors.txt --days 3 --out DIR
  python scripts/yt_research.py --own-uploads --out DIR

competitors.txt: one channel per line, as a channel ID (UC...) or @handle. Lines starting with # are skipped.
Writes DIR/competitors.md, DIR/trending.md or DIR/own_uploads.md.
"""
import argparse
import datetime as dt
import os
import statistics

from yt_common import youtube


def channel_info(yt, ref):
    kw = {"id": ref} if ref.startswith("UC") else {"forHandle": ref.lstrip("@")}
    r = yt.channels().list(part="snippet,contentDetails", **kw).execute()
    if not r.get("items"):
        return None
    it = r["items"][0]
    return it["snippet"]["title"], it["contentDetails"]["relatedPlaylists"]["uploads"]


def uploads(yt, playlist, limit=50):
    ids, token = [], None
    while len(ids) < limit:
        r = yt.playlistItems().list(part="contentDetails", playlistId=playlist,
                                    maxResults=50, pageToken=token).execute()
        ids += [i["contentDetails"]["videoId"] for i in r["items"]]
        token = r.get("nextPageToken")
        if not token:
            break
    return ids[:limit]


def videos(yt, ids):
    out = []
    for i in range(0, len(ids), 50):
        r = yt.videos().list(part="snippet,statistics,contentDetails", id=",".join(ids[i:i + 50])).execute()
        out += r["items"]
    return out


def age_hours(v):
    t = dt.datetime.fromisoformat(v["snippet"]["publishedAt"].replace("Z", "+00:00"))
    return max((dt.datetime.now(dt.timezone.utc) - t).total_seconds() / 3600, 1)


def views(v):
    return int(v["statistics"].get("viewCount", 0))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--competitors")
    ap.add_argument("--days", type=float, default=3)
    ap.add_argument("--own-uploads", action="store_true")
    ap.add_argument("--region", default="IN")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    yt = youtube()

    if a.own_uploads:
        r = yt.channels().list(part="contentDetails", mine=True).execute()
        pl = r["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
        vs = videos(yt, uploads(yt, pl, 500))
        with open(f"{a.out}/own_uploads.md", "w") as f:
            f.write("# Our uploads (never repeat these topics)\n\n")
            for v in vs:
                f.write(f"- {v['snippet']['publishedAt'][:10]} | {v['snippet']['title']} | {views(v)} views\n")
        print(f"{len(vs)} own uploads -> {a.out}/own_uploads.md")
        return

    if a.competitors:
        rows = []
        for line in open(a.competitors):
            ref = line.split("#")[0].strip()
            if not ref:
                continue
            info = channel_info(yt, ref)
            if not info:
                print("not found:", ref)
                continue
            name, pl = info
            vs = videos(yt, uploads(yt, pl, 30))
            med = statistics.median([views(v) for v in vs[3:]] or [1]) or 1
            for v in vs:
                h = age_hours(v)
                if h <= a.days * 24:
                    rows.append((views(v) / h, name, v, views(v) / med))
        rows.sort(key=lambda r: r[0], reverse=True)
        with open(f"{a.out}/competitors.md", "w") as f:
            f.write(f"# Competitor uploads, last {a.days:g} days (sorted by views/hour)\n\n")
            f.write("| views/hr | x channel median | channel | title | link |\n|---|---|---|---|---|\n")
            for vph, name, v, mult in rows:
                f.write(f"| {vph:.0f} | {mult:.1f}x | {name} | {v['snippet']['title']} | https://youtu.be/{v['id']} |\n")
        print(f"{len(rows)} recent competitor videos -> {a.out}/competitors.md")

    r = yt.videos().list(part="snippet,statistics", chart="mostPopular", regionCode=a.region, maxResults=50).execute()
    with open(f"{a.out}/trending.md", "w") as f:
        f.write(f"# Trending now ({a.region})\n\n")
        for v in r["items"]:
            f.write(f"- {v['snippet']['title']} | {v['snippet']['channelTitle']} | {views(v)} views | https://youtu.be/{v['id']}\n")
    print(f"trending -> {a.out}/trending.md")


if __name__ == "__main__":
    main()
