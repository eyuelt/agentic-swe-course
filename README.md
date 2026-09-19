# Shipping With Agents

**A practitioner's curriculum in agentic software engineering**

**v1.0 · 2026-09-17 · Self-paced, mastery-based, project-driven**

**Read it online:** <https://eyuel.com/agentic-swe-course/> — the interactive single-page version, deployed from `curriculum.html` on every push to `main`.

A complete curriculum for an experienced software engineer learning to produce, verify, and own software they did not type — built around how expert practitioners actually work, and designed so that another model can maintain it as the field moves.

## Start here

1. **`SYLLABUS.md`** — what the course is, the thesis, outcomes, structure, policies. Read first.
2. **`CURRICULUM.md`** — 17 modules across 5 phases. Outcomes, teaching content, 70+ labs, mastery artifacts.
3. **Do M1 before anything else.** It takes an afternoon and sets up the log every later lab writes into.

## The files

| File | What it is | Read when |
|---|---|---|
| `SYLLABUS.md` | Goals, thesis, approach, structure, assessment overview, policies | First |
| `CURRICULUM.md` | The course itself: 17 modules, labs, mastery evidence, dependency graph | Throughout |
| `ASSESSMENT.md` | Rubrics, 3 gate assessments, 3 capstone briefs, integrity rules | Before each gate |
| `PRACTITIONER-DOSSIER.md` | 10 profiled practitioners + the Teardown protocol + the disagreement map | M3 onward, monthly after |
| `RESOURCES.md` | Annotated, dated, volatility-tagged index of every source | As directed by modules |
| `TOOLING.md` | Six tool specs for administering and maintaining the course | When maintenance starts hurting |
| `STATE-OF-PLAY-2026-09.md` | Every volatile fact — tools, models, benchmarks, evidence — quarantined in one place | Quarterly, or when a tool claim matters |
| `MAINTENANCE.md` | Design invariants and the refresh protocol, for the next maintainer | **Before editing anything** |
| `tools/` | Two working tools: `curriculum_lint.py`, `feedwatch.py` + `feeds.yaml` | Setup, then on a schedule |
| `CLAUDE.md` | Repo guide for a coding agent: what it may change alone, what needs you | Automatically, by any agent working here |
| `.claude/skills/refresh-curriculum/` | The quarterly refresh runbook, invocable as `/refresh-curriculum` | Quarterly |

## The thesis in one paragraph

Agents made code cheap to write. They did not make it cheap to ship. Verification is the bottleneck. Every durable technique in this course is a way of closing the gap between *code produced* and *code known-good* faster than the agent can widen it. Every agentic workflow is built from three nested blocks — the message, the context window, the loop — each containing the one before, and you master them from the inside out. The course teaches all three, plus the permanent obligation that is not a block: security, comprehension debt, and what happens when a team does this at scale.

## What makes this different from a list of tips

- **It is organized around one idea**, not around tools, so it survives the tools changing.
- **It teaches the disagreements.** Steinberger barely reads code; DHH reviews every diff; Horthy reviews the plan instead of the code; Beck makes tests the binding constraint. They are all shipping. The course teaches you to work out which is right *for you*, with measurements.
- **It starts with instruments.** M1 exists because METR found experienced developers were 19% slower with AI while feeling 20% faster. The course does not ask you to re-run that experiment on yourself; it takes the lesson that felt fluency is unreliable and has you steer your agentic practice by a light log instead.
- **You build an agent in Module 2.** Not as theory. As the fastest available cure for magical thinking about everything downstream.
- **Every module ends in retrieval practice.** 89 ungraded self-checks across the 17 modules — answer from memory, then reveal. Nothing is recorded anywhere; the point is the effort of recalling.
- **It is maintainable.** Volatile facts are quarantined in one file, products appear in the course only as registered examples, the module graph is machine-checkable, and `MAINTENANCE.md` tells a successor exactly what may and may not be changed.

## Verify this course before trusting it

```bash
python3 tools/curriculum_lint.py all          # links, staleness, dependency graph, citations, product names
python3 tools/feedwatch.py fetch              # poll every practitioner source
python3 tools/feedwatch.py report --since 90d # draft a triage inbox
```

`curriculum_lint` was run against this repository during authoring and found — and forced the fix of — sixteen real defects: two prerequisite cycles, a violated ordering constraint, and thirteen dangling citations. That is the course's own method applied to itself, and it is the recommended first thing to do with it.

*(Note: if you run the linter behind a restrictive egress proxy, URL checks report `proxy-blocked`. That is your network, not link rot.)*

## For an assessing or continuing model

Read `MAINTENANCE.md` first — §1 (invariants), §3 (what you may change on your own initiative), §4 (the refresh procedure), §8 (known gaps, stated honestly).

The short version of §3: you may freely refresh `STATE-OF-PLAY-*.md`, resources, and labs. Module content, rubrics, and the dossier need a human decision, because a model refreshing a curriculum from recent feeds drifts toward whatever was loudest this quarter, and in this field the loudest claims are systematically the least verified. Feeds generate proposals; a maintainer decides; the linter verifies.

## Scope note

This is a course in *doing software engineering with agents*, with enough agent-system design (M2, M15) to make you a better practitioner rather than to make you an agent-framework author. Sources were verified live on 2026-09-17; anything about a specific product is stamped and quarantined.
