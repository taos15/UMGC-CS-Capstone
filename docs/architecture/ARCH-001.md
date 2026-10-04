# ARCH-001: canonical feature-oriented backend

The backend is a single installed package at `backend/src/skillmatch/`.
`skillmatch.main:app` is the sole FastAPI application. Root `pyproject.toml`,
`uv.lock`, `.python-version`, and the uv-based CI workflow remain authoritative.

## Boundaries

- Employees/jobs own public schemas, HTTP routers, and in-memory repositories.
  Their seed modules preserve the original runtime data and ordering.
- Recommendations own HTTP request/response schemas and candidate orchestration.
  The service reads the employee repository and creates frozen matching inputs.
- Matching owns tuple-based immutable employee/job DTOs, scoring, stable ranking,
  and explanations. It imports only its own modules, typing, and Pydantic.
- `core/config.py` owns the database URL; `db/` owns the shared SQLModel base,
  engine, session generator, and initialization.
- Health routes remain in the app composition module; public paths and response
  behavior are unchanged.

Files are created only for implemented responsibilities. Simple employee/job
reads do not add pass-through service modules. No auth/feedback/skills or matching
encoder/eligibility placeholders are created.

## Migration sequence and evidence

1. Original suite: `uv run pytest -q` — **9 passed**, 5 dependency warnings.
2. Added `tests/contract/test_architecture.py`; `uv run pytest -q
   tests/contract/test_architecture.py` — **3 expected failures**: missing canonical
   package, missing matching package, legacy source still present.
3. Added root build configuration, canonical features/DB/entrypoint, and temporary
   compatibility imports; `uv lock && uv sync --locked` succeeded.
4. Original tests plus canonical OpenAPI/import-boundary checks — **11 passed**.
5. Reorganized tests and added regression cases; focused unit/integration plus
   OpenAPI/import-boundary checks — **28 passed** after adapting a list comparison
   to the immutable tuple input representation.
6. Removed legacy modules only after canonical imports and focused tests passed.
7. Final `uv sync --locked && uv run pytest -q && git diff --check` succeeded:
   **30 passed**, the same 5 baseline dependency warnings, no whitespace errors.
8. From `/tmp/opencode`, the installed `.venv/bin/python -I` successfully imported
   `skillmatch.main` and loaded `uvicorn.Config("skillmatch.main:app")`, verifying
   the entrypoint independently of the repository working directory and pytest.

## Changed-file inventory

- Root: `.gitignore`, `README.md`, `pyproject.toml`, `pytest.ini`, `uv.lock`.
- Package: `backend/src/skillmatch/{__init__.py,main.py}`;
  `core/{__init__.py,config.py}`; `db/{__init__.py,base.py,session.py}`;
  `features/__init__.py`;
  `features/employees/{__init__.py,schemas.py,repository.py,seed.py,router.py}`;
  `features/jobs/{__init__.py,schemas.py,repository.py,seed.py,router.py}`;
  `features/matching/{__init__.py,schemas.py,scoring.py,ranking.py,explanations.py}`;
  `features/recommendations/{__init__.py,schemas.py,service.py,router.py}`.
- Tests: `tests/contract/test_architecture.py`,
  `tests/unit/test_matching_engine.py`, `tests/integration/api/test_api.py`,
  `tests/integration/database/test_database.py`; removed the original three
  `tests/test_*.py` paths after moving their coverage.
- Data: moved `sample_data/{employees.json,jobs.json}` to
  `data/sample/{employees.json,jobs.json}` without changing their contents.
- Docs: this file, `docs/technical_debt/architecture-migration.md`, and
  `resources/spec_bundle/project/repository_map.md`.
- Removed legacy `app/{__init__.py,main.py,schemas.py,data.py,employee_service.py,
  job_service.py,matching_engine.py,recommendation_service.py}`;
  `backend/{__init__.py,main.py,database.py}`;
  `backend/api/{__init__.py,auth.py,employee.py,job.py,matching.py,feedback_audit.py}`;
  `backend/{domain,repositories,matching,tests}/__init__.py`.

The pre-migration OpenAPI SHA-256 fingerprint is
`3a947396a8954a697bf1ec61a19587d4d5ae9dd1bd2cfea3284cbb47c0aaecb4`.
The contract test checks the same sorted OpenAPI document after migration.
Regression tests cover scores/rounding, explanations, defaults, validation,
candidate/threshold options, retrieval/errors, health degradation, and tied ranks.

See `docs/technical_debt/architecture-migration.md` for remaining feature and
persistence work. Local results are evidence only for the commands actually run;
they do not imply remote CI or deployment success.
