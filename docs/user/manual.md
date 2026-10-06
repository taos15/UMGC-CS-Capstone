# SkillMatch user manual

For installation, accounts, API configuration, and migration commands, use the
[root README](../../README.md). Accounts are configured locally by an operator;
there is no self-registration or default password. Interactive API documentation
is available at `/docs` on the running FastAPI server.

## Sign in and permissions

Enter your configured username and password. Invalid credentials produce a
generic message. The portal attaches the bearer token to later requests; tokens
expire after 15 minutes. Sign in again when your session expires, and sign out
when finished.

ADMIN manages profiles and skill taxonomy and can read every stored match run.
SUPERVISOR requests recommendations and records feedback on their own runs.
VIEWER reads permitted data and their own runs. The API enforces permissions;
seeing a navigation link does not grant permission to write.

## Request and review recommendations

1. Open the jobs page. The initial filter shows OPEN jobs; use the status filter
   to view all jobs when needed.
2. Select a job and review its requirements. Recommendations require an OPEN job
   with matching criteria.
3. Set the maximum results and minimum score. Enable missing skills and
   credentials if you want to review gaps, then request recommendations.
4. Review candidate rank, final score, component scores, eligibility, matched and
   missing evidence, and explanation. Save the match-run ID and model version
   when discussing the result.

Scores describe alignment with structured job evidence, not a probability of
success. Required-skill gaps lower scores. A missing valid mandatory
certification prevents eligibility; non-ACTIVE employees are ineligible. Ordering
uses final score, required-skill coverage, certification coverage, then employee
ID. Use the explanation and human judgment before making staffing decisions.

## Record supervisor feedback

Choose SELECTED, NOT_SELECTED, or DEFERRED in the feedback panel. SELECTED
requires choosing an eligible candidate from that run. Add an optional comment
and submit. The confirmation indicates an audit record was saved. Feedback never
assigns an employee and never changes the live scoring model automatically.

Historical results remain the evidence from their saved run. After profile or
job changes, request a new recommendation run to evaluate current evidence.

## Maintain employee and job profiles

ADMIN can create profiles, edit evidence and status, and save changes. Use
existing skill IDs from the taxonomy. Review field-level validation messages
before resubmitting a rejected form.

If another update has changed the profile, the server returns `STALE_VERSION`.
The portal retains your draft and offers an explicit reload. Preserve any draft
text you need before reloading the latest profile, then reapply and save your
changes. Repeatedly submitting the old version will not overwrite newer data.

Deletion permanently removes the current profile after confirmation. Saved
historical match runs and feedback remain for audit. Deletion also uses the
last-read version and can require stale-version recovery.

## Handle errors

- Validation messages identify fields to correct; the portal does not display raw
  problem JSON.
- A closed job or job with no criteria needs an administrator's correction before
  recommendations can proceed.
- A permission error requires an account with the appropriate role.
- Database or matching service unavailability requires retrying after recovery.
  A failed recommendation does not leave a partial match run.
- Keep the displayed request ID when reporting a problem so the operator can
  correlate it with server logs.

See [repository evidence](../evidence/unit8/repository-evidence.md) for observed
checks and known limitations. Hosted deployment and independent relevance
validation are not established by these local results.
