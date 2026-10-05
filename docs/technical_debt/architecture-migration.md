# Persistence and feature follow-ups after ARCH-001

- Employee and job repositories still read the original in-memory seed lists.
  Persisting these records is a dedicated database/feature story.
- SQLite remains the default database. `init_db()` uses SQLModel `create_all`;
  it does not migrate existing schemas. PostgreSQL/Alembic completion is separate.
- `data/sample/employees.json` preserves the existing two-employee example.
  Runtime seed data additionally contains Sam Rivera. JSON examples are not
  runtime inputs; a validated import story should reconcile that dataset explicitly.
- REC-001 wired `features/recommendations/service.py` to the canonical
  eligibility/scoring engine (`features/matching/{canonical_scoring,eligibility}.py`)
  and to the DB-002 repositories: every successful recommendation request now
  snapshots `ACTIVE` candidates, scores/ranks them, and persists the match run
  before responding. `GET /api/v1/match-runs/{match_run_id}` now returns persisted
  snapshots (REC-002), with ADMIN access to all runs and requester-only access
  for SUPERVISOR/VIEWER. Retrieval does not invoke matching. The feedback endpoint (FDBK-001) now appends scoped,
  validated human decisions to audit history without assignment or model updates.
- `Employee`/`Job` gained a `status` field and structured scoring evidence
  (`skill_evidence`/`certification_evidence`/`skill_requirement_details`) as
  part of REC-001, additive to the existing flat fields so prior employee/job
  read/write behavior is unchanged. See the "Approved recommendation-
  orchestration amendment" in `resources/spec_bundle/api/api_contract.md`.
- CSV import, offline evaluation, and the full React implementation still
  require their own stories.
- The baseline dependency warnings (Starlette/AnyIO portal deprecation and
  Pydantic request-field alias warnings) remain reproducible. Existing request
  behavior and OpenAPI are covered; dependency/schema remediation is separate.
