# Project Analysis Workflow

Use this workflow when dealing with large changes (e.g., refactoring models, changing cross-app relationships).

## Phase 1 - Inspect Dependencies
1. Check how `Accounting` and `Inventory` depend on `Working` (especially `AppUser` and `ProductColor`).
2. Run `python manage.py showmigrations` if migrating.

## Phase 2 - Impact Analysis
1. Determine what views or templates will break.
2. Draft an implementation plan.
3. Ask for explicit user approval before modifying code.
