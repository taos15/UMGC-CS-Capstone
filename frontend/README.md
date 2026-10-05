# SkillMatch portal

Requires Node.js 24 or later. From this directory, run `npm ci`, then `npm run dev`. Vite proxies `/api` to the local backend at `http://127.0.0.1:8000`. Run `npm test` and `npm run build` for validation.

After login, the portal opens the job recommendations page. Workspace navigation also opens employee and job profile management. Both flows share the same session and API client; the session expires automatically.

Recommendation results consume the canonical snake_case CandidateResult response. Candidate cards display employee IDs (the contract has no separate employee name), server ranks and 0–100 scores, normalized component values, matched/missing skill and certification evidence, eligibility reasons, and the server explanation. They preserve server ordering, show empty/malformed response states, and remind supervisors that final staffing authority remains human.

Employee and job forms use the canonical snake_case profile contracts, including skills and certifications. Updates send the exact version from the last successful GET/PUT. A `409 STALE_VERSION` keeps the draft, blocks further changes on the server, and offers a confirmed reload. Profiles without server versions cannot be edited or deleted.

Permanent deletion requires confirmation and sends `DELETE` with JSON `{ "version": <last-read version> }`; successful 204 responses return to the list. The approved ADMIN-only deletion contract is recorded in `resources/spec_bundle/api/api_contract.md`. Server authorization remains authoritative; non-admin attempts surface permission errors.

Current backend POST/PUT profile routes return 501 and legacy reads omit versions; DELETE routes and persisted versioned profiles still need backend implementation. The frontend does not simulate successful saves/deletion or invent versions. Tests use mocked canonical API responses to verify the intended integration contract. Local login requires backend-configured credentials.

Supervisor feedback appears below the returned recommendations and targets that exact `match_run_id`. Choose SELECTED with an eligible returned candidate, or NOT_SELECTED/DEFERRED without an employee ID; the comment is optional. The shared client posts to `/api/v1/match-runs/{match_run_id}/feedback` using the bearer token. Pending submissions are disabled, errors retain the draft, and successful submissions remain disabled until the form changes. Another deliberate submission adds an audit entry. New runs start with a fresh form. Feedback does not assign employees or update the matching model; role and run-scope checks remain authoritative on the server.
