# Shipping With Agents — repository guide

A self-paced curriculum in agentic software engineering. This file tells you how to work in this repo.
**Read `MAINTENANCE.md` before changing anything** — it holds the design invariants and the authority boundary.

## What lives where

| Path | Role | Change freely? |
|---|---|---|
| `SYLLABUS.md` | Goals, thesis, the three building blocks, phases, assessment overview | No — needs a human |
| `CURRICULUM.md` | 17 modules, 70+ labs, self-checks, dependency graph | No — needs a human |
| `ASSESSMENT.md` | Rubrics, 3 gates, 3 capstones | No — needs a human |
| `PRACTITIONER-DOSSIER.md` | 10 practitioners, teardown protocol, disagreement map | No — needs a human |
| `RESOURCES.md` | Annotated index, dated, volatility-tagged | **Yes** — URLs, marks, new entries |
| `STATE-OF-PLAY-2026-09.md` | All volatile facts, quarantined | **Yes** — this is what it is for |
| `TOOLING.md` | Specs for six tools; two are built | Yes |
| `MAINTENANCE.md` | Invariants, refresh procedure, change log | Append to §7 only |
| `tools/` | `curriculum_lint.py`, `feedwatch.py`, `feeds.yaml` | Yes |
| `curriculum.html` | Source of the public site (GitHub Pages deploys it on push) | Only alongside a doc change |

## Hard rules

1. **Products are examples only; every claim about one lives in `STATE-OF-PLAY-*.md`.** The curriculum body
   teaches *capabilities* ("a harness with a plan mode"). It may name a product as an example gloss — "an agent
   harness (e.g. Claude Code or OpenCode)" — but only a name listed in the registry in `STATE-OF-PLAY` §9.1, and
   never a model version, price, benchmark score, feature claim or comparison. No lab may depend on a product. The
   dossier and resource index are exempt. The linter's `products` check enforces this; it is what keeps the course
   refreshable in an afternoon.
2. **Run the linter before you finish.** `python3 tools/curriculum_lint.py all --ci` — zero errors, always.
3. **Every factual claim carries a date and a source.** If you cannot verify something, mark it `?` in the
   verification column rather than asserting it. Never launder a plausible guess into an authoritative statement.
4. **Do not reorder modules.** M13 (security) gates the unattended parts of M11 and M12. M4 precedes M5 and M10.
   The linter enforces these; if it complains, the edit is wrong, not the check.
5. **Do not add graded tests, quizzes or auto-graders.** Self-checks are ungraded retrieval practice and stay that way.
6. **Modules and phases are 1-indexed.** M1–M17, Phase 1–5. Labs are `L<module>.<n>`.

## What you may do on your own initiative

Refresh `STATE-OF-PLAY`, fix and verify URLs, sharpen a lab, add a resource with its date and volatility tag, fix
anything the linter flags, and append to the change log.

## What needs the repo owner to decide

Module content or ordering, rubrics and gates, the dossier's characterization of any practitioner, the disagreement
map, and anything in `MAINTENANCE.md` §1. Draft the change, show it, and wait.

The reason is structural: a model refreshing a curriculum from recent feeds drifts toward whatever was loudest this
quarter, and in this field the loudest claims are systematically the least verified. The pipeline is **feeds
generate proposals → the owner decides → the linter verifies.**

## The common task

The quarterly refresh has its own runbook: `/refresh-curriculum`. Use it rather than improvising.

## Conventions

- Markdown, no line-length limit, tables for anything comparative.
- Resource IDs are `R-nn`, cited inline as `[R-nn]`. Every citation must resolve; the linter checks.
- Prose is direct and unhedged. Attribute techniques to named practitioners with a primary source, label folklore
  as folklore, and mark the course's own positions as its own.
- Append to the `MAINTENANCE.md` §7 change log for anything beyond a typo: date · who · what and why · which
  invariants were touched.
