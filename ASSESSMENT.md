# Assessment

**Version 1.0 · Companion to `SYLLABUS.md` and `CURRICULUM.md`**

---

## 1. Philosophy

This course assesses **judgment**, not output. An agent can produce every artifact here in an afternoon; what it cannot fake is a record of decisions you made, measurements you took, and predictions that turned out wrong.

Accordingly, every rubric weights three things:

1. **The artifact exists and works** — necessary, not sufficient, and worth the least.
2. **The measurement is real** — numbers from your own logs, with the awkward ones included.
3. **The judgment trace** — why you chose this, what you rejected, what surprised you, what you would do differently. This is the bulk of the grade.

A submission with an impressive artifact and no judgment trace scores **Working** at best. A submission with a modest artifact, an honest null result, and a sharp analysis of why, scores **Proficient**.

**On failure reporting.** Any capstone or gate with no failures reported is presumed under-reported and does not pass. This is not a stylistic preference: unattended agent work fails regularly, and a practitioner who is not seeing failures is not looking.

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
| M0 | Log (≥20 rows, ≥4 controls), beliefs statement, annotated session | Control tasks actually done; predictions recorded *before* |
| M1 | Working agent, four-experiment table, one harness feature, teardown | Predictions written before running the break experiments |
| M2 | 5 rewritten briefs, calibration factor, abandonment log, briefing standard | Evidence of abandoning something that felt nearly done |
| M3 | Verifier audit, <15s fast lane, same-context test comparison, gaming catalogue, non-test loop | A measured sub-15-second command that the agent runs unprompted |
| M4 | Review-method comparison, comprehension audit, tuned reviewer, upstream experiment | Read ratio measured honestly and a repaid module |
| M5 | Context census, before/after audit, compaction artifact, rot threshold, subagent spec | A deletion from the always-on file justified by evidence |
| M6 | Verified research doc, plan with scored objections, ratio experiment, reused plan | Spot-checks of research claims against actual source |
| M7 | Scored legibility audit, hygiene sweep, deterministic suite, greppability repair, 2 enforced conventions | Ten consecutive identical test runs |
| M8 | Correction taxonomy, blocking hook, review subagent, MCP cost table | Every extension traced to a specific personal failure |
| M9 | Isolation comparison, throughput curve, decomposition, control plane | A stated ceiling with the constraint that sets it |
| M10 | Terminating loop, 3 stop conditions, overbaking account, verified fan-out, week of logs | A defect the verifier agent caught that the worker missed |
| M11 | Handoff breakdown, phone friction list, review policy, CI agent + threat model | A review policy applied retrospectively with a misclassification rate |
| M12 | Trifecta audit, red-team table, verified sandbox, threat model, supply-chain guardrail | A demonstrated successful injection against your own agent |
| M13 | Eval suite (≥10 tasks), variance table, controlled comparison, memory-file eval | A minimum effect size stated before comparing |
| M14 | Extended agent, token profile improvement, workflow agent, orchestration comparison | Survives compaction and restart on a multi-hour task |
| M15 | Bottleneck analysis, team memory file, review policy, debt register | Memory file rules traced to ≥2 historical review comments |
| M16 | Capstone C, doctrine document, re-run measurements, practice schedule, teaching artifact | The "what I changed my mind about" section, quoted against M0 |

---

## 5. Gate assessments

Gates test **integration**, not recall. Each is a single recorded session or a single change, in a real repository, demonstrating several modules at once.

### ▸ Gate 1 — Operator
*After M4. One recorded session, one real change, 60–120 minutes.*

Demonstrate, in order, in one session:
1. A blast-radius assessment written before starting (M2)
2. A four-part brief including the verification means (M2)
3. A verifier the agent runs itself, at least once, unprompted (M3)
4. One abandonment: a trajectory you discarded and re-briefed rather than corrected twice (M2)
5. A risk-ordered review of the resulting diff, with your read ratio stated (M4)
6. A log entry with prediction and actual (M0)

**Pass:** all six present, plus a 300-word retrospective naming the weakest of the six and what you will change.
**Common failure:** no abandonment, because the session went well. Then re-take it on a harder task — the abandonment reflex is the point, and it only trains under pressure.

### ▸ Gate 2 — Engineer
*After M8. Assembled from Stage 2 work plus Capstone B.*

Submit:
1. A context budget for your main repo: what loads, what it costs, what you removed and why (M5)
2. A change landed in unfamiliar code via research→plan→implement, with both artifacts and the spot-check record (M6)
3. A legibility audit with at least three remediations executed and their effect measured (M7)
4. An extension kit where every item traces to a named incident (M8)

**Pass:** all four, plus a written argument for one place where you deliberately deviated from the course's recommendation, with your evidence.

### ▸ Gate 3 — Orchestrator
*After M12. The highest-stakes gate; it licenses unattended operation.*

Submit:
1. A parallelism ceiling with the throughput curve and the binding constraint (M9)
2. A week of scheduled-loop logs with a correctness assessment, including at least one thing the loop got wrong (M10)
3. A review policy in actual force, with its misclassification rate (M11)
4. A completed trifecta audit with every all-three configuration remediated (M12)
5. Evidence of one successful prompt injection against your own agent in a sandbox, and the fix (M12)

**Pass:** all five. Item 5 is non-negotiable — you do not get to run unattended agents on the basis of believing you are safe.

---

## 6. Capstones

### Capstone A — Ship It
*After Gate 1. Effort ~10 h.*

Build and ship a small but real tool, end to end, with agents. Real means: someone other than you could use it, it is deployed or installable, and it has a README.

**Requirements**
- Scope: something you could hand-write in 4–8 hours
- Every task gets a verifier the agent can run (M3)
- Log every task (M0)
- Ship it — deployed, published, or installed by another human

**Deliverables:** the working thing; the log; a 500-word retrospective covering where agents were faster, where they were slower, and your read ratio for the final codebase.

**Rubric focus:** honesty about the slower parts. Everyone finds some. A retrospective claiming uniform speedup is not describing the experiment accurately.

### Capstone B — Land a Change in a Large Unfamiliar Codebase
*After Gate 2. Effort ~15 h.*

Take a real open-source project with >50k lines that you have never worked in. Find a real open issue. Land a fix using the full Stage 2 toolkit.

**Requirements**
- Research phase with no edit permission; three claims spot-checked against source (M6)
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
- All five loop components present (M10) plus persistent state
- Separate verifier agent; the worker does not grade itself
- Hard budget caps on tokens and wall-clock; a tested rollback; a kill switch
- Sandboxed per M12, with a written threat model
- An append-only action log
- **An incident log** — every time it did something wrong, surprising, wasteful, or unsafe

**Deliverables:** loop design doc; seven days of logs; the incident log; a cost accounting (tokens, money, your time); and a 1,000-word assessment answering: *did this produce value net of the supervision it required, and would you keep running it?*

**Rubric focus:** the incident log and the net-value judgment. **A Capstone C with an empty incident log fails.** Seven days of autonomous operation without incidents means the loop was trivially scoped, the logging was inadequate, or the incidents were not recognised. All three are findings you should report.

**Safety gate:** if at any point the loop touches production data, external users, or anything irreversible, stop and re-scope. The capstone is not worth an outage.

---

## 7. The doctrine document

The final deliverable and the one that outlives the course. 1,500–3,000 words. Structure in `CURRICULUM.md` M16.

| Dimension | Proficient | Expert |
|---|---|---|
| Positions | Takes clear positions with evidence from own work | Positions contradict at least one expert consensus, defensibly |
| Mind-changes | Identifies ≥2 real changes against the M0 beliefs statement, quoted | Explains *why* the earlier belief was held — the reasoning error, not just the wrong answer |
| Verification stack | Documents each rung honestly, gaps included | Explains what each rung cannot catch |
| Autonomy policy | Clear rules for what runs unattended | Rules derived from measured failure rates, not comfort |
| Disagreements | ≥3 specific, argued disagreements with named practitioners | Includes a disagreement the practitioner would find difficult to answer |
| Weaknesses | Names real ones specifically | Names them and states the experiment that would fix them |
| Refresh practice | Scheduled and concrete | Already executed once, with a diff |

---

## 8. Self-assessment integrity

A self-paced course has no invigilator, so these three rules carry the weight:

1. **Predictions before results, always.** A prediction written after the fact is not a prediction and quietly destroys the value of every measurement downstream.
2. **Failures logged at the time.** Reconstructed failure logs are systematically rosier than real ones.
3. **One external signal per stage.** Gate 1: show a colleague your session recording. Capstone B: a maintainer or independent reviewer. Capstone C: someone else reads your incident log and tells you what you are minimizing.

If you are using an agent to help produce these artifacts — and you should be, it would be strange not to — use it for the mechanical parts and write the judgment traces yourself. The judgment trace is the entire point. Outsourcing it means completing a course about thinking without doing any.
