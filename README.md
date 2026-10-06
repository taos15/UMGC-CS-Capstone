# SkillMatch AI

SkillMatch AI recommends employees using structured skills, valid certifications,
and experience. Recommendations support human decisions; feedback never assigns
employees or retrains the live model. This project is being completed individually.

## Setup

Prerequisites: uv, Node.js 24 or newer, and PostgreSQL (the verified local server
was 14.24; CI uses 16). Root `pyproject.toml`, `.python-version`, and `uv.lock` are
the Python dependency source of truth. The canonical package is in
`backend/src/skillmatch/`; React is in `frontend/`.

```sh
uv sync --locked
npm --prefix frontend ci
```

Set `DATABASE_URL` to your PostgreSQL connection using the psycopg driver, for
example `postgresql+psycopg://<user>:<password>@localhost:5432/skillmatch`.
Create the database first. Supply credentials through the environment rather
than committing them. Run from the repository root:

```sh
uv run --locked alembic upgrade head
uv run --locked python scripts/seed_data.py
uv run --locked uvicorn skillmatch.main:app --reload
```

The seed script validates 10 fictional employees, 3 OPEN jobs, and 12 skill IDs
before writing, retains existing profiles, and never overwrites user edits.
See [mock dataset](data/mock/README.md) for three certification types, varied
scores, and a deterministic fixed-date preview. SQLite remains available for
local development when `DATABASE_URL` is omitted; it uses direct table creation.
PostgreSQL requires explicit migrations before application startup.

## Local authentication

Set `SKILLMATCH_JWT_SECRET` to a random secret of at least 32 bytes. Set
`SKILLMATCH_LOCAL_USERS` to a JSON object keyed by username:

```json
{"your-username":{"user_id":"<UUID>","role":"ADMIN","password_hash":"<scrypt hash>"}}
```

Generate a password hash without putting the password in shell history:

```sh
uv run --locked python -c 'from getpass import getpass; from skillmatch.core.security import hash_password; print(hash_password(getpass("Password: ")))'
```

Use ADMIN for profile/taxonomy administration, SUPERVISOR for recommendations
and feedback, or VIEWER for read access. There are no built-in accounts or
fallback signing secrets. Login issues a signed 15-minute bearer token; unknown
users and incorrect passwords receive the same generic 401 response. Tokens are
stored in memory/session storage; passwords are never stored. Server authorization
remains authoritative. ADMIN reads all runs; other roles read their own runs.

## Portal and API

```sh
npm --prefix frontend run dev
```

Open Vite's printed URL. The development proxy targets localhost port 8000;
`SKILLMATCH_API_PROXY_TARGET` changes that target. `VITE_API_BASE_URL` configures
the frontend API base, defaulting to `/api/v1`. Production hosting must route API
traffic to FastAPI; `npm run preview` serves assets only. API documentation is at
`http://127.0.0.1:8000/docs`.

After login, select an OPEN job and request recommendations. Results show the
server rank, score, R/P/C/E components, eligibility, matched/missing evidence,
explanation, match-run ID, and model version `rpce-55-20-15-10-v1`. Choose SELECTED,
NOT_SELECTED, or DEFERRED and optionally comment to append feedback to the run.

Employee and job profile pages create, read, update, and permanently delete
canonical profiles. Writes require ADMIN. PUT/DELETE include the last-read
version; stale changes return 409 STALE_VERSION, retain the draft, and require an
explicit reload. Deletion requires confirmation and retains historical runs
and feedback. Employee/job lists and skill IDs support `page` and `page_size`.

All responses carry `X-Request-ID`. Errors use RFC 9457 `application/problem+json`
with stable `code`, `request_id`, `detail`, and `field_errors`. The portal renders
safe guidance and correlation IDs. Database and matching failures return 503;
failed matches never persist partial runs. See the
[API contract](resources/spec_bundle/api/api_contract.md) for exact roles/shapes.

## Checks and CI

```sh
uv run --locked ruff check backend/src backend/migrations tests scripts
uv run --locked pytest -q
npm --prefix frontend run lint
npm --prefix frontend test
npm --prefix frontend run build
```

For the real browser/PostgreSQL integration check, create a disposable database
whose name ends in `_e2e`, set `SKILLMATCH_E2E_DATABASE_URL` to its psycopg URL,
and install Chromium. This check writes demo profiles, match runs, and feedback
in that database; it generates temporary local credentials and stops its servers.

```sh
node frontend/node_modules/@playwright/test/cli.js install chromium
uv run --locked python scripts/run_postgres_e2e.py
```

GitHub Actions runs backend lint/tests, frontend lint/tests/build, and the real
PostgreSQL browser scenarios. The `CI required` check fails if any job fails or
is skipped. A repository administrator must require this exact GitHub Actions
check for `dev` and `main`, require pull requests and up-to-date branches, and
preserve existing review requirements. The workflow alone does not enforce
branch protection. Unit 5 evidence must link a successful Actions run for the
exact submitted commit SHA; local results are not hosted CI evidence.

See [submission readiness](docs/evidence/unit5/submission-readiness.md),
[technical debt](docs/technical_debt/alpha-register.md), and
[solo review status](docs/peer_review/solo-review-status.md).

Unit 8: [repository evidence and measurements](docs/evidence/unit8/repository-evidence.md)
and [portfolio checklist](docs/evidence/unit8/portfolio-checklist.md). CI uploads
backend and frontend coverage reports; run `npm --prefix frontend run test:coverage`
for local frontend coverage and see the evidence document for backend/benchmark commands.

See the [user manual](docs/user/manual.md) for recommendation, feedback, profile,
and error-recovery workflows.

Unit 8 presentation preparation: [stakeholder video script](docs/portfolio/stakeholder-video-script.md)
and [recording checklist](docs/portfolio/recording-checklist.md).

Unit 8 individual paper: [editable draft](docs/portfolio/position-paper.md),
[PDF](docs/portfolio/James_Lambert_Position_Paper.pdf), and
[verification notes](docs/portfolio/position-paper-notes.md).
