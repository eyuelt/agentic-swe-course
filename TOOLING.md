# Course Tooling

**Version 1.0 · Specifications for tools that administer and maintain *Shipping With Agents***

A course about agentic engineering that is maintained by hand is making a point about itself. These six tools cover the recurring maintenance and instruction load. Each spec gives purpose, interface, data model, implementation sketch, and effort — enough for an agent to build it from this file alone.

Two are shipped as working reference implementations in `tools/`: **T2 (curriculum-lint)** and **T1 (feedwatch)**. The rest are specified, not built.

**Build order, by value per hour:** T2 → T1 → T4 → T3 → T5 → T6.

---

## T1 — `feedwatch`: expert feed aggregator

**The problem.** The dossier (`PRACTITIONER-DOSSIER.md`) names ~15 practitioners whose writing is the course's raw material. Checking them by hand is exactly the kind of recurring, low-judgment, high-value scanning that should not be done by a human, and in practice is not done at all.

**Purpose.** Watch every source in the dossier; surface what is new; classify it; write it into a curriculum inbox for triage.

### Interface
```
feedwatch fetch                 # poll all sources, update the store
feedwatch triage [--since 30d]  # classify new items, write inbox report
feedwatch report --format md    # markdown digest for the maintainer
feedwatch add <url> --person "Name" --kind blog|github|youtube|podcast
```

### Data model
`feeds.yaml` — one entry per source:
```yaml
- person: Armin Ronacher
  handle: mitsuhiko
  dossier_id: ronacher          # links to PRACTITIONER-DOSSIER.md
  sources:
    - kind: rss
      url: https://lucumr.pocoo.org/feed.atom
    - kind: index
      url: https://lucumr.pocoo.org/tags/ai/
  watch_for: ["agent", "coding", "MCP", "context", "loop"]
```
`store.sqlite` — seen items: `(id, person, url, title, published, fetched, classification, summary, triaged)`.

### Classification
Each new item is classified by a small model call into exactly one of:

| Class | Meaning | Action |
|---|---|---|
| `new-technique` | A practice not already in the curriculum | → Teardown candidate; propose a module edit |
| `position-change` | This person now contradicts what the dossier says they believe | **Highest priority.** The dossier is wrong until fixed |
| `tool-change` | A product, model, or version claim | → `STATE-OF-PLAY` refresh item only |
| `evidence` | A study, measurement, or dataset | → evidence base in `RESOURCES.md` |
| `restatement` | Says something the curriculum already says | Log and ignore |
| `noise` | Off-topic for this course | Discard |

The classifier prompt must include the relevant dossier section, so "position-change" is judged against what the course currently claims the person believes. This is the feature that makes the tool worth building: **the dossier's most dangerous failure mode is quietly misrepresenting someone who has changed their mind**, and it has happened to every practitioner in it at least once.

### Output
`inbox/YYYY-MM-DD.md`: grouped by class, highest priority first, each item with person, title, URL, date, a two-sentence summary, and the proposed curriculum action (`module: M7` / `state-of-play: §5` / `dossier: ronacher`).

### Implementation sketch
Python. `feedparser` for RSS/Atom; GitHub REST for repo releases and new repos; YouTube channel RSS (`.../feeds/videos.xml?channel_id=`); podcast RSS. For sources without a feed, fetch the index page and diff the link set against the store — crude and adequate. One model call per new item for summary + classification. Respect `robots.txt`, cache with ETag/Last-Modified, and rate-limit.

**Effort:** ~1 day for a working version; ~3 days with good classification and dedupe.
**Run as:** a scheduled weekly job that writes the inbox and notifies you only when `new-technique` or `position-change` appears.

---

## T2 — `curriculum-lint`: staleness and integrity linter

**The problem.** This curriculum will rot in three ways: links die, volatile claims age past their half-life, and edits break the module dependency graph. All three are mechanically detectable.

**Purpose.** Fail loudly when the curriculum is decaying, before a learner discovers it.

### Interface
```
curriculum-lint links      # verify every URL; report dead and redirected
curriculum-lint staleness  # flag claims older than their volatility tier
curriculum-lint graph      # validate prerequisites and cross-references
curriculum-lint all --ci   # non-zero exit on any error-level finding
```

### Checks

**Links.** Extract every URL from all markdown. `HEAD`, falling back to `GET`. Report: `dead` (4xx/5xx), `moved` (3xx with a new location — propose the update inline), `slow`, `unverified` (marked `?` in `RESOURCES.md`). Update the `✓` column in place with `--fix`.

**Staleness.** Parse volatility tags from `RESOURCES.md`. Thresholds: **F** → warn at 90 days, error at 180. **M** → warn at 365. **D** → never. Separately, error if `STATE-OF-PLAY-*.md`'s compile date is more than 180 days old, and warn at 90.

**Graph.** Parse `⊢` prerequisite lines from `CURRICULUM.md`. Verify: every referenced module exists; no cycles; the hard-ordering constraints in Appendix A hold (M12 before the unattended parts of M10/M11; M3 before M4 and M9; M0 first); every `[R-nn]` citation resolves to an entry in `RESOURCES.md`; every `R-nn` entry is cited at least once (orphan resources are usually a sign of a deleted module); every module ID in `ASSESSMENT.md` §4 exists in `CURRICULUM.md`.

**Effort:** ~4 hours. Shipped in `tools/curriculum_lint.py`.
**Run as:** a pre-commit hook and a monthly scheduled job.

---

## T3 — `lab-check`: lab verification harness

**The problem.** Self-paced learners cannot tell whether they actually hit a lab's success criterion. Several criteria are mechanically checkable.

**Purpose.** Turn checkable success criteria into commands the learner runs.

### Interface
```
lab-check L3.2 --repo ~/work/myrepo   # verify the <15s fast lane
lab-check L7.3 --repo ~/work/myrepo   # verify 10 consecutive identical test runs
lab-check status                      # progress across all checkable labs
```

### Checkable labs and their checks

| Lab | Check |
|---|---|
| L0.1 | `ase/log.md` exists, ≥20 rows, ≥4 rows flagged as control tasks, predictions non-empty |
| L3.2 | Named command exists and completes in <15s over 3 runs; is referenced in the repo's agent memory file |
| L5.2 | Memory file line count decreased; relocation map file exists |
| L7.1 | Audit file present with all 10 checks scored and evidence per score |
| L7.3 | Test suite run 10× produces identical pass/fail sets |
| L8.2 | A configured blocking hook exists and denies a scripted attempt |
| L12.3 | Sandbox container builds; egress to a non-allowlisted host fails; no host credentials mounted |
| L13.1 | Eval suite runs with one command and emits a score |

Everything else — anything requiring judgment — is explicitly out of scope and reported as `manual`. **Do not extend this tool into judging judgment.** That is what the rubrics and the external signals are for; an autograder that scores reflection teaches people to write for the autograder.

**Effort:** ~1 day for eight checks.

---

## T4 — `ase-log`: practice telemetry

**The problem.** M0 requires manual logging, which decays after about ten entries. Automatic capture of the mechanical fields makes the manual fields survivable.

**Purpose.** Capture wall-clock, interventions, verification events, and token cost automatically; prompt for the judgment fields at task close.

### Interface
```
ase start "add rate limiting to the ingest API"   # begins a task; asks for predictions
ase verify                                        # marks a verification event
ase intervene --kind steer|correct|rescue         # one keystroke, from a hotkey
ase done                                          # prompts for read ratio + note, writes the row
ase report --since 90d                            # trends, calibration curve, intervention mix
```

### Captured automatically
Start/end time; commits made during the window; agent session IDs; token and cost totals where the harness exposes them; test/build invocations (via a post-tool hook that calls `ase verify`); files touched.

### Asked at close
Read ratio (0–100%). One-sentence note. Whether the prediction was met.

### Reports
Calibration curve (predicted vs actual, over time). Intervention mix trend (steer:correct:rescue — a rising *rescue* share is the leading indicator that your briefs or your context have degraded). Read-ratio trend against blast radius. Verification events per task.

**Implementation sketch.** A small CLI writing JSONL, plus a harness hook (`PostToolUse` matching the test/build command) that appends verification events. Render to the markdown log M0 requires so the two are the same artifact.

**Effort:** ~1 day CLI + ~2 hours of hooks.
**Caution:** this tool is itself a M0 hazard. Do not spend a week building telemetry instead of taking a baseline. Build it *after* twenty hand-written rows have proved what is worth capturing.

---

## T5 — `eval-suite`: personal golden-task runner

**The problem.** M13's suite needs a runner: fresh checkout at a pinned commit, run the brief, score, repeat N times, aggregate with variance.

**Purpose.** Answer "did that change help?" with a number and an error bar.

### Interface
```
eval run --suite ./evals --model X --runs 5
eval compare baseline.json candidate.json     # with variance-aware verdict
eval add --from-session <id>                  # convert a real session into a golden task
```

### Task format
```yaml
id: rate-limit-middleware
repo: git@github.com:me/service.git
commit: a1b2c3d
brief: |
  Add token-bucket rate limiting to the ingest endpoint...
setup: [docker compose up -d]
check:
  kind: command              # or: rubric
  command: pytest tests/test_ratelimit.py
timeout: 900
known_failure: true          # models currently fail this; watch it
```

### Requirements that make it trustworthy
- Fresh clone at the pinned commit for **every** run — no state leakage
- N runs per task, reporting mean, spread, and pass rate — never a single run
- Held-constant manifest recorded in the result: harness version, memory file hash, tool list, effort setting
- `compare` refuses to declare a winner below the configured minimum effect size, and says so
- Rubric-scored tasks use a *different* model family as judge than the one under test, and sample 20% for human spot-check

**Effort:** ~2 days.
**This is the tool with the longest useful life** — it will still be answering your questions after every technique in this course has been superseded.

---

## T6 — `dossier-diff`: position-change detector

**The problem.** The dossier's worst failure is confidently attributing a superseded belief to a living practitioner. DHH's reversal, Cherny's plan-mode inversion, and Karpathy's refinement of "vibe coding" all happened inside eighteen months.

**Purpose.** Continuously test the dossier's claims against what each person has most recently said.

### Interface
```
dossier-diff check --person cherny
dossier-diff check --all --since 90d
```

### Method
For each dossier claim (extracted as a list of attributed statements with source URLs), gather that person's writing since the claim's source date via T1's store, and ask a model one narrow question: *"Does any of this contradict, qualify, or supersede the claim: '<claim>'?"* Report `contradicts` / `qualifies` / `supports` / `silent`, with the evidence quoted.

Findings go into the inbox at highest priority. A `contradicts` finding makes the dossier **wrong**, not merely stale, and should block a release of the curriculum.

**Effort:** ~half a day given T1.
**Failure mode to watch:** models over-detect contradiction from tone. Require a quoted passage with every `contradicts` finding, and spot-check them.

---

## Things deliberately not built

- **An LLM grader for judgment traces.** Would immediately be optimized against, destroying the thing being measured. External human signals stay human (`ASSESSMENT.md` §8).
- **A progress gamification layer.** Streaks reward continuity, not mastery, and this course is explicitly not time-based.
- **An auto-updating curriculum.** A model that rewrites `CURRICULUM.md` from feeds will drift toward whatever was loudest this month. Feeds generate *proposals*; a maintainer decides. `MAINTENANCE.md` §3 says why this line is drawn here.
- **A chatbot tutor over the curriculum.** The learner already has a frontier model. Adding a RAG layer over these files subtracts context.

---

## Shipped reference implementations

| File | Tool | Status |
|---|---|---|
| `tools/curriculum_lint.py` | T2 | Working: links, staleness, graph, citations |
| `tools/feedwatch.py` | T1 | Working: fetch + diff + report. Classification is stubbed with a documented prompt |
| `tools/feeds.yaml` | T1 | Source list for every dossier practitioner |

Both are dependency-light (standard library plus optional `feedparser`) and are meant to be read and modified, not installed.
