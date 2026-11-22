"""Find and download free images for a shot.

  python scripts/fetch_visuals.py "Pokhran desert 1998" --out videos/<dir>/assets --n 5 [--source wikimedia|pexels|both]

Wikimedia Commons (archives, history, documents) needs no key.
Pexels (general modern scenes) needs secret PEXELS_API_KEY.
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


def wikimedia(q, n):
    r = requests.get("https://commons.wikimedia.org/w/api.php", headers=UA, timeout=30, params={
        "action": "query", "format": "json", "generator": "search", "gsrsearch": f"{q} filetype:bitmap",
        "gsrnamespace": 6, "gsrlimit": n, "prop": "imageinfo",
        "iiprop": "url|extmetadata", "iiurlwidth": 1440})
    out = []
    for p in (r.json().get("query", {}).get("pages", {}) or {}).values():
        ii = p["imageinfo"][0]
        md = ii.get("extmetadata", {})
        lic = md.get("LicenseShortName", {}).get("value", "?")
        artist = re.sub("<[^>]+>", "", md.get("Artist", {}).get("value", "?"))
        out.append((ii.get("thumburl") or ii["url"], f"Wikimedia Commons: {p['title']} | {artist} | {lic} | {ii['descriptionurl']}"))
    return out


def pexels(q, n):
    key = os.environ.get("PEXELS_API_KEY")
    if not key:
        print("PEXELS_API_KEY not set, skipping Pexels")
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
    ap.add_argument("--source", default="both")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    found = []
    if a.source in ("wikimedia", "both"):
        found += wikimedia(a.query, a.n)
    if a.source in ("pexels", "both"):
        found += pexels(a.query, a.n)
    with open(f"{a.out}/CREDITS.md", "a") as credits:
        for i, (url, credit) in enumerate(found, 1):
            name = f"{slug(a.query)}_{i}.jpg"
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
