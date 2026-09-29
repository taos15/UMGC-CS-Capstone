# Shared data contract vocabulary

The Project Design Specification defines minimum concepts, not every concrete field. Do not add new public fields silently.

## EmployeeProfile

- `id`: server UUID.
- `employee_number`: unique business key.
- name/display fields.
- `current_title`: display only; excluded from scoring.
- `status`; only `ACTIVE` is match-eligible.
- `total_years_experience`.
- `version`.
- `skills[]`.
- `certifications[]`.

### EmployeeSkill

`skill_id`; `proficiency` 1-5; `years_experience`; optional `last_used_on`.

### EmployeeCertification

code/id; name; issuer; `issued_on`; `expires_on` when applicable. An expired credential cannot satisfy an active mandatory requirement.

## JobProfile

`id`; unique `job_code`; title; description; `status`; `minimum_years_experience`; `version`; `skill_requirements[]`; `certification_requirements[]`.

### JobSkillRequirement

`skill_id`; level `REQUIRED` or `PREFERRED`; `minimum_proficiency` 1-5; `importance` 1-3.

An `OPEN` job must be match-ready. A job with no usable criteria must not be silently matched; use the canonical validation/error behavior.

## RecommendationOptions

`max_results` 1-100; `minimum_score` 0-100; `include_ineligible` boolean. The Project Design Specification does not define defaults; preserve tested current defaults if present or amend the contract explicitly.

## MatchRun

`match_run_id`, `job_id`, `requested_by`, `model_version`, `snapshot_hash`, options, `generated_at`, ranked results. Stored runs are immutable and retrieval never silently recomputes.

## CandidateResult

rank; `employee_id`; score 0-100; eligibility; component scores; matched/missing skills and certifications; ineligible reasons; explanation.

## Feedback

`match_run_id`; `user_id`; decision `SELECTED` / `NOT_SELECTED` / `DEFERRED`; optional `selected_employee_id`; optional helpfulness/rating/comment according to finalized OpenAPI; `created_at`. Feedback never updates the live model automatically.
