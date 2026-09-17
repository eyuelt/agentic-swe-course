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

**I4 — Volatile facts are quarantined.** Product names, model versions, prices, and benchmark numbers live in `STATE-OF-PLAY-*.md` and nowhere else. The curriculum body refers to capabilities. **This invariant is what makes the course maintainable in an afternoon rather than a month.** Violating it is the single most damaging thing you can do here, and it happens gradually, one convenient product reference at a time.

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
