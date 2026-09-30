# Resolve a canonical contract change

Use when current code/tests or a requested feature conflicts with the Project Design-derived contracts.

1. Read the narrow spec router/file for the affected domain.
2. Identify whether the difference is an observed legacy implementation, an unapproved request, or an approved design amendment.
3. If approval/intent is ambiguous, stop and ask rather than silently changing the public contract.
4. When approved, update the canonical spec/story first, then implement with TDD.
5. Preserve a short decision record in the relevant documentation if the change affects architecture, scoring, API, data, security, or scope.
