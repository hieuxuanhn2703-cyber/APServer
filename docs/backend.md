# Backend Documentation

## Core Framework
- Django 6.0.6

## Authentication & Authorization
The project does not use the default Django `User` model for authentication workflows in the same way standard apps do. Instead, it relies on a custom `AppUser` model inside the `Working` app.
- **Roles**: Defined in `AppUser.ROLE_CHOICES` (`BASIC`, `HOAN_THIEN`, `KCS`, `NHA_CAT`, `KHO`, `KE_TOAN`, `QUAN_LY`, `PREMIUM`).
- **Middleware**: `Working.middleware.LoginRequiredMiddleware` intercepts requests to ensure the user is logged in.
- View-level logic dictates whether a user can see or modify specific reports based on their role.

## Business Logic
Business logic is heavily embedded in Django Views (`views.py`).
- Examples include Excel exports (`export_excel_view`), cascading deletes via `on_delete=models.PROTECT`, and transaction handling when creating related records.
