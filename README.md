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
