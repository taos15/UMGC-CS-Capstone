# Canonical matching integration status

The previously staged canonical scorer is now active in recommendation
orchestration: eligibility -> R/P/C/E scoring -> deterministic ranking ->
explanations -> atomic persistence. Model version is `rpce-55-20-15-10-v1`.
The matcher remains independent of HTTP, ORM sessions, and staffing decisions.

Profiles persist structured proficiency, dated credentials, status, experience,
and job requirements. Private adapters supply existing immutable matching DTOs.
Scores use 55/20/15/10 weights with absent categories renormalized. Missing skills
lower scores; invalid mandatory certification evidence excludes candidates.
Ordering uses score, required-skill coverage, certification coverage, then ID.
Feedback never changes stored evidence or automatically assigns staff.

The adapters and limited measured relevance/performance evidence remain listed
in [the Alpha register](alpha-register.md); they are no longer disconnected
implementation stages.
