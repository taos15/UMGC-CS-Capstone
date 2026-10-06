# SkillMatch portal

Requires Node.js 24 or later. From this directory, run `npm ci`, then `npm run dev`. Vite proxies `/api` to the local backend at `http://127.0.0.1:8000`. Run `npm run lint`, `npm test`, and `npm run build` for validation.

After login, the portal opens the job recommendations page. Workspace navigation also opens employee and job profile management. Both flows share the same session and API client; the session expires automatically.

Recommendation results consume the canonical snake_case CandidateResult response. Candidate cards display employee IDs (the contract has no separate employee name), server ranks and 0–100 scores, normalized component values, matched/missing skill and certification evidence, eligibility reasons, and the server explanation. They preserve server ordering, show empty/malformed response states, and remind supervisors that final staffing authority remains human.

Employee and job forms use the canonical snake_case profile contracts, including skills and certifications. Updates send the exact version from the last successful GET/PUT. A `409 STALE_VERSION` keeps the draft, blocks further changes on the server, and offers a confirmed reload. Profiles without server versions cannot be edited or deleted.

Permanent deletion requires confirmation and sends `DELETE` with JSON `{ "version": <last-read version> }`; successful 204 responses return to the list. The approved ADMIN-only deletion contract is recorded in `resources/spec_bundle/api/api_contract.md`. Server authorization remains authoritative; non-admin attempts surface permission errors.

Profile APIs now return canonical versioned records and persist create/update/permanent delete operations. Unit/component tests use mocked API fixtures; the separate Playwright scenarios exercise actual React, FastAPI, PostgreSQL, matching, and stored feedback without API interception. See the repository README for `scripts/run_postgres_e2e.py` setup. Local login requires backend-configured credentials.

Supervisor feedback appears below the returned recommendations and targets that exact `match_run_id`. Choose SELECTED with an eligible returned candidate, or NOT_SELECTED/DEFERRED without an employee ID; the comment is optional. The shared client posts to `/api/v1/match-runs/{match_run_id}/feedback` using the bearer token. Pending submissions are disabled, errors retain the draft, and successful submissions remain disabled until the form changes. Another deliberate submission adds an audit entry. New runs start with a fresh form. Feedback does not assign employees or update the matching model; role and run-scope checks remain authoritative on the server.

## API configuration and failures

Copy `.env.example` to `.env.local` and set `VITE_API_BASE_URL` to the complete API base, including `/api/v1`. It accepts a same-origin path (default `/api/v1`) or an absolute HTTP(S) URL, such as `https://api.example.test/api/v1`. Restart Vite after changing environment configuration; production values are embedded at build time, so rebuild to change them. Cross-origin deployments must configure backend CORS for the frontend origin. Per-request paths stay relative to the configured base.

For local development, `SKILLMATCH_API_PROXY_TARGET` configures Vite's `/api` proxy (default `http://127.0.0.1:8000`). This target is used only by the dev server; it is not embedded in browser requests.

Loading, empty results, and errors are distinct. Shared problem alerts display safe guidance for stable error codes, actionable 422 field issues, and request IDs for support. Server `detail`, raw JSON, and internal validation messages are not rendered. Login, recommendation, profile, and feedback flows use the same error boundary; failed drafts and existing concurrency protections remain intact.
