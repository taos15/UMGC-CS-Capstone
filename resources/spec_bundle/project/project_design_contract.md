# Project Design Specification implementation contract

This file translates the SkillMatch AI Project Design Specification into implementation invariants while preserving its terminology and scope.

## Architectural intent

- React SPA + one FastAPI process + PostgreSQL.
- Layered modular monolith with serious internal boundaries.
- AI matcher is a distinct in-process package with a narrow extraction point and no direct HTTP/database access.
- Matching is deterministic, versioned, explainable, and has no online self-training.
- Supervisor feedback/selection is recorded against a match run; no endpoint automatically assigns employees.
- MVP external integration is validated mock CSV only; enterprise integrations remain future-facing.

## Responsibility contract

| Module | Owns | Must not own |
| --- | --- | --- |
| React Supervisor Portal | UI state, routing, forms, accessible display, typed API client | scoring formulas, raw SQL, authorization decisions |
| REST API / Controllers | routes, Pydantic schemas, status codes, OpenAPI, request IDs | persistence logic, ranking calculations |
| Authentication & RBAC | JWT validation, role checks, auth audit events | employee/job domain rules |
| Employee Profiles | employee DTOs, skill/certification evidence rules, status transitions | job rules, ranking |
| Job Requirements | required/preferred skill rules, job status, validation | candidate ranking |
| Recommendation Orchestrator | auth context, snapshots, repository calls, matching invocation, match-run persistence | feature math, UI rendering, raw SQL |
| AI Matching Package | taxonomy/config versioning, eligibility, scoring, ranking, explanations | HTTP, ORM/database sessions, automatic staffing decisions |
| Feedback & Audit | supervisor feedback validation, audit metadata, offline-export eligibility | changing the live model |
| Repository boundary | queries, transactions, indexes, persistence mapping | HTTP behavior, score logic |

## Recommendation / feedback flow

1. Supervisor selects an `OPEN` job in React.
2. React calls `POST /api/v1/jobs/{job_id}/recommendations` with bearer token/options.
3. FastAPI validates auth, role, schema, and job state.
4. Orchestrator snapshots input and loads the job plus `ACTIVE` candidates through repositories.
5. Immutable DTOs go to matching; matching does not query PostgreSQL or external services.
6. Matching applies eligibility, component scores, deterministic ranking, and structured explanations.
7. Backend persists match run, model/config version, snapshot hash, options, rankings, and explanation details before returning.
8. Supervisor records `SELECTED`, `NOT_SELECTED`, or `DEFERRED` feedback against the stored run.
9. Separate offline evaluation may compare reviewed feedback with curated expected matches. Production requests never auto-retrain/promote a model.

## Change-control rule

If code changes a defined interface, scoring rule, data contract, or module boundary, update the focused canonical contract or record an approved amendment **before** implementation continues.

## Future extension contract

Keep these outside the core recommendation MVP unless an approved later milestone explicitly activates them:

- resume/free-text NLP or custom language models;
- production HRIS/LMS/payroll/ATS/certification-provider integrations;
- formal assignment approval/override/outcome workflows;
- automatic staffing decisions;
- online self-learning or automatic model/weight promotion;
- training-catalog recommendation workflows;
- location, availability, and schedule optimization;
- production-scale concurrency/availability claims beyond observed prototype evidence.

The matcher remains an in-process package for the MVP but keeps a narrow interface so it can be extracted into a separate service later if real scale/operations justify it.

## Pending design-review items from the supplied specification

The supplied Project Design Specification records Integration Lead review/contact as pending. When that review occurs, capture any approved amendments before changing implementation contracts. Specific items called out for review are:

- in-process MVP matcher and future extraction boundary;
- 55/20/15/10 scoring weights, mandatory-certification eligibility, and deterministic tie-break;
- whether any assignment/outcome functionality is actually required by the course milestone or should remain deferred;
- mock CSV -> PostgreSQL -> matcher -> feedback -> offline evaluation integration risk;
- endpoint names and shared DTO fields.

Do not block unrelated implementation solely because this review is pending; do not represent unreviewed changes as approved amendments.
