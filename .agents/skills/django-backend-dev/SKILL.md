---
name: django-backend-dev
description: Instructions for developing Django backend logic specifically for this project.
---

# Django Backend Development for ProcessMonitoring

## Overview
This skill provides context for developing backend logic for the `ProcessMonitoring` project, which includes `Working`, `Accounting`, and `Inventory` apps.

## Key Principles
1. **Transaction Safety**: When creating or updating records that affect multiple tables (e.g., adding a Product and its Colors/Sizes simultaneously, or linking ExportReports to Working's ProductColor), wrap the logic in `transaction.atomic()`.
2. **N+1 Query Prevention**: Always use `.select_related()` (for ForeignKeys like `nguoi_nhap`, `product_color`) or `.prefetch_related()` when fetching lists of reports to avoid performance bottlenecks.
3. **Role Checks**: Before executing data mutations, verify if the `AppUser.role` has the correct permission. For example, `KCS` role should only write to `KcsReport`.
4. **Data Integrity**: The project relies on `on_delete=models.PROTECT`. If deleting a record fails due to ProtectedError, handle it gracefully rather than forcing cascading deletes.

## Workflow
1. Check existing models to understand the schema (`Working/models.py`, `Accounting/models.py`, `Inventory/models.py`).
2. Write tests before or alongside your view/logic changes.
3. Use `python manage.py check` and `python manage.py test` to validate.
