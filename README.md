# Shipping With Agents

**A practitioner's curriculum in agentic software engineering**

**v1.0 · 2026-09-17 · Self-paced, mastery-based, project-driven**

**Read it online:** <https://eyuelt.github.io/agentic-swe-course/> — the interactive single-page version, deployed from `curriculum.html` on every push to `main`.

A complete curriculum for an experienced software engineer learning to produce, verify, and own software they did not type — built around how expert practitioners actually work, and designed so that another model can maintain it as the field moves.

## Start here

1. **`SYLLABUS.md`** — what the course is, the thesis, outcomes, structure, policies. Read first.
2. **`CURRICULUM.md`** — 17 modules across 5 phases. Outcomes, teaching content, 70+ labs, mastery artifacts.
3. **Do M1 before anything else.** It is the module people skip and later regret.

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

Generation is cheap; verification is the bottleneck. Every durable technique in agentic engineering is a way of closing the gap between *code produced* and *code known-good* faster than the agent widens it. The discipline operates at three levels, each defined by the unit of work you manipulate — the message, the context window, the loop — and each resting on the one below. The course teaches all three, plus the permanent obligation that is not a layer: security, comprehension debt, and what happens when a team does this at scale.

## What makes this different from a list of tips

- **It is organized around one idea**, not around tools, so it survives the tools changing.
- **It teaches the disagreements.** Steinberger barely reads code; DHH reviews every diff; Horthy reviews the plan instead of the code; Beck makes tests the binding constraint. They are all shipping. The course teaches you to work out which is right *for you*, with measurements.
- **It starts with measurement.** M1 exists because METR found experienced developers were 19% slower with AI while feeling 20% faster — and because the follow-up research is now structurally unable to answer the question for you.
- **You build an agent in Module 1.** Not as theory. As the fastest available cure for magical thinking about everything downstream.
- **Every module ends in retrieval practice.** 89 ungraded self-checks across the 17 modules — answer from memory, then reveal. Nothing is recorded anywhere; the point is the effort of recalling.
- **It is maintainable.** Volatile facts are quarantined in one file, the module graph is machine-checkable, and `MAINTENANCE.md` tells a successor exactly what may and may not be changed.

## Verify this course before trusting it

```bash
python3 tools/curriculum_lint.py all          # links, staleness, dependency graph, citations
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
