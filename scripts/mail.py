"""Email the owner and read their replies (Gmail, with an app password).

  python scripts/mail.py send --subject "[RO-SCRIPT 2026-11-23-slug] ..." --body-file videos/<dir>/EMAIL.md
  python scripts/mail.py replies --tag RO-SCRIPT --days 3 [--save-attachments videos]

  python scripts/mail.py notify --title "..." --message "..." [--click URL]

Needs secrets: GMAIL_ADDRESS (the sending Gmail), GMAIL_APP_PASSWORD (Google account →
Security → App passwords), OWNER_EMAIL (where scripts go and whose replies count).
Optional NTFY_TOPIC: every email also pings your phone through the free ntfy app.
`replies` prints JSON: one item per reply from OWNER_EMAIL whose subject has the tag,
with subject, date and the new text only (quoted old mail removed).
With --save-attachments ROOT, images/videos attached to a reply (e.g. Flow generations sent from
the phone) are saved to ROOT/<dir>/assets/flow/, where <dir> comes from "[RO-SCRIPT <dir>]".
"""
import argparse
import datetime as dt
import email
import email.utils
import imaplib
import json
import os
import re
import smtplib
import sys
from email.header import decode_header, make_header
from email.mime.text import MIMEText


def env(k):
    v = os.environ.get(k)
    if not v:
        sys.exit(f"Missing secret {k}. See SETUP.md.")
    return v


def notify(title, message, click=None):
    """Phone push notification through the free ntfy app (optional secret NTFY_TOPIC)."""
    topic = os.environ.get("NTFY_TOPIC")
    if not topic:
        return
    import urllib.request
    headers = {"Title": title.encode("utf-8").decode("latin-1", "ignore")[:200], "Priority": "high", "Tags": "clapper"}
    if click:
        headers["Click"] = click
    req = urllib.request.Request(f"https://ntfy.sh/{topic}", data=message.encode("utf-8"), headers=headers)
    try:
        urllib.request.urlopen(req, timeout=20)
        print("phone notification sent")
    except Exception as e:
        print("notification failed:", e)


def send(subject, body):
    me, pw, to = env("GMAIL_ADDRESS"), env("GMAIL_APP_PASSWORD"), env("OWNER_EMAIL")
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"], msg["From"], msg["To"] = subject, me, to
    msg["Message-ID"] = email.utils.make_msgid(domain="records-office.local")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
        s.login(me, pw)
        s.send_message(msg)
    print("sent:", subject)
    first = next((l for l in body.splitlines() if l.strip() and not l.startswith("Reply")), "")
    notify(subject, (first[:180] or "New email from Records Office") + "\nOpen Gmail to reply.",
           click="https://mail.google.com/mail/u/0/#inbox")


def new_text(m):
    part = None
    if m.is_multipart():
        for p in m.walk():
            if p.get_content_type() == "text/plain" and "attachment" not in str(p.get("Content-Disposition")):
                part = p
                break
    else:
        part = m
    if part is None:
        return ""
    text = part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8", "replace")
    out = []
    for line in text.splitlines():
        if line.startswith(">") or re.match(r"^On .+ wrote:$", line.strip()) or re.match(r"^.+ ने लिखा:$", line.strip()):
            break
        out.append(line)
    return "\n".join(out).strip()


def save_attachments(m, subject, root):
    mt = re.search(r"\[RO-SCRIPT ([^\]\s]+)\]", subject)
    if not mt or not root:
        return []
    folder = os.path.join(root, mt.group(1), "assets", "flow")
    saved = []
    for p in m.walk():
        fn = p.get_filename()
        ctype = p.get_content_type()
        if not fn or not (ctype.startswith("image/") or ctype.startswith("video/")):
            continue
        os.makedirs(folder, exist_ok=True)
        fn = re.sub(r"[^A-Za-z0-9._-]+", "_", str(make_header(decode_header(fn))))
        path = os.path.join(folder, fn)
        with open(path, "wb") as f:
            f.write(p.get_payload(decode=True))
        saved.append(path)
    return saved


def replies(tag, days, root=None):
    me, pw, owner = env("GMAIL_ADDRESS"), env("GMAIL_APP_PASSWORD"), env("OWNER_EMAIL").lower()
    since = (dt.date.today() - dt.timedelta(days=days)).strftime("%d-%b-%Y")
    im = imaplib.IMAP4_SSL("imap.gmail.com")
    im.login(me, pw)
    im.select("INBOX", readonly=True)
    _, ids = im.search(None, f'(SINCE {since} FROM "{owner}" SUBJECT "{tag}")')
    out = []
    for i in ids[0].split():
        _, data = im.fetch(i, "(RFC822)")
        m = email.message_from_bytes(data[0][1])
        sender = email.utils.parseaddr(m["From"])[1].lower()
        if sender != owner or "records-office.local" in (m["Message-ID"] or ""):
            continue  # skip our own sent emails (when sender and owner are the same address)
        subject = str(make_header(decode_header(m["Subject"] or "")))
        out.append({"subject": subject, "date": m["Date"], "message_id": m["Message-ID"],
                    "text": new_text(m), "attachments": save_attachments(m, subject, root)})
    im.logout()
    print(json.dumps(out, ensure_ascii=False, indent=2))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    n = sub.add_parser("notify")
    n.add_argument("--title", required=True)
    n.add_argument("--message", required=True)
    n.add_argument("--click", default=None)
    s = sub.add_parser("send")
    s.add_argument("--subject", required=True)
    s.add_argument("--body-file", required=True)
    r = sub.add_parser("replies")
    r.add_argument("--tag", default="RO-SCRIPT")
    r.add_argument("--days", type=int, default=3)
    r.add_argument("--save-attachments", default=None)
    a = ap.parse_args()
    if a.cmd == "notify":
        notify(a.title, a.message, a.click)
    elif a.cmd == "send":
        send(a.subject, open(a.body_file, encoding="utf-8").read())
    else:
        replies(a.tag, a.days, a.save_attachments)


if __name__ == "__main__":
    main()
