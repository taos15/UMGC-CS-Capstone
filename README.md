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
