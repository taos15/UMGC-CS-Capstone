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
app/             FastAPI application, service modules, and matching engine
backend/         Backend entrypoint and scaffold (api, domain, repositories, matching, tests)
tests/           Matching-engine and API tests
sample_data/     JSON representations of the alpha seed data
docs/            Team workflow and peer-review guidance
```

## Run Locally

Requires [uv](https://docs.astral.sh/uv/getting-started/installation/). Python itself doesn't
need to be installed separately - `uv sync` downloads the version pinned in `.python-version`
(3.12) and creates `.venv` automatically.

```powershell
uv sync
uv run uvicorn backend.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for the API documentation.

`backend.main` reuses the existing application in `app.main`. The modules in
`backend/api` are empty placeholders for Employee, Job, Matching, Feedback/Audit,
and Auth; the remaining backend packages reserve space for future implementation.

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
