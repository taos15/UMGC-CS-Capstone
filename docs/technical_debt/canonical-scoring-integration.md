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
- This function computes scores only. Eligibility, ranking, and explanation
  generation remain separate responsibilities.

Before switching the API to this scorer, migrate employee/job data and the
orchestration adapter to supply actual proficiency, importance, and validated
certification evidence. Then update API score expectations and connect model
version/snapshot persistence. Do not synthesize these values from name-only
seed data. Until that follow-up, `scoring.build_recommendation` remains the
active legacy scorer and production requests do not use canonical scoring.
