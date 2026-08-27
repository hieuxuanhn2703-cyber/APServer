# API Documentation

**Status**: NOT IMPLEMENTED YET.

Currently, there are no REST APIs. All data exchanges occur via standard HTML form submissions and server-rendered HTML responses.

## Future API Architecture (Planned)
**Status**: NOT IMPLEMENTED YET.

- **Framework**: Django REST Framework (DRF).
- **Format**: JSON.
- **URL Prefix**: `/api/v1/`
- **Authentication**: Custom JWT Authentication decoding the token and evaluating the custom `AppUser` model.

### Proposed Endpoints
- **Auth**: `POST /api/v1/auth/login/`, `GET /api/v1/auth/me/`
- **Inventory**: `GET /api/v1/inventory/summary/`, `CRUD /api/v1/inventory/receipts/`, `CRUD /api/v1/inventory/issues/`
- **Accounting**: `GET /api/v1/accounting/dashboard/`, `CRUD /api/v1/accounting/payments/`, `CRUD /api/v1/accounting/prices/`
- **Working**: `CRUD /api/v1/working/users/`, `CRUD /api/v1/working/process-reports/`

### Response Conventions
- **Success (200/201)**: `{ "data": ... }` or `{ "count": 100, "results": [...] }`
- **Validation Errors (400)**: `{ "errors": { "field": ["error message"] } }`
- **Permission Errors (403)**: `{ "error": "Chỉ quản lý mới có quyền chỉnh sửa phiếu nhập kho." }`

### Business Logic Boundaries
- **Keep in Django (API)**: JWT token generation, complex aggregations (`_calculate_cumulative_totals_prod`, `get_inventory_summary_data`), Excel exporting via openpyxl, Role-based view guards.
- **Move to React**: UI interaction logic (`cascade_select.js`, `excel_filter.js`), pre-submit form validation, and pagination UI state.
