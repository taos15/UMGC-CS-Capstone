> Historical check on checkout ea7cab5. Its blockers are superseded by the
> PostgreSQL/browser readiness evidence in [the current submission checklist](../evidence/unit5/submission-readiness.md).

# Integration check: full path blocked

Checked checkout `ea7cab5` with the requested scope: no new product features; fix existing breakage only.

## Observed checks

- Backend: `UV_PROJECT_ENVIRONMENT=/tmp/skillmatch-contracts-venv .venv/bin/uv run --locked pytest -q` — **328 passed**, 6 existing warnings.
- Frontend: `npm exec --yes --package=node@24 -- npm --prefix frontend test` — **68 passed** across 7 files.
- Production bundle: `npm exec --yes --package=node@24 -- npm --prefix frontend run build` — passed.
- No unresolved Git entries or conflict markers were found in source/tests/data.

A live HTTP smoke check started separate Uvicorn and Vite processes on ephemeral localhost ports, with a temporary SQLite database and ephemeral test-only supervisor credentials. Requests went through Vite's configured `/api` proxy without mocked HTTP responses:

1. Frontend HTML and transformed React entry were served successfully.
2. Login returned 200 and issued a bearer token.
3. Job list returned **501 NOT_IMPLEMENTED**.
4. Using an existing known job ID directly, job detail and recommendations returned 200.
5. A separate SQLModel session verified that the run and every returned candidate were stored before the response was inspected.
6. GET match-run returned exactly the recommendation evidence previously returned.
7. SELECTED feedback returned 201; retrieving the run again returned the unchanged snapshot.
8. Every tested API response carried `X-Request-ID`.

Temporary processes, credentials, and database were cleaned up. The live smoke check exercised HTTP/proxy/backend persistence, not automated browser interactions. React rendering/request behavior was covered by the frontend suite with its existing mocked API fixtures.

## Full-path blockers

- `GET /api/v1/jobs` remains a declared stub in `backend/src/skillmatch/features/jobs/router.py`. The live 501 response prevents React from listing/selecting a job.
- Employee/job repositories still load in-memory seeds rather than persistent employee/job tables. The new `data/mock` fixture is not connected to runtime repositories.
- The observed database dialect was SQLite. No `psycopg`, `psycopg2`, or `pg8000` driver was installed, and no local Docker/psql/pg_ctl executable was available. Postgres was not exercised.
- PostgreSQL migrations and persisted profile loading remain dedicated implementation work, as documented in `docs/technical_debt/architecture-migration.md` and DB-003.

The complete React -> FastAPI -> repository -> Postgres -> matcher -> stored run -> React path is **not verified and cannot pass this checkout as-is**. Completing the stub and persistence prerequisites would add missing functionality beyond this integration-only scope. No regression was observed in the implemented paths, so this pass records evidence and blockers without adding product behavior.
