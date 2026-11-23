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


def analytics(video_ids, start, end):
    try:
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        creds = Credentials(None, refresh_token=os.environ["YT_REFRESH_TOKEN"],
                            client_id=os.environ["YT_CLIENT_ID"], client_secret=os.environ["YT_CLIENT_SECRET"],
                            token_uri="https://oauth2.googleapis.com/token")
        ya = build("youtubeAnalytics", "v2", credentials=creds, cache_discovery=False)
        r = ya.reports().query(ids="channel==MINE", startDate=start, endDate=end, dimensions="video",
                               metrics="views,averageViewDuration,averageViewPercentage,subscribersGained,shares,likes",
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
        f.write("| published | title | category | views | likes | comments | avg view % | avg view s | subs | shares |\n")
        f.write("|---|---|---|---|---|---|---|---|---|---|\n")
        for v in sorted(vids, key=lambda v: int(v["statistics"].get("viewCount", 0)), reverse=True):
            s, x = v["statistics"], an.get(v["id"], {})
            f.write(f"| {v['snippet']['publishedAt'][:10]} | {v['snippet']['title'][:60]} | "
                    f"{log.get(v['id'], {}).get('category', '?')} | {s.get('viewCount', 0)} | {s.get('likeCount', 0)} | "
                    f"{s.get('commentCount', 0)} | {x.get('averageViewPercentage', '-')} | {x.get('averageViewDuration', '-')} | "
                    f"{x.get('subscribersGained', '-')} | {x.get('shares', '-')} |\n")
    print(f"audit -> {a.out} ({len(vids)} videos)")


if __name__ == "__main__":
    main()
