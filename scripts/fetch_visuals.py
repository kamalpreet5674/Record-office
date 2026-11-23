"""Find and download free images for a shot.

  python scripts/fetch_visuals.py "Pokhran desert 1998" --out videos/<dir>/assets --n 5 [--source wikimedia|openverse|pexels|nasa|all]
  python scripts/fetch_visuals.py "Apollo 11 launch" --out videos/<dir>/assets --kind video --n 3

--kind image (default) or video. Real video clips come from Wikimedia Commons and NASA (both free,
no key). Use them in SHOTS.tsv as type=video, source=assets/<file>@<start seconds>.

Wikimedia Commons (archives, history, documents) needs no key.
Openverse (millions of free-licence photos, general scenes) needs no key.
Pexels is optional: used only if secret PEXELS_API_KEY is set.
Saves images as <slug>_<n>.jpg and appends licence + credit lines to assets/CREDITS.md.
Always open the images and check they really show what the line says.
"""
import argparse
import os
import re

import requests

UA = {"User-Agent": "records-office-shorts/1.0 (automated documentary research)"}


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:40]


KIND = "image"


def wikimedia(q, n):
    ftype = "video" if KIND == "video" else "bitmap"
    r = requests.get("https://commons.wikimedia.org/w/api.php", headers=UA, timeout=30, params={
        "action": "query", "format": "json", "generator": "search", "gsrsearch": f"{q} filetype:{ftype}",
        "gsrnamespace": 6, "gsrlimit": n, "prop": "imageinfo",
        "iiprop": "url|extmetadata", "iiurlwidth": 1440})
    out = []
    for p in (r.json().get("query", {}).get("pages", {}) or {}).values():
        ii = p["imageinfo"][0]
        md = ii.get("extmetadata", {})
        lic = md.get("LicenseShortName", {}).get("value", "?")
        artist = re.sub("<[^>]+>", "", md.get("Artist", {}).get("value", "?"))
        url = ii["url"] if KIND == "video" else (ii.get("thumburl") or ii["url"])
        out.append((url, f"Wikimedia Commons: {p['title']} | {artist} | {lic} | {ii['descriptionurl']}"))
    return out


def nasa(q, n):
    media = "video" if KIND == "video" else "image"
    r = requests.get("https://images-api.nasa.gov/search", headers=UA, timeout=30,
                     params={"q": q, "media_type": media, "page_size": n})
    out = []
    for it in r.json().get("collection", {}).get("items", [])[:n]:
        d = it["data"][0]
        assets = requests.get(it["href"], headers=UA, timeout=30).json()
        want = ("~mobile.mp4", "~small.mp4", "~orig.mp4") if media == "video" else ("~large.jpg", "~medium.jpg", "~orig.jpg")
        url = next((a for w in want for a in assets if a.endswith(w)), None)
        if url:
            out.append((url.replace("http://", "https://"),
                        f"NASA: {d.get('title')} | {d.get('center', 'NASA')} | NASA media (generally not copyrighted) | https://images.nasa.gov/details/{d['nasa_id']}"))
    return out


def openverse(q, n):
    r = requests.get("https://api.openverse.org/v1/images/", headers=UA, timeout=30, params={
        "q": q, "page_size": n, "license_type": "commercial,modification", "mature": "false"})
    if not r.ok:
        print("Openverse error", r.status_code)
        return []
    return [(i["url"], f"Openverse: {i.get('title') or 'image'} | {i.get('creator') or '?'} | "
                       f"{(i.get('license') or '').upper()} {i.get('license_version') or ''} | {i.get('foreign_landing_url')}")
            for i in r.json().get("results", [])]


def pexels(q, n):
    key = os.environ.get("PEXELS_API_KEY")
    if not key:
        return []
    r = requests.get("https://api.pexels.com/v1/search", headers={"Authorization": key}, timeout=30,
                     params={"query": q, "per_page": n, "orientation": "portrait"})
    return [(p["src"]["large2x"], f"Pexels: photo by {p['photographer']} | Pexels License | {p['url']}")
            for p in r.json().get("photos", [])]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("--out", required=True)
    ap.add_argument("--n", type=int, default=5)
    ap.add_argument("--source", default="all")
    ap.add_argument("--kind", default="image", choices=["image", "video"])
    a = ap.parse_args()
    global KIND
    KIND = a.kind
    os.makedirs(a.out, exist_ok=True)
    found = []

    def safe(fn):
        try:
            return fn(a.query, a.n)
        except Exception as e:  # one source failing should not stop the others
            print(f"{fn.__name__} failed: {e}")
            return []

    if a.source in ("wikimedia", "all", "both"):
        found += safe(wikimedia)
    if a.source in ("nasa", "all"):
        found += safe(nasa)
    if a.source in ("openverse", "all") and KIND == "image":
        found += safe(openverse)
    if a.source in ("pexels", "all", "both") and KIND == "image":
        found += safe(pexels)
    with open(f"{a.out}/CREDITS.md", "a") as credits:
        for i, (url, credit) in enumerate(found, 1):
            ext = (url.split("?")[0].rsplit(".", 1)[-1].lower() if KIND == "video" else "jpg")[:5]
            name = f"{slug(a.query)}_{i}.{ext}"
            r = requests.get(url, headers=UA, timeout=60)
            if not r.ok:
                continue
            open(f"{a.out}/{name}", "wb").write(r.content)
            credits.write(f"- {name}: {credit}\n")
            print(f"{a.out}/{name}  <- {credit}")
    if not found:
        print("Nothing found. Try a simpler or English query.")


if __name__ == "__main__":
    main()
