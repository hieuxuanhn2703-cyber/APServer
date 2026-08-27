# Backend Documentation

## Tech Stack
- Python 3.14 (or compatible)
- Django 6.0.6
- Django REST Framework 3.18.0
- django-cors-headers 4.9.0

## Core Framework
- Django 6.0.6

## Authentication & Authorization
The project does not use the default Django `User` model. It relies entirely on a custom `AppUser` model inside the `Working` app.
- **Passwords**: Currently stored and verified in plaintext (`password=password` in `Working.auth_utils.verify_credentials`).
- **Session**: Uses standard Django sessions (storing `user_id`).
- **Roles & Permissions**: 
  - `BASIC` (Sản xuất): Submit `ProcessReport`, view own reports.
  - `HOAN_THIEN`: Access `finishing_web`.
  - `KCS`: Access `kcs_web`.
  - `NHA_CAT`: Access `cut_web`.
  - `KHO`: Access Inventory Summary, create Receipts/Issues. Cannot edit/delete existing inventory records.
  - `KE_TOAN`: Access Accounting Dashboard, manage prices, exports, and payments.
  - `QUAN_LY`: Access premium dashboards, config lists, edit/delete ANY user's process reports, edit/delete ANY inventory records.
  - `PREMIUM`: Superadmin. Does everything `QUAN_LY` does, plus manage accounts (approve users, change roles).
- **Middleware**: `Working.middleware.LoginRequiredMiddleware` intercepts requests and forces logins for non-public routes.
- **View-level logic**: Explicit checks like `if current_user.role not in ["PREMIUM", "QUAN_LY"]` govern core security, not just UI hiding.

## Business Logic
Business logic is heavily embedded in Django Views (`views.py`).
- Examples include Excel exports (`export_excel_view`), cascading deletes via `on_delete=models.PROTECT`, and transaction handling when creating related records.
