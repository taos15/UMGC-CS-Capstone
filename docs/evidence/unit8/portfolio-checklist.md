# Unit 8 final portfolio checklist

Source: the contributor's supplied Unit 8 Assignment 1 instructions. This is a
preparation checklist, not a claim that the final release or submission is complete.
James Lambert reports working solo. Instructor approval of changes to team/review
requirements is not established by the supplied information.

## Part 1: repository link

| Requirement | Existing evidence | Remaining work |
| --- | --- | --- |
| Integrated functional system | Unit 5 packet records real React/FastAPI/PostgreSQL recommendation, feedback, and CRUD browser scenarios | Recheck the final submission commit and document remaining defects |
| Functional AI feature and value | Deterministic eligibility, R/P/C/E scoring, ranking, explanations, and stored evidence | Describe the rule-based recommendation engine precisely; do not claim learned models, NLP, embeddings, or measured relevance that are not demonstrated |
| CI evidence | Workflow includes lint, automated tests, frontend build, and PostgreSQL browser checks | Record successful Actions URL, commit SHA, and screenshots from an actual run |
| Deployment evidence | No deployed environment or completed deployment pipeline is established in the current packet | Choose deployment scope, demonstrate the actual process, and capture its result; a frontend build or local server alone is not hosted deployment evidence |
| Documentation | README, generated OpenAPI, migration/setup commands, API contracts, and debt register exist | User manual added at docs/user/manual.md; confirm deployment instructions once a target is agreed |
| Coverage | Earlier packet records 382 backend tests and 91 frontend tests, plus 3 browser scenarios | Local coverage measured: backend statements 97.21% / branches 89.23%; frontend lines 94.89% / branches 81.81%. See repository-evidence.md; rerun CI for the submitted commit |
| Performance / reliability | Functional failure tests and deterministic-order checks exist | Measured local P95 39.02 ms across 30 runs with 100 ACTIVE profiles; raw data and limits in recommendation-benchmark.json. Production/concurrent load remains unmeasured |
| Matching relevance | Varied demo dataset and reproducible score preview exist | Any relevance claim requires curated jobs and independently chosen acceptable results; do not infer relevance from score spread |
| Reviews / contributions | Labeled AI-assisted solo report and project history exist | Record actual contributor name and role, actual feedback, and instructor-approved solo arrangement or an independent review |

Historical test counts are observations from the Unit 5 readiness work, not new
Unit 8 measurements. The final evidence must identify its exact commit/environment.

## Part 2: stakeholder video

A [12-minute narration and demo script](../../portfolio/stakeholder-video-script.md)
and [recording checklist](../../portfolio/recording-checklist.md) are prepared.
The actual video still needs recording and duration verification.

Deliver MP4 or a hosted video link, lasting 10–15 minutes. A useful target is 12 minutes:

| Time | Content / demonstration |
| --- | --- |
| 0:00–1:15 | Problem: staffing by job titles misses structured evidence and certification eligibility |
| 1:15–2:30 | Solution, intended users, and human staffing authority |
| 2:30–4:00 | Architecture: React, FastAPI, repositories, PostgreSQL, and the pure matcher |
| 4:00–7:00 | Live login, OPEN job, ranked candidates, score/evidence explanations, and feedback |
| 7:00–8:30 | Profile editing and stale-version recovery; explain why historical runs remain unchanged |
| 8:30–10:00 | Actual CI, deployment, coverage, benchmark, and reliability evidence |
| 10:00–11:00 | Technical tradeoffs, limitations, and stakeholder value |
| 11:00–12:00 | Individual contribution, learning outcomes, and next improvements |

Do not replace absent metrics with invented numbers. Record the working system
and actual results. Remove secrets from terminal views and screenshots. Show the
fictional demo data, not real personnel records. A final script should be written
after repository evidence is collected, so its claims match the demonstrated build.

## Part 3: individual position paper

An [editable paper](../../portfolio/position-paper.md) and
[PDF](../../portfolio/James_Lambert_Position_Paper.pdf) are prepared with verified
400/450/450-word body sections. Personal review and final evidence updates remain.

Deliver a PDF with a 1,300-word paper body:

| Section | Words | Evidence and argument |
| --- | ---: | --- |
| System delivery and integration | 400 | Computational problem, iterative development, concrete code examples, AI value, and truthful solo delivery account |
| Methodology and performance evaluation | 450 | Architecture and process compared with authoritative SEI/IEEE guidance; actual coverage, latency, reliability results; strengths and limitations |
| Professional development roadmap | 450 | Specific skills/technologies, justified by current authoritative industry sources; milestones and a plan for evaluating adoption |

Confirm citation style and whether references/headings count toward the assigned
word limit. Plan an exactly 1,300-word body, with references clearly separated,
unless the instructor specifies a different counting rule. Gather current sources
when drafting; do not invent personal experience, feedback, metrics, or citations.

Describe the contribution imbalance professionally and connect it to workload,
process adaptations, and lessons. Do not present a solo report as independent
peer review. The contributor must read, personalize, and verify the position paper.

## Final submission packet

- [ ] Contributor name and accurate individual-contribution statement.
- [ ] GitHub link and final commit SHA.
- [ ] Successful CI run link and screenshots for that commit.
- [ ] Actual deployment evidence and installation/user documentation.
- [ ] Current coverage reports, benchmark data, and reliability results.
- [ ] Review evidence or written approval of the solo alternative.
- [ ] MP4 or hosted video link, checked for duration, audio, and legibility.
- [ ] PDF paper with verified 400/450/450 section counts and references.
- [ ] Known limitations consistent across code, documentation, video, and paper.

The pasted instructions say Tuesday at 11:59 p.m. Eastern but provide no calendar
date. Verify the dated deadline in the course portal; do not assume which Tuesday.

Measured Unit 8 results and outstanding external evidence are tracked in
[repository evidence](repository-evidence.md).

Suggested commit: `test: add Unit 8 coverage and PostgreSQL benchmark evidence`
