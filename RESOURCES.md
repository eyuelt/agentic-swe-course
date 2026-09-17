# Resource Index

**Version 1.0 · All URLs verified live 2026-09-17 unless marked otherwise.**

Verification history: authored 2026-09-17 against primary sources; independently re-probed the same day from an unrestricted network by `tools/curriculum_lint.py links` — 52 URLs, 0 dead, 1 redirect (R-10, corrected).

**Columns.** `Tier` — ① Core (do not skip) / ② Recommended / ③ Reference.
`Vol` — volatility, i.e. how fast this goes stale: **D** durable (principles, 2+ yr), **M** medium (technique, ~12 mo), **F** fast (tools, models, numbers — ~3 mo).
`✓` — verified reachable on 2026-09-17. `?` — cited from a secondary reference or blocked by the fetcher; confirm before relying on it.

> **Maintainer note:** when refreshing, update the `✓` column first — link rot is the earliest signal of a stale curriculum. `TOOLING.md` §2 specs a linter that does this automatically.

---

## Evidence base — read these before forming opinions

| ID | Resource | Tier | Vol | ✓ | Why it matters |
|---|---|---|---|---|---|
| R-01 | METR, *Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity* (2025-07-10) — `https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/` | ① | D | ✓ | The 19%-slower / 20%-faster-feeling result. The foundational fact about self-assessment. Read the methodology and the caveats, not the headline |
| R-02 | METR, *We are Changing our Developer Productivity Experiment Design* (2026-02-24) — `https://metr.org/blog/2026-02-24-uplift-update/` | ① | M | ✓ | The 2026 update: slowdown narrowed (−18% returning, −4% new, CIs crossing zero) and the study design is breaking because devs now refuse to work without AI. The reason M1 exists |
| R-03 | DORA, *ROI of AI-Assisted Software Development* (2026) — coverage: `https://www.infoq.com/news/2026/05/dora-roi-ai-assisted-dev-report/`; publications index: `https://dora.dev/research/publications/` | ① | M | ✓ | The J-curve, the verification tax, the instability tax, AI-amplifies-the-system. Org-level evidence for M16 |
| R-04 | DORA, *State of AI-assisted Software Development* (2025) — `https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report` | ② | M | ✓ | The prior year's baseline; useful for seeing what changed |
| R-130 | Benchmark landscape and critiques — SWE-bench Pro public leaderboard `https://labs.scale.com/leaderboard/swe_bench_pro_public`; aggregate tracker `https://www.codesota.com/code-generation` | ② | **F** | ✓ | Read for the *caveats*, not the scores. Note that harness choice moves the same base model by double digits. Current numbers are quarantined in `STATE-OF-PLAY` |

## Foundations — what an agent is

| ID | Resource | Tier | Vol | ✓ | Why it matters |
|---|---|---|---|---|---|
| R-10 | Thorsten Ball, *How to Build an Agent* — `https://ampcode.com/notes/how-to-build-an-agent` | ① | D | ✓ | Build the loop in <400 lines. The single highest-value technical artifact in this course. M2 is built on it |
| R-11 | Your harness's own documentation — e.g. `https://code.claude.com/docs/en/features-overview` and the machine-readable index at `https://code.claude.com/docs/llms.txt` | ① | **F** | ✓ | The extension surface, authoritative and current. Re-read after every major release |
| R-12 | Changelog interview with Thorsten Ball on agents — `https://changelog.com/podcast/648` | ③ | M | ✓ | Conversational version of R-10 |
| R-50 | Anthropic, *Effective context engineering for AI agents* — `https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents` | ① | M | ✓ | The canonical vendor-side treatment of context as a budgeted resource. M6 |
| R-81 | *Steering Claude Code: when to use CLAUDE.md, skills, hooks, rules and subagents* — `https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more` | ② | **F** | ✓ | Mechanism-selection guidance; cited from the official docs. M9 |

## Method — the practices

| ID | Resource | Tier | Vol | ✓ | Why it matters |
|---|---|---|---|---|---|
| R-40 | Dex Horthy / HumanLayer, *Advanced Context Engineering for Coding Agents (ACE-FCA)* — `https://github.com/humanlayer/advanced-context-engineering-for-coding-agents/blob/main/ace-fca.md` | ① | M | ✓ | Research→Plan→Implement, intentional compaction, 40–60% utilization, review-the-plan leverage. The most rigorous published methodology. M6 + M7 |
| R-60 | Horthy, *Context Engineering for Complex Codebases* (talk) — `https://ai.engineer/talks/rmvDxxNubIg-context-engineering-for-complex-codebases` | ② | M | ✓ | The talk version, with the worked examples |
| R-63 | *Context engineering with Dex Horthy*, Pragmatic Engineer — `https://newsletter.pragmaticengineer.com/p/context-engineering-with-dex-horthy` | ② | M | ✓ | Interview format; good for the reasoning behind the method |
| R-30 | Kent Beck, *Augmented Coding: Beyond the Vibes* — `https://newsletter.kentbeck.com/p/augmented-coding-beyond-the-vibes` | ① | D | ✓ | The value distinction between augmented and vibe coding; TDD as the agent's stop condition. M4 |
| R-33 | *TDD, AI agents and coding with Kent Beck*, Pragmatic Engineer — `https://newsletter.pragmaticengineer.com/p/tdd-ai-agents-and-coding-with-kent` | ② | M | ✓ | Extended treatment of the same material |
| R-34 | Kent Beck, *Genie Lessons: Nobody Wants Agents* — `https://newsletter.kentbeck.com/p/genie-lessons-nobody-wants-agents` | ③ | M | ✓ | His ongoing experiments; useful for watching a careful mind update |
| R-101 | Addy Osmani, *Loop Engineering* — `https://addyosmani.com/blog/loop-engineering/` | ① | M | ✓ | The clearest definition of the 2026 shift; the five loop components; the three failure modes including comprehension debt. M11 |
| R-100 | HumanLayer, *A Brief History of Ralph* — `https://www.humanlayer.dev/blog/brief-history-of-ralph` | ② | M | ✓ | Origin, mechanics, documented failures (bad specs, overbaking, merge behaviour), and the semantic-diffusion warning. M11 |
| R-103 | Geoffrey Huntley's writing — `https://ghuntley.com/` | ② | M | ✓ | Primary source for Ralph and autonomous loops; verify the specific post before citing |
| R-61 | Spec-driven development toolkits and comparisons (2026) — e.g. `https://www.marktechpost.com/2026/05/08/9-best-ai-tools-for-spec-driven-development-in-2026-kiro-bmad-gsd-and-more-compare/` | ③ | **F** | ✓ | Landscape overview. Treat tool names as perishable; the durable idea is "write intent down before generating" |
| R-62 | Sean Grove, *The New Code* | ② | M | ? | The argument that the spec is the primary artifact. Find the current canonical link |

## Practitioners — primary sources

| ID | Resource | Tier | Vol | ✓ | Why it matters |
|---|---|---|---|---|---|
| R-21 | Peter Steinberger, *Just Talk To It* (2025-10-14) — `https://steipete.me/posts/just-talk-to-it` | ① | M | ✓ | The fullest statement of his workflow: parallel agents, blast radius, same-session tests, screenshots, the Agents.md approach, MCP scepticism |
| R-32 | Steinberger, *Shipping at Inference-Speed* (2025-12-28) — `https://steipete.me/posts/2025/shipping-at-inference-speed` | ① | M | ✓ | *"I don't read much code anymore."* Read it looking for what substitutes for reading — that is the lesson |
| R-23 | Steinberger, *Commanding Your Claude Code Army* (2025-06-05) — `https://steipete.me/posts/2025/commanding-your-claude-code-army` | ② | M | ✓ | Early parallelism practice |
| R-24 | Steinberger, *My Current AI Dev Workflow* (2025-08-25) — `https://steipete.me/posts/2025/optimal-ai-development-workflow` | ② | **F** | ✓ | Snapshot of a full setup; note how much has already changed |
| R-25 | Steinberger, post index — `https://steipete.me/posts` | ③ | **F** | ✓ | Where to check for new material |
| R-26 | Steinberger, *OpenClaw, OpenAI and the future* (2026-02-14) — `https://steipete.me/posts/2026/openclaw` | ③ | D | ✓ | Context on his move to OpenAI; relevant to weighing his claims about harness convergence |
| R-20 | *How Boris Uses Claude Code* — `https://howborisusesclaudecode.com/` **(fan-compiled, not official)** | ① | **F** | ✓ | The most complete collection of Cherny's practical tips, organized by theme and dated. Treat as a secondary source; verify anything load-bearing against his own posts |
| R-27 | Boris Cherny, *Building Claude Code* (YC) — `https://www.ycombinator.com/library/UN-boris-cherny-building-claude-code` | ② | M | ✓ | How the tool was built; the design reasoning behind the extension surface |
| R-28 | *Head of Claude Code: What happens after coding is solved* — Lenny's Newsletter (2026-02-19) — `https://www.lennysnewsletter.com/p/head-of-claude-code-what-happens` | ② | M | ✓ | Cherny on where this goes. Partly paywalled |
| R-42 | DHH, *Promoting AI agents* (2026-01-07) — `https://world.hey.com/dhh/promoting-ai-agents-3ee04945` | ① | D | ✓ | The public position change, in his own words: *"fully capable of producing production-grade contributions"*, and the "supervised collaboration" framing |
| R-43 | *DHH's new way of writing code*, Pragmatic Engineer (2026-04-08) — **superseded in part by R-45** — `https://newsletter.pragmaticengineer.com/p/dhhs-new-way-of-writing-code` | ① | M | ✓ | His actual current workflow: multi-model terminal splits, diff review, beauty-as-correctness, Rails as token-efficient for agents |
| R-44 | *DHH on AI, Vibe Coding and the Future of Programming* — `https://thenewstack.io/dhh-on-ai-vibe-coding-and-the-future-of-programming/` | ③ | M | ✓ | Secondary coverage; useful for the arc |
| R-45 | DHH on Lex Fridman #501 — *Future of Programming, AI, Agentic Engineering, Vibe Coding & Linux* (2026-08-26) — transcript: `https://lexfridman.com/dhh-2-transcript/` · episode: `https://lexfridman.com/dhh-2/` | ① | M | ✓ | His **current** position, and the one that supersedes R-43: risk-tiered review — the shape of all of it, the lines only where risk concentrates. Two months of a real project shipped without hand-writing any of it |
| R-102 | Karpathy, *From Vibe Coding to Agentic Engineering* (Sequoia Ascent 2026) — `https://www.youtube.com/watch?v=96jN2OCOfLs`; his own notes: `https://karpathy.bearblog.dev/sequoia-ascent-2026/` | ① | M | ✓ | The autonomy framing. Both links verified reachable; the notes page blocks automated fetchers, so a linter may flag it — open it in a browser |
| R-104 | Karpathy on *No Priors*: code agents, AutoResearch, the loopy era (2026-03-20) — transcript: `https://podscripts.co/podcasts/no-priors-artificial-intelligence-technology-startups/andrej-karpathy-on-code-agents-autoresearch-and-the-loopy-era-of-ai` | ① | M | ✓ | *"Remove yourself as the bottleneck."* The AutoResearch result. The jaggedness caveat. Third-party transcript — check against the audio for anything load-bearing |
| R-105 | Karpathy, *Software 2.0* (2017) and *Software Is Changing Again* / Software 3.0 (AI Engineer World's Fair, 2025) | ② | D | ? | The conceptual lineage. Find current canonical links; the Medium essay has moved before |
| R-71 | Armin Ronacher, *Agentic Coding Recommendations* (2025-06-12) — `https://lucumr.pocoo.org/2025/6/12/agentic-coding/` | ① | M | ✓ | The practical baseline: tooling, sandboxing, what to automate |
| R-70 | Ronacher, *A Language For Agents* (2026-02-09) — `https://lucumr.pocoo.org/2026/2/9/a-language-for-agents/` | ① | D | ✓ | What agents want from code: explicit types, greppability, local reasoning, braces, result types. The intellectual core of M8 |
| R-73 | Ronacher, *Agentic Coding Things That Didn't Work* (2025-07-30) — `https://lucumr.pocoo.org/2025/7/30/things-that-didnt-work/` | ② | M | ✓ | Negative results, published. Rare and valuable |
| R-52 | Ronacher, *A Year Of Vibes* (2025-12-22) — `https://lucumr.pocoo.org/2025/12/22/a-year-of-vibes/` | ② | M | ✓ | Year-in-review including MCP scepticism and the infrastructure gaps (version control, review, observability) |
| R-74 | Ronacher, AI tag index — `https://lucumr.pocoo.org/tags/ai/` | ③ | **F** | ✓ | Where to check for new material |

## Security

| ID | Resource | Tier | Vol | ✓ | Why it matters |
|---|---|---|---|---|---|
| R-120 | Simon Willison, *The lethal trifecta for AI agents* (2025-06-16) — `https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/` | ① | D | ✓ | Private data + untrusted content + external communication. The clearest security frame in the field. M13 |
| R-121 | Cloud Security Alliance research note on the coding-agent GitHub Action prompt injection (CVE-2025-66032) — `https://labs.cloudsecurityalliance.org/research/csa-research-note-claude-code-github-action-prompt-injection/` | ① | D | ✓ | The full attack chain: crafted issue → permission bypass → env exfiltration → OIDC token → supply-chain commit. The case study M13 is built on |
| R-122 | *Prompt injection still drives most agentic AI security failures in production* (2026-06-11) — `https://www.helpnetsecurity.com/2026/06/11/owasp-prompt-injection-ai-security-failures/` | ② | M | ✓ | 2026 state of practice; confirms this is not theoretical |
| R-123 | Reporting on agents skipping package verification (2026-07) — `https://www.techtimes.com/articles/319457/20260701/ai-coding-agents-skip-package-verification-attackers-are-exploiting-it.htm` | ② | M | ✓ | Supply-chain angle. Secondary source; find the underlying research before citing in anger |
| R-124 | Supply-chain attack landscape 2026 (npm, PyPI, VS Code marketplace, AI agents) — `https://phoenix.security/accelerating-supply-chain-attacks-npm-pypi-vsx-ai-enabled-2026/` | ③ | M | ✓ | Context on the wider ecosystem |

## Conventions and standards

| ID | Resource | Tier | Vol | ✓ | Why it matters |
|---|---|---|---|---|---|
| R-140 | Agent SDK documentation for your harness | ② | **F** | — | Building your own agents and workflow tools. M15 |
| R-141 | *12-Factor Agents* (HumanLayer) | ② | M | ? | Design principles for agent systems. Widely referenced; locate the current canonical repo |
| R-160 | AGENTS.md vs CLAUDE.md state of play (2026) — `https://bestagent.dev/claude-md-vs-agents-md-2026/` | ② | **F** | ✓ | Third-party but well-dated summary: AGENTS.md as vendor-neutral standard, the import-shim pattern for multi-tool repos. Verify against your harness's own docs |

## Practice mechanics and field observation

| ID | Resource | Tier | Vol | ✓ | Why it matters |
|---|---|---|---|---|---|
| R-22 | Your harness's documentation on rewind / checkpointing and session management | ② | **F** | — | The mechanism behind "discard context rather than argue with it" (M3). Every harness names this differently; find yours |
| R-90 | `git worktree` documentation — `https://git-scm.com/docs/git-worktree` | ② | D | ✓ | The primitive under nearly all agent-parallelism tooling. Learn it directly rather than through a wrapper (M10) |
| R-131 | Eval and observability tooling for agents — LangSmith, Braintrust, Langfuse, and the OpenTelemetry GenAI semantic conventions | ③ | **F** | — | Optional infrastructure for M14. A directory of JSON files and a shell script is a legitimate starting point; reach for these when you outgrow it |
| R-151 | Martin Fowler / Thoughtworks, *Exploring Generative AI* memos — `https://martinfowler.com/articles/exploring-gen-ai.html` | ② | M | ✓ | Field observations across many client codebases. The best available corrective to single-practitioner survivorship bias (M16) |

---

## Reading paths

**If you have one weekend:** R-10 (build the agent) → R-40 (the method) → R-120 (the security frame). That is the irreducible core.

**If you have one week:** add R-01 + R-02 (calibration), R-50 (context), R-30 (verification), R-101 (loops), R-21 + R-43 (two contrasting practitioners).

**If you want the disagreement:** R-32 (Steinberger: don't read the code) against R-43 (DHH: review every diff) against R-40 (Horthy: review the plan instead). Read all three in one sitting and write down where you land. That exercise is worth more than any five other resources here.

**What to follow continuously:** Willison's site for breadth, Ronacher and Steinberger for depth, your harness's changelog and docs for capability, METR and DORA for evidence. `TOOLING.md` §1 specs a tool that watches these for you.

---

## Resources deliberately excluded

- **Courses and bootcamps on "AI coding."** Half-life too short; most teach a 2025 tool surface.
- **Benchmark leaderboards as learning material.** Useful for orientation, actively misleading as a guide to what will work for you (M14).
- **Prompt-library repos.** Cargo cult. Your prompts should derive from your failures (M9, L9.1).
- **Vendor marketing.** Engineering blogs from vendors are included where they are genuinely technical (R-50); product pages are not.
- **Most 2026 "guide" and SEO content.** The field has an enormous volume of derivative explainers. This index prefers primary sources; where a secondary source is included it is labelled.
