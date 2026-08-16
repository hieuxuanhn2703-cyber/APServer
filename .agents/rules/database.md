# Database Instructions

## Technology Stack

- **Database:** MySQL

## Rules

Agents MUST:
- Inspect existing models before changing database-related code.
- Understand relationships before modifying models.
- Preserve existing data.
- Preserve existing migrations.
- Avoid destructive database operations.

Agents MUST NOT perform the following unless explicitly requested:
- Drop database
- Reset database
- Delete production data
- Delete migrations
- Recreate database schema unnecessarily
- Run destructive SQL
- Modify production data directly

## Model Modifications

If a model change is required:
1. Explain the intended schema change.
2. Identify affected models.
3. Identify migration impact.
4. Implement only after the task requires it.
5. Run the appropriate Django validation/migration checks (`python manage.py makemigrations`, `python manage.py check`).

## Security

Never hardcode:
- passwords
- API keys
- database credentials
- secret keys
- tokens
