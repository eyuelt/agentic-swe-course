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

> **Generation is cheap. Verification is the bottleneck. Every durable technique in agentic engineering is a way of closing the gap between "code produced" and "code known-good" — faster than the agent can widen it.**

We call this gap the **verification gap.** It is the organizing idea of the whole curriculum. When you evaluate a new tool, a new technique, or an expert's advice, the question is always the same: *what does this do to my verification gap?*

## 2. The three layers, and why the course is shaped this way

The field has moved through three layers in roughly three years. Practitioners who are stuck are usually stuck one layer down from where their problem lives.

| Layer | Era | The unit of work | The skill | Failure mode when stuck here |
|---|---|---|---|---|
| **Prompting** | 2023–24 | The message | Phrasing, examples | Endless re-prompting; blaming the model |
| **Context engineering** | 2025 | The context window | Curation, compaction, isolation | Context rot; agent "forgets"; huge CLAUDE.md that nobody reads |
| **Loop engineering** | 2026 | The loop | System design, verification, autonomy budgeting | Human is the bottleneck; agents idle waiting for you |

Each layer *subsumes* the one below — you still need good briefs at layer 3 — so the course proceeds in that order, then adds a fourth thing that is not a layer but a permanent obligation: **governance** (security, comprehension debt, org effects).

A note on the 2026 term **"loop engineering."** Addy Osmani's formulation is the clearest: *"Loop engineering is replacing yourself as the person who prompts the agent. You design the system that does it instead."* Peter Steinberger puts it more bluntly: *"You shouldn't be prompting coding agents anymore. You should be designing loops that prompt your agents."* Treat the term as useful and probably transient — the underlying skill (designing self-verifying systems) is durable; the label may not be. `MAINTENANCE.md` explains how to swap labels without rewriting the course.

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
Module 0 exists because of one of the most important findings in the field: METR's randomized trial found experienced open-source developers were **19% slower** with early-2025 AI tools while believing they had been **20% faster**. The gap between felt and actual productivity is the default condition, not an anomaly. METR's own 2026 follow-up shows the picture shifting (a smaller, noisier slowdown, and the study design breaking down because developers now refuse to work without AI) — which is itself the lesson: **you cannot outsource this measurement to the literature. You have to take your own baseline.**

### 4.4 Study experts as sources of hypotheses, not authority
Experts disagree sharply and publicly, and the disagreements are where the learning is. Steinberger says he barely reads code any more; DHH reviews every diff before merge; Kent Beck makes tests the binding constraint; Dex Horthy says review the *plan*, because a bad line of research becomes thousands of bad lines of code. They are all shipping. They are not all right about your situation.

The course uses a repeatable **Practitioner Teardown** protocol (`PRACTITIONER-DOSSIER.md`) for converting any expert's claim into an experiment you run on your own repo. You will do at least six.

### 4.5 Build one agent, early
Module 1 has you build a working coding agent from scratch. This is not a detour into agent-system design for its own sake — it is the fastest known cure for magical thinking. Once you have written the loop, "the agent forgot" and "the agent hallucinated a file" stop being mysteries and become debuggable context problems.

### 4.6 Tools are quarantined
Specific tools, models, prices and version numbers live in exactly one file: `STATE-OF-PLAY-2026-09.md`. The curriculum body refers to *capabilities* ("an agent harness with a plan mode", "a context-isolated subagent") rather than product names wherever possible. This is deliberate: it is what lets a successor maintainer refresh the course in an afternoon instead of a month.

## 5. Structure

Five stages, seventeen modules. Prerequisites form a DAG, not a line — Stage 2 modules can be taken in any order once Stage 1 is complete.

```
STAGE 0 — CALIBRATION
  M0  Baseline & Instrumentation

STAGE 1 — OPERATOR  (drive one agent well)
  M1  The Agentic Loop: build an agent
  M2  Briefing, Steering, Abandoning
  M3  Verification-First Development
  M4  Reading the Machine: review discipline
      ▸ GATE 1 + Capstone A

STAGE 2 — ENGINEER  (shape the environment)
  M5  Context Engineering
  M6  Research → Plan → Implement
  M7  Designing Codebases for Agents
  M8  The Extension Surface
      ▸ GATE 2 + Capstone B

STAGE 3 — ORCHESTRATOR  (scale beyond one agent)
  M9   Parallelism
  M10  Loop Engineering
  M11  Async, Remote & Cloud Agents
  M12  Security & Safety for Agentic Development
      ▸ GATE 3

STAGE 4 — ARCHITECT  (build and lead)
  M13  Evals for Your Own Work
  M14  Building Harnesses & Agent Systems
  M15  Teams, Orgs & Comprehension Debt
  M16  Capstone C, Doctrine & Continuous Practice
```

Full module specifications, labs and reading are in `CURRICULUM.md`.

## 6. Assessment

| Instrument | Weight | What it tests |
|---|---|---|
| Module mastery artifacts (17) | 40% | Technique acquisition |
| Gate assessments (3) | 15% | Integration across a stage |
| Capstone A — Ship it | 10% | O1, O3 |
| Capstone B — Land a change in a large unfamiliar codebase | 15% | O1, O4, O5 |
| Capstone C — Operate an autonomous loop for a week | 15% | O6, O7, O8 |
| Doctrine document | 5% | O9 |

Rubrics use four levels — **Novice / Working / Proficient / Expert** — with explicit descriptors per module. "Proficient" is the advancement bar. "Expert" descriptors exist so you can tell what you are still missing; nobody is expected to hit Expert on all seventeen.

**Self-assessment is not sufficient for the capstones.** Capstone B requires an external signal (a merged PR, a maintainer's review, or a colleague's independent code review). Capstone C requires an incident log — including the failures. A capstone with no failures logged is presumed under-reported and does not pass.

**Anti-cheat note, stated plainly:** you can have an agent produce every artifact in this course. If you do, you will have learned nothing and the artifacts will show it — the rubrics weight *judgment traces* (why you rejected an approach, what your measurement showed, what surprised you) far above output volume. Use agents to do the work. Do not use them to fake the reflection.

## 7. Prerequisites

Required: professional software engineering experience (3+ years or equivalent); comfort in a terminal; git, including worktrees or willingness to learn them; one language you know well enough to review code in fluently; a real codebase you own or maintain.

Required access: at least one agentic coding harness with a paid tier (parallelism labs need enough quota to run 3+ concurrent agents); a machine or container you are willing to let an agent modify; a GitHub account.

Not required: ML background, prior agent use, prior prompt-engineering study.

Budget note: Stage 3 is the expensive stage. Expect meaningful token spend during Capstone C. Practitioners operating at the level this course targets commonly report $200–$1,000/month in subscriptions; the labs are designed to be completable at the low end of that.

## 8. Course policies

**Safety.** No lab instructs you to run an agent with unrestricted permissions on a machine with production credentials. M12 is a prerequisite for the unattended portions of M10 and M11, and this ordering is not negotiable — the autonomy labs come *after* the security module, not before.

**Honesty about volatility.** Any factual claim in this course about a specific product, model, price, or benchmark score is stamped with a date and lives in `STATE-OF-PLAY-2026-09.md`. If you are reading this more than ~6 months after the issue date and that file has not been refreshed, treat every product claim as unreliable and every principle as probably still fine.

**Currency of sources.** All URLs in `RESOURCES.md` were verified live on 2026-09-17. Link rot is expected; `TOOLING.md` specs a linter for it.

**Attribution.** Where a technique is attributable to a named practitioner, it is attributed, with a primary source. Where a technique is folklore, it is labelled folklore. Where the course asserts something without a source, that is the course's own position and you should weigh it accordingly.

## 9. How to start

1. Read this syllabus and `MAINTENANCE.md` §1 (design invariants) — 30 minutes.
2. Do **M0** before touching anything else. It is boring and it is the module people skip and later regret, because without a baseline you will spend the rest of the course unable to tell whether anything you did helped.
3. Work Stage 1 in order. After that, follow the DAG and your interests.
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
