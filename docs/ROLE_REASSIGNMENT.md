# Role Reassignment: Integration Lead Responsibilities

## Background

Per the project design specification (Section 10, Team Ownership and Cross-Review),
Frank Petrakian was assigned Integration Lead, owning AI feature integration, the
scoring flow, the human decision gate, the feedback loop, the external adapter
boundary, and the end-to-end integration sequence. Frank has been unreachable since
before implementation started (the specification itself records him as "pending
review/contact") and has not participated in Alpha development.

With the Unit 5 Alpha and Unit 8 Final Portfolio deadlines approaching, James Lambert
and Angel De La Cruz made the decision to stop waiting on Frank and temporarily absorb
his responsibilities so development is not blocked.

## Effective Date

2026-09-28, by mutual agreement of the two active team members.

## Responsibility Split

| Original Integration Lead responsibility | Reassigned to | Notes |
|---|---|---|
| Matching Orchestrator (snapshot creation, repository calls, engine invocation, match-run persistence) | James | Extension of existing Lead Architect ownership of architecture and data-flow consistency |
| AI Matching Package (scoring, eligibility rules, ranking, explanations) | James | Same rationale |
| End-to-end integration sequence (React -> FastAPI -> matcher -> stored run -> React) | James | Owns final integration per existing Lead Architect cross-review duty |
| API <-> AI data contracts, recommendation request/response format | Angel | Extension of existing Interface Designer ownership of endpoint specs and schemas |
| Feedback loop / human decision gate interface | Angel | Same rationale |
| External adapter boundary (mock CSV import path) | Angel | Same rationale |

This split follows each person's existing Lead Architect / Interface Designer
ownership areas rather than creating a new, unfamiliar assignment.

## Unreviewed Items

Specification Section 12 ("Items Frank Should Review When He Rejoins") lists five
sign-offs that were assigned to Frank as Integration Lead: the in-process matcher /
future-extraction boundary, the 55/20/15/10 scoring weights and eligibility/tie-break
rules, the necessity of assignment/outcome functionality, the mock-CSV-to-offline-
evaluation integration path, and the endpoint/DTO naming. James and Angel are deciding
these by mutual agreement instead. This is a deliberate, acknowledged gap in cross-
review coverage - not an oversight - and is recorded here so it can be cited directly
in the Unit 5 Refinement Reports as an identified technical debt item (reduced
architectural review coverage) with its mitigation (two-person mutual review in place
of a third independent reviewer).

## Instructor Notification

The team notified the course instructor of Frank's non-participation on
[DATE - confirm and fill in]. Reference that communication here once sent.

## If Frank Rejoins

Reassigned items revert to standard ownership per the specification's original
Section 10 role assignments. Any decisions made under this reassignment (see
"Unreviewed Items" above) should be reviewed by Frank against the criteria in
specification Section 12 before being considered final.

## Acknowledgment

- James Lambert
- Angel De La Cruz
