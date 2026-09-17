# Shipping With Agents — State of Play, September 2026

**Compiled 2026-09-17 · THIS IS THE VOLATILE FILE · Refresh quarterly**

> **Purpose.** Every fact in this course that has a short half-life lives here and nowhere else. The rest of the curriculum refers to *capabilities* ("a harness with a plan mode", "a context-isolated subagent") rather than product names, so that refreshing this one file refreshes the whole course.
>
> **If you are reading this after ~2027-03, treat every specific claim below as unreliable.** The principles in `CURRICULUM.md` are designed to survive; the contents of this file are not. `MAINTENANCE.md` §4 has the refresh procedure.

---

## 1. How to read this file

Each claim is stamped with a confidence level:

- **[H]** High — verified from a primary source on the compile date
- **[M]** Medium — from a reputable secondary source, or a primary source that may have moved
- **[L]** Low — directional only; do not rely on it

---

## 2. Models

**[M]** The frontier for coding work as of September 2026 spans at least three vendor families, with new point releases roughly every 6–12 weeks. Specific version numbers reported around mid-2026 include Anthropic's Opus 4.6/4.7/4.8 line, OpenAI's GPT-5.x and Codex-tuned variants, and Google's Gemini 3.x line. **Any list of version numbers in this file is wrong by the time you read it.** What is durable:

**[H]** **The harness co-authors the result.** Benchmark scores for the *same base model* vary by double digits depending on agent scaffolding. Never compare a model number without knowing its harness.

**[M]** **Reasoning effort is now a dial, not a model choice.** Practitioners report using a higher effort setting for hard problems and long unattended runs, and a lower one for routine work. Treat effort as a parameter to tune per task class, and eval it (M13).

**[M]** **Multi-model workflows are normal practice among experts**, typically a fast model for iteration and a stronger one for hard reasoning, run in parallel panes. DHH's reported setup is a clear example.

**[H]** **Advice is model-generation-dependent.** Boris Cherny's guidance on plan mode inverted across model versions — first "always plan first, then auto-accept", later "skip plan mode, newer models plan implicitly." This is the canonical illustration of why technique must be re-tested rather than believed (see M13).

## 3. Benchmarks

**[M]** SWE-bench Verified reported leaders in 2026 were in the mid-to-high 80s percent range; SWE-bench Pro and Terminal-Bench exist as harder successors specifically because Verified is approaching saturation.

**[H]** Aggregators publishing these numbers carry the caveat explicitly: *"Pass-rate depends on agent scaffolding; two runs of the same base model can differ by double digits."*

**Durable position:** use benchmarks for coarse capability trends and for deciding what to go test yourself. Use your own eval suite (M13) for decisions. A saturating benchmark tells you the benchmark is finished, not that the problem is.

## 4. Conventions and standards

**[M] AGENTS.md** — a vendor-neutral agent-instructions file, stewarded since December 2025 by the Agentic AI Foundation under the Linux Foundation, reported adopted by 60k+ open-source projects. Read natively by several major tools.

**[M] CLAUDE.md** — Claude Code's own memory file, predating the standard, with hierarchical loading and `@`-imports.

**[M] The current pragmatic pattern for multi-tool repositories:** make `AGENTS.md` canonical and keep a minimal `CLAUDE.md` that imports it (`@AGENTS.md`) plus any Claude-specific notes. As of August 2026 this import-bridge approach was the documented recommendation rather than native cross-reading.

**[H] SKILL.md / Agent Skills** — on-demand, model-invocable or user-invocable instruction files; the third member of the trio, covering reference material and workflows rather than always-on rules.

**[M] MCP (Model Context Protocol)** — the established standard for connecting agents to external systems. Mature enough that harnesses now defer tool schemas and provide tool search to control its context cost. The practitioner critique (context bloat, too many tools per server, CLIs often better) remains live and legitimate.

**Durable position:** the *pattern* — a canonical, version-controlled, human-readable instructions file at the repo root, plus on-demand reference material — will outlive whichever filename wins.

## 5. Harness capability surface

**[H]** As documented for Claude Code in September 2026, the extension surface comprises: always-on memory (`CLAUDE.md`), path-scoped rules (`.claude/rules/`), skills (on-demand, invocable with `/name`, optionally running in forked context), subagents (isolated context, summarized return, optional preloaded skills), dynamic workflows (a script Claude writes that runs many subagents in background), cross-session messaging, code intelligence via LSP, MCP servers, hooks (shell command, HTTP request, MCP tool call, LLM prompt, or subagent, triggered on lifecycle events), plugins and marketplaces, and artifacts for publishing session output as a web page.

**[H]** Documented guidance that is worth knowing as a *number* because it anchors practice: keep the always-on memory file **under ~200 lines**, moving reference material to skills and path-scoped rules.

**[H]** The documented mechanism-selection principle, which is durable: *"An instruction like 'never edit .env' in CLAUDE.md or a skill is a request, not a guarantee. A PreToolUse hook that blocks the edit is enforcement."*

**[M]** Other harnesses (Codex CLI, Cursor, Gemini CLI, Amp, OpenCode, Copilot's agent mode, and others) expose analogous but differently-named surfaces. The curriculum deliberately teaches the *categories* — always-on context, on-demand knowledge, isolated workers, deterministic enforcement, external connection, packaging — because these have been stable across tools even as names change.

**[M]** Capabilities that became mainstream during 2026 and are worth checking for in whatever tool you use: sandboxed execution modes, scheduled and long-running jobs, session portability across devices, agent "control plane" views for managing many concurrent sessions, voice input, and browser control integrations.

## 6. Orchestration and loops

**[H]** "Loop engineering" emerged as the dominant 2026 framing for the shift from prompting agents to designing the systems that prompt them. Practitioner formulations: Osmani's *"replacing yourself as the person who prompts the agent"*; Steinberger's *"You should be designing loops that prompt your agents."*

**[H]** The Ralph technique — a shell loop feeding a specification file to a fresh agent context repeatedly — originated with Geoffrey Huntley in mid-2025, spread widely, and by late 2025 had official tooling support in at least one major harness. Documented failure modes: bad specs amplified across iterations, overbaking (loops generating bizarre unrequested work when run past useful life), poor merge-conflict handling, and unsuitability for exploratory work.

**[M]** Practitioners warn that "Ralph" has undergone semantic diffusion — it is now applied to any automated loop, losing the specific insight about small independent context windows.

## 7. Evidence base

**[H]** **METR 2025:** experienced open-source developers were **19% slower** with early-2025 AI tools while estimating they were **20% faster**.

**[H]** **METR 2026 update (Feb):** later-2025 cohorts showed roughly **−18%** for returning participants and **−4%** for newly recruited ones, confidence intervals crossing zero. METR announced a **redesign** of the experiment because it could no longer recruit cleanly: developers refuse to work half their tasks without AI, 30–50% decline to submit tasks they believe AI handles well, and agentic multitasking makes self-reported time unreliable.

**[M]** **DORA 2026 (ROI of AI-Assisted Software Development, published ~May 2026):** a **J-curve** of value realisation — an initial dip described as "the tuition cost of transformation" (learning, verification tax, process adaptation) before gains; an **instability tax** (individual effectiveness up, delivery stability down); gains strongly task-dependent (**35–40% on simple tasks, ~10% or less on complex legacy code**); illustrative first-year ROI figures for a large engineering org; and the central finding that **AI amplifies the existing organizational system** rather than substituting for it. The report explicitly discourages headcount reduction in favour of retention and upskilling.

**Durable position:** the literature is becoming structurally unable to answer "does this make me faster" for the individual practitioner, because clean control groups no longer exist. This is the standing argument for M0.

## 8. Security

**[H]** **CVE-2025-66032** (GHSA-xq4m-mc3c-vvg3), CVSS 7.8 (v4.0) / 8.7 (v3.1), CWE-20 and CWE-77, in a widely-used coding-agent GitHub Action. `checkWritePermissions` unconditionally trusted any GitHub App actor. Attack chain: malicious GitHub App opens a crafted issue on a public repo → permission bypass → prompt injection in the issue body directs the agent to read the workflow environment → OIDC token extracted → exchanged for repository write access → malicious commit to the action's source, poisoning downstream consumers. Disclosed 2026-01-12, fixed 2026-01-16 (v1.0.94), publicly detailed 2026-06-01. Related in-the-wild exploitation against another AI coding tool was reported in February 2026.

**[H]** Parallel research ("Comment and Control") found that multiple major coding agents processed untrusted GitHub metadata — PR titles, issue bodies, HTML comments — as authentic instructions, enabling live credential theft.

**[M]** As of mid-2026, prompt injection remained the leading cause of agentic AI security failures in production.

**[M]** AI coding agents have been reported skipping package verification — installing dependencies without provenance checks — with attackers exploiting this.

**Durable position:** the lethal trifecta frame (private data + untrusted content + external communication) and the architectural response (break one leg; isolation must rise with autonomy) are stable. The specific CVEs are illustrations, and there will be more.

## 9. Named tools mentioned in the course

Listed here so the body of the curriculum stays tool-agnostic. Presence is not endorsement; absence is not judgment.

- **Terminal agents:** Claude Code, Codex CLI, Gemini CLI, Amp, OpenCode, Aider, Goose, and others
- **IDE-integrated:** Cursor, Windsurf, Zed, GitHub Copilot agent mode, JetBrains Junie
- **Cloud / async:** cloud sessions in the major harnesses, Devin, Jules, Copilot coding agent, Factory
- **Orchestration:** git worktrees plus wrappers; container-based isolation; harness-native parallel session views
- **Codebase hygiene:** duplicate-code detectors (e.g. jscpd), dead-code detectors (e.g. knip), mutation testing tools
- **Spec-driven toolkits:** GitHub Spec Kit, Kiro, BMAD-METHOD and others
- **Observability / evals:** LangSmith, Braintrust, Langfuse, OpenTelemetry GenAI conventions
- **Open-source agent projects:** OpenClaw (moved to foundation governance in 2026)

## 10. Refresh checklist

When refreshing this file (quarterly, per `MAINTENANCE.md`):

- [ ] Re-verify every URL in `RESOURCES.md`; update the `✓` column
- [ ] Check METR's blog for new productivity research
- [ ] Check DORA's publications index for the current-year report
- [ ] Re-read your primary harness's features/changelog docs; update §5
- [ ] Check each dossier practitioner's index page for new writing; note any **position changes** (§`MAINTENANCE.md` treats these as high-priority)
- [ ] Search for new CVEs and incidents in agentic coding; update §8 with at least one current example
- [ ] Check whether the AGENTS.md / CLAUDE.md / skills convergence has changed; update §4
- [ ] Ask: has a new *category* appeared, or only new products? A new category means `CURRICULUM.md` needs editing. New products mean only this file does.
- [ ] Update the compile date and the title of this file
