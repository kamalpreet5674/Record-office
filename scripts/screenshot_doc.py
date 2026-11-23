"""Screenshot a real source page (press release, report, archive record) to show on screen.

  python scripts/screenshot_doc.py URL --out videos/<dir>/assets/doc_rbi.png [--find "exact text to highlight"]

Opens the page, highlights the given text in yellow (if found), scrolls it into view and saves a
1080x1350 screenshot. Use it in SHOTS.tsv as type=doc (the assembler frames it like a document on
screen). Only screenshot the real source of a fact; it is the "record" the channel promises.
Needs: pip install playwright && python -m playwright install --with-deps chromium
"""
import argparse
import os
import sys

from playwright.sync_api import sync_playwright

HIGHLIGHT_JS = """
(text) => {
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let node;
  while ((node = walker.nextNode())) {
    const i = node.nodeValue.indexOf(text);
    if (i >= 0) {
      const range = document.createRange();
      range.setStart(node, i); range.setEnd(node, i + text.length);
      const mark = document.createElement('mark');
      mark.style.background = '#F5C518'; mark.style.color = '#000'; mark.style.padding = '2px 4px';
      range.surroundContents(mark);
      mark.scrollIntoView({block: 'start'}); window.scrollBy(0, -140);
      return true;
    }
  }
  return false;
}
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--out", required=True)
    ap.add_argument("--find", default="")
    a = ap.parse_args()
    with sync_playwright() as p:
        exe = os.environ.get("CHROMIUM_PATH") or None
        b = p.chromium.launch(args=["--no-sandbox"], executable_path=exe)
        page = b.new_page(viewport={"width": 540, "height": 675}, device_scale_factor=2)
        page.goto(a.url, wait_until="networkidle", timeout=60000)
        found = page.evaluate(HIGHLIGHT_JS, a.find) if a.find else False
        if a.find and not found:
            print(f"Text not found on page: {a.find!r} (screenshot taken without highlight)")
        page.wait_for_timeout(500)
        page.screenshot(path=a.out)
        b.close()
    print(f"saved {a.out}" + (" (highlighted)" if found else ""))


if __name__ == "__main__":
    sys.exit(main())
