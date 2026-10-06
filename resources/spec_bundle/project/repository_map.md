# Repository map - canonical backend after ARCH-001

Updated for the behavior-preserving migration to the feature-oriented modular monolith.

| Path | Observed responsibility | Target/migration note |
| --- | --- | --- |
| `pyproject.toml` | Python metadata/dependencies | Keep at repo root. |
| `uv.lock` | locked dependency graph | Keep committed and consumed by CI. |
| `.python-version` | interpreter pin | Keep at repo root. |
| `.github/workflows/ci.yml` | uv-based CI | Preserve semantics while migrating. |
| `backend/src/skillmatch/main.py` | canonical FastAPI application, health, router composition | Startup: `skillmatch.main:app`. |
| `backend/src/skillmatch/core/config.py` | environment configuration | Preserves `DATABASE_URL` and SQLite default. |
| `backend/src/skillmatch/db/` | SQLModel base, engine/session/init | SQLite/create_all remain transitional. |
| `backend/src/skillmatch/features/employees/` | schemas, in-memory repository/seed, HTTP reads | Persistence implementation remains a separate story. |
| `backend/src/skillmatch/features/jobs/` | schemas, in-memory repository/seed, HTTP reads | Persistence implementation remains a separate story. |
| `backend/src/skillmatch/features/matching/` | immutable inputs, scoring, ranking, explanations | No HTTP/database/repository ownership; existing formula preserved. |
| `backend/src/skillmatch/features/recommendations/` | request/response schemas, router, orchestration | Retrieves candidates and converts inputs to immutable matching DTOs. |
| `data/sample/` | moved JSON seed examples | Employee example is a two-employee subset of the three-employee runtime seed. |
| `tests/unit/` | matching behavior and immutable inputs | Canonical imports. |
| `tests/integration/api/` | endpoint regression coverage | Canonical app. |
| `tests/integration/database/` | connection, initialization, session coverage | Canonical DB infrastructure. |
| `tests/contract/` | OpenAPI fingerprint and architecture boundaries | Protects ARCH-001. |
| `app/`, old backend scaffold | removed after canonical tests passed | No compatibility modules remain. |
