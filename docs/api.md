# API Documentation

**Status**: NOT IMPLEMENTED YET.

Currently, there are no REST APIs. All data exchanges occur via standard HTML form submissions and server-rendered HTML responses.

## API Architecture (Foundation Phase)
**Status**: 
- **IMPLEMENTED**: DRF Foundation, `/api/v1/` namespace, Health Endpoint, Pagination config.
- **NOT IMPLEMENTED YET**: Inventory API, Accounting API, Working API, React.

- **Framework**: Django REST Framework (DRF) v3.18.0.
- **Format**: JSON.
- **URL Prefix**: `/api/v1/`
- **Authentication**: Custom JWT Authentication (IMPLEMENTED). Currently `AllowAny` for the health endpoint.
- **Pagination**: `PageNumberPagination` (page_size=20) (IMPLEMENTED).

### 1. Authentication (`/api/v1/auth/`)
**Status:** IMPLEMENTED (Phase 3B-2)

Endpoints for JWT token generation and validation. Integrates seamlessly with the legacy `AppUser` model using a Custom DRF Authentication Class.

- **`POST /api/v1/auth/token/`**
  - **Purpose:** Obtain JWT access and refresh tokens.
  - **Request Body:** `{"account": "...", "password": "..."}`
  - **Response:** `{"access": "...", "refresh": "..."}`
  - **Permissions:** AllowAny
  - **Note:** Internally uses `verify_credentials` to ensure 100% compatibility with legacy passwords.

- **`POST /api/v1/auth/token/refresh/`**
  - **Purpose:** Refresh an expired access token using a valid refresh token.
  - **Request Body:** `{"refresh": "..."}`
  - **Response:** `{"access": "..."}`

- **`GET /api/v1/auth/me/`**
  - **Purpose:** Get details of the currently authenticated API user.
  - **Response:** `{"id": 1, "account": "...", "name": "...", "role": "..."}`
  - **Permissions:** IsAuthenticated

### Endpoints
- **Health (IMPLEMENTED)**: `GET /api/v1/health/` -> `{"status": "ok"}`
- **Auth (IMPLEMENTED)**: `POST /api/v1/auth/token/`, `POST /api/v1/auth/token/refresh/`, `GET /api/v1/auth/me/`
- **Inventory (PLANNED)**: `GET /api/v1/inventory/summary/`, `CRUD /api/v1/inventory/receipts/`, `CRUD /api/v1/inventory/issues/`
- **Accounting (PLANNED)**: `GET /api/v1/accounting/dashboard/`, `CRUD /api/v1/accounting/payments/`, `CRUD /api/v1/accounting/prices/`
- **Working (PLANNED)**: `CRUD /api/v1/working/users/`, `CRUD /api/v1/working/process-reports/`

### Response Conventions (PLANNED)
- **Success (200/201)**: `{ "data": ... }` or `{ "count": 100, "results": [...] }`
- **Validation Errors (400)**: `{ "errors": { "field": ["error message"] } }`
- **Permission Errors (403)**: `{ "error": "Chỉ quản lý mới có quyền chỉnh sửa phiếu nhập kho." }`

### Business Logic Boundaries
- **Keep in Django (API)**: JWT token generation, complex aggregations (`_calculate_cumulative_totals_prod`, `get_inventory_summary_data`), Excel exporting via openpyxl, Role-based view guards.
- **Move to React**: UI interaction logic (`cascade_select.js`, `excel_filter.js`), pre-submit form validation, and pagination UI state.
