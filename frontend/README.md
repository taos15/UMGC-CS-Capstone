# SkillMatch profile portal

Requires Node.js 24 or later. From this directory, run `npm ci`, then `npm run dev`. Vite proxies `/api` to the local backend at `http://127.0.0.1:8000`. Run `npm test` and `npm run build` for validation.

Employee and job forms use the canonical snake_case profile contracts, including skills and certifications. Updates send the exact version from the last successful GET/PUT. A `409 STALE_VERSION` keeps the draft, blocks further changes on the server, and offers a confirmed reload. Profiles without server versions cannot be edited or deleted.

Permanent deletion requires confirmation and sends `DELETE` with JSON `{ "version": <last-read version> }`; successful 204 responses return to the list. The approved ADMIN-only deletion contract is recorded in `resources/spec_bundle/api/api_contract.md`. Server authorization remains authoritative; non-admin attempts surface permission errors.

Current backend POST/PUT profile routes return 501 and legacy reads omit versions; DELETE routes and persisted versioned profiles still need backend implementation. The frontend does not simulate successful saves/deletion or invent versions. Tests use mocked canonical API responses to verify the intended integration contract. Local login requires backend-configured credentials.
