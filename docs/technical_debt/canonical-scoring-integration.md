# MATCH-002 staged integration

The approved scope adds the canonical scorer independently and preserves the
existing recommendation API and its tested scores. `canonical_scoring.py`
implements model version `rpce-55-20-15-10-v1` with immutable internal inputs;
these are not new HTTP request/response schemas.

- Skills use IDs, employee proficiency (1-5), requirement minimum proficiency
  (1-5), importance (1-3), and REQUIRED/PREFERRED levels. Duplicate skill IDs
  are rejected to prevent ambiguous evidence and order-dependent scores.
- Certification inputs are immutable sets of required codes and codes already
  validated for the candidate at the input snapshot. The caller must exclude
  expired/otherwise invalid credentials. The scorer does not infer validity
  from legacy certification names or consult the current clock.
- Components are unrounded 0-1 values, with `None` for absent R/P/C categories.
  Experience always participates. Final scores use renormalized 55/20/15/10
  weights on a 0-100 scale without presentation rounding. A job with no skills,
  required certifications, or positive experience minimum is rejected.
- This function computes scores only. Eligibility is implemented in `eligibility.py`; ranking and explanation
  integration remain separate responsibilities.

Before switching the API to this scorer, migrate employee/job data and the
orchestration adapter to supply actual proficiency, importance, and validated
certification evidence. Then update API score expectations and connect model
version/snapshot persistence. Do not synthesize these values from name-only
seed data. Until that follow-up, `scoring.build_recommendation` remains the
active legacy scorer and production requests do not use canonical scoring.

## MATCH-001 eligibility stage

`matching/eligibility.py` now evaluates status and mandatory certifications as a
pure function. `EmployeeEligibilityInput` and `CertificationEvidence` are frozen
internal DTOs. The caller supplies `as_of` from the fixed recommendation
snapshot; evaluation never consults the current clock or database. A credential
is valid on its issue date and through its expiration date inclusive; no expiry
means it remains valid after issuance. An expired copy does not invalidate a
currently valid renewal with the same code.

`EligibilityResult` supplies `eligible`, sorted `matched_certifications` and
`missing_certifications`, and stable `ineligible_reasons`: `EMPLOYEE_NOT_ACTIVE`
first, followed by sorted `MISSING_MANDATORY_CERTIFICATION:<code>` reasons.
These evidence fields map to the corresponding `CandidateResult` fields.
`valid_certification_codes` feeds the canonical `EmployeeScoringInput` so scoring
and eligibility use the same snapshot. Required skill gaps affect canonical
scores independently and never add an eligibility reason.

The legacy recommendation API still lacks employee status and dated certification
evidence. Connecting this evaluator requires the same profile/job orchestration
adapter described above; status, issue dates, and expiry dates must not be
fabricated from the name-only seed data. Ranking/options integration remains a
separate stage.
