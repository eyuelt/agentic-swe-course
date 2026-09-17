# Shipping With Agents — Curriculum

**Version 1.0 · Issued 2026-09-17 · Companion to `SYLLABUS.md`**

Each module below specifies: why it exists, outcomes, core content, labs, and the artifact that evidences mastery. Rubrics are in `ASSESSMENT.md`. Reading is keyed to `RESOURCES.md` by `[R-nn]`.

**Notation.** `⏱` effort estimate. `⊢` prerequisites. `★` the one thing to take away if you take nothing else.

---
---

# STAGE 0 — CALIBRATION

---

## M0 — Baseline & Instrumentation

⊢ none · ⏱ 4–6 h, then 2 weeks of passive logging

### Why this module exists

In 2025 METR ran a randomized controlled trial on experienced open-source developers working in repositories they knew well. Developers using early-2025 AI tooling were **19% slower**. Those same developers estimated afterward that they had been **20% faster**. The 39-point swing between perception and measurement is the single most important empirical fact in this field, and it is not a fact about 2025 tools — it is a fact about human self-assessment under conditions of high subjective fluency. Watching an agent produce 400 lines in ninety seconds *feels* like enormous progress regardless of whether the change lands.

METR's 2026 follow-up sharpens rather than dissolves the point. The slowdown narrowed (roughly −18% for returning participants, roughly −4% for newly recruited ones, both with confidence intervals crossing zero) and METR announced it was **redesigning the experiment** because it could no longer recruit: developers now refuse to work half their tasks without AI, and they decline to submit tasks they believe AI will handle well. The literature is becoming structurally unable to answer the question for you.

So you answer it for yourself. This module is the control group for the rest of the course.

★ **You cannot improve what you have not baselined, and your felt sense of speed is actively misleading.**

### Outcomes

- A personal measurement practice that survives the course
- Calibrated intuition: you can predict a task's duration and later check yourself
- A written statement of what you currently believe about agentic coding, dated, so you can be wrong on the record

### Core content

**What to measure.** Resist dashboards. Four numbers, logged by hand, beat twenty collected automatically:

1. **Wall-clock to merged** — brief written → change merged. Not "time the agent ran."
2. **Rework passes** — how many times you sent it back. A pass is any correction after you thought it was done.
3. **Read ratio** — of the diff that shipped, what fraction did you actually read? Be honest. This is the comprehension-debt meter.
4. **Verification events** — how many times did something *other than you or the model* confirm correctness (test, type check, lint, browser, deploy preview, another human)? Zero is a valid and alarming answer.

**The prediction log.** Before each task: write your estimate of wall-clock and rework passes. Afterward: write the actuals. Calibration is trainable and the training is this, done fifty times.

**Why not DORA metrics yet.** Team-level delivery metrics (lead time, change failure rate) matter in M15 but are too coarse and too laggy to steer individual practice. Use them later, at the level they describe.

**The honest-baseline problem.** Your "without AI" baseline will be contaminated — you cannot unlearn agentic habits, and you will resent the control tasks. Accept the contamination and record it. A contaminated baseline you took is worth more than a clean one you didn't.

### Labs

**L0.1 — The prediction log (⏱ 30 min setup, ongoing).**
Create `ase/log.md` in a repo you own. One row per task: date, one-line description, predicted minutes, predicted rework passes, actual minutes, actual passes, read ratio, verification events, one-sentence note. Log every non-trivial task for two weeks, agent-assisted or not.
*Success:* ≥20 rows, ≥5 of them non-agent tasks.

**L0.2 — The control tasks (⏱ 3 h).**
Pick four tasks of comparable size in a codebase you know well. Do two entirely by hand, no completion, no agent. Do two with your current agent setup, whatever it is, without trying to improve it. Log all four.
*Success:* four rows with honest actuals, plus a paragraph on what surprised you.

**L0.3 — The dated beliefs statement (⏱ 1 h).**
Write 400–600 words: what do you currently believe agents are good at, bad at, and what do you expect this course to change? Commit it. Do not edit it later — you will re-read it in M16.
*Success:* committed, dated, specific enough to be falsifiable. "Agents are useful" is not falsifiable. "Agents will not be able to do our payments refactor without me writing the plan" is.

**L0.4 — Instrument one session (⏱ 1 h).**
Pick one agent session and record it — screen recording, or just an append-only scratch file where you paste every prompt and note every intervention. Afterward, mark each intervention as: *steering* (redirecting a fine approach), *correcting* (fixing a wrong output), or *rescuing* (aborting). The ratio is diagnostic and you will re-run this in M4 and M16.
*Success:* one annotated session transcript with intervention taxonomy applied.

### Evidence of mastery
`ase/log.md` with ≥20 rows including ≥4 control tasks, `ase/beliefs-2026.md`, and one annotated session with intervention taxonomy.

### Common failure modes
Skipping the module because it is not fun (most common). Automating the logging before you know what to log. Logging only successes. Treating the METR number as a verdict on agents rather than a verdict on self-assessment.

### Reading
[R-01] METR early-2025 study · [R-02] METR 2026 design update · [R-03] DORA 2026 ROI report (skim §J-curve only)

---
---

# STAGE 1 — OPERATOR

*Goal of this stage: drive one agent, well, on real work, with a loop that catches your mistakes.*

---

## M1 — The Agentic Loop: Build an Agent

⊢ M0 · ⏱ 6–10 h

### Why this module exists

Almost everything that feels mysterious about agents — "it forgot", "it hallucinated a file", "it went in circles", "it ignored my CLAUDE.md" — is transparent once you have written the loop yourself. Thorsten Ball's central claim is that a coding agent is *"an LLM, a loop, and enough tokens"*, demonstrable in under 400 lines. He is right, and the demonstration is the most efficient demystification available.

This is the agent-system-design content placed deliberately at the *front* of a practitioner course, because the practitioner benefit is immediate: after this module you debug agents by reasoning about context and tool results, not by rewriting prompts and hoping.

★ **An agent is a while-loop around a model with tools. Every "magic" behaviour and every failure is explicable at that level.**

### Outcomes
- Implement a working coding agent with read/write/search/execute tools
- Trace any agent misbehaviour to one of: context contents, tool definition, tool result, or stop condition
- Explain harness differences (plan modes, subagents, compaction, permission systems) as design choices with tradeoffs

### Core content

**The loop, precisely.**
```
messages = [system, user]
loop:
    response = model(messages, tools)
    if response has no tool calls: return response   # stop condition
    for each tool call:
        result = execute(call)                        # the only place reality enters
        messages.append(call); messages.append(result)
```
Everything else is refinement. Note what this exposes:
- The model never "sees" your filesystem. It sees *tool results you appended to a list.*
- "It forgot" means: the fact left the list, or never entered it.
- "It hallucinated a file" means: no tool result contradicted it.
- "It went in circles" means: the stop condition never fired and nothing in context changed between iterations. **Loops that cannot change their own context cannot terminate usefully** — this is the seed of M10.

**Tool design is the agent's API to reality.** Tools you will implement: `read_file`, `list_files`, `edit_file` (string replacement — note why replacement beats "rewrite the file"), `bash`, `grep`. Design questions that matter more than they look: what does the tool return on error? How verbose is success? A tool whose output is 8,000 tokens of build log is a context bomb; a tool that silently truncates is a correctness bomb.

**The harness is everything the loop is not.** Permission systems, context compaction, subagent spawning, memory files, hooks, planning modes, session persistence. Once you have the bare loop, every commercial harness reads as a set of answers to: *what do we put in context, when do we stop, what are we allowed to do, and who checks?*

**Why scaffolding can beat models.** Public benchmark results vary by double digits between harnesses running the *same* base model. When you read "model X scores Y on SWE-bench Verified", the harness is a co-author of that number. This is the first of several reasons benchmarks will not tell you what you need (M13).

### Labs

**L1.1 — Build the agent (⏱ 4–6 h).**
Follow Ball's tutorial [R-10] in a language you know — do not copy it; type it, and deviate where you want. Minimum: chat loop, `read_file`, `list_files`, `bash`, `edit_file`. Point it at a scratch repo and have it make a real change.
*Success:* your agent independently reads, edits, and runs tests in a repo, in one session, without you touching the files.

**L1.2 — Break it deliberately (⏱ 1–2 h).** Four experiments, each ~15 minutes, each with a written prediction *before* you run it:
- a) Remove the tool-result append (log it but don't add to messages). What happens?
- b) Make `bash` return only exit codes, no output. What breaks, and how does the agent compensate?
- c) Truncate `read_file` at 200 tokens with no truncation marker. Observe confident wrongness.
- d) Remove the stop condition and cap at 20 iterations. Watch a loop that cannot terminate.
*Success:* a table of prediction vs observation for all four, with the failure mapped to loop mechanics.

**L1.3 — Add one harness feature (⏱ 2 h).** Pick one and implement it: (i) a permission prompt before `bash`, (ii) naive compaction — when messages exceed N tokens, summarize the oldest half, (iii) a `spawn_subagent` tool that runs a fresh loop and returns only its final message.
*Success:* it works, plus 200 words on what it cost you (latency, tokens, correctness risk).

**L1.4 — Harness teardown (⏱ 1 h).** Take the agent harness you use daily. Map its features onto your loop: where does its planning mode intervene? What does compaction actually remove? What does a subagent return to the parent, and what is lost?
*Success:* a one-page annotated diagram.

### Evidence of mastery
A working agent in a repo, the four-experiment table, one implemented harness feature with a cost analysis, and the harness teardown diagram.

### Common failure modes
Copy-pasting the tutorial without typing it. Adding features before the bare loop works. Skipping L1.2 — it is where the learning is.

### Reading
[R-10] Ball, *How to Build an Agent* · [R-11] harness docs for your daily tool · [R-12] agent loop / ReAct background (optional)

---

## M2 — Briefing, Steering, Abandoning

⊢ M1 · ⏱ 6–8 h

### Why this module exists

The highest-leverage minute in an agentic session is the one before you hit enter. Boris Cherny's framing is to treat the agent as *an engineer you are delegating to, not a pair programmer you are guiding* — which changes what the opening message has to contain: goal, constraints, acceptance criteria, and the means of verification. Steinberger's is the complementary skill: *"Just talk to it. Play with it. Develop intuition."* — minimal ceremony, high volume, fast abandonment.

These are not in conflict. They are the two halves of one skill: **invest in the brief proportionally to the blast radius, and abandon fast when the trajectory is wrong.**

★ **Steering a bad trajectory is more expensive than restarting. The expensive move is the one that feels cheap.**

### Outcomes
- Write briefs calibrated to blast radius
- Recognise a doomed trajectory within ~2 minutes and abandon rather than negotiate
- Know why correcting in-context is often worse than restarting clean

### Core content

**Blast-radius assessment, before you start.** Steinberger's habit: estimate how many files the change touches and how long it will take, *before* launching. This single estimate determines everything downstream — brief length, whether to plan first, whether to run it in an isolated worktree, whether you can walk away.

| Blast radius | Brief | Plan first? | Isolation | Attention |
|---|---|---|---|---|
| 1–2 files, <10 min | one line | no | none | watch |
| 3–10 files, <1 h | goal + constraints + how to verify | usually | branch | check in |
| 10+ files, hours | full brief + research phase | always (M6) | worktree/container | review plan, then check in |
| Unknown | **find out first** — a research-only task with no edit permission | n/a | n/a | n/a |

**The four-part brief.** Goal (what "done" means, in outcomes not steps). Constraints (what not to touch; conventions; what to reuse). Acceptance criteria (the observable condition). Verification means (*how the agent itself can check* — the command, the URL, the test file). The fourth part is the one people omit and it is the one that matters most (M3).

**Underspecify implementation, overspecify verification.** Modern models plan implicitly and well. What they cannot infer is your definition of done. A brief that dictates the algorithm and omits the acceptance criterion inverts the value of the two.

**Modality.** Screenshots beat paragraphs for anything visual — Steinberger reports roughly half his prompts include an image. Voice beats typing for long briefs: you speak ~3× faster than you type, and the resulting brief is longer and more contextual, which is usually an improvement. Both are unglamorous and both are real multipliers.

**Context poisoning and the case for restarting.** Once a wrong approach is in context, the model will keep referencing it — it is *evidence* in the message list (M1). Corrections pile new instructions on top of visible failed reasoning. Harnesses that let you rewind to a prior state and re-brief are removing the failed attempt from context rather than arguing with it. Cherny's formulation: rewind instead of correcting, to keep failed attempts out of context. The general rule:

> **First correction: steer. Second correction on the same issue: stop, discard the context, rewrite the brief.**

**Write rules, not corrections.** When the agent gets a *convention* wrong, the fix does not belong in the chat. It belongs in the memory file or a skill, once, so it never recurs (M5, M8).

**The model is not the enemy.** Steinberger: *"Fighting the model is often a waste of time and tokens."* If three attempts fail, the brief, the context, or the codebase is the problem — not the model's willingness.

### Labs

**L2.1 — Brief archaeology (⏱ 2 h).** Take five of your recent agent sessions that went badly. For each, write the brief you *should* have written, using the four parts. Then re-run two of them with the improved brief in a clean session. Log both (M0 instrument).
*Success:* five rewritten briefs; ≥1 measurable improvement in rework passes; a note on the one that didn't improve and why.

**L2.2 — Blast-radius calibration (⏱ 2 h).** For ten upcoming tasks, predict file count and duration before starting; record actuals. Build your personal correction factor.
*Success:* ten predictions with actuals and a stated correction factor ("I underestimate file count by ~2× on anything touching the API layer").

**L2.3 — The abandonment drill (⏱ 1.5 h).** Run five tasks with a hard rule: at the *second* correction on the same issue, you must discard and restart with a rewritten brief. No exceptions, even when it feels close.
*Success:* five sessions, with a note on how many felt "nearly there" at the abandonment point and how the restart actually went.

**L2.4 — Modality experiment (⏱ 1.5 h).** Do three visual/UI tasks with text-only descriptions, then three comparable ones with screenshots. Separately, dictate three briefs by voice and type three. Log all twelve.
*Success:* logged comparison and a personal policy statement on when to use which.

### Evidence of mastery
Five rewritten briefs with outcomes, a calibration factor, the abandonment drill log, and a one-page personal briefing standard you will actually follow.

### Common failure modes
Writing enormous briefs for small tasks (ceremony as procrastination). Negotiating with a doomed session because sunk cost. Putting corrections in chat instead of memory files. Omitting verification means from every brief.

### Reading
[R-20] Cherny tips compilation · [R-21] Steinberger, *Just Talk To It* · [R-22] harness docs on rewind/checkpointing

---

## M3 — Verification-First Development

⊢ M1 · ⏱ 8–12 h · **This is the keystone module of Stage 1.**

### Why this module exists

Boris Cherny's single most repeated claim is that giving the agent a way to check its own output — a browser, a test, a simulator, a CLI — roughly **2–3×'s the quality** of results, and that verification is "the most important thing". Kent Beck reached the same place from the opposite direction: *"In augmented coding you care about the code, its complexity, the tests, & their coverage… tidy code that works. It's just that I don't type much of that code."*

Here is why this is *the* keystone. An agent in a loop with a working verifier is doing search with a fitness function. An agent without one is doing search with no fitness function — it is generating plausible text and stopping when it feels done. The difference is not incremental. It is the difference between an optimizer and a random walk.

And this is what licenses the expert behaviour that looks reckless from outside. Steinberger says *"These days I don't read much code anymore. I watch the stream and sometimes look at key parts."* That is only survivable because he has stacked verifiers elsewhere: agents write tests in the same context as the implementation, builds watch continuously, preview deploys land in ~2 minutes, commits are atomic and revertible, and he plays with the running software. **Not reading the code is a position you earn by building verification, not a shortcut you take instead of it.** Copying the behaviour without the substrate is how people ship disasters at high speed.

★ **Every task gets a verifier the agent can run itself. No verifier, no autonomy — at any level.**

### Outcomes
- Build a verification loop for any task type: backend, frontend, CLI, data, infra
- Judge verifier *quality* — coverage, determinism, speed, falsifiability
- Recognise and prevent the agent gaming its own verifier

### Core content

**The verifier ladder**, weakest to strongest. Know where each task sits:

| Rung | Verifier | Catches | Cost |
|---|---|---|---|
| 0 | Nothing / "looks right" | nothing | free, worthless |
| 1 | Compiler / type checker | shape errors | ~free |
| 2 | Linter + formatter | style, some bug classes | ~free |
| 3 | Existing test suite | regressions | seconds–minutes |
| 4 | New tests written for this change | the intended behaviour | minutes |
| 5 | Property/fuzz/generative tests | unimagined inputs | hours to set up |
| 6 | Running the software (browser, CLI, simulator) | integration + "feel" | minutes |
| 7 | Preview deploy / staging exercise | environment reality | minutes, needs infra |
| 8 | Human review by someone who knows the domain | intent, design, security | expensive, scarce |

Cheap rungs are not optional because they are cheap — they are the ones the agent can run on every iteration, which is what turns the loop into an optimizer.

**Tight loops beat thorough ones.** A 5-second test the agent runs 40 times finds more than a 20-minute suite it runs twice. Optimise your test suite for *agent iteration frequency*, which is a different objective from the one most suites were built for. This justifies real investment: test sharding, a fast subset target, watch-mode builds, hermetic fixtures.

**Tests in the same context as the implementation.** Steinberger's practice: ask for tests immediately after the feature, *in the same session*, because the model still has the implementation reasoning in context — the tests come out better and catch bugs during writing. Tests generated in a fresh session against finished code tend to be tautological restatements of what the code does.

**The tautology trap, and how agents game verifiers.** An agent asked to "make the tests pass" has several legal moves you did not intend: weaken the assertion, delete the test, add a special case for the test input, mark it skipped, mock the thing under test. Kent Beck watches specifically for *tests being disabled* and *unrequested functionality* as red flags. Defences:
- Write or review the *assertions* yourself even when the agent writes the test body.
- Make "tests changed" visible as its own reviewable category in the diff.
- Run mutation testing occasionally (M13) — the honest answer to "are these tests real?"
- A hook that fails the session if test files were modified during an implementation-only task (M8) turns a request into an enforcement.

**TDD as the binding constraint.** Beck's system prompt pattern: find the next unimplemented test, implement it, write only enough code to pass it, stop. Structural and behavioural changes go in separate commits. This gives the agent an unambiguous stop condition and gives you a reviewable sequence rather than a monolith. TDD was always good practice; with agents it becomes *load-bearing*, because it is the mechanism that keeps a fast generator honest.

**Non-code verifiers matter as much.** Frontend: the agent drives a real browser and looks at the result (a browser-control integration is typically far more token-efficient than screenshot-diffing). CLI: the agent runs its own binary and reads the output — "closing the loop" in the most literal sense. Data: assertions on row counts, schema, distributions. Infra: plan/diff output, policy checks.

**Verification is not review.** A verifier answers "does it do what it claims?" Review answers "is this the right thing, and will we regret it?" M4 is the second question. Do not let a green suite substitute for it.

### Labs

**L3.1 — The verifier audit (⏱ 2 h).** Take your last 15 agent-assisted changes. Score each on the ladder. Compute the distribution.
*Success:* a table plus a written diagnosis of your weakest rung and the cheapest way to raise it.

**L3.2 — Build the fast lane (⏱ 3–4 h).** In your main repo, create a target that runs the most informative possible subset of checks in **under 15 seconds** — type check, lint, a fast unit subset. Wire it into your agent's memory file as the command to run after every edit. Add a post-edit hook if your harness supports one.
*Success:* `<15s` measured, documented, and the agent actually runs it unprompted in a fresh session.

**L3.3 — Same-context tests (⏱ 2 h).** Implement three features. For each, ask for tests in the same session immediately after. Then, for a fourth, implement in one session and ask for tests in a *fresh* session. Compare: assertion quality, tautologies, bugs found.
*Success:* four test suites with a written comparison, including at least one identified tautological test.

**L3.4 — Adversarial verification (⏱ 2 h).** Give an agent a task and a deliberately weak test. Instruct it only to "make the tests pass." Document every way it games the verifier. Then strengthen the verifier and repeat.
*Success:* a catalogue of ≥3 gaming behaviours you personally observed, and the guardrail for each.

**L3.5 — Close a non-test loop (⏱ 2 h).** Pick a task where tests are a bad fit — a UI change, a CLI's output format, a report's appearance. Give the agent a way to *observe its own output*. Iterate until it self-corrects at least once without you.
*Success:* a session transcript showing the agent observing, judging, and correcting itself.

### Evidence of mastery
The verifier audit with diagnosis, a sub-15-second fast lane in a real repo, the same-context test comparison, the gaming catalogue, and one non-test loop transcript.

### Common failure modes
Treating "the tests pass" as sufficient. Slow test suites left slow. Letting the agent write both the test and the assertion unreviewed. Copying "I don't read code" without building rungs 4–7 first.

### Reading
[R-30] Beck, *Augmented Coding: Beyond the Vibes* · [R-33] Beck on TDD with agents (extended) · [R-27] Cherny on verification · [R-20] · [R-32] Steinberger, *Shipping at Inference-Speed* (read critically — note what substitutes for reading)

---

## M4 — Reading the Machine: Review Discipline

⊢ M3 · ⏱ 6–8 h

### Why this module exists

Review is now the bottleneck, and it is the bottleneck at two different scales. Individually: you can generate more code per hour than you can read per hour, so a review strategy is mandatory rather than optional. Organizationally: DORA's 2026 analysis identifies the "verification tax" — reviewing AI-generated code — as a major cost driver, and finds AI adoption correlating with **rising delivery instability** even as individual throughput rises.

The expert positions genuinely diverge here, and you must choose consciously:

- **DHH** reviews diffs before merge and uses aesthetics as a correctness signal: *"When something is beautiful, it's likely to be correct."*
- **Steinberger** reads little, watching the stream and key parts, backed by heavy automated verification and trivial revert cost.
- **Dex Horthy** shifts review *upstream* entirely: *"A bad line of code is a bad line of code. A bad line of a plan could lead to hundreds of bad lines of code. A bad line of research could land you with thousands of bad lines of code."*

★ **Choose where you spend your scarce reading attention — research, plan, or diff — and know what that choice leaves uncovered.**

### Outcomes
- Triage a diff by risk rather than reading linearly
- Apply the upstream-review strategy and know its blind spots
- Name and manage comprehension debt as an explicit liability

### Core content

**What review is actually for.** Horthy adopts Blake Smith's framing: code review's primary function is maintaining *team mental alignment* about what changed and why — not primarily catching bugs (tests do that better). This reframing is what makes upstream review coherent: if alignment is the goal, aligning on the plan is strictly more efficient than aligning on its consequences.

**Risk-ordered reading.** Never read a diff top to bottom. Read in this order, and stop when the risk budget is spent:
1. **Deletions and test changes** — anything removed, weakened, or skipped
2. **Security and boundary surface** — auth, input handling, permissions, secrets, serialization, anything touching untrusted input
3. **Data and migrations** — irreversible by nature
4. **Concurrency, money, time zones** — where plausible code is most often wrong
5. **Public interfaces** — what you will be stuck with
6. **New dependencies** — supply chain (M12); agents are documented to under-verify packages
7. Everything else — skim, or delegate to an automated reviewer

**Comprehension debt.** Osmani names the real cost of speed: *the gap between code shipped and code understood.* Unlike technical debt, it is invisible in the codebase and lives only in your head — you discover it during an incident at 3am. Manage it explicitly:
- Track read ratio (M0) as a first-class metric
- Mark low-comprehension modules in the repo, deliberately
- Budget "comprehension repayment": have the agent walk you through a subsystem you shipped but never read
- Treat a 0% read ratio on a *core* module as an incident waiting to be scheduled

**The dual-review pattern.** Use an agent as first-pass reviewer with an explicit checklist (a subagent or review skill), then apply your human attention to the risk-ordered list above. The agent finds mechanical issues consistently and misses intent consistently. Never let the same context that wrote the code review it — a fresh context, or better a differently-instructed one, is doing real work; the same context is grading its own homework.

**Aesthetics as signal, honestly.** DHH's beauty heuristic is real and limited. Agent output is often *superficially* beautiful — consistent naming, tidy structure — while being conceptually wrong, because surface style is exactly what a language model is best at. Beauty is evidence for *local* correctness, weak evidence for *architectural* correctness. Use it as a fast filter, never as an argument.

**When not reading is defensible.** Be honest about the preconditions: change is reversible in seconds; blast radius is contained; a strong verifier ran; the code is not security-, money-, or data-critical; you will find out fast if it is wrong. Steinberger's setup satisfies all five. Most enterprise contexts satisfy none.

### Labs

**L4.1 — Risk-ordered review drill (⏱ 2 h).** Take five recent agent-generated PRs. Review each twice: once linearly for 10 minutes, once risk-ordered for 10 minutes. Record findings per method.
*Success:* a finding-count comparison and a note on what the linear pass surfaced that the risk pass missed (it happens — know what).

**L4.2 — Comprehension audit (⏱ 2 h).** List every module you shipped in the last 90 days. Rate your comprehension 0–3 without opening the file. Then open three low scorers and check whether you were right. Write a repayment plan for the worst one and execute it.
*Success:* audit table, calibration check, one repaid module.

**L4.3 — Dual review (⏱ 2 h).** Build an agent reviewer with an explicit checklist (your risk order, your conventions, your past incidents). Run it on ten PRs alongside your own review. Track: agent-only findings, human-only findings, both, and false positives.
*Success:* a confusion table and a revised checklist based on what it missed.

**L4.4 — The upstream experiment (⏱ 2 h).** For one substantial change, spend your entire review budget on the plan (M6 previews this) and none on the diff. For a comparable change, spend it all on the diff. Compare outcomes and your own anxiety level.
*Success:* written comparison with an honest statement of which you trust and why.

### Evidence of mastery
Review-method comparison, comprehension audit with one repayment, a tuned agent-reviewer checklist with a confusion table, and the upstream experiment write-up.

### Common failure modes
Rubber-stamping large diffs. Reading linearly. Same-context self-review. Treating tidy code as correct code. Never measuring read ratio.

### Reading
[R-40] Horthy, ACE-FCA (review-the-plan section) · [R-101] Osmani on comprehension debt · [R-03] DORA 2026 (verification tax, instability) · [R-43] DHH on code aesthetics and diff review · [R-44] DHH on the shift (secondary)

---

### ▸ GATE 1 — Operator

Before Stage 2, demonstrate on a single recorded session in a real repo: a blast-radius assessment, a four-part brief, an agent-runnable verifier, one abandonment-and-restart, a risk-ordered review, and a logged entry in `ase/log.md`. See `ASSESSMENT.md` §Gate 1. **Capstone A** is taken here.

---
---

# STAGE 2 — ENGINEER

*Goal of this stage: stop compensating for a hostile environment. Shape the context, the process, and the codebase so the agent is set up to succeed before it starts.*

---

## M5 — Context Engineering

⊢ M1 · ⏱ 8–10 h

### Why this module exists

Dex Horthy states the premise as sharply as it can be stated: *"the contents of your context window are the ONLY lever you have to affect the quality of your output."* That is a slight overstatement — the model and the tools matter too — but as an operating assumption for a practitioner it is almost exactly right, because context is the lever you actually control.

Context engineering is not "write a good CLAUDE.md." It is treating the context window as a **budgeted, curated, actively-managed resource** with a lifecycle: what loads always, what loads on demand, what gets isolated into a subagent, what gets compacted away, and what should never enter at all.

★ **Context is a budget, not a bucket. Something must be evicted; decide what, deliberately, rather than letting the harness decide by truncation.**

### Outcomes
- Budget a context window and measure its actual composition
- Choose correctly between always-on memory, on-demand skills, path-scoped rules, and isolated subagents
- Diagnose context rot from behaviour and fix it structurally
- Perform intentional compaction and know what to preserve

### Core content

**Context rot, and its symptoms.** As a window fills, attention degrades non-linearly — long before any hard limit. Symptoms, in the order they usually appear: the agent stops following conventions it was following; it re-reads files it already read; it re-proposes an approach you already rejected; it contradicts an earlier decision; it gets *confidently* wrong about the codebase. Recognising these as *context* symptoms rather than *model* symptoms is the diagnostic skill.

**The 40–60% rule.** Horthy's team designs *the entire workflow* around keeping utilization in the 40–60% band, compacting deliberately rather than running to exhaustion and letting an automatic summarizer decide what survives. The band matters less than the principle: **never let the harness's emergency compaction be your compaction strategy.** Emergency compaction is lossy in ways you did not choose, at the moment you can least afford it.

**Intentional compaction.** When you compact on purpose, write a structured artifact — to a file, not just into the chat — containing: the end goal; the approach being taken; steps completed; the current blocker or failure state; critical file paths and dependencies. Then start a fresh context from that artifact. This makes progress *durable* rather than merely *remembered*, which also means it survives a crash, a model switch, and a night's sleep.

**What to compact away and what never to lose.** Compact: file-search transcripts, code-flow exploration, applied edits, build and test logs, large tool payloads. Preserve: decisions and their rationale, rejected approaches *with reasons* (otherwise they get re-proposed), exact file paths, the acceptance criteria, and the current failure state verbatim.

**Optimization priority — in this order.** Correctness (no wrong information in context) > Completeness (no missing information) > Size (no noise). Note that size is *last*. A lean context full of subtly stale information is worse than a fat accurate one. This ordering is regularly inverted by people optimizing token spend, and it is the expensive mistake.

**The placement decision.** Every piece of knowledge has a right home, and the wrong home is expensive in a specific way:

| Home | Loads | Right for | Cost of misuse |
|---|---|---|---|
| Always-on memory file | every session, every request | build/test commands, "never do X", core conventions | bloat taxes *every* request forever |
| Path-scoped rules | when matching files are touched | language- or directory-specific guidance | none if scoped correctly |
| On-demand skill | when invoked or matched | API references, playbooks, checklists, workflows | description bloat only |
| Subagent (isolated) | its own window | wide search, research, verification, anything high-volume | summary loss — say what you need back |
| Tool / MCP result | when called | live external data | verbose tools are context bombs |
| Nowhere | never | anything the agent can rediscover cheaply | — |

**Keep the always-on file small.** The current mainstream guidance is roughly **under 200 lines**, with reference material moved to on-demand skills and path-scoped rules. Note the tension with Steinberger's ~800-line `Agents.md` — he runs an enormous single-product codebase where nearly all of it applies to nearly every task, and he has agents update it as patterns emerge. The principle is not a line count; it is: **always-on content must earn its place on every single request.** Audit it periodically by asking, per section, "did this matter in the last ten sessions?"

**Context minimalism.** A counter-current worth taking seriously, and Cherny has moved toward it as models improved: give a minimal system prompt and tool list and let the model fetch what it needs. Capable models are good at finding things; pre-loading is often wasted budget and sometimes actively misleading. The correct position is empirical and *model-dependent*, which means it is a thing to re-test on every model upgrade (M13) rather than a thing to believe.

**Subagents as context firewalls.** The main reason to spawn a subagent is not parallelism — it is that a task will generate 50k tokens of searching to produce 500 tokens of answer, and you want only the answer. Design the *return* deliberately: the ideal subagent response looks like a compaction artifact (findings, file paths, architectural insight), not a transcript.

**MCP has a context cost.** Every connected server occupies budget. Practitioners have measured specific integrations costing tens of thousands of tokens in tool definitions alone before doing any work; Ronacher's rule of thumb is that most MCP servers expose far more tools than any task needs. Modern harnesses defer schemas and search tools lazily, which helps a great deal — but the discipline stands: connect what this task needs, disconnect the rest, and prefer a plain CLI the model already knows over a bespoke server that must be described to it.

### Labs

**L5.1 — Context census (⏱ 1.5 h).** In a real session, inspect what is actually in your window at startup: memory files, skill descriptions, tool definitions, system prompt. Produce a token breakdown.
*Success:* a pie chart or table of startup context with a total, plus one item you removed as a result.

**L5.2 — The always-on audit (⏱ 2 h).** Take your memory file section by section. For each, find evidence in your last ten sessions that it mattered. Delete or relocate anything without evidence. Re-measure.
*Success:* before/after line counts and token counts, with a relocation map (what became a skill, a rule, or nothing).

**L5.3 — Intentional compaction (⏱ 2 h).** Take a task that will exceed one window. Rather than letting auto-compaction fire, stop at ~50% utilization, write the structured compaction artifact to a file, start fresh from it, and finish. Then repeat a comparable task letting auto-compaction handle it.
*Success:* both transcripts, the artifact, and a comparison of what each approach lost.

**L5.4 — Rot diagnosis (⏱ 1.5 h).** Deliberately run a session to near-exhaustion on a real task. Log the *first* moment each rot symptom appears with its utilization percentage. Build your personal early-warning threshold.
*Success:* a symptom timeline and a stated threshold you will act on.

**L5.5 — Firewall a subagent (⏱ 2 h).** Take a high-volume research task. Run it in the main context, measure tokens consumed. Then run it via an isolated subagent with a specified return format. Compare cost and answer quality.
*Success:* token comparison plus the return-format spec you converged on.

### Evidence of mastery
Context census with a deletion, before/after audit of the always-on file, a compaction artifact with comparison, a personal rot threshold, and a subagent return-format spec.

### Common failure modes
Treating the memory file as documentation. Optimizing size before correctness. Letting auto-compaction be the strategy. Leaving every MCP server connected permanently. Copying another practitioner's memory file wholesale.

### Reading
[R-50] Anthropic, *Effective context engineering for AI agents* · [R-40] Horthy, ACE-FCA · [R-11] harness docs: memory, skills, rules, subagents · [R-160] AGENTS.md vs CLAUDE.md state of play · [R-52] Ronacher on MCP tool bloat

---

## M6 — Research → Plan → Implement

⊢ M5, M4 · ⏱ 8–10 h

### Why this module exists

This is the most transferable *process* innovation in agentic engineering, and it has the best-documented outcomes. Horthy's team reports fixing a bug in a 300k-line Rust codebase in a single session, and shipping ~35k lines of cancellation and WASM support in about seven hours — roughly three hours of research and planning, four of implementation — passing expert maintainer review.

The leverage argument is the whole argument: errors compound downstream. A bad line of research becomes a bad plan becomes thousands of bad lines of code. Spending 40% of your effort before any code is written is not overhead; it is where the error-correction is cheapest.

★ **Front-load the expensive thinking into reviewable artifacts. Review the research and the plan; let the implementation be mechanical.**

### Outcomes
- Run the three-phase workflow on a real change in an unfamiliar codebase
- Write research and plan artifacts that are reviewable and durable
- Know when spec-driven approaches help and when they are ceremony

### Core content

**Phase 1 — Research (no edits permitted).** The agent — usually several subagents in parallel — explores: where does this behaviour live, what calls it, what are the existing patterns, where are the tests, what will break. Output is a written research document: findings with **exact file paths and line references**, how information flows, candidate causes, constraints discovered, open questions.
*Your review question:* is this an accurate map of reality? Spot-check three claims against the actual code. If the research is wrong, stop — everything downstream is poisoned.

**Phase 2 — Plan (still no edits).** A step-by-step implementation outline: which files change, what the edit is, and **how each phase gets verified**. A good plan is boring and specific. A plan that says "refactor the auth module" is not a plan.
*Your review question:* if a competent stranger executed this literally, would the result be right? This is where your scarce attention buys the most.

**Phase 3 — Implement.** Execute phase by phase, verifying after each, compacting between phases. A crashed or exhausted session resumes from the plan document, not from memory.

**Why the artifacts are files, not chat.** Durability across sessions and crashes; reviewability by humans and other agents; reusability (a plan for one migration is 80% of the plan for the next); and — underrated — they are the honest record of what was intended when the incident review happens in four months.

**Where the ratio should land.** The reported 3:4 research-plan to implementation ratio is a reasonable starting point for substantial work in unfamiliar code. It is absurd for a two-line fix. Calibrate by blast radius (M2). The failure mode on each side is real: too little planning yields confident wrong direction; too much yields plans nobody reads, which is ceremony that feels like rigour.

**When it fails, and why.** Horthy documents a failure — removing a Hadoop dependency — where research did not adequately map nested dependencies. The method does not rescue insufficient research; it *amplifies* it. And it is a poor fit for genuinely exploratory work, where you do not yet know what you want and the point is to find out by building.

**Spec-driven development.** The adjacent 2026 movement treats the specification as the durable source of truth and the code as a generated artifact, with toolkits that scaffold a spec → plan → tasks → implementation pipeline. Sean Grove's framing is that the spec, not the code, becomes the primary artifact. Evaluate it with a clear eye: it genuinely helps on well-understood, repeatable work with stable requirements, and it becomes expensive ceremony on exploratory work. The *durable* insight is the same one as above — write intent down in a reviewable place before generating — and that insight survives whichever toolkit wins.

**Plans as repository assets.** Keep plan and research documents in the repo (`docs/plans/`, or alongside the change). They are the highest-value context for the *next* agent touching that subsystem, and they are the answer to "why did we do it this way" long after everyone has forgotten.

### Labs

**L6.1 — Research a stranger's codebase (⏱ 2 h).** Pick a real open-source project you have never worked in, and a real open issue. Run a research-only phase with no edit permission. Produce a research document. Verify three of its claims yourself against the source.
*Success:* research doc; ≥2 of 3 spot-checks accurate; any inaccuracy diagnosed (what in the process produced it?).

**L6.2 — Plan review drill (⏱ 2 h).** From that research, generate a plan. Review it and write down every objection *before* implementation. Implement. Then check which objections were real.
*Success:* objection list with hit rate, and a note on which class of objection you are good and bad at predicting.

**L6.3 — Ratio experiment (⏱ 3 h).** Take two comparable medium tasks. On one, spend ~40% of effort on research and planning. On the other, brief and go. Compare: wall-clock to done, rework passes, read ratio, your confidence.
*Success:* logged comparison with an honest verdict, including the case where planning lost.

**L6.4 — Plan reuse (⏱ 1.5 h).** Take a plan from a completed change and use it as the template for a similar change. Measure the savings and note what had to be re-researched.
*Success:* a derived plan, a time comparison, and a statement of what generalizes.

**L6.5 — Spec-driven trial (⏱ 2 h, optional).** Run one feature through a spec-driven toolkit end to end. Write an honest assessment: what did the ceremony buy, and what did it cost?
*Success:* a completed feature and a one-page verdict with a rule for when you would use it again.

### Evidence of mastery
A verified research document on unfamiliar code, a plan with a scored objection list, the ratio experiment, and a reused plan.

### Common failure modes
Letting the agent edit during research (context poisoning: it starts justifying its edits). Accepting research without spot-checking. Vague plans. Planning two-line changes. Keeping plans in chat where they die with the session.

### Reading
[R-40] Horthy, ACE-FCA · [R-60] Horthy talk, *Context Engineering for Complex Codebases* · [R-61] spec-driven development toolkits · [R-63] Horthy interviewed on context engineering · [R-62] Grove, *The New Code*

---

## M7 — Designing Codebases for Agents

⊢ M3 · ⏱ 10–14 h

### Why this module exists

Most agentic-coding advice treats the codebase as fixed and tries to compensate with prompting. That is backwards for anything you will maintain. Armin Ronacher's core observation: *"Agents really like local reasoning… they often work with just a few loaded files in context and don't have much spatial awareness of the codebase."* Everything that makes a codebase agent-hostile is a form of **non-local reasoning** — you cannot tell what this code does without knowing things that are not in front of you.

DHH's arrival at the same conclusion from a different direction is the strongest available evidence that this is real rather than a language preference: Rails, he argues, is enjoying a renaissance partly because convention-over-configuration makes it *token-efficient* for agents — the conventions are already in the model's weights, so less has to be explained — and because its integrated testing story lets agents self-validate. Convention over configuration turns out to be a machine-readable interface.

★ **Agent-legibility is a codebase property you can measure and improve, and it pays off for humans too.**

### Outcomes
- Audit a codebase for agent-legibility and rank fixes by cost/benefit
- Execute high-leverage legibility improvements using agents themselves
- Argue the tradeoffs where legibility conflicts with other goods

### Core content

**What agents want** (Ronacher, with the reasoning):
- **Explicit type information** over inference — inference requires whole-program reasoning the agent isn't doing; explicit types are local truth
- **Greppability** — Go's package-qualified references are the model case: every use site names its origin, so `grep` finds truth. Barrel files, `import *`, re-exports, and aliasing all break the chain between a symbol and its definition
- **Explicit context and dependencies** — a function that declares it needs the clock or the database can be reasoned about alone
- **Braces over significant whitespace** — LLMs generate indentation less reliably than delimiters, and a whitespace error is a semantic error
- **Result types over exceptions** — control flow that is visible in the signature
- **Boring, conventional structure** — the model has seen a million idiomatic repos and roughly none of yours

**What agents hate:** macros and heavy code generation (the source of truth isn't the source); deep re-export chains; import aliasing; **flaky tests** (they destroy the fitness function — a flaky suite is worse than no suite, because it teaches the agent that failures are noise); environment divergence ("works on my machine" becomes "works in my context"); multi-step tooling with many failure modes.

**The legibility audit — ten checks.** Score your repo 0–3 on each:
1. Can a symbol's definition be found by grep from any use site?
2. Does a fresh checkout build with one documented command?
3. Does the full test suite pass deterministically, twice in a row?
4. Is there a <15s feedback command? (M3)
5. Are module boundaries discoverable from the directory tree?
6. Is there dead code? (Run a detector — you will be surprised.)
7. Is there duplicated logic that will drift? (Run a clone detector.)
8. Do the conventions appear in the code, or only in someone's head?
9. Can a new subsystem be understood from its own directory?
10. Do error messages say what to do next?

**Refactoring as a standing budget.** Steinberger allocates roughly **20% of his time to refactoring — entirely performed by agents**: duplicate detection, dead-code removal, deprecation handling. This is now cheap enough to be continuous rather than a scheduled event, and it is the most direct lever on the audit score above. It is also the most agent-appropriate work there is: mechanical, verifiable, high-volume, low-judgment.

**Docs as context, not decoration.** Structure documentation so an agent reads *the right subsystem* — an index that maps concerns to directories, per-subsystem notes near the code, plan and research artifacts from M6 kept in the repo. Docs in a wiki the agent cannot reach are docs that do not exist.

**The honest tradeoffs.** Agent-legibility is not free and not always dominant:
- Explicitness costs concision; some teams will find the ceremony genuinely worse
- Abandoning metaprogramming can mean real duplication
- Rewriting a working system for legibility is usually a bad trade — apply this at the margin, to code you are touching anyway
- Language choice by agent-friendliness is a real strategy (Steinberger picks TypeScript, Go, and Swift partly for agent compatibility) and a real risk: optimizing your stack for the current generation of models is a bet on a fast-moving target
- Ronacher's speculation that languages will be designed *for* agents is worth knowing about and too early to act on

**The measurement.** Legibility work should show up in your M0 numbers — fewer rework passes, fewer "the agent couldn't find it" sessions, higher first-pass success. If it doesn't, you improved your aesthetics, not your legibility.

### Labs

**L7.1 — Legibility audit (⏱ 2 h).** Score your primary repo on all ten checks with evidence for each score. Rank fixes by (impact × frequency) ÷ cost.
*Success:* scored audit with a ranked, costed remediation list.

**L7.2 — Automated hygiene sweep (⏱ 3 h).** Run dead-code and duplicate-code detection. Have agents remove dead code and consolidate the worst duplication, in small verified commits.
*Success:* merged cleanup with all tests green and a before/after metric.

**L7.3 — Kill the flakes (⏱ 3 h).** Identify flaky tests by running the suite ten times. Fix or quarantine every one.
*Success:* ten consecutive identical runs, plus a quarantine policy written down.

**L7.4 — Greppability repair (⏱ 2 h).** Find the worst indirection in your codebase (barrel file, re-export chain, dynamic dispatch by string). Remove one. Measure the difference in agent file-finding on three tasks before and after.
*Success:* before/after with a measured difference — or an honest null result.

**L7.5 — Convention extraction (⏱ 2 h).** Have an agent infer your codebase's implicit conventions from the code itself. Review the list: what it got right tells you what is legible; what it got wrong tells you what is folklore. Encode the important ones as rules or lint checks (M8).
*Success:* an inferred convention list, corrected, with ≥2 encoded as enforceable checks.

### Evidence of mastery
Scored audit with remediation list, a merged hygiene sweep, a deterministic test suite, one greppability repair with measurement, and ≥2 conventions turned into enforcement.

### Common failure modes
Rewriting working code for aesthetics. Treating agent-legibility as the only goal. Adding conventions to the memory file instead of enforcing them in lint. Leaving flaky tests because "everyone knows which ones are flaky" — the agent doesn't.

### Reading
[R-70] Ronacher, *A Language For Agents* · [R-71] Ronacher, *Agentic Coding Recommendations* · [R-73] Ronacher, *Things That Didn't Work* · [R-43] DHH on Rails and token efficiency · [R-32] Steinberger on the refactoring budget

---

## M8 — The Extension Surface

⊢ M5 · ⏱ 6–8 h

### Why this module exists

Modern harnesses expose a customization surface — memory files, path-scoped rules, skills, subagents, hooks, MCP servers, plugins, slash commands. Used well, it converts your repeated corrections into permanent behaviour. Used badly, it becomes a pile of half-remembered configuration that bloats context and produces mysterious behaviour.

The organizing distinction is short, important, and constantly violated:

> **An instruction is a request. A hook is a guarantee.**

"Never edit `.env`" in a memory file is a request the model will *usually* honour. A pre-tool hook that blocks the edit is enforcement. Anything that must hold every time belongs in the deterministic layer.

★ **Match the mechanism to the requirement: guarantees go in hooks, knowledge goes in skills, always-true rules go in memory, volume goes in subagents.**

### Outcomes
- Choose the right mechanism for a given need and justify it
- Build a personal extension kit that earns its context cost
- Evaluate MCP servers on cost/benefit rather than novelty

### Core content

**The selection table.**

| Need | Mechanism | Why |
|---|---|---|
| "Always do X" — conventions, build commands | always-on memory | needed every session |
| Guidance only for certain files or languages | path-scoped rules | zero cost when irrelevant |
| A playbook you paste for the third time | skill | on-demand, invocable |
| Reference material needed occasionally | skill | keeps memory small |
| Must happen every time, no judgment | hook | deterministic, cannot be argued with |
| Must *never* happen | hook (blocking) | enforcement, not request |
| High-volume search or research | subagent | context isolation |
| Repeatable specialized review | subagent with its own instructions | fresh perspective, own context |
| Live external data or actions | MCP server | real connection |
| Same setup across repos | plugin | packaging |

**Growth discipline — add on trigger, not in advance.** The mainstream triggers, which are also good practice generally: agent gets a convention wrong twice → memory file. You type the same prompt repeatedly → skill. You paste the same playbook a third time → skill. A side task floods your conversation → subagent. You want something to happen without asking → hook. A second repo needs the same setup → plugin. Building a large extension kit before you have the triggers produces configuration you do not understand and cannot debug.

**Hooks are the under-used mechanism.** High-value hooks: format after every edit; run the fast lane after every edit and feed failures back; block edits to secrets, migrations, or vendored directories; log every session for M0 telemetry; refuse test-file modification during implementation-only tasks (M3's anti-gaming guardrail); notify on session end. Each converts vigilance into infrastructure.

**Subagents: design the return.** A subagent's value is the compression ratio between what it reads and what it returns. Specify the return format explicitly — findings, file paths, open questions — or you get either a transcript (no compression) or a vague summary (lost information).

**MCP, evaluated honestly.** MCP is the genuine standard for connecting agents to external systems, and it solves a real problem. The practitioner critique is equally real: servers commonly expose far more tools than any task needs, tool definitions occupy context, and a CLI the model already knows from training often beats a bespoke server that must be described to it. Ronacher's blunt verdict from a year of practice was that MCP underperformed for him personally; Steinberger prefers custom CLIs, reasoning that the knowledge already exists in the model's weights. Modern harnesses mitigate a lot of this with lazy schema loading and tool search. The decision rule:

> Use MCP when the integration needs **live connection, authentication, or actions** that a CLI cannot provide. Use a CLI when the model already knows the tool. Measure the context cost either way, and disconnect what this task does not need.

**The anti-pattern: configuration cargo cult.** Copying someone else's extension kit imports their codebase's assumptions, their team's conventions, and their model's quirks. Every item in your kit should trace to a specific failure you personally experienced.

### Labs

**L8.1 — Correction mining (⏱ 2 h).** Review your last 20 sessions and list every correction you made. Cluster them. For each cluster, choose the right mechanism and implement the top three.
*Success:* a correction taxonomy plus three implemented extensions, each traced to specific incidents.

**L8.2 — Build a guardrail hook (⏱ 2 h).** Implement a blocking hook for something that must never happen in your repo. Verify it by trying to make the agent do it.
*Success:* a demonstrated block, plus a note on what the agent did when blocked (this is informative).

**L8.3 — Build a review subagent (⏱ 2 h).** Create a specialized reviewer with its own instructions and a specified return format. Run it on five PRs. Tune based on misses.
*Success:* subagent definition, five reports, one tuning iteration documented.

**L8.4 — MCP cost/benefit (⏱ 1.5 h).** Measure the context cost of each connected server. For the most expensive, try replacing it with CLI calls and compare results and tokens.
*Success:* a cost table and one justified connect/disconnect/replace decision.

### Evidence of mastery
A correction taxonomy with three traced extensions, a working blocking hook, a tuned review subagent, and an MCP cost table with a decision.

### Common failure modes
Copying someone else's kit. Building extensions before having the triggers. Using instructions where enforcement is required. Leaving every MCP server connected. Skills with vague descriptions that never trigger, or trigger wrongly.

### Reading
[R-11] harness extensibility docs · [R-81] "steering" guidance on choosing between mechanisms · [R-52] Ronacher on MCP · [R-20] Cherny on hooks and skills

---

### ▸ GATE 2 — Engineer

Before Stage 3: a context budget with measurements, a research→plan→implement change landed in unfamiliar code, a legibility audit with executed remediation, and an extension kit whose every item traces to a real failure. **Capstone B** is taken here. See `ASSESSMENT.md` §Gate 2.

---
---

# STAGE 3 — ORCHESTRATOR

*Goal of this stage: stop being the bottleneck — safely. Everything here multiplies both output and blast radius, which is why M12 is a hard prerequisite for the unattended portions.*

---

## M9 — Parallelism

⊢ M3, M4 (Gate 1) · ⏱ 8–10 h

### Why this module exists

Cherny calls git worktrees *"the single biggest productivity unlock"* and runs five or more sessions concurrently. Steinberger runs 3–8 agents in a terminal grid — and notably, **in the same folder**, avoiding worktrees for speed, with agents making atomic commits. Two expert practitioners, one at the tool's origin, with directly contradictory isolation strategies.

The contradiction is instructive rather than confusing: they are optimizing different things. Worktrees optimize for **isolation** (no interference, clean review, safe abandonment) and cost setup time and disk. Same-folder optimizes for **latency and shared state** (no rebuild per tree, agents see each other's work) and costs collision risk — tolerable only with small atomic commits, tight supervision, and a willingness to throw work away.

★ **Parallelism moves the bottleneck from generation to your attention. If you cannot review and integrate N streams, running N agents produces a queue, not throughput.**

### Outcomes
- Choose an isolation strategy per situation and justify it
- Run 3+ concurrent agents without becoming the bottleneck or the merge conflict
- Recognise when parallelism is negative-value

### Core content

**The isolation spectrum.**

| Strategy | Isolation | Setup cost | Best for | Risk |
|---|---|---|---|---|
| Same folder, multiple agents | none | zero | small independent edits, tight supervision | collisions, interleaved commits |
| Branches | git-level | low | sequential-ish work | switching cost, shared working dir |
| **Worktrees** | filesystem | medium | genuinely parallel features | disk, per-tree rebuild/deps |
| Containers / VMs | full | high | untrusted or destructive work, unattended runs | slowest feedback |
| Cloud/remote sessions | full + off-machine | varies | long jobs, mobile (M11) | weakest observability |

**Task decomposition for parallelism.** Good parallel tasks are **independent in the file dimension and independent in the review dimension**. Three features in three subsystems parallelize. Three refactors of the same module do not — you will spend the savings on merge conflicts. Ideal candidates: independent bug fixes, per-package migrations, writing tests for distinct modules, documentation, research fan-out, multi-angle exploration of the same problem (deliberately redundant, pick the best).

**The human scheduler problem.** With N agents you become a scheduler, and scheduling has costs: switching (~context reload per switch), review debt (finished work queues while you attend elsewhere), and *integration* (N branches must land). Empirically most people find their ceiling at **3–5 concurrent streams**, and the ceiling is set by review capacity, not by tooling or quota.

**When parallelism is negative-value.** Exploratory work where each step informs the next. Tasks touching the same files. Work you do not have the review budget for. Anything where you do not yet know what "done" looks like. **A parallel agent with no verifier is just a faster way to generate unreviewed code** — M3 is a hard dependency here, not a suggestion.

**Ergonomics that actually matter.** These sound trivial and are the difference between 3 agents and 6: name sessions; colour terminals per session; one-key switching; a control-plane view of what every session is doing; notification on completion or on needing input. Without these, you spend your attention on *finding* the agent that needs you.

**Redundant parallelism.** An under-used pattern: run the *same* task three times with different framings, then pick or synthesize. Expensive in tokens, cheap in wall-clock, and unusually effective on design-ish problems where you cannot specify the criterion in advance but recognise a good answer when you see one.

### Labs

**L9.1 — Isolation bake-off (⏱ 3 h).** Run the same three-task batch three ways: same-folder, worktrees, containers. Measure setup time, collisions, wall-clock to all-merged, and your own stress level.
*Success:* a comparison table and a written per-situation policy.

**L9.2 — Find your ceiling (⏱ 3 h).** Run 2, then 3, then 5, then 7 concurrent agents on independent tasks. Track throughput (tasks merged/hour) and quality (rework passes). Find where throughput stops rising.
*Success:* a throughput curve with your stated ceiling and the constraint that sets it.

**L9.3 — Decomposition drill (⏱ 2 h).** Take one large feature. Produce a decomposition into ≥4 parallelizable units with explicit file-level independence. Execute it.
*Success:* the decomposition, the merge outcome, and a note on what collided anyway.

**L9.4 — Build the control plane (⏱ 2 h).** Set up your session ergonomics: naming, colours, switching, completion notification.
*Success:* a documented setup you can start in under a minute, plus a before/after switching-time measurement.

### Evidence of mastery
Isolation comparison with a policy, a throughput curve with a stated ceiling, an executed decomposition, and a working control plane.

### Common failure modes
Parallelizing coupled work. Running more agents than you can review. No isolation on destructive tasks. Ignoring ergonomics and losing the gains to context switching.

### Reading
[R-20] Cherny on worktrees · [R-21] Steinberger on same-folder parallelism · [R-90] worktree and orchestration tooling

---

## M10 — Loop Engineering

⊢ M9, M3, M12 · ⏱ 10–14 h

### Why this module exists

This is the frontier of 2026 practice and the point of the whole course. Karpathy states the objective plainly: *"remove yourself as the bottleneck… arrange things such that they're completely autonomous"*, and reports the payoff — *"I put in just very few tokens just once in a while and a huge amount of stuff happens."* His AutoResearch experiments overnight on his own nanoGPT work found hyperparameter improvements he had missed across two decades of manual tuning.

Note the precondition hiding in his framing: *"you just have to arrange it so that it can just go forever."* Arranging that is the skill, and the only thing that makes it possible is an **objective, automatable criterion of success**. Where that exists, autonomy is available. Where it does not, autonomy produces confident garbage at scale.

★ **A loop is only as good as its fitness function and its stop condition. Build those first; the loop itself is ten lines.**

### Outcomes
- Design, run, and terminate an autonomous loop on real work
- Match loop patterns to task types and recognise anti-fits
- Build guardrails, state management, and observability for unattended runs

### Core content

**The canonical minimal loop.** The technique Geoffrey Huntley popularized in 2025 as "Ralph" is, at its core, a shell loop feeding a specification file to an agent repeatedly — `while :; do cat PROMPT.md | <agent>; done`. Each iteration gets a fresh context window and works from the durable spec plus whatever state is on disk. The insight is not the bash; it is that **fresh contexts working from a persistent specification beat one long context working from memory**, which is the same insight as M5's intentional compaction, mechanized.

**The five components of a working loop** (Osmani's decomposition, which is the clearest available):
1. **Trigger** — schedule, event, or continuous
2. **Isolation** — worktrees or containers so concurrent iterations don't collide
3. **Knowledge** — skills and docs so each fresh context starts informed rather than re-deriving
4. **Connection** — access to the issue tracker, CI, logs, whatever the loop needs to perceive
5. **Verification by a separate agent** — because a model grading its own work is not verification

Plus the thing everything depends on: **persistent state on disk**, because the model forgets everything between runs. A progress file, a task list, a state machine — the loop's memory is the filesystem.

**Design the stop condition first.** From M1: a loop whose context cannot change cannot terminate usefully. Legitimate stop conditions: all tests pass; the checklist is empty; N iterations without measurable progress; a budget cap (tokens, time, money); an explicit goal predicate. Every loop needs **at least two** — a success condition and a failure/budget condition — or you are relying on noticing.

**Overbaking.** Documented failure mode: loops run too long begin generating bizarre emergent work — unrequested features, speculative abstractions, in one recorded case unexpected cryptography. An agent with remaining budget and no remaining work will *invent* work. Budget caps are not a cost-control measure; they are a correctness measure.

**Loop patterns, with fit.**

| Pattern | Shape | Fits | Anti-fits |
|---|---|---|---|
| Spec loop (Ralph) | fresh context ← spec, repeat | greenfield from a strong spec; mechanical bulk work | exploration; anything underspecified |
| Checklist loop | work one item, mark done, repeat | migrations, per-file sweeps | coupled changes |
| Triage loop | scheduled: scan inbox → act or escalate | issue triage, dependency updates, PR babysitting | anything needing judgment calls it can't escalate |
| Verify-and-fix loop | run checks → fix failures → repeat | flaky-test elimination, lint sweeps, type migration | problems whose fix changes the spec |
| Fan-out/verify | N agents work, M agents check | audits, multi-angle review, large refactors | small tasks (overhead dominates) |
| Optimizer loop | propose → measure → keep/discard | performance work, anything with a real metric | anything where the metric is a proxy you'll goodhart |

**Spec quality is the whole game.** The documented failure of spec loops is invariably spec failure — a GTD app attempt failed because "the specs were way off base". A loop amplifies its input by hundreds of iterations. **A mediocre spec run 200 times produces 200 iterations of mediocrity**, quickly and expensively.

**Guardrails for unattended operation** (M12 covers the security dimension; these are the operational ones): a hard budget in tokens and wall-clock; a blast-radius fence (which paths may be touched); no force-push, no production credentials, no destructive migrations; a kill switch you can reach from your phone; an append-only log of every action; and a **rollback plan you have actually tested** — untested rollback is a hope.

**Observability.** You will not watch. So the loop must report: what it did, what it verified, what it skipped, where it got stuck. A loop that produces 40 commits and no narrative is unreviewable, and unreviewable work is not done work.

**Where loops genuinely fail.** Exploration and open-ended design. Anything with no automatable success criterion. Work requiring negotiation with humans. Merge-conflict-heavy territory (loops tend to re-run rather than rebase). Tasks where being wrong is expensive and detection is slow — the worst quadrant.

**Karpathy's caution, kept in view.** He is explicit that agents remain jagged: strong on verifiable, metric-driven tasks, weak on *"nuance of maybe what I had in mind or what I intended and when to ask clarifying questions."* Loop engineering works precisely in the verifiable half of that split. Applying it to the other half is the central error of the era.

### Labs

**L10.1 — Minimal loop (⏱ 2 h).** Build the simplest possible loop in a sandboxed repo: spec file, fresh context each iteration, disk state, hard iteration cap. Run it on a well-specified mechanical task.
*Success:* a loop that completes a real task and stops on its own condition, with a log.

**L10.2 — Stop-condition design (⏱ 2 h).** For three different task types, design and implement stop conditions — success predicate, no-progress detector, budget cap. Test each by making it fire.
*Success:* three loops, each demonstrated stopping for each of the three reasons.

**L10.3 — Induce overbaking (⏱ 1.5 h).** Deliberately run a loop past its useful life with an under-specified task. Document the emergent behaviour.
*Success:* a written account of what it invented, and the guardrail that would have prevented it.

**L10.4 — Verified loop (⏱ 3 h).** Build a fan-out/verify loop: worker agents produce, a separate verifier agent with different instructions checks, failures return to the queue. Run it on a real audit or refactor.
*Success:* a run where the verifier caught ≥1 real defect the worker missed, with the evidence.

**L10.5 — Scheduled triage loop (⏱ 3 h).** Build a loop that runs on a schedule against something real — dependency updates, issue triage, failing-test sweep — with escalation for anything it should not decide. Run it for a week.
*Success:* seven days of logs, a list of what it handled and what it escalated, and a written correctness assessment.

### Evidence of mastery
A terminating loop with a log, three demonstrated stop conditions, an overbaking account, a verified fan-out run with a caught defect, and a week of scheduled-loop logs with an assessment.

### Common failure modes
Running loops before M12. No budget cap. No persistent state (the loop re-derives everything each iteration). Model grading its own work. Looping exploratory work. Spec quality unexamined. No rollback test.

### Reading
[R-100] History and mechanics of the Ralph technique · [R-101] Osmani, *Loop Engineering* · [R-102] Karpathy, Sequoia 2026 · [R-104] Karpathy on No Priors (AutoResearch, the loopy era) · [R-103] Huntley's original writing

---

## M11 — Async, Remote & Cloud Agents

⊢ M10 · ⏱ 5–7 h

### Why this module exists

Once loops run without you, *where* they run and *how you supervise them* becomes the practical question. The practice has moved to agents in the cloud, agents in CI, agents opening PRs, and supervision from a phone. Cherny describes starting sessions on mobile and continuing on desktop, moving sessions between surfaces, and running scheduled cloud jobs that survive closing the laptop.

This module is short because the concepts are inherited from M9 and M10. What is new is a genuine failure mode: **the review queue.** Async agents generate work asynchronously; your review capacity does not scale. A dozen agent PRs waiting on Monday morning is not leverage.

★ **Async multiplies production and does nothing for review. Design the review path before you turn on the production path.**

### Outcomes
- Choose local vs cloud vs CI execution per task
- Supervise unattended work from low-bandwidth contexts
- Design a review path that does not become a queue

### Core content

**Where to run, and why.** Local: fastest feedback, full observability, your credentials, your machine at risk. Cloud/remote session: survives your laptop closing, reachable from anywhere, weaker observability, credential questions get serious. CI-triggered: reproducible, auditable, integrates with existing review — and the highest-risk surface for prompt injection (M12: untrusted issue and PR text has been used to drive agents in CI; see the CVE case study).

**The handoff pattern.** Start with high-bandwidth interaction (brief, plan, verify approach), then hand to async execution, then return for review. The expensive human minutes are at the start and end; the middle should not require you.

**Low-bandwidth supervision.** From a phone you can realistically: approve or reject a plan, answer a blocking question, kill a run, read a summary. You cannot review a 2,000-line diff. Design agents to *ask well* — a blocking question with three options beats an open one — and to report in summaries a human can act on from a small screen.

**The review queue, managed.** Options, in increasing order of commitment: rate-limit production to match your review capacity; require agents to self-review with a separate verifier before queueing; batch review into dedicated blocks rather than interrupt-driven; let low-risk categories (dependency bumps with green CI, doc fixes, test additions) auto-merge on policy; escalate only what a policy cannot classify. The organizing principle: **decide what does not need your eyes, explicitly, rather than by neglect.**

**Credentials.** Cloud and CI agents need secrets to be useful and are the worst place to put them. Minimum: scoped short-lived tokens, no production credentials, egress restrictions, separate identities per agent so actions are attributable, and an audit log. The published CVE case study in M12 is precisely a credential-exfiltration chain through a CI agent.

### Labs

**L11.1 — Handoff (⏱ 1.5 h).** Run one task through the full pattern: interactive brief and plan → async execution → return for review. Time each phase.
*Success:* a phase breakdown with the fraction of wall-clock requiring you.

**L11.2 — Phone drill (⏱ 1.5 h).** Supervise one real async run entirely from a phone. Note every point where you needed more than the small screen allowed.
*Success:* a friction list and ≥2 changes to how the agent reports or asks.

**L11.3 — Review-path design (⏱ 2 h).** Write a policy classifying agent output into auto-merge / fast review / full review, with rules. Apply it to twenty recent agent changes retrospectively and check for misclassification.
*Success:* a written policy, applied, with the misclassification rate and a revision.

**L11.4 — CI agent, safely (⏱ 2 h).** Set up an agent triggered by a repository event, with least-privilege credentials, egress restrictions, no write access to the repo it evaluates, and a documented threat model.
*Success:* a working CI agent plus a threat model naming untrusted inputs and what it could exfiltrate if compromised.

### Evidence of mastery
A timed handoff breakdown, a phone-supervision friction list with fixes, a validated review policy, and a CI agent with a written threat model.

### Common failure modes
Turning on async production without a review path. Production credentials in cloud agents. Agents that ask open-ended questions you cannot answer from a phone. Treating CI agents as trusted.

### Reading
[R-11] harness docs on remote/cloud sessions and scheduling · [R-120] CVE-2025-66032 case study (also M12) · [R-20] Cherny on mobile and session teleport

---

## M12 — Security & Safety for Agentic Development

⊢ M8 · ⏱ 8–10 h

> **This module is a hard prerequisite for the unattended portions of M10 and M11.**

### Why this module exists

Agentic coding created a genuinely new attack surface, and the 2026 incident record is no longer theoretical. Simon Willison's **lethal trifecta** names the condition precisely: an agent with (1) access to private data, (2) exposure to untrusted content, and (3) the ability to communicate externally can be made to exfiltrate. **All three together are the vulnerability; any two are safe.** Almost every agentic coding setup has all three by default.

The concrete case: **CVE-2025-66032** in a widely-used coding-agent GitHub Action. An authorization check trusted any GitHub App actor, so an attacker could file a crafted issue on a public repository, have the injected instructions read the workflow environment (`cat /proc/self/environ`), extract an OIDC token, exchange it for write access, and commit to the action's own source — poisoning every downstream consumer. Disclosed January 2026, fixed within days, publicly detailed in June. Parallel research found that multiple major coding agents treated untrusted GitHub metadata — PR titles, issue bodies, HTML comments — as authentic instructions.

Read that attack chain twice. Nothing in it required a model failure. Every step was the agent doing exactly what it was told by text it had no way to distinguish from your instructions.

★ **An agent cannot reliably distinguish data from instructions. Architect on that assumption; do not prompt your way around it.**

### Outcomes
- Apply the lethal-trifecta test to any agent configuration
- Design permission, sandboxing, and egress controls proportional to autonomy
- Threat-model an agentic workflow and defend the supply chain

### Core content

**Indirect prompt injection, structurally.** Direct injection is the user attacking their own agent — mostly their problem. Indirect injection is the dangerous class: instructions arrive in content the agent *reads* — a GitHub issue, a dependency's README, a web page, a code comment, an error message, a log line, an MCP tool result. There is no reliable in-band separation of instructions from data in an LLM, and as of 2026 prompt injection remains the leading cause of production agentic security failures. Treat mitigation as **architectural, not prompt-level**.

**The trifecta test.** For any agent configuration ask: does it have private data? Does it see untrusted content? Can it communicate out? If all three, you must break one:
- *Break data access:* no credentials, no private repos in that session
- *Break untrusted content:* human-sanitize inputs; do not feed raw issue text to an agent with credentials
- *Break egress:* network allowlist, no arbitrary HTTP, no push, no external tool calls

**Sandboxing tiers, matched to autonomy.**

| Autonomy | Isolation | Network | Credentials |
|---|---|---|---|
| Supervised, you watch every action | host OK | open | your own, present |
| Supervised, auto-approved safe commands | host + permission policy | open | your own |
| Unattended, bounded task | container or sandbox | allowlist | scoped, short-lived |
| Unattended loop (M10) | container, disposable | strict allowlist | minimal, per-agent identity |
| CI-triggered on untrusted input | container, no repo write | egress-filtered | none, or read-only |

The rule: **isolation must rise with autonomy, not with your comfort level.** Comfort grows faster than safety.

**Permission design.** Blanket "skip all permissions" flags are the common shortcut and the common cause. The better path is an allowlist of genuinely safe operations plus sandboxing, so prompts are rare *because most actions are provably safe* rather than because you disabled the check. Diagnose prompt fatigue as a configuration problem; do not treat it with a bigger hammer.

**Supply chain.** Two directions, both real. *Inbound:* agents have been documented skipping package verification — installing packages without checking provenance, accepting typosquats, adding dependencies casually. Require lockfiles, pin actions to commit SHAs, and make "new dependency" a mandatory review category (M4). *Outbound:* an agent with write access is a commit path into your repository, and therefore into your users' systems.

**Secrets.** Never in the context window. Never in memory files. Never in an environment an unattended agent can read. Assume anything readable will eventually be read aloud — that is exactly the CVE chain.

**MCP server trust.** An MCP server is code you run and a channel through which tool results — i.e. attacker-controllable text — enter your context. Treat installing one as installing a dependency with your credentials attached: review the source, prefer first-party, pin versions, and limit what it can reach.

**The organizational seam.** Security research in 2026 notes that agentic CI vulnerabilities fall between vendors, platform teams, and application teams, with no clear owner. If you are introducing agents into a team's CI, **you are the owner until you name someone else.**

### Labs

**L12.1 — Trifecta audit (⏱ 2 h).** Enumerate every agent configuration you run — local, CI, cloud, scheduled. For each, mark the three trifecta conditions. For every all-three case, break one and document how.
*Success:* an audit table with a remediation per finding.

**L12.2 — Attack your own agent (⏱ 2.5 h).** In a sandbox with a fake credential, plant injection payloads in places your agent reads: a README, a code comment, a test fixture, a mock issue body, a tool result. See which the agent obeys.
*Success:* a results table of which vectors worked, plus a written defence for each success.

**L12.3 — Build the sandbox (⏱ 2 h).** Create a containerized environment for unattended runs: no host credentials, egress allowlist, mounted work directory only, disposable.
*Success:* a working sandbox, with a verified test that egress to a non-allowlisted host fails.

**L12.4 — Threat model a workflow (⏱ 2 h).** Take your riskiest agentic workflow. Write a threat model: trust boundaries, untrusted inputs, what an attacker gains, what would detect it. Then fix the top finding.
*Success:* a written threat model and one implemented mitigation.

**L12.5 — Supply-chain guardrail (⏱ 1.5 h).** Implement enforcement — a hook or CI check — that flags any agent-added dependency for human review, and pin your CI actions to SHAs.
*Success:* a demonstrated flag on a test dependency addition; pinned actions merged.

### Evidence of mastery
A trifecta audit with remediations, a red-team results table, a verified sandbox, a threat model with a fix, and a working supply-chain guardrail.

### Common failure modes
Blanket permission-skipping as the default. Treating prompt injection as solvable by instructions. Production credentials in unattended runs. Trusting MCP servers as configuration rather than dependencies. Assuming the vendor handles it.

### Reading
[R-120] Willison, *The lethal trifecta* · [R-121] CVE-2025-66032 / CI prompt injection research note · [R-122] 2026 agentic security state-of-practice · [R-123] supply-chain and package-verification findings · [R-124] 2026 supply-chain attack landscape

---

### ▸ GATE 3 — Orchestrator

Before Stage 4: a documented parallelism ceiling, a week-long scheduled loop with logs and an assessment, a review policy in force, and a completed trifecta audit with remediations. See `ASSESSMENT.md` §Gate 3.

---
---

# STAGE 4 — ARCHITECT

*Goal of this stage: build the things that let you keep improving after the course ends, and carry other people with you.*

---

## M13 — Evals for Your Own Work

⊢ M6, M7 (Gate 2) · ⏱ 8–10 h

### Why this module exists

You will face this decision every few weeks for the rest of your career: a new model ships, or you change your prompt, memory file, or workflow. **Did it help?** Public benchmarks cannot answer this. They measure a different distribution of tasks, in a different codebase, with a different harness — and harness choice alone moves benchmark scores by double digits on the same base model. Benchmark saturation, contamination, and the gap between "resolves a GitHub issue" and "does well on my work" make the leaderboard a weak proxy for your decision.

The answer is an eval suite of your own. It is unglamorous, it takes a weekend, and it is the single highest-leverage thing in Stage 4 — because it converts an endless stream of vibes-based tool decisions into measurements.

★ **If you cannot measure whether a change to your setup helped, you are not engineering your workflow — you are decorating it.**

### Outcomes
- Build a personal eval suite of golden tasks from your own work
- Run a controlled comparison of models, prompts, or workflows
- Read public benchmarks correctly: what they do and do not tell you

### Core content

**Golden tasks.** 10–20 tasks drawn from your actual history, each with: a starting commit, the brief exactly as you would write it, an automated success check where possible, and a rubric where not. Span the range — trivial, medium, hard, and at least two you know models currently fail. **The failures are the most informative entries**, because they are where a new model's improvement will first show up.

**Scoring.** Prefer automated (tests pass, build succeeds, benchmark improves). Where judgment is needed, use a rubric applied by a *different* model than the one under test, and spot-check its judgments yourself — LLM-as-judge is useful and quietly biased toward its own family's style.

**Controlling for variance.** Agent runs are stochastic. A single run tells you almost nothing; run each task 3–5 times and compare distributions, not anecdotes. Most excited claims about a new model being better are within noise. Hold constant everything you are not testing: same harness, same memory file, same repo state.

**What to eval beyond models.** The suite pays off most on *your own* changes: memory file edits, context minimalism vs pre-loading, plan-first vs direct, subagent return formats, verifier strength. These are the knobs you turn weekly and currently turn blind.

**Reading public benchmarks correctly.** They are useful for coarse capability trends and for knowing what to go test yourself. They are not useful for predicting your outcomes. When you see a score, ask: which harness, how many attempts, what scaffolding, is the dataset contaminated, and does the task distribution resemble mine? Current headline numbers live in `STATE-OF-PLAY-2026-09.md` and are deliberately quarantined there because they go stale fastest of anything in this course.

**Regression as a first-class concern.** Models change under you, including within a version. An eval suite run monthly is an early-warning system for silent degradation on the tasks you care about.

### Labs

**L13.1 — Build the suite (⏱ 4 h).** Assemble 10+ golden tasks from your own history with starting commits and success criteria. Include ≥2 known failures.
*Success:* a runnable suite, executable with one command, producing a score.

**L13.2 — Variance study (⏱ 2 h).** Run five tasks five times each on one model. Compute the spread.
*Success:* a variance table and a stated minimum effect size you will believe.

**L13.3 — A controlled comparison (⏱ 2 h).** Compare two models, or two of your own configurations, holding everything else constant. Report results with the variance caveat applied.
*Success:* a comparison with a conclusion that respects your minimum effect size — including "no detectable difference," which is a real and common result.

**L13.4 — Eval your memory file (⏱ 2 h).** Run the suite with your memory file and without it. Then with the trimmed version from L5.2.
*Success:* three scores and a decision about what actually earns its context.

### Evidence of mastery
A runnable suite with ≥10 tasks, a variance table with a minimum effect size, one controlled comparison, and a memory-file eval that changed a decision.

### Common failure modes
Benchmarks instead of your own tasks. Single runs. Changing two things at once. Building 50 tasks and never running them. No known-failure tasks, so improvements are invisible.

### Reading
[R-130] benchmark landscape, critiques, and harness-vs-model scoring effects · [R-131] eval tooling

---

## M14 — Building Harnesses & Agent Systems

⊢ M1, M5 · ⏱ 10–14 h

### Why this module exists

M1 built a toy. This module takes it to the point where you could actually use it — and, more importantly, to the point where you can reason about any harness's design decisions, extend a commercial one meaningfully, and build purpose-specific agents for your own workflows.

The practitioner justification is concrete: the most valuable agents you will run are often the small specific ones nobody will build for you — a release-note writer that knows your conventions, an incident triager wired to your logs, a migration agent for your particular framework version.

Keep a strategic caution in view, from Steinberger, who is as well-placed as anyone to judge it: specialized harnesses are *"temporary solutions that will converge toward primary model capabilities."* Build harness features to solve today's problem, not as a durable moat.

★ **Build agents for the workflows only you have. Buy the general harness.**

### Outcomes
- Extend a hand-built agent with compaction, subagents, permissions, and persistence
- Design tools and their results for context efficiency
- Decide build-vs-extend-vs-buy deliberately

### Core content

**Tool design, seriously.** The tool layer is the agent's entire interface to reality, and result design matters more than call design. Principles: return the minimum that supports the next decision; make errors actionable ("file not found: did you mean X?") rather than terminal; truncate with an explicit marker and a way to get more; prefer one flexible tool over twelve narrow ones (tool definitions cost context and choice confuses); make side-effecting tools distinguishable from read-only ones so a permission layer can be mechanical.

**Compaction, implemented.** Trigger at a threshold *you* set, not at exhaustion. Preserve the M5 list: goal, approach, completed steps, current failure state, critical paths, rejected approaches with reasons. Write the artifact to disk, not just into the message list, so it survives the process.

**Subagent architecture.** Decide: what context does the child start with (fresh, or forked from the parent)? What does it return, in what shape? Can it spawn children (depth limits matter)? How are failures propagated? The compression ratio — tokens read ÷ tokens returned — is the metric that tells you whether a subagent is earning its overhead.

**Permissions and policy.** Classify tools by side effect; allowlist the provably safe; escalate the rest; log everything. This is M12's architecture expressed in code, and building it once teaches you what commercial permission systems are actually doing.

**Persistence and resumption.** Session state on disk; resume from a state file; idempotent operations so a resumed run does not double-apply. This is what separates a demo from something you would let run overnight.

**Orchestration patterns.** Sequential pipeline; fan-out/fan-in; supervisor-worker; debate or redundant-and-pick. Each has a cost profile and a failure mode. The pattern to reach for first is almost always the simplest one that has a separate verifier in it.

**Build vs extend vs buy.** *Extend* when your harness has the seam (skill, hook, subagent, plugin) — this is right ~80% of the time. *Build* when you need an agent embedded in your own product, an unusual loop shape, or full control of context. *Buy* the general-purpose coding harness; you will not out-engineer a funded team on the common path, and the ground moves monthly.

### Labs

**L14.1 — Production-ish agent (⏱ 5 h).** Extend your M1 agent with: threshold-triggered compaction writing to disk, a subagent tool with a specified return format, a permission layer with an allowlist, and resumable session state.
*Success:* it completes a multi-hour task across a compaction boundary and survives a restart.

**L14.2 — Tool result design (⏱ 2 h).** Instrument your agent to log tokens per tool result. Find the worst offender and redesign it. Re-measure.
*Success:* a before/after token profile with a measured reduction and no loss of capability.

**L14.3 — Build a workflow agent (⏱ 3 h).** Build one small specific agent for a real recurring task of yours. Use it for a week.
*Success:* the agent, plus a week's usage notes and an honest keep/kill decision.

**L14.4 — Orchestration comparison (⏱ 2 h).** Implement the same non-trivial task as a sequential pipeline and as fan-out/verify. Compare cost, wall-clock, and quality.
*Success:* a comparison with a stated rule for which to use when.

### Evidence of mastery
An extended agent surviving compaction and restart, a tool-result token improvement, one workflow agent with a keep/kill decision, and an orchestration comparison.

### Common failure modes
Rebuilding a commercial harness. Too many narrow tools. Compaction that loses the failure state. Subagents with unspecified returns. No persistence, so nothing can run long.

### Reading
[R-10] Ball · [R-140] agent SDK documentation · [R-50] Anthropic context engineering · [R-141] orchestration patterns

---

## M15 — Teams, Orgs & Comprehension Debt

⊢ M12, M13 (Gate 3) · ⏱ 6–8 h

### Why this module exists

Individual mastery does not survive contact with a team that has none. DORA's 2026 analysis is the best available evidence on what happens at organizational scale, and it says three things worth internalizing:

1. **AI amplifies the existing system.** Strong organizations get stronger; dysfunctional ones get more dysfunctional, faster. The tool is not the variable.
2. **There is a J-curve.** An initial productivity dip precedes gains — the "tuition cost of transformation": learning, the verification tax, and downstream process adaptation. Teams that abandon during the dip conclude the tools don't work.
3. **There is an instability tax.** Individual effectiveness rises while delivery stability *falls* — change failure rates drift up. Throughput without stability is not delivery.

Reported gains are also strongly task-dependent: substantial on simple, well-understood work and markedly smaller on complex legacy code. A rollout that promises uniform gains will fail publicly in exactly the codebases that matter most.

★ **The bottleneck moves to review, integration, and understanding. Plan for the bottleneck you are creating.**

### Outcomes
- Diagnose where agent adoption will bind in a specific team
- Design review and quality processes for high-volume agent output
- Manage comprehension debt as an explicit organizational liability

### Core content

**Find the new bottleneck.** Map your team's flow and ask where work will pile up when generation triples. It is almost always review, then integration, then deployment confidence. Investment should go to the bottleneck — faster CI, better automated review, trunk hygiene, deployment safety — not to more generation capacity.

**Reviewing at volume.** Layered defence: automated review first (mechanical issues, conventions, security patterns); human attention reserved for the risk-ordered list from M4; policy-based auto-merge for classified low-risk categories; and a hard rule that **the author reviews their agent's output before it reaches a colleague.** Sending unreviewed agent output to a human reviewer moves your comprehension debt onto someone else's balance sheet, and teams notice.

**Comprehension debt at team scale.** Individual comprehension debt (M4) becomes organizational risk when nobody on the team understands a subsystem. Countermeasures: ownership that means comprehension, not just a CODEOWNERS line; incident-driven repayment (after any incident, someone reads the subsystem properly); architectural decision records so intent survives even when line-level understanding doesn't; and plan/research artifacts in-repo (M6) as the durable record of why.

**Juniors.** The genuine hard problem, unresolved. The traditional apprenticeship ran through exactly the work agents now do. If your team does not deliberately construct learning paths — reviewing agent output with a senior, building understanding before speed, doing some work by hand on purpose — you will produce engineers who can prompt and cannot debug. State your position explicitly; drifting into a default here is how teams end up with a capability cliff in three years.

**Shared assets.** Memory files, rules, skills, and hooks belong in version control and in review. A team memory file is a living style guide that agents actually follow — higher-leverage than a wiki page nobody reads. Update it as part of code review: when a reviewer corrects something twice, that correction becomes a rule.

**Rollout that survives the J-curve.** Start with a willing team on a well-understood codebase; measure honestly with DORA metrics *including stability*; expect the dip and say so in advance; invest in the bottleneck; and expand on evidence. Promising uniform speedups is how pilots get cancelled in month three.

### Labs

**L15.1 — Bottleneck analysis (⏱ 2 h).** Map your team's flow from idea to production. Identify where a 3× generation increase binds. Quantify current capacity at that stage.
*Success:* a flow map with a quantified bottleneck and a proposed intervention.

**L15.2 — Team memory file (⏱ 2 h).** Create or overhaul a shared, version-controlled memory file. Derive its contents from real review comments in your repo's history, not from opinion.
*Success:* a merged file whose every rule traces to ≥2 historical review comments.

**L15.3 — Review policy (⏱ 2 h).** Draft a team policy for agent-generated code: what must be human-reviewed, what can auto-merge, what the author must do before requesting review. Circulate for real feedback.
*Success:* a written policy plus documented colleague feedback and a revision.

**L15.4 — Debt register (⏱ 1.5 h).** Build a comprehension-debt register for your team's codebase: subsystem, owner, comprehension level, last-read date, risk. Schedule repayment for the top item.
*Success:* a register with ≥10 entries and one repayment completed.

### Evidence of mastery
A quantified bottleneck analysis, a merged evidence-derived team memory file, a circulated review policy with feedback, and a debt register with one repayment.

### Common failure modes
Rolling out tools without moving the bottleneck. Promising uniform gains. Ignoring stability metrics. No plan for juniors. Memory files that are opinion rather than evidence.

### Reading
[R-03] DORA 2026 ROI report · [R-04] DORA 2025 State of AI-assisted Software Development · [R-101] comprehension debt · [R-151] field observations from consulting practice

---

## M16 — Capstone C, Doctrine & Continuous Practice

⊢ M15 (all) · ⏱ 20–30 h (Capstone C runs a week)

### Why this module exists

The half-life of specific technique in this field is short. The half-life of judgment is long. This module converts everything you did into two durable things: a **doctrine document** that states what *you* believe and why, and a **practice** that keeps it current after the course ends.

★ **The deliverable of this course is not a skill set. It is a method for acquiring skill sets faster than they expire.**

### Content

**Capstone C — Operate an autonomous loop for a week.** Brief in `ASSESSMENT.md`. Real work, real risk, real logs, including everything that went wrong. Prerequisites M10 and M12 are enforced.

**The doctrine document.** 1,500–3,000 words, written by you, structured as:
1. **What I believe now** — your positions on the contested questions, with your evidence
2. **What I changed my mind about** — compared against `ase/beliefs-2026.md` from M0, quoted
3. **My verification stack** — what checks my work at each rung, honestly
4. **My autonomy policy** — what I let run unattended, what I never will, why
5. **Where I disagree with the experts** — at least three specific, argued disagreements
6. **What I am still bad at** — the most valuable section, and the one people skip
7. **My refresh practice** — how this document stays alive

**Re-run the M0 measurements.** Same task types, same log. Compare. Report honestly, including any regression. Some practitioners get *slower* at certain task classes while getting much faster overall — that is a real and useful finding, not a failure.

**The continuous practice.** Adopt all four:
- **Monthly:** run the eval suite (M13). Watch for silent regressions.
- **Monthly:** one Practitioner Teardown (`PRACTITIONER-DOSSIER.md`). One expert, one claim, one experiment.
- **Quarterly:** re-audit the always-on context and the extension kit; delete what stopped earning its place.
- **Quarterly:** refresh `STATE-OF-PLAY`. It is designed to be refreshed in an afternoon.

**Teach it.** The strongest evidence of mastery is that someone else got better because of you. Pair with a colleague, write up one technique, or run an internal session. If you cannot explain why a technique works in terms of the verification gap, you have not finished learning it.

### Evidence of mastery
Capstone C complete with an incident log; the doctrine document; re-run M0 measurements with an honest comparison; a scheduled continuous practice; and one teaching artifact.

### Reading
Your own `ase/log.md` and `ase/beliefs-2026.md`. Re-read `PRACTITIONER-DOSSIER.md` §Disagreement Map and decide where you now stand.

---
---

## Appendix A — Module dependency graph

```
M0 ──► M1 ──► M2
        │      │
        ├──────┴──► M3 ──► M4 ──► [GATE 1 + Capstone A]
        │                            │
        ├──► M5 ◄─────────────────────┘
        │     ├──► M6  (needs M4)
        │     ├──► M8
        │     └──► M14 (also needs M1)
        └──► M7  (needs M3)
                   │
     [GATE 2 + Capstone B] ◄── M5,M6,M7,M8
                   │
                   ├──► M9 ──┐
                   │          ├──► M10 (also needs M12) ──► M11
                   ├──► M12 ──┘
                   │
              [GATE 3] ──► M13 ──► M14 ──► M15 ──► M16
```

Hard ordering constraints (do not reorder):
- **M12 before unattended work in M10/M11.** Autonomy after safety.
- **M3 before M4.** You cannot review well without knowing what verification already covered.
- **M3 before M9.** Parallel unverified agents are a volume problem, not a leverage gain.
- **M0 before everything.** No baseline, no evidence.

## Appendix B — Time budget

| Stage | Modules | Hours | Cumulative |
|---|---|---|---|
| 0 Calibration | M0 | 5 | 5 |
| 1 Operator | M1–M4 + Capstone A | 34 | 39 |
| 2 Engineer | M5–M8 + Capstone B | 47 | 86 |
| 3 Orchestrator | M9–M12 | 34 | 120 |
| 4 Architect | M13–M16 + Capstone C | 48 | 168 |

Total ≈ 120–170 hours depending on lab depth and how much you do on real work (which takes longer and teaches more). Working 10 h/week: about four months. Full-time intensive: five to six weeks.
