# Story-generation contract

When generating/revising SkillMatch stories:

- Derive them from concrete Project Design requirements and assignment gates; never use generic placeholder stories such as “As a stakeholder/developer, I want X so the system remains useful.”
- Prefer real actors: administrator, supervisor, viewer, operator, maintainer, contributor, reviewer, project team.
- Keep implementation ownership separate from course roles.
- One story = one testable capability/decision path.
- Preserve canonical endpoints, role matrix, data vocabulary, scoring math, error codes, and human-decision boundary.
- If source is underspecified, add a stop/amendment condition instead of inventing a public contract.
- Every behavior story follows `resources/spec_bundle/quality/tdd_story_contract.md`.
- Phase stories deliberately: Unit 5 Alpha first; Unit 8 hardening/final later. Do not auto-chain.
- Before delivery, verify each in-scope Project Design capability has a story or is explicitly deferred.
