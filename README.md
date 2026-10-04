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
tests/           Matching-engine and API tests
sample_data/     JSON representations of the alpha seed data
docs/            Team workflow and peer-review guidance
```

## Run Locally

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for the API documentation.

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
pytest -q
```

## Errors and request correlation

Every HTTP response includes `X-Request-ID`. An incoming value containing
1–128 ASCII letters, digits, dots, underscores, or hyphens is echoed; absent
or invalid values are replaced with a UUID. Error bodies carry the same ID.

HTTP errors, invalid requests, and unexpected application failures use
`application/problem+json` following [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html):

```json
{
  "type": "about:blank",
  "title": "Unprocessable Entity",
  "status": 422,
  "code": "VALIDATION_ERROR",
  "request_id": "trace-123",
  "detail": "Request validation failed.",
  "field_errors": [
    {"field": "body.topK", "code": "greater_than_equal", "message": "Input should be greater than or equal to 1"}
  ]
}
```

`field_errors` is empty for non-validation errors. Field paths include their
request location and use dots between nested segments. HTTP status codes and
headers such as `Allow` and `WWW-Authenticate` are preserved. Unexpected
failures return a generic `INTERNAL_ERROR`; exceptions are logged with the
request ID. Failures after streaming headers have been sent cannot replace
an already-started response.

Recommendation responses also include snake_case `match_run_id` (a fresh UUID
for each generation) and `model_version` (`rules-v1`, identifying the existing
50/10/25/15 scoring rules). Run IDs identify generated responses; runs are not
persisted by this implementation. Existing recommendation fields retain their
current names and behavior.
