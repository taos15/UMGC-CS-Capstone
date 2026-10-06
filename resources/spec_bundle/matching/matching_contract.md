# AI matching contract

## Boundary

Matching receives immutable DTOs from recommendation orchestration. It does not access FastAPI requests, ORM/database sessions, PostgreSQL, or external services. It never assigns employees.

Allowed scoring evidence: skill IDs, employee proficiency, required proficiency, requirement importance, years of experience, certification validity. Current title and protected personal characteristics are excluded.

## Eligibility

- non-`ACTIVE` employee -> ineligible.
- missing/expired mandatory certification -> ineligible.
- missing required skill -> score reduction + explicit gap, not automatic exclusion unless a later approved hard gate changes the contract.

## Versioned scoring

- `R`: importance-weighted mean of `min(employee_proficiency / minimum_proficiency, 1.0)` for `REQUIRED` skills.
- `P`: same for `PREFERRED` skills.
- `C`: valid required certifications / required certifications; omit if the job has none.
- `E`: `1.0` if job minimum experience is zero, otherwise `min(employee_total_years / job_minimum_years, 1.0)`.
- Final: `100 * weighted_average(0.55R, 0.20P, 0.15C, 0.10E)`.
- Remove absent categories and renormalize remaining weights.

Expose final scores on 0-100. Internal components may remain 0.0-1.0.

## Ranking

Apply eligibility/options before return. Deterministic tie-break: final score descending -> required-skill coverage descending -> certification coverage descending -> employee_id stable/ascending. Respect `minimum_score`, `include_ineligible`, and `max_results`. Same input snapshot + `model_version` yields identical ordering/scores.

## Explainability and change control

Every result includes component scores, matched/missing evidence, eligibility reasons, and a structured/template explanation. No generative LLM explanations in MVP. Supervisor feedback is offline evaluation evidence only; no production request retrains, mutates, or promotes the live scoring config automatically.
