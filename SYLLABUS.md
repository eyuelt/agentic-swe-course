# Shipping With Agents — Syllabus

**Course:** Shipping With Agents — a curriculum in agentic software engineering
**Course code:** ASE
**Version:** 1.0
**Issued:** 2026-09-17
**Format:** Self-paced, mastery-based, project-driven
**Audience:** Experienced software engineers with light prior agent use
**Maintainer contract:** see `MAINTENANCE.md` (read it before editing anything in this repo)

---

## 1. What this course is

Agentic Software Engineering (ASE) is the discipline of **producing, verifying, and owning software that you did not type.** It is not prompt engineering with a new hat on. It is a shift in where an engineer's judgment is applied: away from the keystroke, toward the specification, the verification loop, and the system that runs the agents.

This course teaches the *practice*, not the vocabulary. Every module ends in an artifact you built, a measurement you took, or a loop you ran — never in a quiz about what MCP stands for.

The course takes a strong position, stated here so a reader can disagree with it deliberately:

> **Agents made code cheap to write. They did not make it cheap to ship. Verification is the bottleneck. Every durable technique in this course is a way of closing the gap between "code produced" and "code known-good" — faster than the agent can widen it.**

We call this gap the **verification gap.** It is the organizing idea of the whole curriculum. When you evaluate a new tool, a new technique, or an expert's advice, the question is always the same: *what does this do to my verification gap?*

## 2. The building blocks of an agentic workflow

Every agentic workflow is built from three nested blocks: **the message, the context window, and the loop.** Each
block contains the one before it — a context window holds many messages; a loop runs many context windows. Moving
outward means taking the next block as the thing you design; the blocks inside it do not go away.

This course builds your command of all three, working from the inside out. Prompting comes first, to get the message
right; then context engineering, to get right everything the model can see; then loop engineering, to get right the
system that runs without you. An outer block never replaces an inner one: you still need a good brief after you have
moved on to designing loops.

| Building block | Discipline | Era | The skill | Stuck here looks like | Taught in |
|---|---|---|---|---|---|
| **The message** | Prompting | 2023–24 | Phrasing, examples, iteration by hand | Endless re-prompting; blaming the model when it doesn't land | Phase 2 |
| **The context window** | Context engineering | 2025 | Curation, compaction, isolation — budgeting what the model can see | Context rot; a huge memory file nobody reads; the agent "forgetting" | Phase 3 |
| **The loop** | Loop engineering | 2026 | System design, verification, deciding how much autonomy a task can carry | You are the bottleneck; agents sit idle waiting for your attention | Phase 4 |

Most people who feel stuck are working one block inside where their problem actually lives.

**The blocks are not the parts of the course** — the five phases in §5 are that — though the phases follow the same
order. Phase 1 comes before all three: it is measurement, so you can tell whether anything you do on any of them is
actually working. Phase 5 steps outside the outermost block: building the harnesses, and carrying a team.

Because each block contains the one before it, the course proceeds from the inside out, then adds the thing that is not a block
but a permanent obligation: **governance** — security, comprehension debt, and what happens when a team does this
at scale.

A note on the 2026 term **"loop engineering."** Addy Osmani's formulation is the clearest: *"Loop engineering is
replacing yourself as the person who prompts the agent. You design the system that does it instead."* Peter
Steinberger puts it more bluntly: *"You shouldn't be prompting coding agents anymore. You should be designing loops
that prompt your agents."* Treat the term as useful and probably transient — the underlying skill (designing
self-verifying systems) is durable; the label may not be. `MAINTENANCE.md` explains how to swap labels without
rewriting the course.

## 3. Learning outcomes

On completion, a graduate can:

**O1 — Operate.** Drive a coding agent through a non-trivial change in an unfamiliar codebase, from brief to merged, with a verification loop the agent can run itself.

**O2 — Explain.** Describe precisely what an agent is — the loop, the tools, the context window, the harness — and implement a working one in under 400 lines. Debug an agent's behaviour by reasoning about its context rather than guessing at prompts.

**O3 — Engineer context.** Budget and shape a context window deliberately: decide what belongs in always-on memory, on-demand skills, isolated subagents, or nowhere. Diagnose context rot from symptoms.

**O4 — Shape the codebase.** Make a repository measurably more agent-legible (greppability, local reasoning, deterministic fast tests, hermetic builds, explicit types) and justify each change in terms of the verification gap.

**O5 — Orchestrate.** Run multiple agents in parallel without becoming the bottleneck or the merge conflict. Know when parallelism is negative-value.

**O6 — Automate the loop.** Design, run, and safely terminate an autonomous loop on real work, with guardrails, a state file, and a defined blast radius.

**O7 — Verify.** Build a personal eval suite that tells you whether a model or workflow change helped — independent of public benchmarks.

**O8 — Govern.** Identify and mitigate the security failure modes specific to agentic development (indirect prompt injection, the lethal trifecta, agent-mediated supply-chain compromise) and manage comprehension debt on a team.

**O9 — Judge.** Read a new expert claim, locate the verification mechanism it depends on, decide whether it transfers to your context, and run a cheap experiment to find out. This is the outcome that outlives the curriculum.

## 4. Approach

### 4.1 Mastery-based, not time-based
There are no weeks. Each module has an **evidence-of-mastery artifact** and a **rubric** (`ASSESSMENT.md`). You advance when the artifact exists and clears the "Proficient" bar, not when a calendar says so. Typical total effort is 90–140 hours; a fast experienced engineer working intensively has completed comparable ground in 5–6 weeks, and treating it as a 4–6 month background practice is equally valid.

### 4.2 Everything runs against your real work
Toy repositories teach toy lessons. The single biggest predictor of whether this transfers is whether you do the labs on code you actually care about and will still be maintaining in six months. Where a lab needs an unfamiliar large codebase, we use real open-source projects, not fixtures.

### 4.3 Measure before you believe
Module 1 exists because of one of the most important findings in the field: METR's randomized trial found experienced open-source developers were **19% slower** with early-2025 AI tools while believing they had been **20% faster**. The gap between felt and actual productivity is the default condition, not an anomaly. METR's own 2026 follow-up shows the picture shifting (a smaller, noisier slowdown, and the study design breaking down because developers now refuse to work without AI) — which is itself the lesson: **you cannot outsource this measurement to the literature. You have to take your own baseline.**

### 4.4 Study experts as sources of hypotheses, not authority
Experts disagree sharply and publicly, and the disagreements are where the learning is. Steinberger says he barely reads code any more; DHH reviews every diff before merge; Kent Beck makes tests the binding constraint; Dex Horthy says review the *plan*, because a bad line of research becomes thousands of bad lines of code. They are all shipping. They are not all right about your situation.

The course uses a repeatable **Practitioner Teardown** protocol (`PRACTITIONER-DOSSIER.md`) for converting any expert's claim into an experiment you run on your own repo. You will do at least six.

### 4.5 Build one agent, early
Module 2 has you build a working coding agent from scratch. This is not a detour into agent-system design for its own sake — it is the fastest known cure for magical thinking. Once you have written the loop, "the agent forgot" and "the agent hallucinated a file" stop being mysteries and become debuggable context problems.

### 4.6 Products are examples, never foundations
The course teaches *capabilities* ("an agent harness with a plan mode", "a context-isolated subagent"), and names products only as examples so you know what is meant — "an agent harness (e.g. Claude Code or OpenCode)". Nothing in a module or lab depends on a particular product. Every *claim* about a product — what it can do, which version, what it costs, how it scores — lives in exactly one file, `STATE-OF-PLAY-2026-09.md`, which also lists every product the course is allowed to name. This is deliberate: it is what lets a successor maintainer refresh the course in an afternoon instead of a month.

## 5. Structure

Five phases, seventeen modules. Prerequisites form a DAG, not a line — Phase 3 modules can be taken in any order once Phase 2 is complete.

```
PHASE 1 — CALIBRATION
  M1  Baseline & Instrumentation

PHASE 2 — OPERATOR  (drive one agent well)
  M2  The Agentic Loop: build an agent
  M3  Briefing, Steering, Abandoning
  M4  Verification-First Development
  M5  Reading the Machine: review discipline
      ▸ GATE 1 + Capstone A

PHASE 3 — ENGINEER  (shape the environment)
  M6  Context Engineering
  M7  Research → Plan → Implement
  M8  Designing Codebases for Agents
  M9  The Extension Surface
      ▸ GATE 2 + Capstone B

PHASE 4 — ORCHESTRATOR  (scale beyond one agent)
  M10  Parallelism
  M11  Loop Engineering
  M12  Async, Remote & Cloud Agents
  M13  Security & Safety for Agentic Development
      ▸ GATE 3

PHASE 5 — ARCHITECT  (build and lead)
  M14  Evals for Your Own Work
  M15  Building Harnesses & Agent Systems
  M16  Teams, Orgs & Comprehension Debt
  M17  Capstone C, Doctrine & Continuous Practice
```

Full module specifications, labs and reading are in `CURRICULUM.md`.

## 6. Assessment

| Instrument | What it tests |
| --- | --- |
| Module mastery artifacts (17) | Technique acquisition |
| Gate assessments (3) | Integration across a phase |
| Capstone A — Ship it | O1, O3 |
| Capstone B — Land a change in a large unfamiliar codebase | O1, O4, O5 |
| Capstone C — Operate an autonomous loop for a week | O6, O7, O8 |
| Doctrine document | O9 |

Rubrics use four levels — **Novice / Working / Proficient / Expert** — with explicit descriptors per module. "Proficient" is the advancement bar. "Expert" descriptors exist so you can tell what you are still missing; nobody is expected to hit Expert on all seventeen.

**Self-assessment is not sufficient for the capstones.** Capstone B requires an external signal (a merged PR, a maintainer's review, or a colleague's independent code review). Capstone C requires an incident log — including the failures. A capstone with no failures logged is presumed under-reported and does not pass.

**On using agents to do the coursework:** obviously yes — it would be strange not to, in this of all courses. Use them for the mechanical parts: building the labs, running the sweeps, drafting the write-ups. The one part worth doing yourself is the judgment trace — why you rejected an approach, what your measurement showed, what surprised you — because writing that down *is* the learning, and it is the only part of the artifact that is about your thinking rather than the artifact's.

## 7. Prerequisites

Required: professional software engineering experience (3+ years or equivalent); comfort in a terminal; git, including worktrees or willingness to learn them; one language you know well enough to review code in fluently; a real codebase you own or maintain.

Required access: at least one agentic coding harness (e.g. Claude Code, Codex CLI or Cursor) with a paid tier (parallelism labs need enough quota to run 3+ concurrent agents); a machine or container you are willing to let an agent modify; a GitHub account.

Not required: ML background, prior agent use, prior prompt-engineering study.

Budget note: Phase 4 is the expensive phase. Expect meaningful token spend during Capstone C. Practitioners operating at the level this course targets commonly report $200–$1,000/month in subscriptions; the labs are designed to be completable at the low end of that.

## 8. Course policies

**Safety.** No lab instructs you to run an agent with unrestricted permissions on a machine with production credentials. M13 is a prerequisite for the unattended portions of M11 and M12, and this ordering is not negotiable — the autonomy labs come *after* the security module, not before.

**Honesty about volatility.** Any factual claim in this course about a specific product, model, price, or benchmark score is stamped with a date and lives in `STATE-OF-PLAY-2026-09.md`. If you are reading this more than ~6 months after the issue date and that file has not been refreshed, treat every product claim as unreliable and every principle as probably still fine.

**Currency of sources.** All URLs in `RESOURCES.md` were verified live on 2026-09-17. Link rot is expected; `TOOLING.md` specs a linter for it.

**Attribution.** Where a technique is attributable to a named practitioner, it is attributed, with a primary source. Where a technique is folklore, it is labelled folklore. Where the course asserts something without a source, that is the course's own position and you should weigh it accordingly.

## 9. How to start

1. Read this syllabus and `MAINTENANCE.md` §1 (design invariants) — 30 minutes.
2. Do **M1** before touching anything else. It is boring and it is the module people skip and later regret, because without a baseline you will spend the rest of the course unable to tell whether anything you did helped.
3. Work Phase 2 in order. After that, follow the DAG and your interests.
4. Keep a single running `doctrine.md` from day one. It becomes your final deliverable.

---

### Companion documents

| File | Purpose |
|---|---|
| `CURRICULUM.md` | Module specifications: outcomes, content, labs, mastery evidence |
| `ASSESSMENT.md` | Rubrics, gates, capstone briefs |
| `PRACTITIONER-DOSSIER.md` | Expert profiles, the disagreement map, the Teardown protocol |
| `RESOURCES.md` | Annotated, dated, volatility-tagged resource index |
| `TOOLING.md` | Specifications for course-administration tools you can build |
| `STATE-OF-PLAY-2026-09.md` | Quarantined volatile facts: tools, models, benchmarks, evidence |
| `MAINTENANCE.md` | Instructions for the next maintainer, human or model |
