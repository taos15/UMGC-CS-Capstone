# SkillMatch AI project scope

## Source status

Canonical source: **SkillMatch AI Project Design Specification**, dated September 10, 2026. It defines one implementation target for the eight-week CMSC 495 prototype. Status: working project specification; Integration Lead review still pending.

Course coordination roles remain James Lambert (Lead Architect), Angel De La Cruz (Interface Designer), and Frank Petrakian (Integration Lead, pending review/contact). These roles are assignment/accountability context only and do not create code-ownership restrictions.

## Core purpose

SkillMatch AI is an explainable workforce decision-support system. It compares an `OPEN` job with `ACTIVE` employee profiles using structured skills, proficiency, experience, and certification evidence. It returns an ordered candidate list with component scores, matched/missing requirements, eligibility reasons, and evidence-based explanations. A supervisor retains final authority.

## Canonical technology direction

- React supervisor SPA.
- One FastAPI application.
- PostgreSQL persistence.
- Distinct in-process, Scikit-learn-compatible matching package with no direct HTTP or database access.
- Repository-level Python dependency management via `uv` (`pyproject.toml`, `.python-version`, `uv.lock`) in the latest supplied `dev`.

## In scope

- Structured employee profiles: skills, proficiency, certifications, experience, status.
- Structured jobs: required/preferred skills, minimum proficiency, certification rules, minimum experience.
- Explainable recommendation ranking and supervisor review.
- Validated mock CSV import and PostgreSQL persistence.
- 50-100 mock employees and 15-20 jobs for validation.
- Stored immutable match runs and supervisor feedback tied to those runs.

## Deferred

Resume/free-text NLP/custom language models; production HRIS/LMS/payroll/ATS/certification-provider integrations; automatic assignment; online self-learning/automatic weight promotion; production-scale concurrency claims; full assignment/outcome/training/location/schedule workflows.
