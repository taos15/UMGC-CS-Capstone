# REST API contract

Canonical base path: `/api/v1`.

## Authorization roles

- `ADMIN`: create/update skills, employees, jobs; request recommendations; submit feedback; read within scope.
- `SUPERVISOR`: read skills/employees/jobs; request recommendations; read authorized match runs; submit feedback.
- `VIEWER`: read skills/employees/jobs and authorized prior match runs only.
- `POST /auth/login` is public.
- `GET /health` is an operations endpoint; the Project Design Specification does not define its exact exposure/auth policy.

## Endpoint set

| Method | Path | Allowed role(s) | Purpose |
| --- | --- | --- | --- |
| POST | `/auth/login` | Public | Exchange local credentials for a short-lived bearer token. |
| GET | `/skills` | ADMIN / SUPERVISOR / VIEWER | List/search controlled skill taxonomy. |
| POST | `/skills` | ADMIN | Create a skill. |
| GET | `/employees` | ADMIN / SUPERVISOR / VIEWER | List/filter employee profiles. |
| POST | `/employees` | ADMIN | Create an employee profile. |
| GET | `/employees/{employee_id}` | ADMIN / SUPERVISOR / VIEWER | Retrieve one employee. |
| PUT | `/employees/{employee_id}` | ADMIN | Replace editable fields using optimistic versioning. |
| GET | `/jobs` | ADMIN / SUPERVISOR / VIEWER | List/filter jobs. |
| POST | `/jobs` | ADMIN | Create a job profile. |
| GET | `/jobs/{job_id}` | ADMIN / SUPERVISOR / VIEWER | Retrieve one job. |
| PUT | `/jobs/{job_id}` | ADMIN | Update using optimistic versioning. |
| POST | `/jobs/{job_id}/recommendations` | ADMIN / SUPERVISOR | Generate, store, return ranked recommendation run. |
| GET | `/match-runs/{match_run_id}` | Authorized roles within scope | Return immutable stored recommendation snapshot; never silently recompute. |
| POST | `/match-runs/{match_run_id}/feedback` | ADMIN / SUPERVISOR | Record supervisor feedback tied to the run. |
| GET | `/health` | Operations | Return service/dependency health. |

## Shared conventions

- JSON uses `snake_case`.
- Server identifiers are UUID strings. `employee_number` and `job_code` are unique business keys.
- Timestamps are UTC ISO 8601 with `Z`; date-only values use `YYYY-MM-DD`.
- Pagination: `page >= 1`, `page_size` 1-100, default 25.
- `PUT` includes `version`; stale update -> `409 STALE_VERSION`.
- Errors use `application/problem+json`, RFC 9457-style fields with stable `code`, `request_id`, `detail`, and field errors.
- Every response carries `X-Request-ID`.
- Recommendation responses also expose `match_run_id` and `model_version`.

## Underspecified details

The Project Design Specification does not fully define the full Skill object schema, search/filter query parameters, or the exact health response shape. Preserve tested current behavior if it exists; otherwise record an approved contract amendment instead of silently inventing a public schema.

## Approved local-login amendment

Approved by the user in this implementation session:

- `POST /auth/login` accepts JSON `username` and `password` strings.
- Success is HTTP 200 with `access_token`, `token_type: "bearer"`, and
  `expires_in: 900` (seconds). The response is not cacheable.
- JWTs use HS256 and contain `sub` (user UUID), `role` (ADMIN/SUPERVISOR/VIEWER),
  `iat` and `exp` (Unix seconds), with a 15-minute lifetime.
- Local accounts are configured as password hashes, with no built-in accounts.
  `SKILLMATCH_LOCAL_USERS` is a JSON object keyed by exact username, with
  `user_id`, `role`, and `password_hash` per entry. `SKILLMATCH_JWT_SECRET` is
  an externally supplied signing secret of at least 32 UTF-8 bytes.
- Hash format is `scrypt$<base64 salt>$<base64 digest>` with a random 16-byte
  salt, N=16384, r=8, p=1, and a 64-byte digest.
- Username length is 1–128; password length is 1–1024. Password values are
  excluded from validation errors and logging.
- Unknown usernames and wrong passwords return the same 401 problem:
  `AUTH_INVALID_CREDENTIALS`, detail `Invalid username or password.`, and
  `WWW-Authenticate: Bearer`. Missing/malformed/expired bearer credentials
  on workforce routes return generic 401 `AUTH_REQUIRED`.
- Configuration failures return generic 503 `AUTH_UNAVAILABLE`; no fallback
  signing secret or default account is used.
- Login and health remain public. Workforce routes validate bearer tokens and
  enforce the section 5 role matrix through centralized route dependencies.

## Approved permanent-deletion amendment

Approved by the user in this implementation session (permanent deletion replaces the proposed archive behavior):

- ADMIN-only `DELETE /employees/{employee_id}` and `DELETE /jobs/{job_id}` accept JSON `{"version": <last-read positive integer version>}`.
- Success returns HTTP 204 with no body and permanently removes the profile.
- A stale version returns `409 STALE_VERSION`; missing IDs use the existing employee/job not-found code.
- Stored match-run snapshots and feedback remain immutable historical records. Deletion does not recompute or remove them.
- The portal requires explicit permanent-deletion confirmation. A stale DELETE retains the draft and requires an explicit reload; it never retries with a guessed version.
- Backend persistence and DELETE routes must implement this contract before live deletion is available.

## Approved recommendation-orchestration amendment (REC-001)

Approved in this implementation session:

- `POST /jobs/{job_id}/recommendations` now runs the canonical eligibility/scoring
  engine (`55/20/15/10`, `resources/spec_bundle/matching/matching_contract.md`)
  instead of the earlier ad hoc weights, and persists every successful run via
  `features/recommendations/repository.py` before responding.
- `recommendations` in the response is now a list of the data contract's
  `CandidateResult` shape (`rank`, `employee_id`, `score`, `eligible`,
  `component_scores`, `matched_skills`, `missing_skills`,
  `matched_certifications`, `missing_certifications`, `ineligible_reasons`,
  `explanation`) in `snake_case`, replacing the legacy camelCase `Recommendation`/
  `scoreBreakdown` shape. `component_scores` values are the unrounded 0.0-1.0
  internal components, per matching_contract.md.
- The request gains `include_ineligible` (alias `includeIneligible`, default
  `false`), matching `RecommendationOptions` in the data contract. The request's
  other fields keep their existing camelCase aliases for now - only the
  response changed in this amendment.
- `Employee` and `Job` gain a `status` field (`ACTIVE`/`INACTIVE`,
  `OPEN`/`CLOSED`) and structured scoring evidence (`skill_evidence`,
  `certification_evidence` on Employee; `skill_requirement_details` on Job),
  additive to their existing flat `skills`/`required_skills`/etc. fields so
  existing employee/job read/write behavior is unchanged.
- A job that is not `OPEN` returns `409 JOB_NOT_OPEN`; a job with no usable
  skill/certification/experience criteria returns `422 JOB_HAS_NO_CRITERIA`.
  The orchestrator snapshots `ACTIVE` candidates only - `INACTIVE` employees
  are excluded before scoring, not merely marked ineligible.
- `GET /match-runs/{match_run_id}` returns the persisted snapshot (REC-002).

## Approved match-run retrieval scope (REC-002)

Approved by the user in this implementation session:

- ADMIN can read all stored runs. SUPERVISOR and VIEWER can read only runs whose `requested_by` equals their authenticated user ID.
- Unknown IDs return `404 MATCH_RUN_NOT_FOUND`. Out-of-scope runs return generic `403 FORBIDDEN`, without rankings, evidence, or requester details.
- GET returns the canonical `MatchRun` shape, with snake_case options and results, UTC `generated_at`, and stored rank ordering. Historical camelCase option keys are normalized without modifying stored rows.
- Retrieval never reads live employee/job profiles or invokes matching. Database failures return `503 DATABASE_UNAVAILABLE`.

## Approved feedback contract (FDBK-001)

Approved by the user in this implementation session:

- `POST /match-runs/{match_run_id}/feedback` accepts `decision` (`SELECTED`, `NOT_SELECTED`, `DEFERRED`) and optional `selected_employee_id`, `rating`, and `comment`. Unknown fields are rejected; run ID, caller ID, and creation time are server-controlled.
- `SELECTED` requires `selected_employee_id`. It must reference an eligible candidate in the stored run, otherwise return `409 FEEDBACK_CONFLICT`. Other decisions require a null/omitted selected employee; invalid field combinations return `422 VALIDATION_ERROR`.
- ADMIN can submit feedback against any run; SUPERVISOR only against their own runs. VIEWER cannot submit. Missing runs return `404 MATCH_RUN_NOT_FOUND`; out-of-scope access returns generic `403 FORBIDDEN` before candidate evidence is loaded.
- Success returns HTTP 201 with the saved canonical `Feedback`, including server-authenticated `user_id` and UTC `created_at`. Existing rating/comment types are preserved without inventing a rating scale.
- Every valid submission appends an audit entry, including repeated submissions; prior entries and stored runs remain unchanged. Feedback does not assign employees, alter live matching, or trigger retraining.
- Database failure returns `503 DATABASE_UNAVAILABLE`, with failed writes rolled back.
