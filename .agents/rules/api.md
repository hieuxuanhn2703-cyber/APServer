# API Development Instructions

**Status**: NOT IMPLEMENTED YET

## Technology Stack (Target)

- **Framework**: Django REST Framework (DRF) (Planned)
- **Authentication**: JWT or Session/CSRF (To be decided)
- **Serialization**: DRF Serializers

## Rules

- **Do NOT implement APIs yet** unless explicitly requested. The project currently relies on standard Django Views.
- When APIs are implemented, they MUST:
  - Adhere to RESTful conventions.
  - Return JSON format exclusively.
  - Be versioned (e.g., `/api/v1/...`).
- **Authentication**: Endpoints must enforce the custom `AppUser` roles (`BASIC`, `HOAN_THIEN`, `KCS`, etc.) just like the current `LoginRequiredMiddleware` and view-based checks do.
- **Serialization**: Avoid exposing sensitive internal database IDs directly if possible; however, given the current schema, ensure primary keys used for relationships (like `ProductColor` IDs) are clearly documented in API payloads.
- **Error Handling**: Use consistent error structures (e.g., `{"error": "message", "details": {...}}`).
- **N+1 Problem**: Always use `select_related()` and `prefetch_related()` in ViewSets and APIViews for nested relationships (e.g., `ProcessReport` -> `AppUser`).
