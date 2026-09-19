# Maintenance Protocol

**For the next maintainer of *Shipping With Agents* — human or model.**
**Version 1.0 · Written 2026-09-17**

You are reading this because you have been asked to continue, extend, correct, or refresh this course. Read §1 and §2 before changing anything. They exist to stop well-intentioned edits from destroying what makes the course work.

---

## 1. Design invariants — do not change these without a deliberate decision

These are load-bearing. If you change one, you are writing a different course, which is allowed — but do it knowingly and record it in §7.

**I1 — The verification gap is the spine.** Every technique is taught as an answer to "what does this do to the gap between code produced and code known-good?" This is what makes the course cohere instead of being a list of tips. If you add content, connect it to the spine or leave it out.

**I2 — Mastery-based, not time-based.** No weeks. No schedule. Artifacts and rubrics gate advancement. Resist requests to turn this into a 12-week syllabus; the field moves too fast for cohorts and the audience is self-directed.

**I3 — Practice over vocabulary.** Every module ends in something built, measured, or run. If you find yourself writing a module that ends in "understand X", you have written a blog post, not a module.

**I4 — Volatile facts are quarantined; products are examples only.** Every *claim* about a product — features, model versions, prices, benchmark numbers, comparisons — lives in `STATE-OF-PLAY-*.md` and nowhere else. The curriculum body teaches capabilities, and no module or lab may depend on a particular product. The body **may** name a product as an example, written as a gloss — "an agent harness (e.g. Claude Code or OpenCode)" — because a newcomer often cannot tell what a capability term refers to without one. Every name used this way must be in the example registry in `STATE-OF-PLAY-*.md` §9.1; `curriculum_lint.py products` enforces that, and flags every mention of a product once the registry marks it retired. The dossier and the resource index are exempt: describing a person or a source means naming what they built. **This invariant is what makes the course maintainable in an afternoon rather than a month.** Violating it is the single most damaging thing you can do here, and it happens gradually, one convenient product reference at a time.

**I5 — Experts are hypotheses, not authority.** The dossier presents disagreements and teaches a protocol for testing claims. Never resolve a disagreement by picking the most famous person. If you add a practitioner, add their context dependencies and their critics.

**I6 — Security precedes autonomy.** M13 is a hard prerequisite for the unattended parts of M11 and M12. Do not reorder for narrative flow. The ordering is the safety argument.

**I7 — Honest about uncertainty.** Sources are dated and marked verified or not. Claims the course cannot support are labelled as the course's own position. Do not launder a plausible guess into an authoritative statement — the audience is experienced engineers who will notice, and correctly discount everything else.

**I8 — Judgment traces are the assessment.** Rubrics weight reasoning over output because output is now cheap. Do not add auto-graders for reflection (`TOOLING.md` says why).

---

## 2. Volatility tiers — what rots at what rate

| Tier | Content | Half-life | Where it lives | Refresh |
|---|---|---|---|---|
| **Durable** | The verification gap; context as a budget; loops need fitness functions and stop conditions; the lethal trifecta; measure-don't-assume; local reasoning | 2–5 yr | `CURRICULUM.md` core sections, `SYLLABUS.md` | Only when contradicted by evidence |
| **Technique** | Research→plan→implement; intentional compaction; parallelism strategies; the extension-surface categories; specific ratios and thresholds | ~12 mo | `CURRICULUM.md` labs and specifics | Annually, or when a practitioner you track changes position |
| **Instance** | Tool names, model versions, benchmark scores, prices, URLs, feature names | ~3 mo | `STATE-OF-PLAY-*.md`, `RESOURCES.md`, `feeds.yaml` | Quarterly |

**The diagnostic question for any edit:** *would this still be true if every product in the field were renamed tomorrow?* Yes → Durable or Technique, belongs in the body. No → Instance, belongs in `STATE-OF-PLAY`.

---

## 3. What you may change, and what needs a human

**Change freely:**
- `STATE-OF-PLAY-*.md` — that is what it is for
- URLs and verification marks in `RESOURCES.md`
- Adding a lab, or sharpening an existing one
- Adding a resource, with its date and volatility tag
- Fixing anything the linter flags

**Change with care, and record it in §7:**
- Module content and ordering
- Rubrics and gate requirements
- The dossier's characterization of a practitioner
- The disagreement map

**Do not change without a human deciding:**
- The design invariants in §1
- Removing a module or a phase
- The security ordering (I6)
- The assessment philosophy (I8)

**A specific instruction for a model maintainer.** You may generate proposals for any of the above. You may not merge changes to the second and third categories on your own initiative. The reason is structural, not procedural: a model refreshing a curriculum from recent feeds drifts toward whatever was loudest this quarter, and the loudest claims in this field are systematically the least verified. The pipeline is: **feeds generate proposals → a maintainer decides → the linter verifies.** Keep the human in the middle step.

---

## 4. The quarterly refresh — a half-day procedure

**Step 1 — Run the linter (15 min).**
```
python3 tools/curriculum_lint.py all --ci
```
Fix every error. Note that `proxy-blocked` findings mean *your machine* cannot reach the URL, not that the link is dead — re-run somewhere with unrestricted outbound HTTPS before editing anything.

**Step 2 — Run feedwatch (15 min + reading).**
```
python3 tools/feedwatch.py fetch && python3 tools/feedwatch.py report --since 90d
```
Triage the inbox. **Handle `position-change` findings first** — a dossier entry that misrepresents a living practitioner is the worst defect this curriculum can have, and it has a specific tell: the person's newer writing quietly contradicts an older quote the course still uses. Verify against the primary source, then fix the dossier and the disagreement map together.

**Step 3 — Refresh `STATE-OF-PLAY` (2 h).** Work the checklist at the end of that file. Rename it to the new date. Keep the old one in `archive/` — the diff between two state-of-play files is the most useful artifact for understanding what actually changed, as opposed to what was announced.

**Step 4 — Ask the category question (30 min).** For everything new since the last refresh: *is this a new product, or a new category?*
- **New product** → `STATE-OF-PLAY` only. Most things are this.
- **New category** → a capability that did not exist before and changes what a practitioner must know. This needs curriculum surgery. In the last two years, genuine new categories were: context isolation via subagents, deterministic hooks, autonomous loops, agent-driven CI, and scheduled agents. That is roughly one every four months. If you think you have found three in one quarter, you have probably found three products.

**Step 5 — Re-verify the evidence base (1 h).** Check METR and DORA for new work. Evidence changes slowly and matters more than tooling; a single new RCT is worth more to this course than a year of product launches.

**Step 6 — Record it (15 min).** Append to §7.

---

## 5. How to tell this curriculum has rotted

Watch for these. Two or more means a full revision, not a refresh.

1. **The linter reports staleness errors** — `STATE-OF-PLAY` is over six months old.
2. **A practitioner in the dossier has publicly reversed a position the course still attributes to them.** Highest severity.
3. **Learners report that a lab's tooling assumptions no longer hold** — e.g. a mechanism the course treats as universal no longer exists in any current harness.
4. **A module's core technique has become automatic.** If harnesses now do intentional compaction correctly without instruction, M6 needs rewriting from "how to do it" to "how to verify your harness is doing it."
5. **The disagreement map has gone quiet** — everyone now agrees. Either the field matured (rewrite the map as settled practice) or you stopped tracking dissent (more likely; go find the critics).
6. **The evidence section still cites only 2025–2026 studies** while the course is being taught in 2028.
7. **Nobody has failed a capstone.** Rubrics have drifted toward participation.

---

## 6. How to add a practitioner to the dossier

The bar is deliberately high. The dossier is valuable because it is short.

**Required:**
1. **Primary sources.** Their own writing, talks, or code. Not a thread about them.
2. **A replicable practice.** Something a learner can do on Tuesday. "Has good instincts" does not qualify.
3. **Evidence they ship.** Real software, real codebases, real outcomes.
4. **Context dependencies, stated.** Codebase, language, risk tolerance, budget, team. Without these the entry teaches cargo-culting.
5. **A `Read critically` section.** Every entry has one. If you cannot write it, you do not understand them well enough yet.
6. **A teardown target.** At least one cheap experiment a learner can run.

**Disqualifying:** advice with no mechanism; claims with no verification story; anyone whose primary output is commentary on other practitioners; anyone whose track record is confined to demos.

**When someone should be removed:** they have stopped working in the field; their distinctive practice has become universal (fold it into the curriculum body and drop the attribution); or their context has diverged so far from any learner's that the entry teaches nothing transferable.

---

## 7. Change log

| Date | Maintainer | Change | Invariants touched |
|---|---|---|---|
| 2026-09-17 | Initial authoring (Claude, Opus 5) | v1.0 created. 17 modules, 5 phases, 3 gates, 3 capstones. Research base: primary sources verified live on this date; see `RESOURCES.md`. | — (establishes I1–I8) |
| 2026-09-17 | Eyuel | Course renamed *Shipping With Agents*; agentic software engineering retained as the field, not the title. | none |
| 2026-09-17 | Eyuel | Modules and phases renumbered to 1-index (M1–M17, Phase 1–5); "stages" renamed "phases". "Three layers" reframed as **three levels of practice**, defined by the unit of work and mapped to the phase that teaches each. 89 ungraded self-checks added (retrieval practice, not assessment — I8 holds). Anti-cheat framing removed throughout: this is voluntary self-study and integrity policing added nothing. `CLAUDE.md` and `/refresh-curriculum` added for agent-run maintenance. | I2, I8 (clarified) |
| 2026-09-17 | Eyuel (caught) / Claude (applied) | **position-change**: DHH's entry was written from an April 2026 source and missed his August position — by Lex Fridman #501 (2026-08-26) he reports shipping two months of a project without hand-writing any code and reviewing *the shape* rather than every line. Entry and Disagreement Map row rewritten; R-45 added; R-43 marked superseded. All entries now carry **As of** stamps and the dossier carries a short currency note. Common public names (steipete, Boris, DHH, mitsuhiko, ghuntley) added. | I5, I7 (upheld) |
| 2026-09-17 | Eyuel | First independent link run from an unrestricted network: 52 URLs, 0 dead, 1 redirect. R-10 corrected to its canonical path; R-81/R-90/R-102/R-103/R-151 promoted from unverified to verified on that evidence. Eight citations added to reduce orphaned resources. | I7 (upheld) |
| 2026-09-17 | Eyuel (asked) / Claude (applied) | Site published on GitHub Pages. `.github/workflows/pages.yml` deploys `curriculum.html` as the index on push to `main`, wrapping the artifact fragment in a doctype/charset/viewport skeleton at build time so the repo keeps one copy of the page. Repo transferred from the `EyuelBotCollab` org to `eyuelt` and made public, because Pages on a free plan requires a public repo. No course content changed. | none |
| 2026-09-17 | Eyuel (directed) / Claude (applied) | **Overview and framing pass.** (1) **Thesis reworded** to tie it to the course title: "Agents made code cheap to write. They did not make it cheap to ship. Verification is the bottleneck. …" — same claim, same verification-gap spine; updated in `SYLLABUS.md` §1, README and the page, where it now sits under the title as the hook. (2) "Three levels of practice" renamed **the building blocks of an agentic workflow** (message ⊂ context window ⊂ loop), mastered from the inside out. The "rests on the one below" layer metaphor is replaced by containment because the reversed 3→2→1 stack read backwards; the blocks are deliberately **unnumbered** — phases and modules are the only numbered schemes. `SYLLABUS.md` §2 restructured to match; page gets a nested diagram and left-to-right cards. (3) **Assessment weights removed** (`SYLLABUS.md` §6 and page): the 40/15/10/15/15/5 column was never used by `ASSESSMENT.md` — there is no points scheme or aggregate score, only rubric levels with Proficient as the bar — so it implied a grading system that does not exist. (4) **Remaining zero-indexing fixed:** "Module 0"/"Module 1" prose leftovers in `SYLLABUS.md` §4.3/§4.5 and README; time-budget phase labels 0–4 → 1–5 (`CURRICULUM.md` Appendix B and page); volatility tiers lose their 0/1/2 numbers and go by name (Durable / Technique / Instance) in §2 above and on the page. (5) **Follow links** added per practitioner (dossier and page), each taken from the person's own site or GitHub profile and passing the link check; one Bluesky link dropped because the checker cannot fetch it. (6) Page only: title is the course name; phases shown as a roadmap with a route line; resources get an unread / in-progress / read status saved with progress; dark-mode grays lightened; type sizes and label casing made consistent. | I1 (upheld — wording only), I2 (upheld — weights implied points; rubrics gate advancement), I7 (upheld for new links), I8 (upheld — nothing graded added) |
| 2026-09-17 | Eyuel (directed) / Claude (applied) | Page only — header bar. On narrow screens the tabs, progress meter and theme button no longer wrap onto extra lines: the tab row scrolls sideways with an edge fade where more tabs lie beyond, the active tab is kept in view, and the theme button stays top-right. Date removed from the header because the footer already carries it. No course content changed. | none |
| 2026-09-17 | Eyuel (decided) / Claude (applied) | **I4 rewritten — deliberately.** The blanket ban on product names in the body is replaced by: products may appear **as examples only**, as an `(e.g. …)` gloss, drawn from a registry in `STATE-OF-PLAY` §9.1; every *claim* about a product still lives only in `STATE-OF-PLAY`; no lab may depend on a product; dossier and resource index are exempt. **Why:** a newcomer often cannot tell what a capability term like "agent harness" refers to without an example, and the ban had already pushed the dossier into evasions ("creator of open-source agent tooling" for OpenClaw). **What keeps it refreshable:** the rule was previously unenforced; `curriculum_lint.py products` now checks it and reports every body mention of a product once the registry marks it `retired`, so a refresh is still one file plus a list of flagged lines. First glosses added at the points where harness, memory file, spec-driven toolkits and cloud agents are introduced. `SYLLABUS.md` §4.6, `CLAUDE.md` rule 1, `TOOLING.md` T2, the refresh skill and the page updated to match. | **I4 (changed)** |
| 2026-09-17 | Eyuel (flagged) / Claude (applied) | Dossier identity lines corrected against primary sources: Steinberger now leads with OpenClaw (his own About page), Ball is co-founder and co-creator of Amp (his own site), Karpathy gains his career line and the 2026-02-04 "agentic engineering" proposal, Horthy gains co-founder/CEO and the early "everything is context engineering" argument — stated as his account, not as "coined". | I5, I7 (upheld) |
| 2026-09-17 | Eyuel (directed) / Claude (applied) | Page only — **settings menu and optional Google Drive progress sync.** The theme button becomes a settings button; the menu holds a System / Light / Dark control and a Progress section. Progress always saves in the browser. If `GOOGLE_CLIENT_ID` in `curriculum.html` is set, readers can sign in with Google and keep a copy in the site's private app-data folder in their own Drive (scope `drive.appdata` only — the site cannot see their other files; the access token is held in memory, never stored). On connect the two copies are merged so no tick is lost; after that every change is pushed. Sign-in lasts about an hour, after which sync pauses and offers a reconnect. **The client ID ships empty, so the Drive option is hidden until the owner creates an OAuth web client with this site's origin and pastes the ID in.** Sync logic was tested against stubbed Google services, not against real Google sign-in. No course content changed. | none |
| 2026-09-17 | Eyuel (decided) / Claude (applied) | The original claude.ai artifact copy of the page was deleted; `eyuel.com/agentic-swe-course/` (GitHub Pages, deployed from `curriculum.html` on push) is now the only published copy. `CLAUDE.md`, the refresh skill and the deploy workflow's comment updated so nobody goes looking for an artifact to republish. The page's account-sync code path is left in place; it is inert outside the artifact host. | none |
| 2026-09-17 | Eyuel (supplied) / Claude (applied) | Google Drive progress sync switched on: the owner's OAuth web client ID is set in `curriculum.html`, so the settings menu now offers "Sign in with Google". The ID is public by design; the client secret is not used anywhere and must never be committed. The client only issues tokens to its authorized origin (`https://eyuel.com`), so sign-in will not work from a fork or a local file without its own client. | none |
| 2026-09-17 | Eyuel (asked) / Claude (applied) | Page only — favicon added: the three nested building blocks (loop, context window, message) in the site's teal. `assets/favicon.svg` is the source, with PNG fallbacks for browsers and home screens that ignore SVG icons; the deploy workflow copies `assets/` into the site. | none |
| 2026-09-17 | Eyuel (decided) / Claude (applied) | Page only — Drive sync no longer pauses on every page load. The Google access token is now remembered in the browser's localStorage until it expires (about an hour), so refreshes and new tabs stay connected; after that it is one click to reconnect. **This reverses the earlier "token in memory only" choice, knowingly:** the token is scoped to `drive.appdata`, so the most it can open is this site's own progress file. Persistent sign-in (weeks, no clicks) would need a backend and the client secret; not done. The paused message now says why it paused instead of always blaming the one-hour limit. | none |
| 2026-09-17 | Eyuel (found) / Claude (fixed) | Page only — **Drive sync got conflicts wrong across two devices.** The merge kept whichever side was "further along" (ticked beats unticked, read beats unread) and carried no times, so un-marking on one device was undone by the other; and each save overwrote the whole file without reading it first. Now every item records when it was last changed and **the newest change wins, including un-marking**; every save pulls and merges before writing, and skips the write when nothing differs; a connected tab re-checks Drive every 20 seconds while visible and when it regains focus. Progress saved before item times existed still merges by the old further-along rule, once, so nothing is lost. Known limits: it trusts each device's clock, and two devices saving within the same second can still race — the loser's change is restored at its next sync. Tested with two simulated devices against a stubbed Drive; not against real Google. | none |
| 2026-09-19 | Eyuel (asked) / Claude (applied) | Page only — three reader changes. (1) **On narrow screens, picking a module scrolls to it.** The module list stacks above the module there, so a tap changed content that was off-screen and looked like nothing happened; the same now applies to the ← / → buttons and to opening a module from the overview, which used to jump back up to the list. Wide screens are unchanged. (2) **Each module's Reading list links to what it cites.** The page had plain-text reading lines with no IDs; they now carry the `[R-nn]` citations from `CURRICULUM.md`. The title opens the source, the R-id opens that entry in the Resources tab, and a reading status set there shows beside the item. To make every citation resolve, the page's resource list grew from 25 to 45 entries — the 20 added are the ones a module cites, copied from `RESOURCES.md` with their tier (③ reference now shown), volatility and blurb. Five have no verified link in `RESOURCES.md` (R-22, R-62, R-131, R-140, R-141) and render as text, saying so, rather than gaining a guessed URL. **Citation fix found on the way (owner approved):** `CURRICULUM.md` M12 Reading cited the CVE-2025-66032 case study as R-120, which is Willison's lethal-trifecta post; corrected to R-121, the research note the label describes. (3) **A fourth reading status, DNR (do not read), in red**, for a resource the reader has judged not worth their time; it has its own filter and count, and syncs like the other statuses. Tested in a headless browser at phone and desktop widths; no course content changed. | I7 (upheld — no link invented for unverified entries) |
| 2026-09-19 | Eyuel (decided, as a learner) / Claude (applied) | **M1 stops asking whether agents beat working by hand.** Owner's objection on reaching M1: the goal is to learn agentic engineering, which the career now requires regardless, so hours spent on a by-hand control group to prove a speed-up could not change any decision. Accepted. **Removed:** L1.2 (the control tasks), the ≥5 non-agent rows and ≥20-row quota in L1.1, the two-week logging period, the "honest-baseline problem" paragraph, and M17's "re-run the M1 measurements". **Kept, and why:** the four numbers, the prediction log, the beliefs statement and the annotated session — M3, M5, M8, Gate 1, the dossier's teardown protocol and M17 all read them, and read ratio and verification events are the verification-gap meters, not speed meters. They now compare one agentic technique against another and early rows against late rows, never agents against no agents. M1 renamed **Instrumentation**, 4–6 h + 2 weeks → 2–3 h; L1.3/L1.4 renumbered L1.2/L1.3 (a browser tick saved against the old L1.2–L1.4 now points at a different lab); M17 compares the first and last twenty log rows instead (page lab C.3, 3 h → 1 h); time budget 168 → 166 h. The METR facts are unchanged; the conclusion drawn from them is now marked as the course's own position. `SYLLABUS.md` §4.3 retitled "Steer by instruments, not by feel", §9, README, `ASSESSMENT.md` §4 rows M1/M17, `TOOLING.md` T3 check and T4 caution, and the page updated to match. **Disagreement Map, "Are we faster?" — course position changed** from "measure your own" to: the course does not try to settle it; the durable lesson is that felt speed is unreliable. | I1 (upheld — the kept instruments are the gap meters), I3 (upheld — M1 still ends in built artifacts), I7 (upheld — new stance labelled as the course's own), I8 (upheld) |

**Format for entries.** Date · who · what changed and why · which invariants were touched or deliberately broken. Keep it terse. A maintainer two years from now needs to know *why* a decision was made, which is the one thing the diff cannot tell them.

---

## 8. Known gaps in v1.0

Stated honestly so the next maintainer does not have to rediscover them.

- **Thin on non-code agentic work.** Infrastructure, data engineering, and ML workflows get less attention than application development. The principles transfer; the labs largely do not.
- **Single-practitioner bias in the evidence.** Much of the dossier is self-reported by people with an incentive to report success. Thoughtworks-style field observation (R-151) is the only real counterweight and it is under-used.
- **The junior-developer question is named and not answered** (M16). Nobody has answered it; the course should say so rather than invent a curriculum for it, but it deserves revisiting as evidence appears.
- **Cost modelling is absent.** The course says Phase 4 is expensive without helping a learner budget. A cost-per-outcome module would be useful and would need real data.
- **No treatment of regulated or safety-critical environments.** Medical, aerospace, finance-with-auditors. These have constraints the course simply ignores, and the M13 material is necessary but nowhere near sufficient for them.
- **T3–T6 are specs, not code.** `TOOLING.md` ships only two working tools.
- **The eval module (M14) deserves to be larger.** It is the most durable content in the course and currently gets less space than M8.
