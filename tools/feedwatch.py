#!/usr/bin/env python3
"""
feedwatch (T1) — expert feed aggregator for the *Shipping With Agents*
curriculum.

Watches every practitioner named in PRACTITIONER-DOSSIER.md, detects new
writing, and drafts an inbox report proposing what the curriculum should do
about it.

    python3 feedwatch.py fetch                 # poll sources, record what is new
    python3 feedwatch.py report [--since 30d]  # write inbox/YYYY-MM-DD.md
    python3 feedwatch.py classify --print-prompt   # emit the classifier prompt
    python3 feedwatch.py sources               # list configured sources + health

Design notes
------------
* Classification is deliberately NOT hardcoded to a vendor API. `report`
  emits items with a ready-to-run classification prompt; wire it to whatever
  model you use, or pipe the report into your coding agent and let it triage.
  The tool's job is detection and framing, not judgment.
* `index` sources are handled by diffing the set of links on a page. Crude,
  robust, and requires no feed.
* Everything is stored in SQLite so a missed week does not lose history.

Dependencies: standard library. `pyyaml` for the config, `feedparser`
optional (RSS falls back to a regex parser if absent).
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sqlite3
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
DB = HERE / "feedwatch.sqlite"
CONFIG = HERE / "feeds.yaml"
INBOX = HERE.parent / "inbox"
UA = "feedwatch/1.0 (curriculum maintenance)"

CLASSES = ["position-change", "new-technique", "evidence", "tool-change",
           "restatement", "noise"]

CLASSIFIER_PROMPT = """\
You are triaging new writing by a practitioner tracked in a curriculum on
agentic software engineering. Classify the item into EXACTLY ONE class.

The curriculum currently attributes these positions to {person}:
---
{dossier_excerpt}
---

The new item:
  Title: {title}
  URL: {url}
  Published: {published}
  Content: {content}

Classes, in priority order — if more than one applies, choose the highest:

1. position-change — the author now contradicts, qualifies, or supersedes a
   position the curriculum attributes to them above. You MUST quote the passage
   that shows this. If you cannot quote it, this is not a position-change.
2. new-technique — a concrete practice not already covered by the curriculum.
3. evidence — a study, measurement, benchmark, or dataset.
4. tool-change — a claim about a specific product, model, version, or price.
5. restatement — says something the curriculum already says.
6. noise — not relevant to agentic software engineering.

Respond as JSON:
{{"class": "...", "summary": "<two sentences>", "quote": "<required for
position-change, else null>", "proposed_action": "<e.g. 'module: M8 — add to
what-agents-want list' or 'state-of-play: §5' or 'none'>", "confidence":
"high|medium|low"}}

Be conservative. Most items are restatements. Over-reporting position-changes
destroys the signal this tool exists to provide.
"""

# ------------------------------------------------------------------ store

SCHEMA = """
CREATE TABLE IF NOT EXISTS items (
  id TEXT PRIMARY KEY, person TEXT, dossier_id TEXT, source TEXT,
  url TEXT, title TEXT, published TEXT, first_seen TEXT,
  classification TEXT, summary TEXT, triaged INTEGER DEFAULT 0
);
CREATE TABLE IF NOT EXISTS fetches (
  source TEXT PRIMARY KEY, last_ok TEXT, last_status TEXT, item_count INTEGER
);
"""


def db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB)
    conn.executescript(SCHEMA)
    return conn


# ------------------------------------------------------------------ fetch

def http_get(url: str, timeout: int = 20) -> tuple[int, str]:
    ctx = ssl.create_default_context()
    bundle = "/root/.ccr/ca-bundle.crt"
    if os.path.exists(bundle):
        try:
            ctx.load_verify_locations(bundle)
        except Exception:
            pass
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:  # noqa: BLE001
        reason = str(getattr(e, "reason", e))
        if "Tunnel connection failed" in reason:
            return -407, ""      # egress proxy refused; not the source's fault
        return -1, reason


ENTRY_RE = re.compile(
    r"<(?:entry|item)\b.*?</(?:entry|item)>", re.S | re.I)
TAG_RE = {
    "title": re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I),
    "link": re.compile(r'<link[^>]*href="([^"]+)"|<link[^>]*>(.*?)</link>', re.S | re.I),
    "date": re.compile(r"<(?:published|updated|pubDate)[^>]*>(.*?)</", re.S | re.I),
}
HREF_RE = re.compile(r'href="([^"#?]+)"')


def clean(s: str) -> str:
    s = re.sub(r"<!\[CDATA\[(.*?)\]\]>", r"\1", s, flags=re.S)
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"\s+", " ", s).strip()


def parse_feed(body: str, base: str) -> list[dict]:
    out = []
    for raw in ENTRY_RE.findall(body):
        title = clean(TAG_RE["title"].search(raw).group(1)) if TAG_RE["title"].search(raw) else ""
        lm = TAG_RE["link"].search(raw)
        link = (lm.group(1) or clean(lm.group(2) or "")) if lm else ""
        dm = TAG_RE["date"].search(raw)
        out.append({"title": title, "url": urllib.parse.urljoin(base, link),
                    "published": clean(dm.group(1)) if dm else ""})
    return out


def parse_index(body: str, base: str) -> list[dict]:
    """Treat every same-host link as a candidate item; dedupe by URL."""
    host = urllib.parse.urlparse(base).netloc
    seen, out = set(), []
    for href in HREF_RE.findall(body):
        url = urllib.parse.urljoin(base, href)
        p = urllib.parse.urlparse(url)
        if p.netloc != host or url in seen or len(p.path.strip("/")) < 4:
            continue
        seen.add(url)
        out.append({"title": p.path.strip("/").split("/")[-1].replace("-", " "),
                    "url": url, "published": ""})
    return out


def item_id(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()[:16]


def load_config() -> dict:
    try:
        import yaml
    except ImportError:
        sys.exit("feedwatch needs pyyaml for the config: pip install pyyaml")
    return yaml.safe_load(CONFIG.read_text())


def cmd_fetch(args) -> int:
    cfg, conn = load_config(), db()
    now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    entries = [(p["person"], p.get("dossier_id", ""), s)
               for p in cfg.get("people", []) for s in p.get("sources", [])]
    entries += [(i["name"], "", s)
                for i in cfg.get("institutions", []) for s in i.get("sources", [])]

    new_total = blocked = 0
    for person, did, src in entries:
        kind, url = src.get("kind"), src.get("url", "")
        if kind in ("manual", "github"):
            print(f"  skip  {person}: {kind} source needs {'manual review' if kind=='manual' else 'the GitHub API'} — {url}")
            continue
        status, body = http_get(url)
        if status == -407:
            blocked += 1
            print(f"  BLOCK {person}: egress proxy refused {url}")
            conn.execute("REPLACE INTO fetches VALUES (?,?,?,?)", (url, None, "proxy-blocked", 0))
            continue
        if status != 200 or not body:
            print(f"  FAIL  {person}: HTTP {status} {url}"
                  + ("   <- marked unverified in feeds.yaml" if src.get("unverified") else ""))
            conn.execute("REPLACE INTO fetches VALUES (?,?,?,?)", (url, None, str(status), 0))
            continue
        items = parse_feed(body, url) if kind == "rss" else parse_index(body, url)
        added = 0
        for it in items:
            iid = item_id(it["url"])
            if conn.execute("SELECT 1 FROM items WHERE id=?", (iid,)).fetchone():
                continue
            conn.execute("INSERT INTO items (id,person,dossier_id,source,url,title,"
                         "published,first_seen) VALUES (?,?,?,?,?,?,?,?)",
                         (iid, person, did, url, it["url"], it["title"],
                          it["published"], now))
            added += 1
        new_total += added
        conn.execute("REPLACE INTO fetches VALUES (?,?,?,?)", (url, now, "ok", len(items)))
        print(f"  ok    {person}: {added} new of {len(items)} — {url}")
    conn.commit()
    print(f"\n{new_total} new item(s). {blocked} source(s) blocked by an egress proxy.")
    if blocked:
        print("Proxy-blocked sources say nothing about the source. Re-run where "
              "outbound HTTPS is unrestricted.")
    return 0


def parse_since(s: str) -> dt.datetime:
    n, unit = int(s[:-1]), s[-1]
    days = {"d": 1, "w": 7, "m": 30}[unit] * n
    return dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=days)


def cmd_report(args) -> int:
    conn = db()
    cutoff = parse_since(args.since).isoformat(timespec="seconds")
    rows = conn.execute(
        "SELECT person,title,url,published,first_seen,classification,summary "
        "FROM items WHERE first_seen >= ? ORDER BY person, first_seen DESC",
        (cutoff,)).fetchall()
    INBOX.mkdir(exist_ok=True)
    out = INBOX / f"{dt.date.today().isoformat()}.md"
    lines = [f"# Curriculum inbox — {dt.date.today().isoformat()}", "",
             f"{len(rows)} item(s) first seen in the last {args.since}.", "",
             "Unclassified items are listed under **needs triage**. Run each "
             "through the classifier prompt (`feedwatch.py classify "
             "--print-prompt`) or hand this file to your agent and ask it to "
             "triage against `PRACTITIONER-DOSSIER.md`.", ""]
    by_class: dict[str, list] = {}
    for r in rows:
        by_class.setdefault(r[5] or "needs triage", []).append(r)
    for cls in ["position-change", "new-technique", "evidence", "tool-change",
                "needs triage", "restatement", "noise"]:
        items = by_class.get(cls)
        if not items:
            continue
        flag = "  ⚠ **CURRICULUM IS WRONG UNTIL RESOLVED**" if cls == "position-change" else ""
        lines += [f"## {cls} ({len(items)}){flag}", ""]
        for person, title, url, published, seen, _c, summary in items:
            lines.append(f"- **{person}** — [{title or url}]({url})"
                         + (f" · {published}" if published else "")
                         + (f"\n  \n  {summary}" if summary else ""))
        lines.append("")
    out.write_text("\n".join(lines))
    print(f"wrote {out} ({len(rows)} items)")
    return 0


def cmd_classify(args) -> int:
    if args.print_prompt:
        print(CLASSIFIER_PROMPT)
        return 0
    print("Wire this to your model of choice. The prompt is printed by "
          "`--print-prompt`; store the JSON result in items.classification "
          "and items.summary.", file=sys.stderr)
    return 0


def cmd_sources(args) -> int:
    cfg, conn = load_config(), db()
    health = {r[0]: (r[1], r[2], r[3]) for r in
              conn.execute("SELECT source,last_ok,last_status,item_count FROM fetches")}
    for p in cfg.get("people", []) + [
            {"person": i["name"], "sources": i["sources"]} for i in cfg.get("institutions", [])]:
        print(f"\n{p.get('person')}")
        for s in p.get("sources", []):
            h = health.get(s.get("url", ""), (None, "never fetched", 0))
            mark = "?" if s.get("unverified") else " "
            print(f"  [{mark}] {s['kind']:6} {s.get('url','')}\n"
                  f"        last: {h[1]}  items: {h[2]}  at: {h[0] or '-'}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("fetch").set_defaults(fn=cmd_fetch)
    r = sub.add_parser("report"); r.add_argument("--since", default="30d"); r.set_defaults(fn=cmd_report)
    c = sub.add_parser("classify"); c.add_argument("--print-prompt", action="store_true"); c.set_defaults(fn=cmd_classify)
    sub.add_parser("sources").set_defaults(fn=cmd_sources)
    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
