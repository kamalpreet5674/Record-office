#!/usr/bin/env python3
"""Search or fetch real photos/documents from Wikimedia Commons WITH license + credit line.

Usage:
  python3 fetch_commons.py search "Apollo 11 launch" --limit 8          # list candidates + licenses
  python3 fetch_commons.py get "File:Aldrin_Apollo_11_original.jpg" --out assets/raw --width 2000

Every download appends a record to <out>/CREDITS.json and CREDITS.md:
  file, title, author, license, license_url, source_page, credit_line, description
Rejects files whose license is not reusable (no "NC"/"ND" unless --allow-restricted).
Only Python stdlib. Backs off on HTTP 429 (Wikimedia rate limit).
"""
import argparse, html, json, os, re, sys, time, urllib.parse, urllib.request

API = "https://commons.wikimedia.org/w/api.php"
UA = "VideoEditingSkill/2.0 (asset sourcing; respectful rate)"


def _get(url, binary=False, tries=6):
    delay = 4
    for i in range(tries):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                data = r.read()
                return data if binary else data.decode("utf-8")
        except urllib.error.HTTPError as e:
            if e.code in (429, 503) and i < tries - 1:
                ra = e.headers.get("Retry-After", "")
                wait = int(ra) if ra.isdigit() else delay
                print(f"rate limited ({e.code}); waiting {wait}s", file=sys.stderr)
                time.sleep(min(wait, 120)); delay = min(delay * 2, 120); continue
            raise


def _strip(s):
    s = re.sub(r"<[^>]+>", "", s or "")
    return html.unescape(s).strip()


def info(titles, width=None):
    q = {"action": "query", "format": "json", "prop": "imageinfo",
         "iiprop": "url|extmetadata|size|mime", "titles": "|".join(titles)}
    if width:
        q["iiurlwidth"] = str(width)
    d = json.loads(_get(API + "?" + urllib.parse.urlencode(q)))
    out = []
    for p in d.get("query", {}).get("pages", {}).values():
        if "imageinfo" not in p:
            continue
        ii = p["imageinfo"][0]; m = ii.get("extmetadata", {})
        v = lambda k: _strip(m.get(k, {}).get("value", ""))
        lic = v("LicenseShortName") or v("UsageTerms")
        author = v("Artist") or v("Credit") or "Unknown"
        out.append({
            "title": p["title"], "author": author[:160], "license": lic,
            "license_url": v("LicenseUrl"), "source_page": ii.get("descriptionurl", ""),
            "url": ii.get("thumburl") or ii.get("url"), "width": ii.get("width"),
            "height": ii.get("height"), "mime": ii.get("mime"),
            "description": v("ImageDescription")[:300], "date": v("DateTimeOriginal")[:60],
            "credit_line": f"{author[:80]} / {lic} / Wikimedia Commons",
        })
    return out


def restricted(lic):
    l = (lic or "").upper()
    return any(t in l for t in ("-NC", " NC", "-ND", " ND", "NON-COMMERCIAL", "FAIR USE")) or not l


def search(term, limit):
    q = {"action": "query", "format": "json", "list": "search", "srnamespace": "6",
         "srsearch": term, "srlimit": str(limit)}
    d = json.loads(_get(API + "?" + urllib.parse.urlencode(q)))
    titles = [h["title"] for h in d.get("query", {}).get("search", [])]
    return info(titles) if titles else []


def get(title, out, width, allow_restricted):
    if not title.startswith("File:"):
        title = "File:" + title
    recs = info([title], width)
    if not recs:
        sys.exit(f"not found: {title}")
    r = recs[0]
    if restricted(r["license"]) and not allow_restricted:
        sys.exit(f"REFUSED (license '{r['license']}' not clearly reusable): {title}")
    os.makedirs(out, exist_ok=True)
    name = re.sub(r"[^\w.\-]+", "_", title[5:])
    path = os.path.join(out, name)
    with open(path, "wb") as f:
        f.write(_get(r["url"], binary=True))
    r["file"] = path
    cj = os.path.join(out, "CREDITS.json")
    data = json.load(open(cj)) if os.path.exists(cj) else []
    data = [x for x in data if x.get("title") != r["title"]] + [r]
    json.dump(data, open(cj, "w"), indent=2, ensure_ascii=False)
    with open(os.path.join(out, "CREDITS.md"), "w") as f:
        f.write("# Asset credits (paste into video description)\n\n")
        for x in data:
            f.write(f"- {os.path.basename(x['file'])}: {x['credit_line']} — {x['source_page']}\n")
    print(json.dumps({k: r[k] for k in ("file", "license", "author", "source_page")}, ensure_ascii=False))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search"); s.add_argument("term"); s.add_argument("--limit", type=int, default=8)
    g = sub.add_parser("get"); g.add_argument("title"); g.add_argument("--out", default="assets/raw")
    g.add_argument("--width", type=int, default=2000); g.add_argument("--allow-restricted", action="store_true")
    a = ap.parse_args()
    if a.cmd == "search":
        for r in search(a.term, a.limit):
            flag = "RESTRICTED" if restricted(r["license"]) else "ok"
            print(f"[{flag}] {r['title']} | {r['license']} | {r['width']}x{r['height']} | {r['author'][:50]}")
    else:
        get(a.title, a.out, a.width, a.allow_restricted)
