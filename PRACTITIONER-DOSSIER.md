# Practitioner Dossier

**Version 1.0 · Compiled 2026-09-17 · All claims sourced; see `RESOURCES.md` for URLs**

This file exists because the fastest route to expertise in a young field is to study people who are demonstrably good at it — and because they disagree, which is where the actual learning lives. Read this as a set of **hypotheses attached to names**, never as authority. The Teardown protocol below is how you convert a name into a measurement.

> **A warning that matters.** Every practitioner here operates in a specific context: their codebase, their language, their risk tolerance, their revert cost, their financial ability to burn tokens. Techniques do not transfer context-free. The most common failure in this field is copying an expert's *behaviour* without their *substrate* — imitating "I don't read code" without building the verification stack that makes it survivable.

---

## Part 1 — The Practitioner Teardown Protocol

Do this at least six times during the course, and monthly afterwards (M17).

**Step 1 — Find a primary source.** Their words: a post, a talk, a repo, a transcript. Not a summary of them, not a thread about them. Secondary sources reliably drop the caveats, and the caveats are where the transferability lives.

**Step 2 — Extract the claim, precisely.** One sentence, falsifiable. "Steinberger asks for tests in the same session as the implementation because the model still holds the implementation reasoning in context." Not "Steinberger is big on tests."

**Step 3 — Locate the verification mechanism.** The course's central question: *what closes the verification gap here?* If a practice looks reckless, the verifier is usually somewhere you haven't looked — fast reverts, preview deploys, atomic commits, a separate reviewing agent. If you genuinely cannot find one, you have found either a bad practice or an undisclosed one. Say which you think it is.

**Step 4 — Identify the context dependencies.** What must be true for this to work? Codebase size and age, language, test quality, revert cost, team size, review requirements, budget, personal risk tolerance. Write them down. Then check which you have.

**Step 5 — Design the cheap experiment.** Smallest version that could falsify it in your context. Three tasks, one afternoon, one metric from M1.

**Step 6 — Run it and record.** In `ase/log.md`. Prediction first, then result.

**Step 7 — Keep, adapt, or discard — in writing.** "Adapted: same-session tests work for me on features but not on bug fixes, where the reproduction case is the better artifact." Adaptations are the real output; unmodified adoption usually means you didn't test it.

---

## Part 2 — The practitioners

> **These entries are dated snapshots.** Everyone here can change their mind, and the practitioners worth
> studying are often the ones revising in public — DHH has moved twice in eighteen months, and Boris Cherny's advice
> on plan mode inverted across model generations. Each entry carries an **As of** stamp. If one is a few months
> behind, that is normal and not much of a problem; check the person's current writing before quoting them at
> anyone, and if you find a real divergence, it is worth folding back in (`MAINTENANCE.md` §4).

### Peter Steinberger — “steipete” — *maximum throughput, minimum ceremony*

**As of — 2025-12-28 (*Shipping at Inference-Speed*); role updated 2026-02.**

**Follow:** [Blog](https://steipete.me/) · [X](https://x.com/steipete) · [GitHub](https://github.com/steipete)

**Who:** Founder of PSPDFKit; became one of the most visible high-volume agentic practitioners in 2025 through relentless public documentation of his workflow; creator of open-source agent tooling; joined OpenAI in February 2026 to work on agents, stating his mission as *"build an agent that even my mum can use."*

**Doctrine.** Ceremony is waste. Model intuition beats process. Run many agents, commit atomically, refactor continuously, and let verification live in the loop rather than in your eyeballs.

**Specifics worth stealing:**
- **Blast-radius assessment before launching** — file count and duration estimated up front, determining everything downstream (M3)
- **Same-session tests** — ask for tests immediately after implementation, in the same context, for better tests and bugs caught during writing (M4)
- **3–8 parallel agents in a terminal grid**, same folder, atomic commits, no worktrees — optimizing for latency over isolation (M10)
- **~20% of time on refactoring, performed entirely by agents** — duplicate detection, dead-code removal, deprecation sweeps (M8)
- **Screenshots over prose** — roughly half his prompts include an image (M3)
- **A large, agent-maintained `Agents.md`** (~800 lines for a ~300k-line codebase) that agents update as patterns emerge (M6)
- **Custom CLIs over MCP servers** — the knowledge is already in the weights; a heavyweight integration can cost tens of thousands of context tokens (M9)
- **Language choice for agent compatibility** — TypeScript, Go, Swift (M8)

**Quotes:** *"These days I don't read much code anymore. I watch the stream and sometimes look at key parts."* · *"I basically never revert or use checkpointing. If something isn't how I like it, I ask the model to change it."* · *"Fighting the model is often a waste of time and tokens."* · *"Most software does not require hard thinking."* · *"You shouldn't be prompting coding agents anymore. You should be designing loops that prompt your agents."*

**Read critically.** His substrate is unusual and largely undisclosed in the headline claims: a codebase he wrote and knows completely, two-minute preview deploys, atomic commits with trivial revert, very high token budget, no external review requirement, and consumer-product risk rather than financial or safety-critical risk. *"I don't read code"* is the conclusion of that stack, not a technique you can adopt directly. Also note the strategic claim that specialized harnesses will converge into model capabilities — plausible, self-interested given his employer, and unfalsifiable on any useful timescale.

**Teardown targets:** same-session tests (cheap, high value, transfers widely) · same-folder parallelism (test before adopting — it fails badly with slow builds) · the 20% agent refactoring budget (transfers well, needs M4 verifiers first)

---

### Boris Cherny — “Boris” — *delegation, verification, and the extension surface*

**As of — 2026-06 (latest tips in the compiled index).**

**Follow:** [X](https://x.com/bcherny) · [Blog](https://borischerny.com/) · [GitHub](https://github.com/bcherny) · [Tips compilation (fan-run)](https://howborisusesclaudecode.com/)

**Who:** Creator and head of Claude Code at Anthropic — briefly departed to Cursor in late 2025 and returned within two weeks. As of early 2026 he reported Claude Code representing ~4% of public GitHub commits. He publishes practical tips continuously, which makes him unusual: you can watch his advice *change* as models improve, which is itself instructive.

**Doctrine.** Treat the agent as an engineer you delegate to, not a pair programmer you guide. Verification is the highest-leverage investment. Convert corrections into durable rules rather than repeating them.

**Specifics worth stealing:**
- **Verification above all** — give the agent a way to check its output (browser, tests, simulator); he attributes a 2–3× quality difference to this (M4)
- **Worktrees as "the single biggest productivity unlock"**, 5+ concurrent sessions, named and colour-coded (M10)
- **Full-context briefs** — goal, constraints, acceptance criteria — and delegation framing (M3)
- **Rules, not corrections** — when the agent errs, write the fix to the memory file or a skill so it never recurs (M3, M9)
- **Rewind rather than correct**, to keep failed attempts out of context (M3, M6)
- **Extension surface used deliberately** — post-edit hooks for formatting, subagents for review and verification, slash commands for repeated workflows, sandboxing to reduce permission prompts *and* increase safety (M9)
- **Voice input** — *"you speak 3x faster than you type"*; he reports doing most of his coding by speaking (M3)
- **Mobile and session portability** — start on a phone, continue on a desktop, schedule cloud jobs (M12)
- **Context minimalism** — as models improved, he moved toward minimal system prompt and tool list, letting the model fetch what it needs (M6)

**Watch the drift, it's the lesson.** His advice on plan mode inverted across model generations — first "always start in plan mode and refine," later "skip it, newer models plan implicitly." This is the single best illustration in the dossier of why **technique is model-dependent and must be re-tested rather than believed** (M14). When you read any tip from any practitioner, ask which model generation it was formed on.

**Read critically.** He is the creator of a specific harness and his advice is naturally shaped by its feature set; much of it generalizes, some of it is product-specific. Anthropic's internal environment — exceptional test infrastructure, unlimited quota, colleagues who built the tool — is not most people's.

**Teardown targets:** verification-first briefing (highest value in the dossier) · worktrees vs same-folder (run against Steinberger's claim directly) · rules-not-corrections (cheap, compounding)

---

### Andrej Karpathy — “Karpathy” — *the conceptual frame, and the honest limits*

**As of — 2026-03-20 (No Priors).**

**Follow:** [Blog](https://karpathy.bearblog.dev/) · [YouTube](https://www.youtube.com/@AndrejKarpathy) · [X](https://x.com/karpathy) · [GitHub](https://github.com/karpathy)

**Who:** Co-founder of OpenAI, former director of AI at Tesla, founder of Eureka Labs. Coined "vibe coding" (February 2025) and has spent the time since refining and partly disowning the popular reading of it. Author of the *Software 2.0* essay and the *Software Is Changing Again* / Software 3.0 framing. His teaching repos — micrograd, nanoGPT, llm.c, nanochat — are the best available route to understanding what is under the agent.

**Doctrine.** Autonomy is a slider, not a switch. Set it by how well the task can be verified. Remove yourself as the bottleneck where verification is objective; stay in the loop where it is not.

**Specifics worth stealing:**
- **The autonomy slider** — calibrate delegation to verifiability, per task, not per tool (M11, and the spine of the whole course)
- **"Remove yourself as the bottleneck… arrange things such that they're completely autonomous"** — with the precondition stated: *"you just have to arrange it so that it can just go forever"*, which requires an objective metric (M11)
- **Leverage framing** — *"I put in just very few tokens just once in a while and a huge amount of stuff happens"* (M11)
- **The loopy era** — nested optimization: models → agents → orchestration → optimization over the instructions themselves (M11, M15)
- **AutoResearch as proof of the pattern** — an overnight loop on his own nanoGPT work found hyperparameter improvements he had missed over two decades, *because the metric was objective and automatable*
- **Jaggedness, stated honestly** — agents excel on verifiable metric-driven tasks and remain weak on *"nuance of maybe what I had in mind or what I intended and when to ask clarifying questions"*

**On vibe coding.** He coined it to describe a specific, deliberately low-stakes mode — giving in to the vibes, not reading the diffs, fine for throwaway weekend projects. Its adoption as a label for professional practice is a misreading he has pushed back on. In this curriculum, vibe coding is a *legitimate mode for disposable work* and a *category error for anything maintained*. Kent Beck's "augmented coding" is the professional counterpart.

**Read critically.** He works on research code with clean objective metrics, which is the most favourable possible terrain for autonomy — most software engineering has no equivalent of validation loss. His reports of not having typed code since December 2025 describe that terrain. His timeline predictions (a "decade of agents") are explicitly speculative and he says so.

**Teardown targets:** the autonomy slider applied per-task in your own work · metric-driven optimizer loops on something you can actually measure (performance work, bundle size, flaky-test rate)

---

### David Heinemeier Hansson — “DHH” — *the documented mind-change, twice*

**As of — 2026-08-26 (Lex Fridman #501).**

**Follow:** [Blog](https://world.hey.com/dhh) · [X](https://x.com/dhh) · [YouTube](https://www.youtube.com/@dhh37) · [Podcast (REWORK)](https://37signals.com/podcast/)

**Who:** Creator of Ruby on Rails, CTO of 37signals. The value of studying him is partly the content and
substantially the worked example of **updating on evidence in public, repeatedly.**

**The arc, which is the point.** Autocomplete-era assistants he found *"genuinely annoying for experienced
developers."* By January 2026 he was writing that agents had crossed a threshold — the change being that models
gained *"the tools to take their capacity beyond pure reasoning."* By April 2026 he was running a fast model and a
powerful model in parallel terminal splits and **reviewing every diff before merge.** By August 2026 he had gone
considerably further: on his Omarchy Quattro project he reports *"I have not written any of the code that's shipped
in Quattro by hand"* across two months.

**His current review discipline — and note what it is not.** He has not stopped reviewing. He has made review
**risk-tiered**:

> *"I've reviewed the shape of all of it. I've reviewed the individual lines of anything that critical in the model
> layer of the system, and I've not looked at a bunch of the UI code."*

Read that against M5. Shape everywhere; lines where the risk concentrates; nothing where it doesn't. That is
**risk-ordered reading**, arrived at independently by someone with very high standards who spent a year resisting
the whole idea. It is the strongest available evidence that M5's triage is the position experienced engineers
converge on under real volume — and it is emphatically *not* "stopped caring about the code."

**Specifics worth stealing:**
- **Risk-tiered review** — architectural shape always; line-by-line in the layers where being wrong is expensive; skip where it isn't (M5)
- **Multi-model workflow** — a fast model and a powerful model in parallel terminal splits, editor at the centre, a dedicated diff-review tool (M10)
- **Aesthetics as a correctness signal** — *"When something is beautiful, it's likely to be correct"* (M5, with the caveat that agent output is often superficially beautiful and conceptually wrong)
- **Conventions as machine-readable interface** — his argument that Rails is enjoying a renaissance partly because convention-over-configuration is *token-efficient* for agents, and its integrated testing lets agents self-validate. Generalizes far beyond Rails: **the more your codebase looks like the idiom the model already knows, the less context you spend explaining yourself** (M8)

**Read critically.** He works in a mature, conventional, heavily-tested codebase in a framework saturated in
training data — close to the best case. Omarchy Quattro is also his own project, on his own risk tolerance, with no
external review requirement; "I haven't hand-written any of it" is a claim about a context most readers don't share.
And note the meta-lesson: he has moved twice in eighteen months. A position held firmly can still be wrong,
including the current one.

### Dex Horthy — “Dex” — *upstream review and intentional compaction*

**As of — 2026-09-17 (ACE-FCA as published).**

**Follow:** [Blog](https://www.humanlayer.dev/blog) · [X](https://x.com/dexhorthy) · [YouTube](https://www.youtube.com/@humanlayerdev) · [GitHub](https://github.com/humanlayer)

**Who:** Founder of HumanLayer; author of the 12-Factor Agents framework and *Advanced Context Engineering for Coding Agents* (ACE-FCA). The most rigorous published methodology in the field, with the most specific outcome claims.

**Doctrine.** The context window is the only lever. Design the entire workflow around it. Review research and plans, not code.

**Specifics worth stealing:**
- **Research → Plan → Implement**, with research and plan phases producing reviewable *files* (M7)
- **Frequent intentional compaction**, keeping utilization in the **40–60%** band rather than running to exhaustion (M6)
- **The compaction artifact format** — goal, approach, steps completed, current failure state, critical paths (M6)
- **Review leverage** — *"A bad line of code is a bad line of code. A bad line of a plan could lead to hundreds of bad lines of code. A bad line of research could land you with thousands of bad lines of code."* (M5, M7)
- **Optimization priority: correctness > completeness > size** (M6)
- **Subagents as context firewalls**, with returns shaped like compaction artifacts (M6)
- **Code review as mental alignment** (via Blake Smith) rather than primarily bug-catching (M5)

**Evidence he offers:** a bug fixed in a 300k-line Rust codebase in one session; ~35k lines of cancellation and WASM support in ~7 hours (≈3 research/planning, ≈4 implementation), passing expert maintainer review. He also publishes a **failure** — a Hadoop dependency removal where research didn't map nested dependencies — which raises rather than lowers his credibility.

**Read critically.** The process has real overhead and is genuinely wrong for small or exploratory work. The headline results involve deep human engagement and codebase expertise, which the method amplifies rather than replaces. Results are self-reported.

**Teardown targets:** the 40–60% utilization band (easy to test, immediately felt) · plan-review-only on one substantial change · the compaction artifact format (cheap, works everywhere)

---

### Kent Beck — *tests as the binding constraint*

**As of — 2026-09-17 (newsletter, ongoing).**

**Follow:** [Newsletter](https://newsletter.kentbeck.com/) · [X](https://x.com/KentBeck) · [YouTube](https://www.youtube.com/@kentbeck) · [Site](https://kentbeck.com/)

**Who:** Creator of extreme programming and modern TDD; author of *Tidy First?*. Has been publishing sustained experiments in working with agents since 2025 under the banner **"augmented coding."**

**Doctrine.** *"In augmented coding you care about the code, its complexity, the tests, & their coverage… The value system is similar to hand coding — tidy code that works. It's just that I don't type much of that code."*

**Specifics worth stealing:**
- **Augmented coding vs vibe coding as a value distinction**, not a tooling one (M4)
- **TDD as the agent's stop condition** — find the next unimplemented test, implement it, write only enough code to pass, stop (M4)
- **Explicit red flags to watch for:** loops, unrequested functionality, tests being disabled (M4's anti-gaming catalogue)
- **Separate structural from behavioural commits** — reviewable sequences instead of monoliths (M4, M5)
- **Programming as decision-making rather than typing** — the cleanest one-line statement of the whole shift

**Read critically.** TDD has real costs and real critics, and agents make some of those costs worse (they will happily generate large tautological suites). Beck's own framing is exploratory and he revises it publicly.

**Teardown targets:** the TDD stop-condition prompt pattern · the red-flag list as an explicit review checklist

---

### Armin Ronacher — “mitsuhiko” — *design the environment, not the prompt*

**As of — 2026-02-09 (*A Language For Agents*).**

**Follow:** [Blog](https://lucumr.pocoo.org/) · [X](https://x.com/mitsuhiko) · [YouTube](https://www.youtube.com/@ArminRonacher) · [GitHub](https://github.com/mitsuhiko)

**Who:** Creator of Flask, Jinja2, and much of the modern Python ecosystem; publishes unusually candid long-form on agentic coding, including what did *not* work.

**Doctrine.** Agents reason locally. Codebases and languages that support local reasoning get better results, and this is a more durable investment than any prompting technique.

**Specifics worth stealing:**
- **What agents want:** explicit types over inference, greppability (Go's package-qualified references as the model), explicit dependencies, braces over significant whitespace, result types over exceptions, boring conventional structure (M8)
- **What agents hate:** macros and codegen, barrel files and re-exports, import aliasing, flaky tests, environment divergence (M8)
- **The core insight:** *"Agents really like local reasoning… they often work with just a few loaded files in context and don't have much spatial awareness of the codebase."*
- **MCP scepticism from practice** — a year of use left him finding it underperformed relative to simpler mechanisms (M9)
- **Publishing failures explicitly** — his "things that didn't work" writing is more useful than most success reports

**Read critically.** He is speculating publicly about languages designed for agents; interesting, too early to act on. His preferences are shaped by systems programming and infrastructure work.

**Teardown targets:** greppability repair with before/after measurement · the flaky-test purge (unglamorous, large effect) · MCP cost/benefit on your own setup

---

### Geoffrey Huntley — “ghuntley” — *the loop, in its rawest form*

**As of — 2026-01 (Ralph retrospective).**

**Follow:** [Blog](https://ghuntley.com/) · [X](https://x.com/GeoffreyHuntley) · [YouTube](https://www.youtube.com/@GeoffreyHuntley) · [GitHub](https://github.com/ghuntley)

**Who:** Engineer who popularized the "Ralph" technique in 2025 — an agent loop reduced to its essentials — and pushed it to deliberately absurd extremes to find where it breaks, including generating a programming language with it.

**Doctrine.** A fresh context working from a durable specification, repeated, beats one long context working from memory. The bash is trivial; the spec is everything.

**Specifics worth stealing:**
- **The minimal loop** — spec file piped to an agent, repeatedly, each iteration fresh (M11)
- **Specs as the source of truth**, with code as the regenerable artifact (M7, M11)
- **Empirical extremism as method** — run it until it breaks, then report what broke

**Read critically.** Ralph is cheerfully presented as a dumb technique that works, and its documented failure modes are serious: bad specs amplified hundreds of times; overbaking (loops that run past their useful life start inventing work, in one recorded case unexpected cryptography features); poor merge-conflict behaviour; and unsuitability for exploration. Practitioners including Horthy warn that the term has diffused semantically — people now call anything automated "a Ralph."

**Teardown targets:** one minimal loop on genuinely mechanical work · deliberately inducing overbaking so you recognise it in the wild

---

### Thorsten Ball — *demystification*

**As of — 2026-09-17 (the tutorial is stable).**

**Follow:** [Newsletter](https://registerspill.thorstenball.com/) · [Podcast (Raising an Agent)](https://ampcode.com/podcast) · [X](https://x.com/thorstenball) · [Site](https://thorstenball.com/)

**Who:** Author of *Writing an Interpreter in Go*; worked on Amp at Sourcegraph. His *How to Build an Agent* is the single most valuable technical artifact in this dossier for a practitioner.

**Doctrine.** An agent is an LLM, a loop, and enough tokens. Under 400 lines. The mystique is the main obstacle to using them well.

**Why it matters here:** M2 is built on this. Once you have written the loop, every downstream concept — context engineering, compaction, subagents, harness design — is a variation you can reason about rather than a feature you must trust.

**Teardown target:** build it, then break it deliberately (L2.2)

---

### Addy Osmani — *the 2026 synthesis*

**As of — 2026-09-17 (*Loop Engineering*).**

**Follow:** [Blog](https://addyosmani.com/blog/) · [Newsletter](https://addyo.substack.com/) · [X](https://x.com/addyosmani) · [YouTube](https://www.youtube.com/@addyosmani)

**Who:** Engineering leader at Google, prolific writer on AI-assisted engineering; among the clearest explainers of the 2026 shift to loop engineering.

**Specifics worth stealing:**
- **Loop engineering defined:** *"replacing yourself as the person who prompts the agent. You design the system that does it instead."* (M11)
- **The five loop components:** automations, isolation (worktrees), knowledge (skills), connections, and separate verification sub-agents — plus persistent state, *"since the model forgets everything between runs"* (M11)
- **The three failure modes:** verification risk (unattended mistakes go unseen), **comprehension debt** (the gap between shipped and understood), and cognitive surrender (accepting output uncritically) (M5, M11)
- **The neutrality point:** *"Two people can build the exact same loop and get completely opposite results"* — the loop is neutral; what differs is whether it accelerates understanding or avoids it

**Teardown target:** audit one of your loops against all five components; the missing one is usually verification

---

### Also worth following

**Simon Willison** — the field's most reliable running documentation, and the author of the **lethal trifecta** framing that M13 is built on. If you follow one person for breadth, follow him.
**Mitchell Hashimoto** — creator of Terraform and Ghostty; a careful, sceptical, high-standards practitioner working on a real systems codebase. The useful counterweight to enthusiasm.
**Steve Yegge** — "Revenge of the Junior Developer," the *Vibe Coding* book with Gene Kim, agent-fleet framing. Loud, early, often right about direction and wrong about timing.
**Birgitta Böckeler / Thoughtworks** — field observations from consulting engagements across many client codebases; the best available corrective to single-practitioner survivorship bias.
**Gene Kim** — brings the DevOps analytic tradition to agentic work; useful at the org level (M16).
**Sean Grove** — *The New Code*: the argument that the specification, not the code, is the durable artifact (M7).
**Martin Fowler's site** — slow, careful, well-edited writing in a field of hot takes.

---

## Part 3 — The Disagreement Map

Where the experts actually conflict. Each row is a real decision you must make; the course's position is stated so you can disagree with it deliberately.

| Question | Position A | Position B | Course position |
|---|---|---|---|
| **Read the generated code?** | DHH (Aug 2026): review the *shape* of all of it, the *lines* only where risk concentrates | Steinberger: watch the stream, read key parts, verify elsewhere | These have converged more than they once diverged — and both land close to M5's risk-ordered triage. Choose your tiers by revert cost, blast radius and criticality, and know your read ratio |
| **Where does review attention go?** | Traditional: the diff | Horthy: research and plan; the diff is downstream | Upstream review has better leverage on large changes; diff review remains mandatory on security, money, and data. Do not substitute one for the other |
| **How much process?** | Horthy: heavy, structured, artifact-producing | Steinberger: minimal, intuition, just talk to it | Scale process to blast radius (M3). Both camps fail when they apply their default to the other's territory |
| **Worktrees or same folder?** | Cherny: worktrees, the single biggest unlock | Steinberger: same folder, atomic commits, speed | Situational. Test both (L10.1). Slow builds and coupled work push you to worktrees; fast small edits tolerate same folder |
| **Is TDD necessary?** | Beck: tests are the constraint that makes agents safe | Steinberger: tests yes, TDD ceremony no | A verifier is mandatory; *TDD* is one strong implementation. Never accept zero verification |
| **MCP: infrastructure or bloat?** | Vendors: the standard for tool connection | Ronacher, Steinberger: underperforms; prefer CLIs | Use it for live connection, auth, and actions. Measure its context cost. Prefer CLIs the model already knows (M9) |
| **Big memory file or minimal context?** | Steinberger: ~800 lines, agent-maintained | Cherny (recent): context minimalism, let the model fetch | Model-dependent and codebase-dependent. This is exactly what an eval suite is for (M14) |
| **Can agents work unattended?** | Karpathy: yes, where the metric is objective | Sceptics: verification risk makes it irresponsible | Both. Autonomy is licensed by verifiability, per task, not per tool (M11) |
| **Are we faster?** | Practitioners: dramatically | METR 2025: 19% *slower*, while feeling 20% faster | Measure your own (M1). The literature is now structurally unable to answer this for you |
| **What happens to juniors?** | Yegge: revenge of the junior developer | Others: the apprenticeship path is being destroyed | Unresolved. Teams must construct learning paths deliberately or produce engineers who can prompt and cannot debug (M16) |

**How to use this map.** When you hit a decision, find the row, read both positions in their primary sources, identify which context dependencies you share, and run the cheap experiment. Do not resolve these by preference. Resolve them by measurement — and then write the resolution into your doctrine document (M17) with the evidence attached.
