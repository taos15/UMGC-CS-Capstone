# Persistence and feature follow-ups after ARCH-001

- Employee and job repositories still read the original in-memory seed lists.
  Persisting these records is a dedicated database/feature story.
- SQLite remains the default database. `init_db()` uses SQLModel `create_all`;
  it does not migrate existing schemas. PostgreSQL/Alembic completion is separate.
- `data/sample/employees.json` preserves the existing two-employee example.
  Runtime seed data additionally contains Sam Rivera. JSON examples are not
  runtime inputs; a validated import story should reconcile that dataset explicitly.
- DB-002 added `features/recommendations/{models.py,repository.py}` (MatchRun,
  CandidateResult) and `features/feedback/{models.py,repository.py}` (Feedback),
  covering the persistence boundary only. No router/service calls these
  repositories yet - wiring a live recommendation request to actually persist
  a match run, and exposing `GET /api/v1/match-runs/{id}` and the feedback
  endpoint, remain separate stories (REC-002, FDBK-001).
- Auth, skills taxonomy, CSV import, offline evaluation, and React
  implementation still require their own stories. No empty feature modules
  were added during the architecture migration or DB-002.
- The baseline dependency warnings (Starlette/AnyIO portal deprecation and
  Pydantic request-field alias warnings) remain reproducible. Existing request
  behavior and OpenAPI are covered; dependency/schema remediation is separate.
