# Feature Implementation Workflow

Use this process when implementing a new feature in this project.

## Phase 1 — Understand

1. Read the user's request.
2. Identify the expected behavior.
3. Inspect the relevant existing code.
4. Find related models, views, URLs, templates, JavaScript and CSS.
5. Identify existing functionality that can be reused.

## Phase 2 — Plan

Before modifying code:
1. Explain the implementation approach.
2. List files that need to change.
3. Explain why each file needs to change.
4. Identify possible side effects.
5. Identify database/migration impact if any.

For small, obvious changes, keep the plan concise.
For architectural or database changes, ask for confirmation before proceeding.

## Phase 3 — Implement

Implement the smallest reasonable change.

Rules:
- Follow existing project conventions.
- Reuse existing code.
- Avoid unrelated refactoring.
- Do not modify unrelated files.
- Do not introduce unnecessary dependencies.

## Phase 4 — Validate

After implementation:
1. Run appropriate project checks (`python manage.py check`).
2. Run relevant tests if any. Ensure 23+ tests pass successfully.
3. Check for syntax errors.
4. Check affected frontend behavior, including mobile responsiveness (`max-width: 640px`).
5. **Verify Database Queries:** Use `select_related()` to ensure no N+1 query overhead in list/dashboard views.
6. **Verify Roles:** Check that UI restrictions (buttons, sidebar links) hide correctly for `PREMIUM`, `QUAN_LY`, and other roles.
7. Review git diff.

## Phase 5 — Report

Provide:

### Changes made
List the important changes.

### Files changed
List every modified/created file.

### Validation
List commands/tests executed and their results.

### Potential issues
Mention anything that still needs attention.
