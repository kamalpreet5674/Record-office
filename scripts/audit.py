"""Channel performance audit (run every 3 days by Routine C).

  python scripts/audit.py --days 30 --out data/audits/<date>.md

Pulls our recent uploads with views, likes, comments (YouTube Data API) and, if the token has the
yt-analytics.readonly scope, retention and subscriber numbers (YouTube Analytics API):
average view %, average view duration, subscribers gained, shares.
Joins them with data/topics_log.csv (category, topic) so Claude can see which topics, hooks and
lengths work. CTR/impressions are not in the API: the owner can paste Studio exports into
data/channel_insights.md.
"""
import argparse
import csv
import datetime as dt
import os

from yt_common import youtube


DUBAI = dt.timezone(dt.timedelta(hours=4))


def local(v):
    return dt.datetime.fromisoformat(v["snippet"]["publishedAt"].replace("Z", "+00:00")).astimezone(DUBAI)


def iso_seconds(d):
    import re
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", d or "")
    return sum(int(x or 0) * k for x, k in zip(m.groups(), (3600, 60, 1))) if m else 0


def analytics(video_ids, start, end):
    try:
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        creds = Credentials(None, refresh_token=os.environ["YT_REFRESH_TOKEN"],
                            client_id=os.environ["YT_CLIENT_ID"], client_secret=os.environ["YT_CLIENT_SECRET"],
                            token_uri="https://oauth2.googleapis.com/token")
        ya = build("youtubeAnalytics", "v2", credentials=creds, cache_discovery=False)
        r = ya.reports().query(ids="channel==MINE", startDate=start, endDate=end, dimensions="video",
                               metrics="views,engagedViews,averageViewDuration,averageViewPercentage,subscribersGained,shares,likes",
                               filters="video==" + ",".join(video_ids[:200]), sort="-views", maxResults=200).execute()
        cols = [c["name"] for c in r["columnHeaders"]]
        return {row[0]: dict(zip(cols, row)) for row in r.get("rows", [])}
    except Exception as e:
        print("Analytics API not available (add the yt-analytics.readonly scope to the token):", str(e)[:200])
        return {}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    yt = youtube()
    ch = yt.channels().list(part="contentDetails,statistics", mine=True).execute()["items"][0]
    pl = ch["contentDetails"]["relatedPlaylists"]["uploads"]
    since = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=a.days)
    ids, token = [], None
    while True:
        r = yt.playlistItems().list(part="contentDetails", playlistId=pl, maxResults=50, pageToken=token).execute()
        ids += [i["contentDetails"]["videoId"] for i in r["items"]]
        token = r.get("nextPageToken")
        if not token or len(ids) >= 100:
            break
    vids = []
    for i in range(0, len(ids), 50):
        vids += yt.videos().list(part="snippet,statistics,contentDetails", id=",".join(ids[i:i + 50])).execute()["items"]
    vids = [v for v in vids if dt.datetime.fromisoformat(v["snippet"]["publishedAt"].replace("Z", "+00:00")) >= since]
    log = {}
    if os.path.exists("data/topics_log.csv"):
        for row in csv.DictReader(open("data/topics_log.csv", encoding="utf-8")):
            log[row.get("video_id", "")] = row
    an = analytics([v["id"] for v in vids], since.date().isoformat(), dt.date.today().isoformat()) if vids else {}
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(f"# Audit {dt.date.today()} (uploads from the last {a.days} days)\n\n")
        f.write(f"Channel: {ch['statistics'].get('subscriberCount')} subscribers, {ch['statistics'].get('viewCount')} total views\n\n")
        f.write("stayed % = engaged views / views: viewers who did not swipe away at the start (Shorts target 70+).\n\n")
        f.write("| published (Dubai) | title | category | len s | views | stayed % | likes | comments | avg view % | avg view s | subs | shares |\n")
        f.write("|---|---|---|---|---|---|---|---|---|---|---|---|\n")
        for v in sorted(vids, key=lambda v: int(v["statistics"].get("viewCount", 0)), reverse=True):
            s, x = v["statistics"], an.get(v["id"], {})
            pct = x.get("averageViewPercentage")
            pct = round(pct, 1) if isinstance(pct, (int, float)) else "-"
            stayed = round(100 * x["engagedViews"] / x["views"]) if x.get("views") and "engagedViews" in x else "-"
            f.write(f"| {local(v):%Y-%m-%d %H:%M} | {v['snippet']['title'][:60]} | "
                    f"{log.get(v['id'], {}).get('category', '?')} | {iso_seconds(v['contentDetails'].get('duration', ''))} | "
                    f"{s.get('viewCount', 0)} | {stayed} | {s.get('likeCount', 0)} | "
                    f"{s.get('commentCount', 0)} | {pct} | {x.get('averageViewDuration', '-')} | "
                    f"{x.get('subscribersGained', '-')} | {x.get('shares', '-')} |\n")
        # views by posting hour (Dubai), Shorts only (<= 3 min), for the publish-slot decision
        buckets = {}
        for v in vids:
            if iso_seconds(v["contentDetails"].get("duration", "")) > 180:
                continue
            h = local(v).hour
            b = f"{h - h % 3:02d}-{h - h % 3 + 3:02d}h"
            x = an.get(v["id"], {})
            buckets.setdefault(b, []).append((int(v["statistics"].get("viewCount", 0)), x.get("averageViewPercentage")))
        f.write("\n## Shorts: views by posting hour (Dubai)\n\n| window | Shorts | avg views | median views | avg view % |\n|---|---|---|---|---|\n")
        for b in sorted(buckets):
            vs = sorted(n for n, _ in buckets[b])
            pc = [p for _, p in buckets[b] if p is not None]
            f.write(f"| {b} | {len(vs)} | {sum(vs) // len(vs)} | {vs[len(vs) // 2]} | "
                    f"{round(sum(pc) / len(pc), 1) if pc else '-'} |\n")
    print(f"audit -> {a.out} ({len(vids)} videos)")


if __name__ == "__main__":
    main()
