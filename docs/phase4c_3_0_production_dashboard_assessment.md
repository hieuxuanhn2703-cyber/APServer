# Phase 4C-3-0 — Production Dashboard Migration Assessment

---

## 1. Executive Summary

### 1.1 Context & Objectives
This assessment is conducted under **Phase 4C-3-0: Production Dashboard Migration Assessment** of the `ProcessMonitoring` project. The overarching objective is to migrate the legacy Django Template production monitoring views to the modern React application (`frontend/`) in an incremental, zero-regression manner.

Prior completed phases:
* **Phase 3A – 3D**: Django REST API architecture, JWT authentication, and app-specific REST endpoints (PASS).
* **Phase 4A – 4B**: React Foundation and App Shell (PASS).
* **Phase 4C-1A / 4C-1B**: Accounting Dashboard Migration & Verification (PASS).
* **Phase 4C-2 / 4C-2B / 4C-2B-FINAL**: Inventory Summary Migration & Verification (PASS).

This assessment determines whether the **Production Dashboard** (`Báo Cáo Sản Xuất` / `Tổng Hợp Dữ Liệu` and `Theo Dõi Đơn Hàng`) is technically ready for React migration without altering backend business logic, changing database schema, or disrupting operational stability.

### 1.2 Key Audit Findings
1. **Dual Architectural Scope in Legacy Production Reporting**:
   * **Stage-by-Stage Detailed Activity Log** (Tabbed Dashboard: `/dashboard/cut/`, `/dashboard/prod/`, `/dashboard/kcs/`, `/dashboard/finishing/`): Displays chronological daily report entries (115 Cut rows, 113 Process rows, 105 KCS rows, 104 Finishing rows in the active database) featuring daily input values alongside running cumulative totals calculated dynamically via in-memory ordering (`_calculate_cumulative_totals_*`), with inline Edit/Delete actions and server-side multi-column cascading filter dropdowns.
   * **Order Balance Tracking Matrix** (`/tracking/`): Compares total order commitments (`ProductColor.quantity`) across all 7 sewing and finishing stages (`nhan_btp`, `vao_chuyen`, `giua_chuyen`, `ra_chuyen`, `thu_hoa`, `la_thanh_pham`, `nhap_hoan_thien`) to display completed vs. remaining balances for each product-color variant.
2. **Existing REST API Architecture & Granularity Mismatch**:
   * Under `/api/v1/working/dashboards/` (`cut/`, `process/`, `kcs/`, `finishing/`), existing endpoints return high-level summary aggregations grouped by `(ma_hang, mau)`. They do **not** return the chronological daily log entries or running cumulative totals.
   * Under `/api/v1/working/reports/` (`cut/`, `process/`, `kcs/`, `finishing/`), ViewSets return individual report entries with pagination, but they do **not** provide cumulative running sums or joined order quantities (`tong_don_hang`).
3. **Critical Missing API**:
   * There is **no REST API endpoint** for the Order Tracking Matrix (`get_tracking_data()`).
4. **Role & Permission Mismatch**:
   * Legacy Django views allow access to roles `['PREMIUM', 'QUAN_LY', 'KE_TOAN']`.
   * Existing `Dashboard*APIView` endpoints enforce `permission_classes = [IsAdminOrManager]`, which only permits `['PREMIUM', 'QUAN_LY']`. A user with role `KE_TOAN` receives an HTTP `403 Forbidden` despite having navigation access in `Sidebar.jsx`.

### 1.3 Assessment Verdict
**Verdict: `READY WITH CONDITIONS`**

The project has robust data models, functioning database aggregations, and proven React architectural patterns. However, before UI components can be built in Phase 4C-3, three specific backend gaps (Tracking API endpoint, `KE_TOAN` permission alignment, and activity log response shape) must be addressed.

---

## 2. Current Legacy Production Dashboard

The legacy production reporting interface consists of two primary functional components accessible from the main navigation:

### 2.1 Tabbed Stage-by-Stage Dashboard (`/dashboard/`)
* **URLs**:
  * `/dashboard/` (Alias to `/dashboard/cut/`, route name `premium_dashboard`)
  * `/dashboard/cut/` (Route name `dashboard_cut`)
  * `/dashboard/prod/` (Route name `dashboard_prod`)
  * `/dashboard/kcs/` (Route name `dashboard_kcs`)
  * `/dashboard/finishing/` (Route name `dashboard_finishing`)
  * `/dashboard/kho/` (Route name `dashboard_kho` — inventory summary tab, already migrated in Phase 4C-2)
* **Templates**:
  * `dashboard_cut.html`: Displays 4 cutting stages (Cắt chính, Cắt lót, Cắt Mex, Cắt bông).
  * `dashboard_prod.html`: Displays 7 sewing stages (Nhận BTP, Vào chuyền, Giữa chuyền, Ra chuyền, Thu hóa, Là TP, Nhập HT) grouped by Xưởng and Tổ.
  * `dashboard_kcs.html`: Displays 4 quality inspection stages (Qua tay, Đạt, Lỗi, Tổng đạt).
  * `dashboard_finishing.html`: Displays 3 packing stages (Thẻ bài, Gấp hàng, Treo/Đóng thùng) + comparison against `tong_nhap_hoan_thien` from `ProcessReport`.
  * `dashboard_nav_tabs.html`: Shared tab bar linking all 5 tabs.
* **Key Visual Characteristics**:
  * Diagonal split table cells (`.diagonal-cell`) displaying daily input (`.top-val`) and cumulative sum (`.bot-val`).
  * Row actions: "Sửa" (`/edit/<id>/`) and "Xóa" (`/delete/<id>/`).
  * Date range filter (`start_date`, `end_date`).
  * Excel-style multi-column filter dropdowns (`.excel-filter-btn`) powered by server-side cascading options (`_get_cascade_options`).
  * Pagination (50 rows per page).
  * Excel Export button (`/export-excel/`).

### 2.2 Order Tracking Matrix (`/tracking/`)
* **URL**: `/tracking/` (Route name `tracking`), `/tracking/export/` (Route name `tracking_export_excel`)
* **Template**: `tracking.html`
* **Purpose**: Provides order balance visibility per `(Product, ProductColor)`.
* **Table Columns (17 columns)**:
  1. Mã hàng (Product name)
  2. Màu (Color name)
  3. Số lượng ĐH (Order quantity from `ProductColor.quantity`)
  4. Nhận BTP: Đã Nhập / Còn lại
  5. Vào Chuyền: Đã Vào / Còn lại
  6. Giữa chuyền: Đã Ra / Còn lại
  7. Ra Chuyền: Đã Ra / Còn lại
  8. Thu Hoá: Đã Thu / Còn lại
  9. Là thành phẩm: Đã Làm / Còn lại
  10. Nhập Hoàn Thiện: Đã Nhập / Còn lại
* **Logic**: `Còn lại = Số lượng ĐH - Đã làm`. If negative, the cell is highlighted with class `con-lai-am` (red badge).
* **Filters**: Mã hàng, Màu (cascading dropdowns).

---

## 3. Source-of-Truth Audit

### 3.1 Traceability Mapping Table

| UI Element / View | Template Path | Django View | Service / Helper | Data Source | Calculation Logic |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Tổng hợp Cắt** | `Working/templates/dashboard_cut.html` | `dashboard_cut_view` (`views.py:1448`) | `_calculate_cumulative_totals_cut`, `_dashboard_cut_report_to_row` | `CutReport`, `ProductColor` | Running cumulative sum per `(ma_hang, mau)` ordered by `(created_at, id)` |
| **Tổng hợp Sản xuất** | `Working/templates/dashboard_prod.html` | `dashboard_prod_view` (`views.py:1523`) | `_calculate_cumulative_totals_prod`, `_dashboard_prod_report_to_row` | `ProcessReport`, `ProductColor` | Running cumulative sum per `(ma_hang, mau, xuong, to)` ordered by `(created_at, id)` |
| **Tổng hợp KCS** | `Working/templates/dashboard_kcs.html` | `dashboard_kcs_view` (`views.py:1613`) | `_calculate_cumulative_totals_kcs`, `_dashboard_kcs_report_to_row` | `KcsReport`, `ProductColor` | Running cumulative sum per `(ma_hang, mau)` ordered by `(created_at, id)` |
| **Tổng hợp Hoàn thiện**| `Working/templates/dashboard_finishing.html` | `dashboard_finishing_view` (`views.py:1703`) | `_calculate_cumulative_totals_finishing`, `_dashboard_finishing_report_to_row` | `FinishingReport`, `ProcessReport`, `ProductColor` | Running cumulative sum per `(ma_hang, mau)` + total `nhap_hoan_thien` from `ProcessReport` |
| **Theo dõi Đơn hàng** | `Working/templates/tracking.html` | `tracking_view` (`views.py:850`) | `get_tracking_data` (`views.py:796`) | `Product`, `ProductColor`, `ProcessReport` | Aggregates all 7 sewing stages per `(ma_hang, mau)` and calculates `remaining = order_qty - stage_sum` |
| **Tổng hợp Kho (Tab)** | `Working/templates/dashboard_kho.html` | `dashboard_kho_view` (`views.py:1796`) | `Inventory.views.get_inventory_summary_data` | `MaterialReceipt`, `MaterialIssue` | Inventory balance (already migrated to `/inventory` in Phase 4C-2) |

---

## 4. Legacy Data Flow

### 4.1 Production Pipeline Data Flow
```text
[Product] ──(1:N)──> [ProductColor] (Order Target: quantity)
                           │
    ┌──────────────────────┼──────────────────────┬──────────────────────┐
    ▼                      ▼                      ▼                      ▼
[CutReport]         [ProcessReport]          [KcsReport]        [FinishingReport]
(Stage: Cắt)        (Stage: Chuyền May)     (Stage: KCS)        (Stage: Đóng gói)
- cat_chinh         - nhan_btp               - qua_tay           - the_bai
- cat_lot           - vao_chuyen             - dat               - gap_hang
- cat_mex           - giua_chuyen            - loi               - treo_dong_thung
- cat_bong          - ra_chuyen              - tong_dat                  │
    │               - thu_hoa                     │                      │
    │               - la_thanh_pham               │                      │
    │               - nhap_hoan_thien ────────────┼──────────────────────┘
    │                      │                      │           (Cross-stage balance)
    ▼                      ▼                      ▼                      ▼
[dashboard_cut]     [dashboard_prod]       [dashboard_kcs]     [dashboard_finishing]
(Daily & Cumulative) (Daily & Cumulative)  (Daily & Cumulative) (Daily & Cumulative)
                           │
                           ▼
                    [tracking_view]
            (Order Quantity vs 7 Stages Matrix)
```

### 4.2 Data Integrity Details
* `Product` has a 1-to-many relationship with `ProductColor`.
* Production report tables (`CutReport`, `ProcessReport`, `KcsReport`, `FinishingReport`) store `ma_hang` and `mau` as strings. Joins with `ProductColor` are performed in Python application code using composite key tuples `(ma_hang, mau)`.
* Report ownership is enforced via `nguoi_nhap` (`ForeignKey` to `AppUser`).
* Audit timestamps (`created_at`) determine the sequence for running cumulative totals.

---

## 5. Production Business Logic

### 5.1 Calculations Inventory

| Calculation Name | Code Location | Inputs | Output | Exposed in REST API? | React Direct Usability |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Cumulative Totals (Cut)** | `Working/views.py:1268` | `CutReport.objects.order_by('created_at', 'id')` | Dict: `report.id -> {total_cat_chinh, total_cat_lot, total_cat_mex, total_cat_bong}` | **NO** (API only returns grouped total) | Requires backend exposure |
| **Cumulative Totals (Process)** | `Working/views.py:1290` | `ProcessReport.objects.order_by('created_at', 'id')` grouped by `(ma_hang, mau, xuong, to)` | Dict: `report.id -> {total_nhan_btp, ..., total_nhap_hoan_thien}` | **NO** (API only returns grouped total) | Requires backend exposure |
| **Cumulative Totals (KCS)** | `Working/views.py:1246` | `KcsReport.objects.order_by('created_at', 'id')` | Dict: `report.id -> {total_qua_tay, total_dat, total_loi, total_tong_dat}` | **NO** (API only returns grouped total) | Requires backend exposure |
| **Cumulative Totals (Finishing)**| `Working/views.py:1226` | `FinishingReport.objects.order_by('created_at', 'id')` | Dict: `report.id -> {total_the_bai, total_gap_hang, total_treo_dong_thung}` | **NO** (API only returns grouped total) | Requires backend exposure |
| **Stage Aggregations** | `Working/services.py:4-125` | `CutReport`, `ProcessReport`, `KcsReport`, `FinishingReport` + filters | List of dicts grouped by `(ma_hang, mau)` with sums | **YES** (`/api/v1/working/dashboards/*`) | Ready for summary cards & charts |
| **Tracking Matrix (Balances)** | `Working/views.py:796` | `Product`, `ProductColor`, `ProcessReport` | List of dicts with `so_luong`, completed, and remaining per stage | **NO** (No API endpoint exists) | Critical missing backend logic |
| **Pending Exceptions Count** | `Working/views.py:1770` | `DefectReturnReport`, `SampleTakeReport` | Integer: `total_pending_ngoai_le` | **PARTIAL** (Can count via report list API) | Can be queried or provided in meta |

> [!IMPORTANT]
> In accordance with Migration Principle 2.1 and Rule 7, React must NOT reimplement in-memory running cumulative calculations or order balance subtractions. All cumulative progressions and balance calculations must be delivered directly by the backend.

---

## 6. Existing REST API Inventory

### 6.1 Inventory Table (`/api/v1/working/`)

| Endpoint | Method | Purpose | Serializer | Permission | Response Shape | Production Dashboard Usable? |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `/api/v1/working/dashboards/cut/` | `GET` | Cut summary totals | Dict (ad-hoc) | `IsAdminOrManager` | `[{ma_hang, mau, total_cat_chinh, ..., tong_don_hang}]` | **YES** (For summary view) |
| `/api/v1/working/dashboards/process/`| `GET` | Sewing process summary totals | Dict (ad-hoc) | `IsAdminOrManager` | `[{ma_hang, mau, total_nhan_btp, ..., tong_don_hang}]` | **YES** (For summary view) |
| `/api/v1/working/dashboards/kcs/` | `GET` | KCS summary totals | Dict (ad-hoc) | `IsAdminOrManager` | `[{ma_hang, mau, total_qua_tay, ..., tong_don_hang}]` | **YES** (For summary view) |
| `/api/v1/working/dashboards/finishing/`| `GET` | Finishing summary totals | Dict (ad-hoc) | `IsAdminOrManager` | `[{ma_hang, mau, total_the_bai, ..., tong_don_hang}]` | **YES** (For summary view) |
| `/api/v1/working/reports/cut/` | `GET`, `POST` | Cut report entries CRUD | `CutReportSerializer` | `IsAppUser` + role check | Paginated list / Object | **PARTIAL** (Has entries, lacks cumulative sums) |
| `/api/v1/working/reports/process/` | `GET`, `POST` | Process report entries CRUD | `ProcessReportSerializer` | `IsAppUser` + role check | Paginated list / Object | **PARTIAL** (Has entries, lacks cumulative sums) |
| `/api/v1/working/reports/kcs/` | `GET`, `POST` | KCS report entries CRUD | `KcsReportSerializer` | `IsAppUser` + role check | Paginated list / Object | **PARTIAL** (Has entries, lacks cumulative sums) |
| `/api/v1/working/reports/finishing/`| `GET`, `POST` | Finishing report entries CRUD | `FinishingReportSerializer`| `IsAppUser` + role check | Paginated list / Object | **PARTIAL** (Has entries, lacks cumulative sums) |
| `/api/v1/working/dashboards/tracking/`| `GET` | Order progress tracking matrix | None | None | None | **MISSING** (Endpoint does not exist) |

---

## 7. Production Matrix API Assessment

| Capability | Legacy Template | Existing REST API | Status | Source-Code Evidence |
| :--- | :--- | :--- | :--- | :--- |
| **Production Summary** | Present in legacy tabs | Available | **READY** | `Working/services.py:4-125` via `Dashboard*APIView` |
| **Order Tracking Matrix** | `tracking.html` | Not implemented | **MISSING** | `Working/views.py:796` (`get_tracking_data`) has no DRF counterpart |
| **Product-level Production** | Present | Available | **READY** | Filterable by `ma_hang` query param |
| **Color-level Production** | Present | Available | **READY** | Filterable by `mau` query param |
| **Size-level Production** | Optional in reports | In serializers | **NOT REQUIRED** | Dashboard views group by `(ma_hang, mau)`, not size |
| **Production Stage Comparison**| Tracking table | Not exposed | **MISSING** | 7-stage comparison only in `get_tracking_data` |
| **Stage Remaining Balances** | Tracking table | Not exposed | **MISSING** | Negative balance calculation in `get_tracking_data` |
| **Activity Log Cumulative Sums**| Present in all 4 tabs | Not exposed | **MISSING** | Cumulative running totals only exist in `views.py:1226-1330` |
| **Date Filtering** | `start_date`, `end_date` | Available | **READY** | Accepted by `Dashboard*APIView` query params |
| **Workshop/Team Filtering** | `xuong`, `to` in Prod/KCS | Partial | **PARTIAL** | ViewSets support filter, `DashboardProcessAPIView` lacks `xuong`/`to` params |

---

## 8. Role & Authorization Assessment

### 8.1 Authorization Comparison Matrix

| Role | Legacy View Permission | Existing DRF API Permission | Expected React Route | Alignment Status |
| :--- | :--- | :--- | :--- | :--- |
| `PREMIUM` | Allowed (`views.py:1450`) | Allowed (`IsAdminOrManager`) | `/dashboard` | **ALIGNED** |
| `QUAN_LY` | Allowed (`views.py:1450`) | Allowed (`IsAdminOrManager`) | `/dashboard` | **ALIGNED** |
| `KE_TOAN` | Allowed (`views.py:1450`, `852`)| **FORBIDDEN (HTTP 403)** | `/dashboard` | **MISMATCH (GAP-PROD-02)** |
| `KHO` | Allowed for `dashboard_kho` | Forbidden for prod dashboards | `/inventory` | **ALIGNED** (Managed under Phase 4C-2) |
| `NHA_CAT` | Forbidden from Dashboard | Forbidden from Dashboard | `/working` | **ALIGNED** |
| `BASIC` | Forbidden from Dashboard | Forbidden from Dashboard | `/working` | **ALIGNED** |
| `KCS` | Forbidden from Dashboard | Forbidden from Dashboard | `/working` | **ALIGNED** |
| `HOAN_THIEN`| Forbidden from Dashboard | Forbidden from Dashboard | `/working` | **ALIGNED** |

### 8.2 Detailed Discrepancy Note: `KE_TOAN` Access
In `Working/views.py`:
```python
if current_user.role not in ['PREMIUM', 'QUAN_LY', 'KE_TOAN']:
    raise PermissionDenied("Chỉ quản trị viên cấp cao mới có quyền truy cập trang Dashboard.")
```
In `frontend/src/components/layout/Sidebar.jsx`:
```javascript
const canSeeDashboard = hasAnyRole(['PREMIUM', 'QUAN_LY', 'KE_TOAN']);
```
However, in `Working/api/views.py`:
```python
class DashboardCutAPIView(APIView):
    permission_classes = [IsAdminOrManager]  # Only 'PREMIUM' and 'QUAN_LY'
```
Consequently, when a `KE_TOAN` user logs in, they see the navigation link in the React sidebar, but all API calls to `/api/v1/working/dashboards/*` fail with an HTTP 403 Forbidden.

---

## 9. Production Actions / CRUD Assessment

| UI Action | Legacy Endpoint / Handler | Existing REST API | React Migration Readiness |
| :--- | :--- | :--- | :--- |
| **Sửa báo cáo Cắt** | `GET /cut/edit/<id>/` | `PATCH /api/v1/working/reports/cut/<id>/` | **READY** |
| **Xóa báo cáo Cắt** | `POST /cut/delete/<id>/` | `DELETE /api/v1/working/reports/cut/<id>/` | **READY** |
| **Sửa báo cáo Sản xuất** | `GET /edit/<id>/` | `PATCH /api/v1/working/reports/process/<id>/` | **READY** |
| **Xóa báo cáo Sản xuất** | `POST /delete/<id>/` | `DELETE /api/v1/working/reports/process/<id>/` | **READY** |
| **Sửa báo cáo KCS** | `GET /kcs/edit/<id>/` | `PATCH /api/v1/working/reports/kcs/<id>/` | **READY** |
| **Xóa báo cáo KCS** | `POST /kcs/delete/<id>/` | `DELETE /api/v1/working/reports/kcs/<id>/` | **READY** |
| **Sửa báo cáo Hoàn thiện**| `GET /finishing/edit/<id>/` | `PATCH /api/v1/working/reports/finishing/<id>/`| **READY** |
| **Xóa báo cáo Hoàn thiện**| `POST /finishing/delete/<id>/` | `DELETE /api/v1/working/reports/finishing/<id>/`| **READY** |
| **Nhận lại hàng lỗi** | `POST /finishing/tra-hang/nhan-lai/<id>/` | `POST /api/v1/working/exceptions/defects/<id>/receive/` | **READY** |
| **Nhận lại mẫu** | `POST /finishing/lay-mau/nhan-lai/<id>/` | `POST /api/v1/working/exceptions/samples/<id>/receive/` | **READY** |
| **Xuất Excel Dashboard** | `GET /export-excel/?start_date=...` | Legacy URL / Client-side blob | **READY** (Can link directly or generate) |
| **Xuất Excel Tracking** | `GET /tracking/export/` | Legacy URL / Client-side blob | **READY** (Can link directly or generate) |

---

## 10. React Frontend Readiness

### 10.1 Inspection of `frontend/src/`
* **Route Configuration (`AppRoutes.jsx`)**:
  * `/dashboard` is currently routed to `<DashboardPlaceholder />`.
  * `HomeRedirect` sends `PREMIUM`, `QUAN_LY`, `KE_TOAN` to `/dashboard`.
* **Sidebar (`Sidebar.jsx`)**:
  * Displays "Báo Cáo Sản Xuất" (`/dashboard`) for `['PREMIUM', 'QUAN_LY', 'KE_TOAN']`.
  * Displays "Nhật Ký Làm Việc" (`/working`) for worker roles.
  * Displays "Quản Lý Kho" (`/inventory`) and "Kế Toán & Tài Chính" (`/accounting`).
* **Existing Reusable UI Primitives**:
  * Card containers: `.dash-card`, `.summary-card`
  * Tables: `.table-wrapper`, `.modern-table`
  * Buttons: `.btn-dash-filter`, `.btn-dash-clear`, `.btn-dash-excel`, `.action-btn-group`
  * Badges: `.badge-danger`, `.header-status-pill`
  * Dialogs / Modals: Established modal patterns from Accounting and Inventory migrations.
* **Component Architecture Recommendation for Phase 4C-3**:
  * `ProductionDashboardPage.jsx` (Main page container with tab switcher: "Tiến Độ Đơn Hàng" and "Chi Tiết Công Đoạn").
  * `OrderTrackingTab.jsx` (Replicates `tracking.html` matrix).
  * `StageActivityTab.jsx` (Replicates `dashboard_cut/prod/kcs/finishing.html` with sub-tabs for Cắt, Sản Xuất, KCS, Hoàn Thiện).
  * `ProductionSummaryCards.jsx` (Summary KPIs by stage).
  * `DiagonalCell.jsx` (Component rendering daily vs. cumulative values).

---

## 11. Legacy vs API Data Consistency

### 11.1 Real Database Quantitative Audit
Audited against the active MySQL database records:
* **Product**: 7 items
* **ProductColor**: 17 items
* **CutReport**: 115 records
* **ProcessReport**: 113 records
* **KcsReport**: 105 records
* **FinishingReport**: 104 records

### 11.2 Comparative Sample Verification
Comparing aggregated calculations between legacy Python service/views and DRF API views for sample product `AT1 - Navy` (Target order quantity: 1,000):

| Field / Metric | Legacy View Calculation | REST API Output (`DashboardCutAPIView`) | Status | Notes |
| :--- | :---: | :---: | :---: | :--- |
| `total_cat_chinh` | 2,450 | 2,450 | **MATCH** | Exact mathematical consistency |
| `total_cat_lot` | 2,055 | 2,055 | **MATCH** | Exact mathematical consistency |
| `total_cat_mex` | 1,544 | 1,544 | **MATCH** | Exact mathematical consistency |
| `total_cat_bong` | 1,969 | 1,969 | **MATCH** | Exact mathematical consistency |
| `tong_don_hang` | 1,000 | 1,000 | **MATCH** | Joined correctly from `ProductColor` |
| **Rows returned (Cut)** | 115 (individual entries) | 13 (summary rows) | **MISMATCH** | Aggregated vs. row-level detail discrepancy |
| **Tracking rows** | 17 (variant balances) | None (API 404/Missing) | **MISMATCH** | Tracking API missing |

---

## 12. Automated Verification

Automated checks were executed directly in the project environment:

### 12.1 Django System Check
* **Command**: `python manage.py check`
* **Result**: `System check identified no issues (0 silenced).` (Exit code: 0) — **PASS**

### 12.2 Django Migration Status Check
* **Command**: `python manage.py makemigrations --check`
* **Result**: `No changes detected` (Exit code: 0) — **PASS**

### 12.3 Working API Automated Test Suite
* **Command**: `python manage.py test Working.api.tests`
* **Result**:
  ```text
  Ran 7 tests in 0.195s
  OK
  Destroying test database for alias 'default'...
  ```
  — **PASS**

### 12.4 Working Comprehensive System Test Suite
* **Command**: `python manage.py test Working.tests`
* **Result**:
  ```text
  Ran 19 tests in 1.421s
  OK
  Destroying test database for alias 'default'...
  ```
  — **PASS**

---

## 13. Performance / Request Pattern Assessment

1. **Dashboard Tab Loading Pattern**:
   * If a unified dashboard page fetches all 4 stage summaries concurrently: 4 HTTP requests (`/dashboards/cut/`, `/dashboards/process/`, `/dashboards/kcs/`, `/dashboards/finishing/`).
   * Alternatively, with tab-based lazy loading, only 1 request is fired per active tab.
2. **Order Tracking Matrix Request Pattern**:
   * Once implemented, the tracking matrix requires **1 request** (`/api/v1/working/dashboards/tracking/`) with optional query filters (`ma_hang`, `mau`).
3. **Database Query Efficiency**:
   * Services in `Working/services.py` utilize `.values('ma_hang', 'mau').annotate(Sum(...))` which executes as a single SQL `GROUP BY` query.
   * `ProductColor` lookup is pre-cached into a Python dictionary (`color_map`), eliminating N+1 database queries.

---

## 14. Migration Risk Assessment

| Risk ID | Risk Description | Severity | Evidence | Impact | Recommended Mitigation |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **RISK-01** | Missing Order Tracking API | **HIGH** | `get_tracking_data` only exists in `Working/views.py:796` | Cannot render `/tracking/` in React | Expose `DashboardTrackingAPIView` before React implementation |
| **RISK-02** | Granularity Mismatch (Summary vs Daily Logs) | **HIGH** | `Dashboard*APIView` returns 13 rows; legacy tables render 115 daily rows | React UI cannot show daily logs if relying solely on dashboard endpoints | Design React UI with distinct Summary and Activity Log sections; enhance Report ViewSets to return cumulative sums |
| **RISK-03** | Authorization Mismatch for `KE_TOAN` | **MEDIUM** | `IsAdminOrManager` restricts to `['PREMIUM', 'QUAN_LY']` | `KE_TOAN` users experience 403 Forbidden | Update permission class to allow `KE_TOAN` on read-only dashboard endpoints |
| **RISK-04** | Dual Concept Confusion in Navigation | **LOW** | Legacy sidebar has "Tổng hợp dữ liệu" and "Theo dõi Đơn hàng" as 2 links | Users could be disoriented if merged improperly | Provide clear sub-tabs in React: "Tiến Độ Đơn Hàng" (Tracking) & "Báo Cáo Công Đoạn" (Stages) |
| **RISK-05** | Cascading Filter State Complexity | **LOW** | Legacy uses server-rendered `_get_cascade_options` | Filter dropdown options need dynamic updates | Fetch unique product/color options from existing config endpoints |

---

## 15. Migration Readiness Matrix

| Capability | Legacy Template Status | REST API Status | React Application Status | Overall Readiness |
| :--- | :---: | :---: | :---: | :---: |
| **Routing** | PASS | PASS | PASS (Placeholder at `/dashboard`) | **PASS** |
| **Authentication** | PASS | PASS (JWT) | PASS (`AuthContext`) | **PASS** |
| **Authorization** | PASS | PARTIAL (`KE_TOAN` blocked) | PASS (`useRoles`) | **PARTIAL** |
| **Production Summary (KPIs)**| PASS | PASS (`Dashboard*APIView`) | READY to implement | **PASS** |
| **Order Tracking Matrix** | PASS | MISSING | READY to implement | **MISSING** |
| **Product Filter** | PASS | PASS (`ma_hang`) | READY to implement | **PASS** |
| **Color Filter** | PASS | PASS (`mau`) | READY to implement | **PASS** |
| **Workshop/Team Filter** | PASS | PARTIAL | READY to implement | **PARTIAL** |
| **Date Range Filter** | PASS | PASS (`start_date`, `end_date`)| READY to implement | **PASS** |
| **Production Stages (4 tabs)**| PASS | PASS | READY to implement | **PASS** |
| **KPI Calculations** | PASS | PASS | READY to implement | **PASS** |
| **Cumulative Running Totals**| PASS | MISSING in ViewSets | READY to implement | **MISSING** |
| **Status / Remainder Display**| PASS | MISSING in API | READY to implement | **MISSING** |
| **CRUD Actions (Sửa / Xóa)** | PASS | PASS (ViewSets) | READY to implement | **PASS** |
| **Exception Receive Actions** | PASS | PASS (`defects/receive`) | READY to implement | **PASS** |
| **Error / Empty / Loading** | PASS | PASS | PASS (Standardized React components)| **PASS** |
| **Responsive UI (Mobile Cards)**| PASS | N/A | READY (Vanilla CSS patterns) | **PASS** |
| **Legacy Fallback / Parallel** | PASS | PASS | PASS (Django routes remain intact) | **PASS** |

---

## 16. Backend/API Gap Analysis

### GAP-PROD-01: Order Tracking Matrix API Missing
* **Description**: Legacy `tracking_view` calls `get_tracking_data(filter_ma_hang, filter_mau)` to produce the 7-stage order progress balance matrix. No REST API endpoint currently exposes this data.
* **Current State**: Only exists in `Working/views.py:796`.
* **Required State**: Dedicated GET endpoint `/api/v1/working/dashboards/tracking/`.
* **Affected Files**: `Working/services.py`, `Working/api/views.py`, `Working/api/urls.py`.
* **Request**: `GET /api/v1/working/dashboards/tracking/?ma_hang=...&mau=...`
* **Response**: List of variant objects containing `ma_hang`, `mau`, `so_luong`, and pairs of `(lam, con)` for all 7 stages.
* **Permission**: `PREMIUM`, `QUAN_LY`, `KE_TOAN`.
* **Risk**: High (Blocker for Tracking view migration).
* **Recommended Phase**: Phase 4C-3A.

### GAP-PROD-02: Permission Restriction Blocking `KE_TOAN`
* **Description**: `DashboardCutAPIView`, `DashboardProcessAPIView`, `DashboardKcsAPIView`, `DashboardFinishingAPIView` use `permission_classes = [IsAdminOrManager]`, which only checks `['PREMIUM', 'QUAN_LY']`. In legacy Django, `KE_TOAN` has full access to dashboards and tracking.
* **Current State**: `IsAdminOrManager` excludes `KE_TOAN`.
* **Required State**: Allow `['PREMIUM', 'QUAN_LY', 'KE_TOAN']` on dashboard read-only endpoints.
* **Affected Files**: `Working/api/permissions.py` (or view-level permission classes in `Working/api/views.py`).
* **Risk**: Medium.
* **Recommended Phase**: Phase 4C-3A.

### GAP-PROD-03: Activity Log Cumulative Totals in Report APIs
* **Description**: The legacy dashboard tables display daily report records along with running cumulative totals up to that record's date. Existing ViewSets (`CutReportViewSet`, etc.) return records without cumulative sums.
* **Current State**: In-memory calculations exist only in `Working/views.py:1226-1330`.
* **Required State**: Either:
  1. Add an annotated or serialized running total field to the report list endpoints when requested with `?with_totals=true`, or
  2. Structure the React Production Dashboard to prominently feature the Summary Aggregations & Order Tracking Matrix, with a drill-down/activity tab that calls the report list.
* **Affected Files**: `Working/api/views.py`, `Working/api/serializers.py`.
* **Risk**: Medium.
* **Recommended Phase**: Phase 4C-3A.

---

## 17. Recommended Phase 4C-3 Scope

To ensure a smooth, zero-regression implementation, Phase 4C-3 should be structured into three sub-phases:

### Sub-Phase 4C-3A: Backend & API Hardening
* Implement `get_tracking_dashboard_data()` in `Working/services.py` based on `get_tracking_data()`.
* Create `DashboardTrackingAPIView` under `/api/v1/working/dashboards/tracking/`.
* Update permissions on dashboard endpoints to permit `KE_TOAN` (matching legacy views).
* Write automated DRF test coverage for all dashboard endpoints including tracking and role isolation.

### Sub-Phase 4C-3B: React Production Dashboard Implementation
* Replace `DashboardPlaceholder.jsx` with full `ProductionDashboardPage.jsx`.
* Implement tabbed interface:
  * **Tab 1: Tiến Độ Đơn Hàng (Order Tracking)**: Summary matrix of order quantity vs 7 stages, progress bars, negative balance highlighting (`con-lai-am`).
  * **Tab 2: Tổng Hợp Công Đoạn (Stage Summaries)**: 4 sub-views (Cắt, Sản Xuất, KCS, Hoàn Thiện) showing summary metrics, KPI cards, and activity logs.
* Implement filter bar: Date range, product multi-select, color multi-select.
* Implement mobile responsive card layouts matching project standards.
* Add Excel export link integrating legacy export endpoints.

### Sub-Phase 4C-3C: Verification & Hardening
* Automated tests (Django backend + frontend build verification).
* Verification of data consistency against live MySQL database.
* Full browser verification of role-based visibility and interactive filters.

---

## 18. Explicit Out-of-Scope Items

The following items are explicitly **OUT OF SCOPE** for Phase 4C-3:
1. **Worker Data Entry Forms**: Migrating the daily entry forms (`/web/`, `/cut/`, `/kcs/`, `/finishing/`) remains under Phase 4D.
2. **Database Schema / Migration Changes**: No new database fields or table alterations.
3. **Inventory & Accounting Codebase**: Inventory summary and accounting dashboards were already migrated and sealed in Phases 4C-1 and 4C-2.
4. **Altering Production Calculations**: The formulas for order balance, stage sums, and cumulative totals must remain 100% identical to legacy Django views.

---

## 19. Change Control

* **Files modified**: `0`
* **Files added**: `1` (`docs/phase4c_3_0_production_dashboard_assessment.md`)
* **Files deleted**: `0`
* **Models modified**: `0`
* **Migrations created**: `0`
* **Dependencies added**: `0`
* **Tests modified**: `0`

---

## 20. Final Verdict

# VERDICT: READY WITH CONDITIONS

### Summary of Conditions:
1. **Condition 1 (GAP-PROD-01)**: Implement `/api/v1/working/dashboards/tracking/` to expose the Order Progress Tracking Matrix before React UI implementation.
2. **Condition 2 (GAP-PROD-02)**: Update DRF dashboard view permissions to authorize `KE_TOAN` in alignment with legacy views and `Sidebar.jsx`.
3. **Condition 3 (GAP-PROD-03)**: Finalize API response format for detailed activity logs to support running cumulative progression.

Once these three small, well-bounded backend conditions are resolved in Phase 4C-3A, React implementation in Phase 4C-3B can proceed with zero risk of architectural rework or regression.
