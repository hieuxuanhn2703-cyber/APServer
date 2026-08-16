# Django Instructions

## Architecture

- **Models:** The primary models are `ProcessReport`, `AppUser`, `FinishingReport`, `KcsReport`, `CutReport`, `Product`, `ProductColor`, and `ProductSize`. Always inspect `Working/models.py` before making changes.
- **Views:** Views handle the business logic. Check `Working/views.py` to understand existing flows before creating new views.
- **URLs:** Routing is split between `ProcessMonitoring/urls.py` and `Working/urls.py`.
- **Forms:** Forms are defined in `Working/forms.py` and rendered using Django Templates.
- **Templates:** Use existing templates in `Working/templates/` as references for structure.
- **Static files:** Placed in `Working/static/working/`.
- **Authentication:** The project uses a custom `AppUser` model with specific roles (`BASIC`, `HOAN_THIEN`, `KCS`, `NHA_CAT`, `QUAN_LY`, `PREMIUM`). Do not change authentication behavior or bypass this model without explicit approval.
- **APIs:** No distinct API framework (e.g., DRF) is currently implemented. The project uses standard Django form submissions.
- **Migrations:** Located in `Working/migrations/`.

## Rules

- Inspect existing implementation before creating a new one.
- Reuse existing models, views, utilities, and services when appropriate.
- Do not duplicate business logic.
- Do not modify database models unless the task explicitly requires it.
- Do not delete or rewrite migrations unnecessarily.
- Follow existing Django app boundaries (`Working` app).
- Follow existing naming conventions.
- Keep business logic out of templates.
- Do not change authentication behavior without explicit approval.

## Validation Commands

After Python/Django changes, use the project's validation commands:
- `python manage.py check`

## Django Backend Guidelines (Learned from Session)

- **Database Performance:** MUST use `.select_related()` (e.g., `.select_related('nguoi_nhap')`) for report lists (List and Dashboard views) to prevent N+1 Query problems when displaying related models.
- **Data Integrity:** MUST wrap critical cross-model operations in `transaction.atomic()`. If an operation can fail halfway through (e.g., adding products and colors simultaneously), use transactions to ensure all-or-nothing saves.
- **Deletion Rules:** The project uses `on_delete=models.PROTECT` extensively (e.g., deleting a User with associated reports throws `ProtectedError`). Do NOT ignore this error implicitly; handle it gracefully or leave it to be resolved architecturally.
- **Toggle Features:** Be mindful of feature toggles like `ENABLE_SIZES`. Logic that handles sizes should respect this toggle to keep the system operational if it is disabled.
- **Dynamic Contexts:** Any view that renders an edit template for an entry form MUST include `config = load_config()` in its context so the frontend Javascript can function properly.
