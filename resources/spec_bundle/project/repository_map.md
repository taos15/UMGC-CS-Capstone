# Repository map - latest supplied `dev`

Snapshot basis: `capstone_project_uv-version.tar.gz`, supplied as the latest `dev` before this package update.

| Path | Observed responsibility | Target/migration note |
| --- | --- | --- |
| `pyproject.toml` | Python metadata/dependencies | Keep at repo root. |
| `uv.lock` | locked dependency graph | Keep committed and consumed by CI. |
| `.python-version` | interpreter pin | Keep at repo root. |
| `.github/workflows/ci.yml` | uv-based CI | Preserve semantics while migrating. |
| `app/main.py` | active FastAPI routes | transitional; migrate feature-by-feature. |
| `app/schemas.py` | current schemas | split by feature while preserving contracts. |
| `app/data.py` | in-memory seed objects | replace runtime globals with repositories; reusable mock data -> `data/sample/`. |
| `app/employee_service.py` | employee reads | -> `features/employees/`. |
| `app/job_service.py` | job reads | -> `features/jobs/`. |
| `app/matching_engine.py` | existing matcher | move behavior-preserving first; formula change only via MATCH story. |
| `app/recommendation_service.py` | recommendation orchestration | -> `features/recommendations/service.py`. |
| `backend/main.py` | compatibility entrypoint | temporary re-export allowed. |
| `backend/database.py` | SQLModel engine/session/init | -> `skillmatch/db/`; SQLite remains transitional if still present. |
| `backend/api`, `backend/domain`, `backend/repositories`, `backend/matching` | scaffold placeholders | do not preserve as target layers. |
| `tests/` | current API/database/matching tests | preserve, then organize into unit/integration/contract. |
