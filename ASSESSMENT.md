# Assessment

**Version 1.0 · Companion to `SYLLABUS.md` and `CURRICULUM.md`**

---

## 1. Philosophy

This course assesses **judgment**, not output. Artifacts are cheap to produce now; what makes one worth having is the record attached to it — decisions you made, measurements you took, predictions that turned out wrong.

Accordingly, every rubric weights three things:

1. **The artifact exists and works** — necessary, not sufficient, and worth the least.
2. **The measurement is real** — numbers from your own logs, with the awkward ones included.
3. **The judgment trace** — why you chose this, what you rejected, what surprised you, what you would do differently. This is the bulk of the grade.

A submission with an impressive artifact and no judgment trace scores **Working** at best. A submission with a modest artifact, an honest null result, and a sharp analysis of why, scores **Proficient**.

**On failure reporting.** If a capstone or gate produced no failures worth recording, go back and look again. Unattended agent work fails regularly; a run that appears clean usually means the logging was too coarse or the scope was too small to be interesting. Both are useful findings — write down which one it was.

---

## 2. The four levels

| Level | Meaning |
|---|---|
| **Novice** | Knows the concept exists. Cannot apply it without a guide. |
| **Working** | Applies it when prompted, on familiar ground. Cannot yet adapt it. |
| **Proficient** | Applies it unprompted, adapts it to context, and can say why. **This is the advancement bar.** |
| **Expert** | Extends or contradicts the standard practice, with evidence. Can teach it. |

Nobody is expected to reach Expert across all seventeen modules. The Expert descriptors exist so you can see the shape of what you have not yet learned.

---

## 3. Generic rubric

Applied to every module artifact unless the module specifies otherwise.

| Dimension | Novice | Working | Proficient | Expert |
|---|---|---|---|---|
| **Artifact** | Missing or non-functional | Works on the happy path | Works, handles the failure case, documented | Reusable by someone else; generalized |
| **Measurement** | None | Numbers reported without method | Method stated, controls noted, uncertainty acknowledged | Variance quantified; effect size stated before believing it |
| **Judgment trace** | Absent | Describes what was done | Explains what was rejected and why | Identifies a case where the standard advice is wrong, with evidence |
| **Honesty** | Only successes | Mentions difficulty | Reports a failure and its diagnosis | Reports a failure that changed the practice |
| **Transfer** | Copied a source | Applied to own work | Adapted, with context dependencies named | Adaptation documented well enough for others to reuse |

---

## 4. Module mastery artifacts — quick reference

| Module | Artifact | The one thing assessors look for |
|---|---|---|
| M1 | Log (first three rows), beliefs statement, annotated session | Predictions recorded *before*; beliefs specific enough to be falsifiable |
| M2 | Working agent, four-experiment table, one harness feature, teardown | Predictions written before running the break experiments |
| M3 | 5 rewritten briefs, calibration factor, abandonment log, briefing standard | Evidence of abandoning something that felt nearly done |
| M4 | Verifier audit, <15s fast lane, same-context test comparison, gaming catalogue, non-test loop | A measured sub-15-second command that the agent runs unprompted |
| M5 | Review-method comparison, comprehension audit, tuned reviewer, upstream experiment | Read ratio measured honestly and a repaid module |
| M6 | Context census, before/after audit, compaction artifact, rot threshold, subagent spec | A deletion from the always-on file justified by evidence |
| M7 | Verified research doc, plan with scored objections, ratio experiment, reused plan | Spot-checks of research claims against actual source |
| M8 | Scored legibility audit, hygiene sweep, deterministic suite, greppability repair, 2 enforced conventions | Ten consecutive identical test runs |
| M9 | Correction taxonomy, blocking hook, review subagent, MCP cost table | Every extension traced to a specific personal failure |
| M10 | Isolation comparison, throughput curve, decomposition, control plane | A stated ceiling with the constraint that sets it |
| M11 | Terminating loop, 3 stop conditions, overbaking account, verified fan-out, week of logs | A defect the verifier agent caught that the worker missed |
| M12 | Handoff breakdown, phone friction list, review policy, CI agent + threat model | A review policy applied retrospectively with a misclassification rate |
| M13 | Trifecta audit, red-team table, verified sandbox, threat model, supply-chain guardrail | A demonstrated successful injection against your own agent |
| M14 | Eval suite (≥10 tasks), variance table, controlled comparison, memory-file eval | A minimum effect size stated before comparing |
| M15 | Extended agent, token profile improvement, workflow agent, orchestration comparison | Survives compaction and restart on a multi-hour task |
| M16 | Bottleneck analysis, team memory file, review policy, debt register | Memory file rules traced to ≥2 historical review comments |
| M17 | Capstone C, doctrine document, early-versus-late log comparison, practice schedule, teaching artifact | The "what I changed my mind about" section, quoted against M1 |

---

## 5. Gate assessments

Gates test **integration**, not recall. Each is a single recorded session or a single change, in a real repository, demonstrating several modules at once.

### ▸ Gate 1 — Operator
*After M5. One recorded session, one real change, 60–120 minutes.*

Demonstrate, in order, in one session:
1. A blast-radius assessment written before starting (M3)
2. A four-part brief including the verification means (M3)
3. A verifier the agent runs itself, at least once, unprompted (M4)
4. One abandonment: a trajectory you discarded and re-briefed rather than corrected twice (M3)
5. A risk-ordered review of the resulting diff, with your read ratio stated (M5)
6. A log entry with prediction and actual (M1)

**Pass:** all six present, plus a 300-word retrospective naming the weakest of the six and what you will change.
**Common failure:** no abandonment, because the session went well. Then re-take it on a harder task — the abandonment reflex is the point, and it only trains under pressure.

### ▸ Gate 2 — Engineer
*After M9. Assembled from Phase 3 work plus Capstone B.*

Submit:
1. A context budget for your main repo: what loads, what it costs, what you removed and why (M6)
2. A change landed in unfamiliar code via research→plan→implement, with both artifacts and the spot-check record (M7)
3. A legibility audit with at least three remediations executed and their effect measured (M8)
4. An extension kit where every item traces to a named incident (M9)

**Pass:** all four, plus a written argument for one place where you deliberately deviated from the course's recommendation, with your evidence.

### ▸ Gate 3 — Orchestrator
*After M13. The highest-stakes gate; it licenses unattended operation.*

Submit:
1. A parallelism ceiling with the throughput curve and the binding constraint (M10)
2. A week of scheduled-loop logs with a correctness assessment, including at least one thing the loop got wrong (M11)
3. A review policy in actual force, with its misclassification rate (M12)
4. A completed trifecta audit with every all-three configuration remediated (M13)
5. Evidence of one successful prompt injection against your own agent in a sandbox, and the fix (M13)

**Pass:** all five. Item 5 is non-negotiable — you do not get to run unattended agents on the basis of believing you are safe.

---

## 6. Capstones

### Capstone A — Ship It
*After Gate 1. Effort ~10 h.*

Build and ship a small but real tool, end to end, with agents. Real means: someone other than you could use it, it is deployed or installable, and it has a README.

**Requirements**
- Scope: something you could hand-write in 4–8 hours
- Every task gets a verifier the agent can run (M4)
- Log every task (M1)
- Ship it — deployed, published, or installed by another human

**Deliverables:** the working thing; the log; a 500-word retrospective covering where agents were faster, where they were slower, and your read ratio for the final codebase.

**Rubric focus:** honesty about the slower parts. Everyone finds some. A retrospective claiming uniform speedup is not describing the experiment accurately.

### Capstone B — Land a Change in a Large Unfamiliar Codebase
*After Gate 2. Effort ~15 h.*

Take a real open-source project with >50k lines that you have never worked in. Find a real open issue. Land a fix using the full Phase 3 toolkit.

**Requirements**
- Research phase with no edit permission; three claims spot-checked against source (M7)
- Reviewed plan committed as an artifact before implementation
- Verification appropriate to the project's own standards
- **External signal required:** a submitted PR with maintainer response, or an independent review by a competent human who did not write it

**Deliverables:** research doc, plan, the PR link, the external feedback verbatim, and a 700-word analysis of where your process helped, where it added overhead, and what the maintainer's feedback revealed that your process missed.

**Rubric focus:** the gap between what you thought was good and what the maintainer thought. If there is no gap, you picked too easy a project.

**Note:** merge is not required. Maintainers are slow and PRs are rejected for reasons unrelated to quality. Substantive feedback is the signal.

### Capstone C — Operate an Autonomous Loop for a Week
*After Gate 3. Effort ~15–20 h over 7 days.*

Design, deploy, and operate an autonomous loop doing real work for seven consecutive days.

**Requirements**
- Real work with real consequences — no toy tasks
- All five loop components present (M11) plus persistent state
- Separate verifier agent; the worker does not grade itself
- Hard budget caps on tokens and wall-clock; a tested rollback; a kill switch
- Sandboxed per M13, with a written threat model
- An append-only action log
- **An incident log** — every time it did something wrong, surprising, wasteful, or unsafe

**Deliverables:** loop design doc; seven days of logs; the incident log; a cost accounting (tokens, money, your time); and a 1,000-word assessment answering: *did this produce value net of the supervision it required, and would you keep running it?*

**Rubric focus:** the incident log and the net-value judgment. **A Capstone C with an empty incident log fails.** Seven days of autonomous operation without incidents means the loop was trivially scoped, the logging was inadequate, or the incidents were not recognised. All three are findings you should report.

**Safety gate:** if at any point the loop touches production data, external users, or anything irreversible, stop and re-scope. The capstone is not worth an outage.

---

## 7. The doctrine document

The final deliverable and the one that outlives the course. 1,500–3,000 words. Structure in `CURRICULUM.md` M17.

| Dimension | Proficient | Expert |
|---|---|---|
| Positions | Takes clear positions with evidence from own work | Positions contradict at least one expert consensus, defensibly |
| Mind-changes | Identifies ≥2 real changes against the M1 beliefs statement, quoted | Explains *why* the earlier belief was held — the reasoning error, not just the wrong answer |
| Verification stack | Documents each rung honestly, gaps included | Explains what each rung cannot catch |
| Autonomy policy | Clear rules for what runs unattended | Rules derived from measured failure rates, not comfort |
| Disagreements | ≥3 specific, argued disagreements with named practitioners | Includes a disagreement the practitioner would find difficult to answer |
| Weaknesses | Names real ones specifically | Names them and states the experiment that would fix them |
| Refresh practice | Scheduled and concrete | Already executed once, with a diff |

---

## 8. Keeping yourself honest

There is no invigilator and no reason for one — you are doing this to get better at the work. But three habits are
easy to drop and expensive to lose, because each one protects a measurement you cannot reconstruct later:

1. **Predictions before results.** A prediction written after the fact is not a prediction, and it quietly destroys
   the value of every calibration measurement downstream. This is the one that matters most.
2. **Failures logged at the time.** Reconstructed failure logs are systematically rosier than real ones. You will
   not remember the twenty minutes you spent arguing with a doomed session; the log will.
3. **One external signal per phase.** Not for verification — for the blind spots you cannot see by definition. Show
   a colleague your Gate 1 session recording. Get a maintainer's response on Capstone B. Have someone else read your
   Capstone C incident log and tell you what you are minimizing.

Use agents freely for everything else. The judgment traces are worth writing yourself, not as a rule but because
writing them is where most of the thinking happens.
