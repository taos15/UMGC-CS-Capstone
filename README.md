# SkillMatch AI

SkillMatch AI is an alpha workforce-matching prototype that recommends employees for jobs based on skills, certifications, and experience rather than job title alone. Recommendation results are decision support only: a supervisor remains the final decision-maker.

## Features

- Employee and job retrieval
- Ranked employee recommendations with transparent weighted scores
- Explainable score breakdowns for required skills, preferred skills, certifications, and experience
- Matched skills and certifications plus missing requirements
- FastAPI endpoint and interactive OpenAPI documentation
- Automated matching and API tests with GitHub Actions CI

## Project Structure

```text
backend/src/skillmatch/
  main.py        Canonical FastAPI application and health endpoints
  core/          Cross-cutting configuration
  db/            Shared SQLModel base, engine, and sessions
  features/      Employees, jobs, recommendations, and pure matching
tests/           Unit, API/database integration, and architecture contract tests
data/sample/     JSON examples of alpha seed data
docs/            Architecture, technical debt, workflow, and review guidance
```

## Run Locally

Requires [uv](https://docs.astral.sh/uv/getting-started/installation/). Python itself doesn't
need to be installed separately - `uv sync` downloads the version pinned in `.python-version`
(3.12) and creates `.venv` automatically.

```powershell
uv sync
uv run uvicorn skillmatch.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for the API documentation.

Root `pyproject.toml` installs `skillmatch` from `backend/src/` during `uv sync`.
Each implemented feature owns its HTTP/schema/data-access responsibilities.
Recommendation orchestration retrieves candidates and passes immutable DTOs to
matching, which has no HTTP or database dependencies.

See [architecture](docs/architecture/ARCH-001.md) and
[remaining technical debt](docs/technical_debt/architecture-migration.md).

## Example

Send a `POST` request to `/api/v1/jobs/job-electrician/recommendations`:

```json
{
  "candidateEmployeeIds": null,
  "topK": 5,
  "includeMissingSkills": true,
  "minimumScore": 0.0
}
```

Run the tests with:

```powershell
uv run pytest -q
```

## REST endpoint stubs and role annotations

All section 5 routes are registered under `/api/v1`, including
`GET /api/v1/health`. The original `/health` remains available for compatibility.
The listed routes represent 15 method/path operations.

OpenAPI descriptions and `x-allowed-roles` record the intended role policy:
read operations allow ADMIN, SUPERVISOR, and VIEWER; profile and skill writes
allow ADMIN; recommendations and feedback allow ADMIN and SUPERVISOR.
Match-run retrieval additionally requires authorized run scope. Login is public.
The health role policy is unspecified (`x-role-policy: unspecified`).

Workforce routes require a valid bearer token. Role annotations remain
documentation only; role enforcement is the separate AUTH-002 task. Existing employee retrieval, job
retrieval, recommendations, and health behavior remain functional. The remaining feature stubs
return HTTP 501 after authentication with `{"detail": "Not implemented"}`. Request/response
contracts for these placeholders will be connected during feature implementation.

## Local login

Configure `SKILLMATCH_JWT_SECRET` with a random secret of at least 32 bytes and
`SKILLMATCH_LOCAL_USERS` with a JSON object containing your local accounts:

```json
{
  "your-username": {
    "user_id": "<user UUID>",
    "role": "SUPERVISOR",
    "password_hash": "<salted scrypt hash>"
  }
}
```

Roles are ADMIN, SUPERVISOR, or VIEWER. There are no built-in accounts or
fallback signing keys. Supply these values through your local environment;
keep secrets and account configuration out of source control. Generate a
password hash interactively without placing the password in command history:

```sh
uv run python -c 'from getpass import getpass; from skillmatch.core.security import hash_password; print(hash_password(getpass("Password: ")))'
```

Login with JSON `{"username": "your-username", "password": "your-password"}` at
`POST /api/v1/auth/login`. Success returns `access_token`, `token_type: "bearer"`,
and `expires_in: 900`. Subsequent workforce requests use
`Authorization: Bearer <access_token>`. Tokens expire after 15 minutes; login
again to obtain a new token. Login responses use `Cache-Control: no-store`.
JWT signatures and expiry are handled by [PyJWT](https://pyjwt.readthedocs.io/en/v2.14.0/usage.html)
with a fixed HS256 algorithm.

Wrong passwords and unknown usernames return identical HTTP 401
`application/problem+json` responses with `AUTH_INVALID_CREDENTIALS` and the
generic detail `Invalid username or password.` Missing, invalid, or expired
bearer tokens return `AUTH_REQUIRED`. Both use `WWW-Authenticate: Bearer`.
Error bodies and every response carry matching request IDs. Invalid auth
configuration fails with generic HTTP 503 `AUTH_UNAVAILABLE`.
Health endpoints remain public. Role authorization and run-scope checks
remain AUTH-002 work; authentication alone does not enforce the role annotations.
