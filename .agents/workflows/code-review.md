# Code Review Workflow

Use this workflow to conduct code reviews.

1. **Analyze**: Read the provided diff or code snippet.
2. **Plan**: Compare against `.agents/rules/` (specifically `django.md` and `database.md`).
3. **Review**:
   - Check for N+1 queries.
   - Check for `transaction.atomic()` usage on multi-model saves.
   - Check for Role validation (e.g., checking `AppUser.role`).
   - Check that UI components didn't break mobile layouts.
4. **Report**: Provide a structured review with exact line numbers and recommendations.
