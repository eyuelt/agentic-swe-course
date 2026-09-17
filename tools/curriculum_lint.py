#!/usr/bin/env python3
"""
curriculum-lint (T2) — staleness and integrity linter for the
*Shipping With Agents* curriculum.

Checks that the curriculum has not rotted:
  links      every URL is reachable; reports dead and moved
  staleness  volatile claims are past their half-life
  graph      module prerequisites, citations and cross-references resolve
  all        run everything

Usage:
    python3 curriculum_lint.py all [--dir PATH] [--ci] [--timeout N]
    python3 curriculum_lint.py links --dir .. --fix

Dependencies: standard library only. Honours HTTPS_PROXY/HTTP_PROXY.
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import ssl
import sys
import urllib.error
import urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

# ---------------------------------------------------------------- config

# Volatility tier -> (warn_days, error_days). None means never stale.
STALENESS = {"F": (90, 180), "M": (365, 730), "D": None}
STATE_OF_PLAY_WARN, STATE_OF_PLAY_ERROR = 90, 180

# Hard ordering constraints from CURRICULUM.md Appendix A.
# (earlier, later) — `earlier` must be a prerequisite of `later`, directly or transitively.
HARD_ORDER = [("M12", "M10"), ("M3", "M4"), ("M3", "M9"), ("M1", "M14")]

USER_AGENT = "curriculum-lint/1.0 (+curriculum maintenance; contact repo owner)"

# ---------------------------------------------------------------- model

class Finding:
    __slots__ = ("level", "check", "where", "message")

    def __init__(self, level: str, check: str, where: str, message: str):
        self.level = level          # "error" | "warn" | "info"
        self.check = check
        self.where = where
        self.message = message

    def __str__(self) -> str:
        icon = {"error": "ERROR", "warn": " WARN", "info": " INFO"}[self.level]
        return f"{icon}  [{self.check}] {self.where}: {self.message}"


def md_files(root: Path) -> list[Path]:
    return sorted(p for p in root.rglob("*.md") if ".git" not in p.parts)


# ---------------------------------------------------------------- links

URL_RE = re.compile(r"https?://[^\s<>()\[\]`\"'|]+")


def extract_urls(root: Path) -> dict[str, list[str]]:
    """url -> list of 'file:line' occurrences."""
    found: dict[str, list[str]] = defaultdict(list)
    for path in md_files(root):
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for url in URL_RE.findall(line):
                found[url.rstrip(".,;:")].append(f"{path.name}:{lineno}")
    return found


def probe(url: str, timeout: int) -> tuple[str, str]:
    """Return (status, detail). status in ok|moved|dead|blocked|error."""
    ctx = ssl.create_default_context()
    bundle = "/root/.ccr/ca-bundle.crt"
    if os.path.exists(bundle):
        try:
            ctx.load_verify_locations(bundle)
        except Exception:
            pass

    def _request(method: str):
        req = urllib.request.Request(url, method=method, headers={"User-Agent": USER_AGENT})
        return urllib.request.urlopen(req, timeout=timeout, context=ctx)

    for method in ("HEAD", "GET"):
        try:
            with _request(method) as resp:
                final = resp.geturl()
                if final.rstrip("/") != url.rstrip("/"):
                    return "moved", final
                return "ok", str(resp.status)
        except urllib.error.HTTPError as e:
            if e.code in (403, 405, 429) and method == "HEAD":
                continue                      # some hosts refuse HEAD; retry with GET
            if e.code in (401, 403, 429):
                return "blocked", f"HTTP {e.code} (may be bot protection, verify by hand)"
            return "dead", f"HTTP {e.code}"
        except urllib.error.URLError as e:
            reason = str(e.reason)
            if "Tunnel connection failed" in reason or "407" in reason:
                # An egress proxy refused the connect. This says nothing about the
                # target URL; it means this machine cannot reach it directly.
                return "proxy-blocked", reason
            if method == "GET":
                return "error", reason
        except Exception as e:                # noqa: BLE001 - report anything else
            if method == "GET":
                return "error", type(e).__name__
    return "error", "unreachable"


def check_links(root: Path, timeout: int, workers: int) -> list[Finding]:
    urls = extract_urls(root)
    findings: list[Finding] = []
    print(f"  probing {len(urls)} unique URLs...", file=sys.stderr)
    with ThreadPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(lambda u: (u, probe(u, timeout)), urls))
    blocked = sum(1 for _, (s, _d) in results if s == "proxy-blocked")
    if blocked:
        print(f"  note: {blocked} URLs unreachable because an egress proxy refused "
              f"the connection. These are NOT dead links — re-run somewhere with "
              f"direct outbound HTTPS before believing this report.", file=sys.stderr)
    for url, (status, detail) in results:
        where = urls[url][0]
        if status == "ok":
            continue
        level = {"moved": "warn", "blocked": "warn", "dead": "error",
                 "error": "warn", "proxy-blocked": "info"}[status]
        findings.append(Finding(level, "links", where, f"{status}: {url} -> {detail}"))
    return findings


# ------------------------------------------------------------ staleness

DATE_RE = re.compile(r"(20\d{2})-(\d{2})-(\d{2})")


def check_staleness(root: Path, today: dt.date) -> list[Finding]:
    findings: list[Finding] = []

    # 1. STATE-OF-PLAY compile date
    for path in root.glob("STATE-OF-PLAY-*.md"):
        text = path.read_text(encoding="utf-8")
        m = re.search(r"Compiled\s+(\d{4}-\d{2}-\d{2})", text)
        if not m:
            findings.append(Finding("error", "staleness", path.name,
                                    "no 'Compiled YYYY-MM-DD' stamp found"))
            continue
        age = (today - dt.date.fromisoformat(m.group(1))).days
        if age > STATE_OF_PLAY_ERROR:
            findings.append(Finding("error", "staleness", path.name,
                                    f"compiled {age} days ago; volatile facts are unreliable. "
                                    "Run the refresh checklist."))
        elif age > STATE_OF_PLAY_WARN:
            findings.append(Finding("warn", "staleness", path.name,
                                    f"compiled {age} days ago; quarterly refresh is due"))

    # 2. Fast-volatility resources with no recent verification
    res = root / "RESOURCES.md"
    if res.exists():
        text = res.read_text(encoding="utf-8")
        m = re.search(r"verified live (\d{4}-\d{2}-\d{2})", text)
        verified_age = (today - dt.date.fromisoformat(m.group(1))).days if m else None
        fast = [ln for ln in text.splitlines()
                if ln.startswith("| R-") and re.search(r"\|\s*\*\*F\*\*\s*\|", ln)]
        if verified_age is not None:
            tier = STALENESS["F"]
            if verified_age > tier[1]:
                findings.append(Finding("error", "staleness", "RESOURCES.md",
                                        f"{len(fast)} fast-volatility entries last verified "
                                        f"{verified_age} days ago"))
            elif verified_age > tier[0]:
                findings.append(Finding("warn", "staleness", "RESOURCES.md",
                                        f"{len(fast)} fast-volatility entries last verified "
                                        f"{verified_age} days ago"))
        else:
            findings.append(Finding("warn", "staleness", "RESOURCES.md",
                                    "no 'verified live YYYY-MM-DD' stamp found"))

        unverified = [ln.split("|")[1].strip() for ln in text.splitlines()
                      if ln.startswith("| R-") and "?" in ln.split("|")[5]]
        if unverified:
            findings.append(Finding("info", "staleness", "RESOURCES.md",
                                    f"{len(unverified)} entries marked unverified: "
                                    f"{', '.join(unverified[:8])}"))
    return findings


# ---------------------------------------------------------------- graph

MODULE_RE = re.compile(r"^##\s+(M\d+)\s+[—-]\s+(.+)$", re.M)
PREREQ_RE = re.compile(r"^⊢\s*(.+?)\s*·", re.M)
CITE_RE = re.compile(r"\[R-(\d+)\]")
RESOURCE_ID_RE = re.compile(r"^\|\s*(R-\d+)\s*\|", re.M)


def check_graph(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    cur = root / "CURRICULUM.md"
    if not cur.exists():
        return [Finding("error", "graph", "CURRICULUM.md", "file missing")]
    text = cur.read_text(encoding="utf-8")

    modules = dict(MODULE_RE.findall(text))
    if not modules:
        return [Finding("error", "graph", "CURRICULUM.md", "no module headings parsed")]

    # Prerequisites: associate each ⊢ line with the module heading above it.
    prereqs: dict[str, set[str]] = {}
    current = None
    for line in text.splitlines():
        h = MODULE_RE.match(line)
        if h:
            current = h.group(1)
            continue
        if line.startswith("⊢") and current:
            refs = set(re.findall(r"M\d+", line))
            prereqs[current] = refs

    for mod, refs in prereqs.items():
        for ref in refs:
            if ref not in modules:
                findings.append(Finding("error", "graph", f"CURRICULUM.md/{mod}",
                                        f"prerequisite {ref} does not exist"))

    # Cycle detection
    colour: dict[str, int] = {}

    def visit(node: str, stack: list[str]) -> None:
        colour[node] = 1
        for nxt in prereqs.get(node, ()):
            if nxt not in modules:
                continue
            if colour.get(nxt) == 1:
                findings.append(Finding("error", "graph", "CURRICULUM.md",
                                        f"prerequisite cycle: {' -> '.join(stack + [node, nxt])}"))
            elif colour.get(nxt, 0) == 0:
                visit(nxt, stack + [node])
        colour[node] = 2

    for mod in modules:
        if colour.get(mod, 0) == 0:
            visit(mod, [])

    # Transitive closure for hard-ordering constraints
    def reaches(a: str, b: str, seen: set[str] | None = None) -> bool:
        seen = seen or set()
        if a in seen:
            return False
        seen.add(a)
        for nxt in prereqs.get(a, ()):
            if nxt == b or reaches(nxt, b, seen):
                return True
        return False

    for earlier, later in HARD_ORDER:
        if earlier in modules and later in modules and not reaches(later, earlier):
            findings.append(Finding("error", "graph", "CURRICULUM.md",
                                    f"hard ordering violated: {earlier} must precede {later} "
                                    f"(see Appendix A)"))

    # Citations resolve
    res = root / "RESOURCES.md"
    if res.exists():
        rtext = res.read_text(encoding="utf-8")
        defined = {rid.split("-")[1] for rid in RESOURCE_ID_RE.findall(rtext)}
        cited: set[str] = set()
        for path in md_files(root):
            if path.name == "RESOURCES.md":
                continue
            for num in CITE_RE.findall(path.read_text(encoding="utf-8")):
                cited.add(num)
                if num not in defined:
                    findings.append(Finding("error", "graph", path.name,
                                            f"citation [R-{num}] has no entry in RESOURCES.md"))
        orphans = sorted(defined - cited)
        if orphans:
            findings.append(Finding("info", "graph", "RESOURCES.md",
                                    f"{len(orphans)} resources never cited: "
                                    f"{', '.join('R-' + o for o in orphans)}"))

    # ASSESSMENT module table matches CURRICULUM
    ass = root / "ASSESSMENT.md"
    if ass.exists():
        listed = set(re.findall(r"^\|\s*(M\d+)\s*\|", ass.read_text(encoding="utf-8"), re.M))
        for mod in sorted(listed - set(modules)):
            findings.append(Finding("error", "graph", "ASSESSMENT.md",
                                    f"{mod} listed but not defined in CURRICULUM.md"))
        for mod in sorted(set(modules) - listed):
            findings.append(Finding("warn", "graph", "ASSESSMENT.md",
                                    f"{mod} has no row in the mastery-artifact table"))

    findings.append(Finding("info", "graph", "CURRICULUM.md",
                            f"{len(modules)} modules, {sum(len(v) for v in prereqs.values())} "
                            f"prerequisite edges parsed"))
    return findings


# ----------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("check", choices=["links", "staleness", "graph", "all"])
    ap.add_argument("--dir", default=str(Path(__file__).resolve().parent.parent))
    ap.add_argument("--ci", action="store_true", help="exit non-zero on any error")
    ap.add_argument("--timeout", type=int, default=15)
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()

    root = Path(args.dir).resolve()
    today = dt.date.today()
    findings: list[Finding] = []

    if args.check in ("graph", "all"):
        print("· graph", file=sys.stderr)
        findings += check_graph(root)
    if args.check in ("staleness", "all"):
        print("· staleness", file=sys.stderr)
        findings += check_staleness(root, today)
    if args.check in ("links", "all"):
        print("· links", file=sys.stderr)
        findings += check_links(root, args.timeout, args.workers)

    order = {"error": 0, "warn": 1, "info": 2}
    for f in sorted(findings, key=lambda f: (order[f.level], f.check, f.where)):
        print(f)

    errors = sum(1 for f in findings if f.level == "error")
    warns = sum(1 for f in findings if f.level == "warn")
    print(f"\n{errors} error(s), {warns} warning(s) — {root}")
    return 1 if (args.ci and errors) else 0


if __name__ == "__main__":
    sys.exit(main())
