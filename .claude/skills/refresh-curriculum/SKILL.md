---
name: refresh-curriculum
description: Run the quarterly refresh of the Shipping With Agents curriculum — lint, poll practitioner feeds, triage findings, refresh the state-of-play file, and propose changes. Use when asked to refresh, update, or check the currency of this curriculum.
---

# Quarterly curriculum refresh

A half-day procedure, in order. **Do not skip step 0.** Work through it, then present a single summary of what you
changed and what needs the owner's decision.

## 0. Read the boundary first

Read `MAINTENANCE.md` §1 (invariants) and §3 (what may change without a human). You have authority over
`STATE-OF-PLAY-*.md`, `RESOURCES.md`, labs and the tools. You do **not** have authority over module content,
rubrics, the dossier's characterizations, or the disagreement map — for those, draft and ask.

## 1. Lint (15 min)

```bash
python3 tools/curriculum_lint.py all --ci
```

Fix every **error**. Notes on reading the output:

- `proxy-blocked` means *this machine* cannot reach the URL. It says nothing about the target. Do not "fix" these
  by deleting resources — re-run somewhere with unrestricted outbound HTTPS.
- `blocked: HTTP 403` is usually bot protection (GitHub does this). Open it in a browser before believing it.
- `moved` — update the URL in place to the redirect target.
- `dead` — try to find the new home. If the resource has genuinely gone, replace it with an equivalent and say so
  in the change log; do not silently drop a cited source.
- Uncited resources are `INFO`, not a defect. Some entries exist to support the dossier prose.

## 2. Poll the feeds (15 min, plus reading)

```bash
python3 tools/feedwatch.py fetch
python3 tools/feedwatch.py report --since 90d
python3 tools/feedwatch.py sources     # check for dead feeds
```

Then triage `inbox/<date>.md`. `feedwatch classify --print-prompt` emits the classification prompt; apply it
yourself against `PRACTITIONER-DOSSIER.md`.

**Handle `position-change` first and treat it as the highest-value output of this whole procedure.** A dossier
entry that misrepresents what a living practitioner currently believes is the worst defect this repo can carry.
Requirements before you act on one:

- Quote the passage that shows the change. No quote, no finding — models over-detect contradiction from tone.
- Verify against the **primary source**, not a summary of it.
- Note that a *refinement* is not a reversal. DHH moving from "review every diff" to risk-tiered review is a real
  change; a practitioner restating a position in new words is not.
- Draft the revised entry, update its `As of` stamp, check whether the disagreement map row also needs revising,
  and **present it rather than merging it.**

Other classes: `new-technique` → propose where it belongs, do not insert it. `evidence` → add to `RESOURCES.md`
yourself. `tool-change` → `STATE-OF-PLAY` only. `restatement` and `noise` → log and drop.

A dead feed is the silent failure mode here: it looks identical to a practitioner who stopped writing. Fix any
source `feedwatch sources` reports failing, especially ones still marked `unverified: true` in `feeds.yaml`.

## 3. Refresh the state of play (2 h)

Work the checklist at the end of `STATE-OF-PLAY-*.md`. Then:

- Rename the file to the new date and move the old one to `archive/`.
- Keep the confidence markers `[H] / [M] / [L]` honest. Demote anything you could not re-verify.
- Update `RESOURCES.md`'s "verified live" stamp and the verification-history line.

The diff between two state-of-play files is the single most useful artifact this repo produces — it shows what
actually changed, as opposed to what was announced. Do not overwrite the old one.

## 4. Ask the category question (30 min)

For everything new since the last refresh: **a new product, or a new capability category?**

- **New product** → `STATE-OF-PLAY` only. Almost everything is this.
- **New category** → a capability that did not exist before and changes what a practitioner must know. This needs
  curriculum surgery, which means the owner decides. Genuine new categories have appeared roughly every four
  months (context isolation via subagents, deterministic hooks, autonomous loops, agent-driven CI, scheduled
  agents). **If you think you found three in one quarter, you found three products.**

## 5. Re-verify the evidence base (1 h)

Check METR (`metr.org/blog`) and DORA (`dora.dev/research/publications/`) for new work. Evidence changes slowly and
matters more than tooling — a single new RCT is worth more here than a year of product launches. Add findings to
`RESOURCES.md` and, if they bear on it, to `STATE-OF-PLAY` §7.

## 6. Check for rot (15 min)

From `MAINTENANCE.md` §5. Two or more of these means a full revision is due, not a refresh:

1. Linter reports staleness errors
2. A practitioner has reversed a position the dossier still attributes to them
3. A lab's tooling assumptions no longer hold in any current harness
4. A module's core technique has become automatic — it needs rewriting from "how to do it" to "how to verify your
   harness does it"
5. The disagreement map has gone quiet
6. The evidence section cites nothing from the last two years

## 7. Record it (15 min)

Append to the `MAINTENANCE.md` §7 change log: date · who · what changed and why · which invariants were touched.
Terse. A maintainer two years out needs the *why*, which the diff cannot tell them.

## 8. Re-lint and report

```bash
python3 tools/curriculum_lint.py all --ci
```

Then give the owner one summary with three sections: **changed** (what you did on your own authority), **needs your
decision** (drafts awaiting approval, position-changes first), and **noticed but not acted on**.

## If you also update the published page

`curriculum.html` is an offline copy of the artifact at `claude.ai/artifact/UrtxDpYCvHk8Ep7yJC77UH`. Editing the
file does not republish it. Keep them in step: after a content change, tell the owner the page needs republishing.

The same file is also served by GitHub Pages at `eyuel.com/agentic-swe-course/` (`eyuelt.github.io/agentic-swe-course/` redirects there). That copy *does*
redeploy by itself: `.github/workflows/pages.yml` publishes `curriculum.html` as the site index on every push to
`main` that touches it. So after a push the Pages site is current and only the artifact needs republishing.
