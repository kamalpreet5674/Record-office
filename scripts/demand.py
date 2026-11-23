"""Free search-demand check for candidate topics (no vidIQ needed).

  python scripts/demand.py "rani ki vav" "stepwell gujarat" --out videos/_research/<date>/demand.md

For each query:
- YouTube autocomplete suggestions (what people actually type; more and longer = more demand)
- Top 15 YouTube results for India/Hindi: views, age, views per day, how many are recent
- A rough demand score so candidates can be compared side by side
Costs about 101 YouTube API units per query (10,000 free per day).
"""
import argparse
import datetime as dt
import statistics

import requests

from yt_common import youtube


def suggestions(q):
    try:
        r = requests.get("https://suggestqueries.google.com/complete/search", timeout=20,
                         params={"client": "firefox", "ds": "yt", "q": q, "hl": "hi", "gl": "IN"})
        return r.json()[1]
    except Exception as e:
        print("suggest failed:", e)
        return []


def results(yt, q):
    s = yt.search().list(part="id", q=q, type="video", maxResults=15, regionCode="IN",
                         relevanceLanguage="hi", order="relevance").execute()
    ids = [i["id"]["videoId"] for i in s.get("items", [])]
    if not ids:
        return []
    v = yt.videos().list(part="snippet,statistics,contentDetails", id=",".join(ids)).execute()
    now = dt.datetime.now(dt.timezone.utc)
    out = []
    for it in v["items"]:
        pub = dt.datetime.fromisoformat(it["snippet"]["publishedAt"].replace("Z", "+00:00"))
        days = max((now - pub).days, 1)
        views = int(it["statistics"].get("viewCount", 0))
        out.append({"title": it["snippet"]["title"], "channel": it["snippet"]["channelTitle"],
                    "views": views, "days": days, "vpd": views / days, "id": it["id"]})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("queries", nargs="+")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    yt = youtube()
    rows, detail = [], []
    for q in a.queries:
        sug = suggestions(q)
        res = results(yt, q)
        med_vpd = statistics.median([r["vpd"] for r in res]) if res else 0
        recent = sum(1 for r in res if r["days"] <= 30)
        hot = sum(1 for r in res if r["days"] <= 30 and r["vpd"] > med_vpd)
        # Rough score: demand (views/day) and interest (suggestions), boosted if recent videos are winning.
        score = round((med_vpd ** 0.5) * (1 + len(sug) / 10) * (1 + hot / 5), 1)
        rows.append((q, score, len(sug), round(med_vpd), recent, hot))
        detail.append(f"\n## {q}\nSuggestions: {', '.join(sug[:10]) or '(none)'}\n")
        for r in sorted(res, key=lambda r: r["vpd"], reverse=True)[:8]:
            detail.append(f"- {r['vpd']:.0f}/day · {r['views']} views · {r['days']}d · {r['channel']} · "
                          f"{r['title']} · https://youtu.be/{r['id']}")
    rows.sort(key=lambda r: r[1], reverse=True)
    with open(a.out, "w", encoding="utf-8") as f:
        f.write("# Demand check (higher score = more people searching and watching now)\n\n")
        f.write("| query | score | suggestions | median views/day | videos last 30d | recent winners |\n|---|---|---|---|---|---|\n")
        for q, sc, ns, vpd, rc, hot in rows:
            f.write(f"| {q} | {sc} | {ns} | {vpd} | {rc} | {hot} |\n")
        f.write("\n".join(detail) + "\n")
    print(f"demand -> {a.out}")
    for r in rows:
        print(r)


if __name__ == "__main__":
    main()
