# Phase 4C-3A — Production Dashboard Backend & API Hardening

## 1. Executive Summary

Phase 4C-3A resolves all three backend/API gaps identified during Phase 4C-3-0 (Production Dashboard Migration Assessment):
- **GAP-PROD-01**: The legacy Order Tracking Matrix business logic (`get_tracking_data()`) has been refactored into a reusable, authoritative service (`get_tracking_dashboard_data()`) in `Working/services.py` and exposed via REST API endpoint `GET /api/v1/working/dashboards/tracking/`.
- **GAP-PROD-02**: Permission authorization for the Production Dashboard suite has been hardened via `IsProductionDashboardViewer` (`Working/api/permissions.py`), granting access to `PREMIUM`, `QUAN_LY`, and `KE_TOAN` (resolving the previous HTTP 403 Forbidden for Accountant roles) while strictly blocking worker roles (`BASIC`, `NHA_CAT`, `KCS`, `HOAN_THIEN`, `KHO`).
- **GAP-PROD-03**: Activity log endpoints (`/reports/cut/`, `/reports/process/`, `/reports/kcs/`, `/reports/finishing/`) now optionally support running cumulative progression totals via `?with_totals=true`. When omitted, endpoints maintain 100% backwards compatibility for existing worker data-entry clients.

**Key Metrics & Verification**:
- Database Schema Changes: **0 models modified, 0 migrations created**.
- Automated Backend Tests: **13/13 API tests passed**, **19/19 Working legacy tests passed**.
- Legacy vs. API Consistency Verification: **887/887 data points matched (100% agreement, 0 mismatches)** across operational database records.
- React Implementation: **0 frontend files modified**; Phase 4C-3B gate conditions fully met.
- **Phase Verdict: PASS**.

---

## 2. GAP-PROD-01 — Tracking API

### 2.1 Legacy Logic
In the legacy Django monolith, `tracking_view(request)` in `Working/views.py` queried all products with prefetch colors (`Product.objects.prefetch_related('colors').all()`), aggregated total completion for all 7 production stages from `ProcessReport` grouped by `('ma_hang', 'mau')`, and calculated stage-by-stage remaining quantities (`con = so_luong - da_lam`), allowing negative balances when production exceeded order quantities.

### 2.2 Service Extraction
The business logic was extracted into `Working/services.py` as:
```python
def get_tracking_dashboard_data(filter_ma_hang=None, filter_mau=None):
```
To eliminate code duplication, `Working/views.py`'s `get_tracking_data()` was refactored to delegate directly to `get_tracking_dashboard_data()`. Both legacy view templates (`tracking.html`), Excel exports (`tracking_export_excel_view`), and the REST API share this single source of truth.

### 2.3 API Endpoint
Registered in `Working/api/urls.py` as:
```text
GET /api/v1/working/dashboards/tracking/
Endpoint Name: api:dashboard-tracking
Controller: DashboardTrackingAPIView (Working/api/views.py)
```

### 2.4 Request Parameters
The endpoint supports optional filtering by product and color:
- `?ma_hang=<str>` or `?ma_hang=<val1>&ma_hang=<val2>`: Filter by one or more product names.
- `?mau=<str>` or `?mau=<val1>&mau=<val2>`: Filter by one or more color names.
- Case-sensitivity and empty filter behavior replicate legacy `tracking_view()`.

### 2.5 Response Contract
The endpoint returns an array of objects. Each item contains both the structured stage objects (recommended for React UI component binding) and flat legacy keys (for legacy backward compatibility):
```json
[
  {
    "ma_hang": "AT1",
    "mau": "Navy",
    "so_luong": 1000,
    "nhan_btp": { "lam": 900, "con": 100 },
    "vao_chuyen": { "lam": 850, "con": 150 },
    "giua_chuyen": { "lam": 800, "con": 200 },
    "ra_chuyen": { "lam": 750, "con": 250 },
    "thu_hoa": { "lam": 700, "con": 300 },
    "la_thanh_pham": { "lam": 650, "con": 350 },
    "nhap_hoan_thien": { "lam": 600, "con": 400 },
    "nhan_btp_nhap": 900,
    "nhan_btp_con": 100,
    "vao_chuyen_vao": 850,
    "vao_chuyen_con": 150,
    "giua_chuyen_ra": 800,
    "giua_chuyen_con": 200,
    "ra_chuyen_ra": 750,
    "ra_chuyen_con": 250,
    "thu_hoa_thu": 700,
    "thu_hoa_con": 300,
    "la_thanh_pham_lam": 650,
    "la_thanh_pham_con": 350,
    "nhap_hoan_thien_nhap": 600,
    "nhap_hoan_thien_con": 400
  }
]
```

### 2.6 Permission
Secured with `IsProductionDashboardViewer` requiring JWT authentication and role in `['PREMIUM', 'QUAN_LY', 'KE_TOAN']`.

### 2.7 Tests
Automated test `test_tracking_dashboard_data_shape_and_calculations` in `Working/api/tests.py` verifies:
- All 7 stages, order quantities, completed values, and remaining balances.
- Negative remaining values when production exceeds orders (e.g. order 1,000, nhan_btp 1,100 -> remaining -100).
- Filter testing in `test_tracking_dashboard_filters` covering `?ma_hang=`, `?mau=`, and combined filtering.

---

## 3. GAP-PROD-02 — KE_TOAN Permission

### 3.1 Previous Behavior
Previously, production dashboard views (`DashboardCutAPIView`, `DashboardProcessAPIView`, `DashboardKcsAPIView`, `DashboardFinishingAPIView`) were secured with `IsAdminOrManager`, which allowed only `PREMIUM` and `QUAN_LY`. Consequently, `KE_TOAN` received `HTTP 403 Forbidden` despite possessing legitimate view access on the legacy templates.

### 3.2 New Behavior
A dedicated permission class `IsProductionDashboardViewer` was introduced without altering `IsAdminOrManager` elsewhere:
```python
class IsProductionDashboardViewer(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user 
            and hasattr(request.user, 'role') 
            and request.user.role in ['PREMIUM', 'QUAN_LY', 'KE_TOAN']
        )
```

### 3.3 Permission Design
The permission was attached to all 5 dashboard views:
1. `DashboardCutAPIView`
2. `DashboardProcessAPIView`
3. `DashboardKcsAPIView`
4. `DashboardFinishingAPIView`
5. `DashboardTrackingAPIView`

### 3.4 Regression Tests
Automated test `test_dashboard_permissions_and_ke_toan_access` in `Working/api/tests.py` explicitly tests:
- **Unauthenticated**: 401 Unauthorized across all 5 dashboard endpoints.
- **Authorized Roles (200 OK)**:
  - `PREMIUM`: 200 OK across all 5 endpoints.
  - `QUAN_LY`: 200 OK across all 5 endpoints.
  - `KE_TOAN`: 200 OK across all 5 endpoints (verifying GAP-PROD-02 resolution).
- **Unauthorized Worker Roles (403 Forbidden)**:
  - `BASIC`: 403 Forbidden across all 5 endpoints.
  - `NHA_CAT`: 403 Forbidden across all 5 endpoints.
  - `KCS`: 403 Forbidden across all 5 endpoints.
  - `HOAN_THIEN`: 403 Forbidden across all 5 endpoints.
  - `KHO`: 403 Forbidden across all 5 endpoints.

---

## 4. GAP-PROD-03 — Activity Log Cumulative Totals

### 4.1 Legacy Algorithm
The legacy production dashboard computes cumulative progression totals in chronological order (`order_by('created_at', 'id')`).
- **Cut**: Grouped by `(ma_hang, mau)` accumulating `cat_chinh`, `cat_lot`, `cat_mex`, `cat_bong`.
- **Process**: Grouped by `(ma_hang, mau, xuong, to)` accumulating `nhan_btp`, `vao_chuyen`, `giua_chuyen`, `ra_chuyen`, `thu_hoa`, `la_thanh_pham`, `nhap_hoan_thien`.
- **KCS**: Grouped by `(ma_hang, mau)` accumulating `qua_tay`, `dat`, `loi`, `tong_dat`.
- **Finishing**: Grouped by `(ma_hang, mau)` accumulating `the_bai`, `gap_hang`, `treo_dong_thung`.

These algorithms are implemented in `Working/services.py`:
- `calculate_cumulative_totals_cut()`
- `calculate_cumulative_totals_prod()`
- `calculate_cumulative_totals_kcs()`
- `calculate_cumulative_totals_finishing()`

Legacy views (`Working/views.py`) have been refactored to delegate directly to these service functions.

### 4.2 API Design
To avoid breaking existing mobile/web worker clients, cumulative totals are triggered by query parameter:
```text
?with_totals=true
```
When `with_totals=true` is requested:
- ViewSets compute the cumulative map in a single pass ($O(N)$) and inject it into serializer context.
- Serializers (`to_representation`) attach:
  - `cumulative`: Dict of cumulative totals up to that record.
  - `tong_don_hang`: Total order quantity for `(ma_hang, mau)`.
  - `tong_nhap_hoan_thien`: Total received from sewing (`nhap_hoan_thien`) for Finishing reports.

### 4.3 Backwards Compatibility
When `with_totals` is absent or false:
- Serializers omit `cumulative` and `tong_don_hang`.
- Existing worker data entry and CRUD flows remain 100% identical.

### 4.4 Pagination Behavior
Because cumulative totals are calculated chronologically across the entire dataset in the service layer, records on Page 2, Page 3, etc., correctly preserve their cumulative progression relative to history. They do NOT restart at 0 on page transitions.

### 4.5 Tests
Automated tests in `Working/api/tests.py`:
- `test_cumulative_totals_activity_log_cut`: Confirms lack of cumulative fields without parameter, and exact cumulative progression (`100 -> 150 -> 175`) with `?with_totals=true`.
- `test_cumulative_totals_activity_log_process`: Confirms grouping boundary isolation (`(ma_hang, mau, xuong, to)`) between different workshops (`xuong=1` vs `xuong=2`).
- `test_cumulative_totals_activity_log_kcs_and_finishing`: Confirms KCS and Finishing progression and order quantity attachments.

---

## 5. Legacy vs REST API Data Consistency

A rigorous consistency verification script (`scratch/verify_consistency.py`) was executed against the real operational MySQL database records:

```text
======================================================================
1. VERIFY TRACKING DATA: LEGACY VS API
======================================================================
Number of tracking records - Legacy: 17, API: 17
Tracking fields compared: 527
Tracking matches: 527
Tracking mismatches: 0

======================================================================
2. VERIFY CUMULATIVE TOTALS: CUT REPORTS
======================================================================
Cut records checked: 20
Cut fields compared: 80
Cut matches: 80
Cut mismatches: 0

======================================================================
3. VERIFY CUMULATIVE TOTALS: PROCESS REPORTS
======================================================================
Process records checked: 20
Process fields compared: 140
Process matches: 140
Process mismatches: 0

======================================================================
4. VERIFY CUMULATIVE TOTALS: KCS REPORTS
======================================================================
KCS records checked: 20
KCS fields compared: 80
KCS matches: 80
KCS mismatches: 0

======================================================================
5. VERIFY CUMULATIVE TOTALS: FINISHING REPORTS
======================================================================
Finishing records checked: 20
Finishing fields compared: 60
Finishing matches: 60
Finishing mismatches: 0

======================================================================
OVERALL SUMMARY: 887/887 MATCHES, 0 MISMATCHES (100.0% CONSISTENCY)
======================================================================
```

---

## 6. Security Verification

1. **Role Access Control**:
   - `PREMIUM`, `QUAN_LY`, `KE_TOAN` authorized.
   - `BASIC`, `NHA_CAT`, `KCS`, `HOAN_THIEN`, `KHO` strictly rejected with HTTP 403 Forbidden.
2. **Unauthenticated Access**:
   - Rebuffed with HTTP 401 Unauthorized on all endpoints.
3. **Sensitive Field Protection**:
   - Passwords, hashes, and internal secret credentials are not exposed.
   - `nguoi_nhap` identity is preserved and protected against spoofing.

---

## 7. Performance Assessment

- **Single-Pass In-Memory Processing**: Cumulative maps are computed once per request in $O(N)$ memory passes, preventing $N \times M$ database query cascades.
- **Prefetch Optimization**: Product and color queries utilize `prefetch_related('colors')` and `select_related('nguoi_nhap')` to avoid N+1 query bottlenecks.
- **Execution Times**:
  - `Working.api.tests` (13 tests): 0.433 seconds.
  - `Working.tests` (19 tests): 1.396 seconds.

---

## 8. Automated Verification

| Command | Output | Status |
| :--- | :--- | :--- |
| `python manage.py check` | `System check identified no issues (0 silenced).` | PASS |
| `python manage.py makemigrations --check` | `No changes detected` | PASS |
| `python manage.py test Working.api.tests` | `Ran 13 tests in 0.433s - OK` | PASS |
| `python manage.py test Working.tests` | `Ran 19 tests in 1.396s - OK` | PASS |

---

## 9. Files Changed

1. `Working/services.py`:
   - Added `get_tracking_dashboard_data(filter_ma_hang, filter_mau)`.
   - Added `calculate_cumulative_totals_cut()`, `calculate_cumulative_totals_prod()`, `calculate_cumulative_totals_kcs()`, `calculate_cumulative_totals_finishing()`.
2. `Working/api/permissions.py`:
   - Added `IsProductionDashboardViewer` (`['PREMIUM', 'QUAN_LY', 'KE_TOAN']`).
3. `Working/api/serializers.py`:
   - Added `to_representation` cumulative logic to `CutReportSerializer`, `ProcessReportSerializer`, `KcsReportSerializer`, `FinishingReportSerializer` (active only when `with_totals=true`).
4. `Working/api/views.py`:
   - Added `DashboardTrackingAPIView`.
   - Updated permissions on `DashboardCutAPIView`, `DashboardProcessAPIView`, `DashboardKcsAPIView`, `DashboardFinishingAPIView` to `IsProductionDashboardViewer`.
   - Enhanced `BaseTrackingViewSet` with date filtering and cumulative context injection when `with_totals=true`.
5. `Working/api/urls.py`:
   - Registered `dashboards/tracking/` (`name='dashboard-tracking'`).
6. `Working/views.py`:
   - Refactored `get_tracking_data()` and `_calculate_cumulative_totals_*()` to delegate to `Working/services.py`.
7. `Working/api/tests.py`:
   - Added 6 test suites covering permissions, tracking shape, tracking calculations, filters, and cumulative calculations across all 4 production stages.

---

## 10. Database / Migration Status

- Models modified: **0**
- Database tables altered: **0**
- Migrations created: **0**
- Database schema remains completely untouched.

---

## 11. Known Limitations

- **Dataset Scale**: In-memory single-pass accumulation is optimal for current workloads (< 50,000 active production log records per season). If dataset grows to hundreds of thousands of records, database window functions (`SUM(...) OVER (PARTITION BY ... ORDER BY ...)`) or summary aggregate tables can be introduced without changing serializer output contracts.
- **Exporting**: Excel export endpoints currently remain handled by Django views (`tracking_export_excel_view`, etc.).

---

## 12. Phase 4C-3B Readiness

All three gate prerequisites from Section 37 have been met:
- `GAP-PROD-01 = RESOLVED`: Tracking Matrix API is live, tested, and 100% consistent with legacy calculations.
- `GAP-PROD-02 = RESOLVED`: `KE_TOAN` permission is fixed and verified with regression tests.
- `GAP-PROD-03 = RESOLVED`: Activity log cumulative totals are available via `?with_totals=true` with backward compatibility guaranteed.

---

## 13. Final Verdict

# PASS

Backend and API hardening for the Production Dashboard is functionally complete, thoroughly tested, and ready for Phase 4C-3B React migration.
