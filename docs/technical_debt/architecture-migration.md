# Persistence and feature follow-ups after ARCH-001

- Employee and job repositories still read the original in-memory seed lists.
  Persisting these records is a dedicated database/feature story.
- SQLite remains the default database. `init_db()` uses SQLModel `create_all`;
  it does not migrate existing schemas. PostgreSQL/Alembic completion is separate.
- `data/sample/employees.json` preserves the existing two-employee example.
  Runtime seed data additionally contains Sam Rivera. JSON examples are not
  runtime inputs; a validated import story should reconcile that dataset explicitly.
- Auth, skills taxonomy, feedback/audit, match-run persistence, CSV import,
  offline evaluation, and React implementation still require their own stories.
  No empty feature modules were added during the architecture migration.
- The baseline dependency warnings (Starlette/AnyIO portal deprecation and
  Pydantic request-field alias warnings) remain reproducible. Existing request
  behavior and OpenAPI are covered; dependency/schema remediation is separate.
