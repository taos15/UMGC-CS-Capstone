# Reproducible mock dataset

All people, jobs, issuers, and credential records are fictional demonstration data.

- `employees.json`: 10 canonical `EmployeeProfile` records (9 ACTIVE, 1 INACTIVE), with UUIDs, unique employee numbers, version fields, proficiency, skill experience/recency, and dated certifications.
- `jobs.json`: 3 canonical OPEN `JobProfile` records, each with weighted REQUIRED/PREFERRED skills and a mandatory certification.
- `skills.json`: 12 unique controlled skill IDs referenced by the profiles.
- `certification_codes.json`: 3 certification types: licensed electrician, EPA 608, OSHA 10. Employees may hold multiple credential instances of those types.
- `score_preview.json`: observed diagnostic ranks/scores/eligibility from the actual canonical engine, with model version `rpce-55-20-15-10-v1` and fixed date **2026-10-05**.

## Deliberate variation

| Job | High eligible example | Medium eligible example | Low eligible example |
| --- | --- | --- | --- |
| Commercial Electrician | Alex Morgan: 100.00 | Jordan Lee: 76.24 | Casey Park: 23.86 |
| HVAC Service Technician | Sam Rivera: 100.00 | Taylor Brooks: 79.83 | Casey Park: 16.25 |
| Facilities Maintenance Technician | Riley Chen: 100.00 | Jamie Patel: 61.90 | Casey Park: 21.49 |

These are observed scores, not manual labels returned by the matcher. Fixture tests require at least one eligible score >=85, one between 40 and 80, and one <=35 for each job. Skills, proficiency, preferred-skill coverage, and experience vary. Casey has valid credentials but substantial skill/experience gaps, so scores fall without a skill-based hard exclusion. Quinn's OSHA 10 credential expired on 2025-12-31; Avery is INACTIVE despite strong evidence. Other candidates deliberately lack a job's mandatory credential.

The diagnostic preview includes ineligible candidates to show their reasons. Production orchestration filters out INACTIVE employees before matching and excludes other ineligible candidates by default. Nothing in this dataset assigns employees.

## Verify / regenerate

From the repository root:

```bash
uv run --locked python scripts/preview_mock_dataset.py
uv run --locked pytest -q tests/contract/test_mock_dataset.py
```

To regenerate the versioned preview:

```bash
uv run --locked python scripts/preview_mock_dataset.py > data/mock/score_preview.json
```

The optional `--as-of YYYY-MM-DD` evaluates credential validity on a different explicit date. Tests compare the checked-in preview against a fresh engine run at the fixed date, preventing silently stale score documentation.

This fixture uses established JSON profile contracts. After configuring the database and running Alembic migrations, `uv run --locked python scripts/seed_data.py` validates and persists it without overwriting existing profiles. It introduces no CSV import schema. Legacy seed modules remain test compatibility fixtures rather than runtime repositories.
