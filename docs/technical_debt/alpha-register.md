# Alpha technical-debt register

Owner for all implementation items: the solo contributor. Priorities below are
relative to submission; no retirement date or unmeasured metric is fabricated.

| Item / evidence | Benefit of current choice | Impact and affected area | Priority / mitigation / retirement evidence |
| --- | --- | --- | --- |
| Profile evidence stored as JSON (`employees/models.py`, `jobs/models.py`) | Preserves canonical nested contracts with small feature-local repositories | Database cannot enforce skill-reference integrity inside JSON; ad hoc analytics/filtering may require scans | Medium. API validation checks taxonomy. Normalize skill/cert evidence when query needs justify it; require migration, relationship tests, and equivalent snapshot results before retirement. |
| Private legacy matching DTO adapters (`employees/repository.py`, `jobs/repository.py`) | Preserves tested scoring while exposing canonical profile APIs | Two representations must remain synchronized; adapters add maintenance cost | Medium. Contract/evidence tests and browser checks cover current boundary. Retire adapters by changing the orchestrator to canonical DTOs with unchanged score/eligibility/ranking tests. |
| SQLite direct `create_all` for local/tests (`db/session.py`) | Fast, isolated tests and easy development setup | SQLite cannot establish PostgreSQL behavior or migrate existing local schema changes | Low for local use. PostgreSQL uses Alembic and browser integration CI. Stop using SQLite for release evidence; retain the shortcut only while explicitly documented. |
| Local environment-managed users (`auth/repository.py`) | Small, fail-closed Alpha authentication with no built-in credentials | Operational account provisioning/revocation requires configuration updates | Medium before wider deployment. Add managed identity or persisted account lifecycle separately; verify revoked-account rejection and role/scope parity. Use TLS outside localhost. |
| Dependency warnings / React-compatible ESLint 9 | Avoids unrelated dependency migrations; preserves existing interfaces | Six backend warnings remain; ESLint 9 is deprecated and React plugin currently declares compatibility through 9 | Medium. Upgrade compatible dependency pairs, test schema aliases and session behavior, and retire only after warnings disappear without weakening tests. |
| Deterministic rules, limited relevance evidence | Reproducible transparent R/P/C/E recommendations | Demo score spread does not prove staffing relevance or the specified performance/relevance targets | High before claiming measured quality. Run the required 30-run/100-profile P95 benchmark; curate 15 jobs and independent acceptable candidates. Record actual outcomes, not inferred metrics. |

## Retired in this readiness change

- Runtime seed-only employee/job repositories: replaced with database-backed
  canonical profiles and explicit validated demo loading.
- REST stubs for profiles, job listing, and skill taxonomy: replaced with
  authorized operations and exact approved contracts.
- Missing PostgreSQL driver/migrations: psycopg and Alembic now provision the
  schema; real PostgreSQL migrations and browser workflows were observed.
- Snapshot hash based only on IDs/options: now hashes matching evidence,
  snapshot date, options, and model version. A regression test changes experience
  evidence and verifies a changed hash; display title remains outside scoring.

## External release prerequisites, not code shortcuts

Hosted CI for the final submitted SHA, required branch protection, and an
instructor-approved solo peer-review arrangement remain separately verifiable
submission requirements. See the submission checklist; do not mark them resolved
because local tests pass.
