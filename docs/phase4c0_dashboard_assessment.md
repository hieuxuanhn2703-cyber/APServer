# BÁO CÁO ĐÁNH GIÁ MIGRATION DASHBOARD (PHASE 4C-0)
**Tài liệu:** `docs/phase4c0_dashboard_assessment.md`  
**Giai đoạn:** Phase 4C-0 — Dashboard Migration Assessment (Audit / Analysis Only)  
**Trạng thái:** HOÀN TẤT ĐÁNH GIÁ (AUDIT COMPLETE)  
**Phạm vi:** Kiểm toán kiến trúc, rà soát dữ liệu, đối soát REST API hiện có, xác định khoảng cách (Gap Analysis) và lập kế hoạch kỹ thuật cho React Migration. **KHÔNG VIẾT CODE MIGRATION HOẶC THAY ĐỔI BACKEND TRONG PHASE NÀY.**

---

## 1. TỔNG QUAN ĐIỀU HÀNH (EXECUTIVE SUMMARY)

### 1.1. Mục tiêu kiểm toán
Thực hiện đánh giá toàn diện hiện trạng Dashboard của dự án **ProcessMonitoring**, bao gồm cả Dashboard Báo cáo Sản xuất (`Working`), Dashboard Kế toán (`Accounting`) và phần tích hợp Cân đối Kho (`Inventory`). Mục tiêu là xác định mức độ sẵn sàng của hệ thống REST API (`/api/v1/`), phát hiện toàn bộ khoảng cách (gaps) giữa giao diện Django Templates hiện tại và API endpoints, từ đó đề xuất kiến trúc React và lộ trình triển khai an toàn cho Phase 4C.

### 1.2. Hiện trạng kiến trúc Dashboard
Hệ thống hiện tại thực chất bao gồm **hai khu vực Dashboard chuyên biệt**:
1. **Dashboard Báo Cáo Sản Xuất (`Working`)**:
   - URL: `/dashboard/`, `/dashboard/cut/`, `/dashboard/prod/`, `/dashboard/kcs/`, `/dashboard/finishing/`, `/dashboard/kho/`.
   - Bản chất: Hệ thống bảng ma trận theo dõi tiến độ chi tiết (Tracking Matrices) phân chia theo 5 tab: Cắt (Cut), Sản xuất (Prod), KCS, Hoàn thiện (Finishing), và Kho (Inventory Balance).
   - Điểm đặc thù: Hiển thị các ô đường chéo (Diagonal Cells) so sánh sản lượng **Trong ngày (Daily)** với **Lũy kế (Cumulative)** cho từng dòng báo cáo thực tế (`report.id`), kèm bộ lọc cột đa năng dạng Excel (`excel_filter.js`), phân trang 50 dòng/trang và các nút thao tác Sửa/Xóa trực tiếp trên từng dòng.
2. **Dashboard Doanh Thu & Xuất Hàng Kế Toán (`Accounting`)**:
   - URL: `/accounting/` (name: `accounting:dashboard`).
   - Bản chất: Màn hình quản trị tài chính tổng hợp với 4 thẻ KPI tài chính lớn (Tổng giá trị ĐH, Tổng tiền đã xuất, Tiền đã thanh toán, Tiền chưa thanh toán), thanh tiến độ giao hàng %, bảng thống kê sản phẩm - màu kèm đơn giá, thành tiền, nợ đọng, và 2 popup Modal tương tác trực tiếp: Ghi nhận thanh toán (`PaymentReport`) và Lịch sử thanh toán.

### 1.3. Mức độ sẵn sàng của REST API
- **Dashboard Kế Toán (`Accounting`)**: **READY (Sẵn sàng 100%)**. Đã có đầy đủ endpoint `/api/v1/accounting/dashboard/` (trả về toàn bộ 4 thẻ KPI, danh sách rows và map lịch sử thanh toán) cùng ViewSet `/api/v1/accounting/payments/` để thêm/xóa thanh toán.
- **Tích hợp Cân đối Kho (`Inventory Summary`)**: **READY (Sẵn sàng 100%)**. Đã có endpoint `/api/v1/inventory/summary/` cung cấp ma trận nhập - xuất - tồn theo mã hàng, màu, vật tư.
- **Dashboard Sản Xuất (`Working`)**: **PARTIAL (Sẵn sàng một phần / Có khoảng cách kiến trúc)**.
  - Các API hiện tại (`/api/v1/working/dashboards/cut/`, `/dashboards/process/`, `/dashboards/kcs/`, `/dashboards/finishing/`) được xây dựng ở Phase 3D trả về **dữ liệu tổng hợp gom nhóm theo `(mã hàng, màu)` (Aggregated Summary)**.
  - Tuy nhiên, giao diện Django Dashboard hiện tại (`dashboard_*.html`) lại hiển thị **bảng chi tiết từng dòng báo cáo (Per-report log rows)** với các ô lũy kế chéo (diagonal cells), người nhập, ngày làm việc, phân trang và cascade filter.
  - Do đó, nếu Phase 4C yêu cầu tái hiện chính xác 100% bảng ma trận dòng chi tiết như Django thì API hiện tại chưa đủ (thiếu trường lũy kế theo từng dòng, thiếu cascade options API, thiếu pagination). Nếu Phase 4C triển khai Dashboard dạng Tổng quan (Executive Summary / KPIs / Charts) thì API hiện tại đã đáp ứng tốt.

### 1.4. Kết luận sơ bộ
Dashboard Kế toán có thể chuyển đổi sang React ngay lập tức. Dashboard Sản xuất cần một quyết định kiến trúc rõ ràng về phạm vi giao diện (Summary vs Detailed Matrix) trước khi code.

---

## 2. KẾT QUẢ KIỂM TOÁN DỰ ÁN (REPOSITORY INSPECTION)

### 2.1. Các quy tắc và tài liệu hướng dẫn đã rà soát
- `.agents/rules/project.md`: Nguyên tắc chung về cấu trúc dự án.
- `.agents/rules/django.md`: Kiến trúc backend Django, mô hình `AppUser`, quy tắc `select_related`, `PROTECT`.
- `.agents/rules/api.md`: Tiêu chuẩn REST API, JWT auth, conventions response.
- `.agents/rules/frontend.md`: Hướng dẫn giao diện Django Template hiện hành, bảng zebra-stripe, mobile single-column.
- `.agents/rules/react.md`: Quy chuẩn SPA React, cấm Tailwind/Bootstrap, Vanilla CSS, quản lý state, bảo toàn UI/UX.
- `.agents/rules/migration.md`: Quy trình di chuyển từng module, không xóa code cũ khi chưa nghiệm thu.

### 2.2. Các kỹ năng (Skills) đã tham chiếu
- `django-backend-dev`: Phát triển backend logic theo chuẩn ProcessMonitoring.
- `django-rest-api-dev`: Thiết kế serializer, viewset, permission DRF cho `AppUser`.
- `django-to-react-migration`: Quy trình chuyển đổi từ Django View/Template sang React Component.
- `react-frontend-dev`: Cấu trúc component, hook, context trong thư mục `frontend/`.
- `code-review-and-debugging`: Danh mục rà soát lỗi N+1, phân quyền và validation.

### 2.3. Danh mục tệp tin liên quan trực tiếp đến Dashboard

| Phân nhóm | Đường dẫn tệp tin | Vai trò / Mô tả |
| :--- | :--- | :--- |
| **Working Views** | `Working/views.py` (L1220 - L1860) | Chứa 5 view Dashboard (`dashboard_cut_view`, `dashboard_prod_view`, `dashboard_kcs_view`, `dashboard_finishing_view`, `dashboard_kho_view`), hàm tính lũy kế `_calculate_cumulative_totals_*`, hàm sinh dòng `_dashboard_*_report_to_row`, và hàm lọc cascade `_get_cascade_options`. |
| **Accounting Views** | `Accounting/views.py` (L30 - L120) | Chứa `accounting_dashboard_view` và xử lý POST tạo thanh toán `PaymentReport`. |
| **Working Templates** | `Working/templates/dashboard_cut.html` | Template tổng hợp quy trình Cắt. |
| | `Working/templates/dashboard_prod.html` | Template tổng hợp quy trình May / Sản xuất. |
| | `Working/templates/dashboard_kcs.html` | Template tổng hợp quy trình KCS. |
| | `Working/templates/dashboard_finishing.html` | Template tổng hợp Hoàn thiện (kèm badge ngoại lệ). |
| | `Working/templates/dashboard_kho.html` | Template tổng hợp Kho nguyên liệu (nhúng `summary_table.html`). |
| | `Working/templates/dashboard_nav_tabs.html` | Thanh chuyển tab điều hướng 5 phân hệ Dashboard. |
| | `Working/templates/premium_dashboard.html` | Template tổng hợp cũ (Legacy monolithic dashboard, hiện không còn view nào render). |
| **Accounting Templates**| `Accounting/templates/accounting/dashboard.html` | Template Dashboard Doanh thu & Xuất hàng (KPIs, bảng công nợ, modals). |
| **Static Assets** | `Working/static/working/js/excel_filter.js` | Logic lọc dữ liệu dạng Excel popup, search, select all, reload GET params. |
| | `Working/static/working/css/premium.css` | Toàn bộ CSS định kiểu cho Dashboard, diagonal cell, KPI cards, table wrapper. |
| **Backend Services** | `Working/services.py` | Các hàm `get_cut_dashboard_data`, `get_process_dashboard_data`, `get_kcs_dashboard_data`, `get_finishing_dashboard_data`. |
| | `Accounting/services.py` | Hàm `get_dashboard_data` (tính 4 KPI, gom nhóm công nợ, map thanh toán). |
| | `Inventory/services.py` | Hàm `get_inventory_summary_data` (tính cân đối kho). |
| **REST API Views** | `Working/api/views.py` (L228 - L283) | `DashboardCutAPIView`, `DashboardProcessAPIView`, `DashboardKcsAPIView`, `DashboardFinishingAPIView`. |
| | `Accounting/api/views.py` (L64 - L75) | `AccountingDashboardAPIView`, `PaymentReportViewSet`. |
| | `Inventory/api/views.py` (L40 - L56) | `InventorySummaryAPIView`. |
| **REST API URLs** | `Working/api/urls.py` | Định tuyến `/api/v1/working/dashboards/*`. |
| | `Accounting/api/urls.py` | Định tuyến `/api/v1/accounting/dashboard/`, `/api/v1/accounting/payments/`. |
| | `Inventory/api/urls.py` | Định tuyến `/api/v1/inventory/summary/`. |
| **React Frontend** | `frontend/src/pages/DashboardPlaceholder.jsx` | Trang placeholder hiện tại của Dashboard. |
| | `frontend/src/routes/AppRoutes.jsx` | Định tuyến `/dashboard` bảo vệ bởi `ProtectedRoute`. |
| | `frontend/src/components/layout/Sidebar.jsx`| Menu điều hướng Dashboard theo quyền `PREMIUM`, `QUAN_LY`, `KE_TOAN`. |
| **Tests** | `Working/api/tests.py` | Kiểm tra quyền truy cập API Dashboard (`test_dashboard_access`). |
| | `Accounting/api/tests.py` | Kiểm tra API Dashboard Kế toán (`test_accounting_dashboard`). |
| | `Accounting/tests.py` | Kiểm tra tính toán số liệu và thanh toán trên Dashboard Kế toán. |
| | `Inventory/tests.py` | Kiểm tra tính toán bảng cân đối kho (`get_inventory_summary_data`). |

### 2.4. Bất đồng bộ giữa mã nguồn và tài liệu hiện có (Documentation Discrepancies)
Trong tệp [docs/api.md](file:///c:/Users/P.X.Hieu/.vscode/project/ProcessMonitoring/docs/api.md), các endpoint Dashboard của `Working`, `Accounting`, và `Inventory` vẫn đang được đánh dấu là `(PLANNED)`. Tuy nhiên, trong mã nguồn thực tế:
- Cả 3 phân hệ đều đã có endpoint API hoạt động hoàn chỉnh từ Phase 3B-3, 3C, 3D.
- Theo quy tắc **ACTUAL CODE > DOCUMENTATION**, hệ thống REST API thực tế đã tồn tại và đang phục vụ các bài test tự động đạt kết quả PASS.

---

## 3. KIẾN TRÚC DASHBOARD HIỆN TẠI (DASHBOARD ARCHITECTURE)

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                               HIỆN TRẠNG DASHBOARD HỆ THỐNG                            │
├───────────────────────────────────────────┬────────────────────────────────────────────┤
│ 1. PRODUCTION DASHBOARD (Working)         │ 2. FINANCIAL DASHBOARD (Accounting)        │
├───────────────────────────────────────────┼────────────────────────────────────────────┤
│ URLs:                                     │ URL:                                       │
│  - /dashboard/ (redirect / cut)           │  - /accounting/ (name: accounting:dashboard│
│  - /dashboard/cut/                        │ View:                                      │
│  - /dashboard/prod/                       │  - Accounting.views.accounting_dashboard_view
│  - /dashboard/kcs/                        │ Templates:                                 │
│  - /dashboard/finishing/                  │  - Accounting/templates/accounting/        │
│  - /dashboard/kho/                        │    dashboard.html                          │
│ Views:                                    │ Services:                                  │
│  - dashboard_cut_view                     │  - Accounting.services.get_dashboard_data  │
│  - dashboard_prod_view                    │ REST APIs:                                 │
│  - dashboard_kcs_view                     │  - GET /api/v1/accounting/dashboard/       │
│  - dashboard_finishing_view               │  - CRUD /api/v1/accounting/payments/       │
│  - dashboard_kho_view                     │ Tính năng:                                 │
│ Templates:                                │  - 4 Thẻ KPI Tài chính lớn (VNĐ / Cái)     │
│  - dashboard_cut.html                     │  - Thanh tiến độ xuất hàng (Progress Bar)  │
│  - dashboard_prod.html                    │  - Bảng tài chính Mã hàng - Màu - Đơn giá  │
│  - dashboard_kcs.html                     │  - Modal Ghi nhận thanh toán công nợ       │
│  - dashboard_finishing.html               │  - Modal Lịch sử thanh toán                │
│  - dashboard_kho.html                     │  - Lọc nhanh theo Mã hàng (Select Dropdown)│
│  - dashboard_nav_tabs.html                │                                            │
│ Services:                                 │                                            │
│  - Working.services.get_*_dashboard_data  │                                            │
│ REST APIs:                                │                                            │
│  - GET /api/v1/working/dashboards/cut/    │                                            │
│  - GET /api/v1/working/dashboards/process/│                                            │
│  - GET /api/v1/working/dashboards/kcs/    │                                            │
│  - GET /api/v1/working/dashboards/finishing/│                                          │
│  - GET /api/v1/inventory/summary/         │                                            │
│ Tính năng:                                │                                            │
│  - 5 Tab điều hướng ngang                 │                                            │
│  - Lọc khoảng ngày (Từ ngày - Đến ngày)   │                                            │
│  - Bộ lọc Excel cột cascade (Người nhập,  │                                            │
│    Mã hàng, Màu, Xưởng, Tổ, Đơn vị,...)   │                                            │
│  - Ô ma trận chéo (Ngày / Lũy kế)         │                                            │
│  - Phân trang server-side 50 dòng/trang   │                                            │
│  - Xuất báo cáo Excel từng phân hệ        │                                            │
│  - Thao tác nhanh Sửa/Xóa từng dòng       │                                            │
│  - Thống kê đơn ngoại lệ Hoàn thiện treo  │                                            │
│  - Tích hợp bảng cân đối kho vật tư       │                                            │
└───────────────────────────────────────────┴────────────────────────────────────────────┘
```

---

## 4. DANH MỤC TÍNH NĂNG DASHBOARD (DASHBOARD FEATURE INVENTORY)

| Mã ID | Tính năng (Feature) | Triển khai hiện tại (Django) | Trạng thái REST API | Độ phức tạp | Ghi chú di chuyển sang React |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **F-01** | Điều hướng Tabs Dashboard | `dashboard_nav_tabs.html` (5 tabs) | READY (Frontend Route) | LOW | Dùng React Router `<NavLink>` hoặc Tab State nội bộ. |
| **F-02** | Lọc theo khoảng ngày | Form GET (`start_date`, `end_date`) | READY (`?start_date=&end_date=`) | LOW | Quản lý bằng React State / URL Query Params. |
| **F-03** | Thẻ KPI Doanh thu & Đơn hàng | 4 Cards trong `accounting/dashboard.html` | READY (`/api/v1/accounting/dashboard/`) | LOW | Component `<KPICard />` tái sử dụng, render mượt mà. |
| **F-04** | Thanh tiến độ xuất hàng % | HTML/CSS `progress-bar-fill` | READY (trả về `kpi_tien_do_tong`) | LOW | CSS Pure Vanilla với dynamic `style={{ width: \`${pct}%\` }}`. |
| **F-05** | Bảng công nợ & xuất hàng | Table trong `accounting/dashboard.html` | READY (`rows` trong dashboard API) | MEDIUM | Component `<AccountingTable />`, format số tiền VNĐ. |
| **F-06** | Modal Ghi nhận thanh toán | JS + Modal HTML form POST | READY (`POST /api/v1/accounting/payments/`) | MEDIUM | Component `<PaymentModal />` gọi API qua `apiClient`. |
| **F-07** | Modal Lịch sử thanh toán | JS + Modal HTML table | READY (`payments_by_pc` hoặc API payments) | MEDIUM | Component `<PaymentHistoryModal />` kèm nút xóa thanh toán. |
| **F-08** | Lọc mã hàng Kế toán | Select form GET reload | READY (`?ma_hang=...`) | LOW | Dropdown select kích hoạt fetch lại dữ liệu. |
| **F-09** | Bảng Cân đối Kho (Vật tư) | `Inventory/summary_table.html` | READY (`/api/v1/inventory/summary/`) | MEDIUM | Component `<InventorySummaryTable />`. |
| **F-10** | Ma trận tổng hợp sản lượng Cắt | Table `dashboard_cut.html` (dòng chi tiết) | PARTIAL (API chỉ trả tổng hợp mã hàng) | HIGH | Cần quyết định: Render ma trận tóm tắt hay ma trận dòng chi tiết. |
| **F-11** | Ma trận tổng hợp Sản xuất | Table `dashboard_prod.html` (dòng chi tiết) | PARTIAL (API chỉ trả tổng hợp mã hàng) | HIGH | Tương tự F-10. |
| **F-12** | Ma trận tổng hợp KCS | Table `dashboard_kcs.html` (dòng chi tiết) | PARTIAL (API chỉ trả tổng hợp mã hàng) | HIGH | Tương tự F-10. |
| **F-13** | Ma trận tổng hợp Hoàn thiện | Table `dashboard_finishing.html` (dòng chi tiết) | PARTIAL (API chỉ trả tổng hợp mã hàng) | HIGH | Tương tự F-10. |
| **F-14** | Ô ma trận chéo (Ngày/Lũy kế) | CSS `.diagonal-cell` (.top-val, .bot-val) | PARTIAL (API chưa trả cặp ngày/lũy kế theo dòng) | MEDIUM | CSS đã có trong `premium.css`, cần dữ liệu tương ứng. |
| **F-15** | Bộ lọc Excel đa cột cascade | `excel_filter.js` + `#excel-filter-config` | MISSING (Không có API trả options cascade) | HIGH | Trong React, nên tính options trực tiếp client-side từ dữ liệu fetched. |
| **F-16** | Nút Sửa/Xóa dòng trên Dashboard | Link `*_edit` và Form POST `*_delete` | READY (Có endpoints CRUD reports riêng) | MEDIUM | Điều hướng tới form edit hoặc mở dialog xác nhận xóa qua API. |
| **F-17** | Nút Xuất Excel | Link gọi view Django `export_excel` | READY (Giữ nguyên backend view export) | LOW | Link trực tiếp tới URL backend để download file binary Excel. |
| **F-18** | Badge đơn ngoại lệ Hoàn thiện | Query `DefectReturnReport` & `SampleTakeReport` | READY (Có endpoints exceptions riêng) | LOW | Hiển thị badge số lượng đơn ngoại lệ đang treo. |
| **F-19** | Chuyển đổi giao diện Mobile Card | CSS `@media (max-width: 900px)` | READY (Thuần CSS) | LOW | Bảo toàn markup song song `.desktop-table` và `.mobile-cards`. |

---

## 5. ÁNH XẠ LUỒNG DỮ LIỆU (DATA FLOW MAPPING)

### 5.1. Luồng dữ liệu Dashboard Kế toán (Financial Dashboard)
```text
[React Client: DashboardPage / AccountingDashboard]
    │
    ▼ GET /api/v1/accounting/dashboard/?ma_hang=... (JWT Bearer Token)
[Django DRF: AccountingDashboardAPIView]
    │
    ▼ Gọi hàm nghiệp vụ
[Service: Accounting.services.get_dashboard_data]
    │
    ├─► ORM: ProductColor.objects.select_related('product', 'price')
    ├─► ORM: ExportReport.objects.values('ma_hang', 'mau').annotate(Sum)
    ├─► ORM: PaymentReport.objects.values('product_color_id').annotate(Sum)
    └─► ORM: PaymentReport.objects.select_related('nguoi_nhap').order_by(...)
    │
    ▼ Tính toán tổng hợp 4 KPIs + danh sách Rows + map payments
[MySQL Database]
    │
    ▼ Trả về JSON Data
[React: Render 4 KPICards, Progress Bar, Bảng công nợ, Modals thanh toán]
```

### 5.2. Luồng dữ liệu Dashboard Kho (Inventory Summary)
```text
[React Client: InventorySummarySection]
    │
    ▼ GET /api/v1/inventory/summary/?ma_hang=...&mau=... (JWT Bearer Token)
[Django DRF: InventorySummaryAPIView]
    │
    ▼ Gọi hàm nghiệp vụ
[Service: Inventory.services.get_inventory_summary_data]
    │
    ├─► ORM: MaterialReceipt.objects.filter(...)
    └─► ORM: MaterialIssue.objects.filter(...)
    │
    ▼ Tính toán cân đối: nhập, xuất, tồn kho, cấp cắt, thu hồi
[MySQL Database]
    │
    ▼ Trả về JSON Matrix
[React: Render Bảng Cân Đối Kho]
```

### 5.3. Luồng dữ liệu Dashboard Báo cáo Sản xuất (`Working`)
#### Hiện trạng qua API Phase 3D:
```text
[React Client] 
    │
    ▼ GET /api/v1/working/dashboards/cut/?start_date=...&end_date=...
[Django DRF: DashboardCutAPIView]
    │
    ▼ Gọi hàm nghiệp vụ
[Service: Working.services.get_cut_dashboard_data]
    │
    ├─► ORM: CutReport.objects.filter(...).values('ma_hang', 'mau').annotate(Sum)
    └─► ORM: ProductColor.objects.select_related('product') (lấy tổng đơn hàng)
    │
    ▼ Trả về mảng JSON tổng hợp sản lượng theo từng sản phẩm/màu
[MySQL Database]
```
#### Hiện trạng trên Django Template (`Working/views.py`):
```text
[Django Template: dashboard_cut.html]
    │
    ▼ Gọi dashboard_cut_view
[View: dashboard_cut_view]
    │
    ├─► ORM: CutReport.objects.select_related('nguoi_nhap').filter(date_range)
    ├─► Helper: _calculate_cumulative_totals_cut() (Lặp toàn bộ CutReport để tính lũy kế theo thời gian)
    ├─► Helper: _get_cascade_options() (Tính danh sách lọc riêng cho từng cột)
    ├─► Helper: _dashboard_cut_report_to_row() (Tạo object từng dòng chứa cả ngày & lũy kế)
    └─► Paginator: Paginator(cut_rows, 50)
    │
    ▼ Render HTML với excel_filter.js và table ma trận ô chéo
[Browser]
```

---

## 6. MA TRẬN ĐỐI SOÁT API (API READINESS MATRIX)

| Yêu cầu nghiệp vụ | Endpoint REST API | Trạng thái | Khoảng cách (Gap) | Hành động khuyến nghị cho Phase 4C |
| :--- | :--- | :--- | :--- | :--- |
| **KPIs & Bảng Kế toán** | `GET /api/v1/accounting/dashboard/` | **READY** | Không có. Đã trả đầy đủ KPIs, rows, payments. | Sử dụng trực tiếp trong React. |
| **Ghi nhận thanh toán** | `POST /api/v1/accounting/payments/` | **READY** | Không có. Đã hỗ trợ tạo phiếu thanh toán. | Gọi API khi submit modal thanh toán. |
| **Xóa phiếu thanh toán**| `DELETE /api/v1/accounting/payments/{id}/` | **READY** | Không có. Đã hỗ trợ xóa phiếu thanh toán. | Gọi API khi bấm xóa trong modal lịch sử. |
| **Bảng cân đối kho** | `GET /api/v1/inventory/summary/` | **READY** | Không có. Hỗ trợ đầy đủ bộ lọc ma_hang, mau, vat_tu. | Sử dụng trực tiếp cho tab Kho. |
| **Báo cáo tóm tắt Cắt** | `GET /api/v1/working/dashboards/cut/` | **READY** (Summary) | Trả về tổng hợp theo `(ma_hang, mau)`. Chưa có dòng chi tiết. | Phù hợp cho màn hình tóm tắt / Biểu đồ tiến độ Cắt. |
| **Báo cáo tóm tắt May** | `GET /api/v1/working/dashboards/process/` | **READY** (Summary) | Trả về tổng hợp theo `(ma_hang, mau)`. Chưa có dòng chi tiết. | Phù hợp cho màn hình tóm tắt / Biểu đồ tiến độ May. |
| **Báo cáo tóm tắt KCS** | `GET /api/v1/working/dashboards/kcs/` | **READY** (Summary) | Trả về tổng hợp theo `(ma_hang, mau)`. Chưa có dòng chi tiết. | Phù hợp cho màn hình tóm tắt / Biểu đồ KCS. |
| **Báo cáo tóm tắt HT** | `GET /api/v1/working/dashboards/finishing/` | **READY** (Summary) | Trả về tổng hợp theo `(ma_hang, mau)`. Chưa có dòng chi tiết. | Phù hợp cho màn hình tóm tắt / Biểu đồ Hoàn thiện. |
| **Bảng ma trận dòng chi tiết** | Chưa có endpoint chuyên biệt | **MISSING** (Nếu cần) | Các endpoint `/dashboards/*` hiện tại không trả danh sách dòng chi tiết từng báo cáo kèm số lũy kế. | Cần quyết định phạm vi: Nếu cần bảng chi tiết, bổ sung query param `?mode=detailed` hoặc tạo endpoint `/api/v1/working/dashboards/tracking/`. |
| **Lọc cascade đa cột** | Chưa có endpoint | **PARTIAL** | Django tính options bằng `_get_cascade_options` trên server. | Khuyến nghị: Tính toán cascade options ngay trên React Client từ danh sách bản ghi, không cần gọi thêm API. |
| **Xuất file Excel** | `GET /export-excel/`, `/accounting/export-excel/` | **READY** (Legacy) | File binary Excel được tạo bởi openpyxl trong Django. | Giữ nguyên backend Django export views, React tạo link trực tiếp với query params. |

---

## 7. KIỂM TOÁN LOGIC NGHIỆP VỤ (BUSINESS LOGIC AUDIT)

### 7.1. Phân định ranh giới xử lý logic

| Thành phần logic | Cơ chế tính toán hiện tại | Quyết định di chuyển (Migration Decision) | Rationale (Lý do) |
| :--- | :--- | :--- | :--- |
| **Tính lũy kế sản xuất theo thời gian** | `_calculate_cumulative_totals_*` trong `Working/views.py` lặp qua toàn bộ DB records | **KEEP IN DJANGO** | Lũy kế phụ thuộc vào toàn bộ dữ liệu lịch sử trong DB, React không thể tự tính nếu dữ liệu bị phân trang. |
| **Tính toán 4 KPI Kế toán & tiến độ %** | `Accounting.services.get_dashboard_data` tổng hợp SQL qua `Sum` và gom nhóm | **KEEP IN DJANGO** | Đảm bảo tính nhất quán tuyệt đối về tiền tệ và số liệu tài chính, không phụ thuộc client. |
| **Tính cân đối nguyên vật liệu kho** | `Inventory.services.get_inventory_summary_data` gom nhóm `MaterialReceipt` và `MaterialIssue` | **KEEP IN DJANGO** | Logic kho phức tạp (đơn vị tính, trừ kho, thu hồi) bắt buộc thực thi tập trung ở backend. |
| **Lọc dữ liệu theo ngày (`date_range`)** | Django ORM filter `created_at__gte` và `created_at__lte` | **KEEP IN DJANGO** | Giảm thiểu băng thông, backend chỉ trả dữ liệu thuộc phạm vi ngày được yêu cầu. |
| **Lọc cascade Excel options** | Server tính danh sách distinct thông qua `_get_cascade_options` | **MOVE TO REACT** | Sau khi tải dữ liệu trang hoặc dữ liệu tổng hợp về client, React có thể tự trích xuất danh sách options distinct tức thì, không cần tải lại trang. |
| **Format tiền tệ, ngày tháng, phần trăm** | Template filter `comma_num`, `format_date` | **MOVE TO REACT** | Sử dụng các hàm tiện ích chuẩn JavaScript (`Intl.NumberFormat('vi-VN')`, `toLocaleDateString`). |
| **Phân trang giao diện** | Django `Paginator(rows, 50)` | **NEEDS DECISION** | Với bảng tóm tắt sản phẩm: Client-side pagination hoặc giữ nguyên danh sách. Với bảng chi tiết lớn: Server-side pagination qua DRF `PageNumberPagination`. |

---

## 8. MA TRẬN PHÂN QUYỀN DASHBOARD (ROLE MATRIX)

| Vai trò (Role) | Quyền truy cập Dashboard | Các Widget / Tab được xem | Phạm vi dữ liệu (Data Scope) | Cơ chế kiểm soát hiện tại | Yêu cầu trên React (Phase 4C) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`PREMIUM`** | Toàn quyền (Full Access) | Tất cả các Tab: Cắt, May, KCS, Hoàn thiện, Kho, Kế toán | Xem toàn bộ dữ liệu toàn công ty | `current_user.role in ['PREMIUM', 'QUAN_LY', 'KE_TOAN']` | Hiển thị đầy đủ menu, tabs và các nút quản trị. |
| **`QUAN_LY`** | Toàn quyền (Full Access) | Tất cả các Tab: Cắt, May, KCS, Hoàn thiện, Kho, Kế toán | Xem toàn bộ dữ liệu toàn công ty | Tương tự `PREMIUM` | Hiển thị đầy đủ như `PREMIUM` (trừ quản lý tài khoản người dùng). |
| **`KE_TOAN`** | Toàn quyền xem Dashboard | Tab Kế toán, Tab Kho, và các Tab Sản xuất | Xem toàn bộ dữ liệu tài chính & sản xuất | Được cấp quyền xem trong cả `Working` và `Accounting` | Mặc định landing vào `/accounting` hoặc `/dashboard`. Có quyền ghi nhận thanh toán. |
| **`KHO`** | Giới hạn Tab Kho | Chỉ được truy cập `/dashboard/kho/` và màn hình Kho | Xem dữ liệu cân đối vật tư kho | View check `role in ['PREMIUM', 'QUAN_LY', 'KE_TOAN', 'KHO']` | Ẩn tab Sản xuất & Kế toán; điều hướng mặc định vào `/inventory`. |
| **`NHA_CAT`** | Không có quyền Dashboard | Không | Chỉ xem báo cáo cá nhân tại `/cut/list/` | Bị chặn bởi `PermissionDenied` (HTTP 403) | Ẩn menu Dashboard; chuyển hướng landing về `/working`. Nếu cố truy cập báo 403. |
| **`KCS`** | Không có quyền Dashboard | Không | Chỉ xem báo cáo cá nhân tại `/kcs/list/` | Bị chặn bởi `PermissionDenied` (HTTP 403) | Ẩn menu Dashboard; chuyển hướng landing về `/working`. |
| **`HOAN_THIEN`**| Không có quyền Dashboard | Không | Chỉ xem báo cáo cá nhân tại `/finishing/list/` | Bị chặn bởi `PermissionDenied` (HTTP 403) | Ẩn menu Dashboard; chuyển hướng landing về `/working`. |
| **`BASIC`** | Không có quyền Dashboard | Không | Chỉ xem báo cáo cá nhân tại `/list/` | Bị chặn bởi `PermissionDenied` (HTTP 403) | Ẩn menu Dashboard; chuyển hướng landing về `/working`. |

*Ghi chú bảo mật:* Việc ẩn menu và chuyển hướng trên React chỉ nhằm tối ưu trải nghiệm người dùng (UX). Lớp bảo mật thực sự nằm tại DRF Permission Classes (`IsAdminOrManager`, `IsAccountingTeam`, `IsInventoryViewer`) trả về `HTTP 403 Forbidden` đối với bất kỳ request API trái phép nào.

---

## 9. ÁNH XẠ GIAO DIỆN LEGACY SANG REACT (LEGACY FRONTEND MAPPING)

```text
┌──────────────────────────────────────────────┬──────────────────────────────────────────────┐
│ DJANGO TEMPLATES / LEGACY ASSETS             │ THÀNH PHẦN REACT TƯƠNG ỨNG (TARGET)          │
├──────────────────────────────────────────────┼──────────────────────────────────────────────┤
│ dashboard_nav_tabs.html                      │ <DashboardNavTabs activeTab={...} />         │
│ Form lọc ngày GET (dash-filter-form)         │ <DashboardDateFilter onFilterChange={...} /> │
│ Thẻ KPI accounting (kpi-card blue/emerald/..)│ <KPICard title=... value=... sub=... />      │
│ Thanh tiến độ progress-bar-fill              │ <ProgressBar percentage={...} />             │
│ Table Kế toán (dashboard-table-card)         │ <AccountingSummaryTable data={...} />        │
│ Modal Ghi nhận thanh toán (createPaymentForm)│ <PaymentCreateModal isOpen=... />            │
│ Modal Lịch sử thanh toán (historyModal)      │ <PaymentHistoryModal payments=... />         │
│ Table Cân đối Kho (Inventory/summary_table)  │ <InventorySummaryTable data={...} />         │
│ Table Cắt / May / KCS / Hoàn thiện          │ <ProductionSummaryTable module={...} />      │
│ Ô ma trận đường chéo (.diagonal-cell)        │ <DiagonalCell topVal={...} botVal={...} />   │
│ Excel Filter Popup (excel_filter.js)         │ <ColumnFilterDropdown options=... />         │
│ Phân trang (pagination-container)            │ <Pagination currentPage=... totalPages=... />│
│ Stylesheet premium.css                       │ Giữ nguyên các class tokens trong index.css   │
└──────────────────────────────────────────────┴──────────────────────────────────────────────┘
```

---

## 10. ĐỀ XUẤT KIẾN TRÚC COMPONENT REACT (PROPOSED REACT ARCHITECTURE)

```text
frontend/src/
├── pages/
│   ├── DashboardPage.jsx                    # Trang Dashboard chính (quản lý tab & context)
│   └── AccountingDashboardPage.jsx          # Trang Dashboard Kế toán (nếu tách route riêng)
├── components/
│   └── dashboard/
│       ├── DashboardNavTabs.jsx             # Thanh chuyển Tab (Cắt, May, KCS, Hoàn thiện, Kho, Kế toán)
│       ├── DashboardDateFilter.jsx          # Thanh lọc thời gian (Từ ngày - Đến ngày) & Nút Xuất Excel
│       ├── KPICard.jsx                      # Thẻ hiển thị chỉ số thống kê (Doanh thu, Sản lượng)
│       ├── ProgressBar.jsx                  # Thanh tiến độ phần trăm hoàn thành
│       ├── DiagonalCell.jsx                 # Ô bảng hiển thị 2 giá trị Ngày / Lũy kế có đường chéo
│       ├── ColumnFilterDropdown.jsx         # Dropdown lọc dữ liệu từng cột (thay thế excel_filter.js)
│       ├── ProductionSummaryTable.jsx       # Bảng số liệu sản xuất theo module
│       ├── AccountingSummaryTable.jsx       # Bảng theo dõi doanh thu & công nợ kế toán
│       ├── PaymentCreateModal.jsx           # Dialog ghi nhận phiếu thanh toán
│       ├── PaymentHistoryModal.jsx          # Dialog xem và xóa lịch sử thanh toán
│       └── InventorySummaryTable.jsx        # Bảng cân đối kho nguyên vật liệu
```

### Chi tiết trách nhiệm của các Component nòng cốt:
1. `<DashboardPage />`:
   - Quản lý Server State (gọi API tương ứng với tab được chọn), URL Query State (đồng bộ tab và date filter lên URL search params).
   - Kiểm tra quyền truy cập của người dùng qua `useRoles()`. Nếu người dùng không có quyền xem module, render cảnh báo `403 Forbidden` thân thiện thay vì crash.
2. `<DiagonalCell />`:
   - Nhận props: `{ topValue, bottomValue, topLabel = "Ngày", bottomLabel = "Tổng" }`.
   - Sử dụng CSS `.diagonal-cell` từ `premium.css` để đảm bảo 100% độ sắc nét và vị trí số liệu chuẩn xác.
3. `<PaymentCreateModal />`:
   - Nhận props: `{ isOpen, onClose, productColor, onSuccess }`.
   - Sử dụng `apiClient.post('/api/v1/accounting/payments/', ...)` để ghi nhận thanh toán và reload dữ liệu mà không cần tải lại trang.

---

## 11. KẾ HOẠCH QUẢN LÝ STATE (STATE MANAGEMENT PLAN)

Tuân thủ nghiêm ngặt quy tắc tại `.agents/rules/react.md`: **KHÔNG sử dụng Redux, MobX, hay Zustand.** Hệ thống sử dụng kết hợp React Local State, URL Search Params, và Custom Context đã có sẵn:

1. **Server State (Dữ liệu từ API)**:
   - Dữ liệu KPIs và danh sách rows: Quản lý bằng `useState` kết hợp `useEffect` bên trong component Dashboard.
   - Trạng thái tải: `loading` (boolean), `error` (string / null).
2. **UI State (Trạng thái giao diện)**:
   - Tab đang chọn: `activeTab` ('cut' | 'prod' | 'kcs' | 'finishing' | 'kho' | 'accounting').
   - Modal hiển thị: `isPaymentModalOpen`, `isHistoryModalOpen`, `selectedProductColor`.
   - Bộ lọc tìm kiếm nội bộ: Text input tìm kiếm giá trị trong dropdown lọc cột.
3. **URL Search Params (Trạng thái trên đường dẫn)**:
   - `start_date`, `end_date`: Lưu trên URL để khi người dùng reload trang hoặc chia sẻ link thì khoảng thời gian vẫn được giữ nguyên.
   - `tab`: Đồng bộ tab hiện tại trên URL (`/dashboard?tab=cut`).
   - `ma_hang`: Bộ lọc mã hàng của Kế toán.
4. **Authentication State (Trạng thái xác thực & quyền)**:
   - Được cung cấp toàn cục bởi `AuthContext` (`useAuth()` và `useRoles()`).
5. **Derived State (Dữ liệu phái sinh)**:
   - Danh sách các lựa chọn distinct cho bộ lọc cột: Được trích xuất bằng `useMemo()` trực tiếp từ mảng `rows` đã tải về.

---

## 12. KẾ HOẠCH TRẠNG THÁI TẢI / LỖI / RỖNG (LOADING, ERROR, EMPTY STATE PLAN)

Mọi khối dữ liệu Dashboard trên React bắt buộc phải xử lý đủ 4 trạng thái:

1. **Trạng thái Đang tải (Loading State)**:
   - Hiển thị skeleton loading hoặc spinner có text: *"Đang tải dữ liệu báo cáo..."*.
   - Vô hiệu hóa nút Lọc ngày và dropdown để tránh gửi request trùng lặp.
2. **Trạng thái Dữ liệu rỗng (Empty State)**:
   - Khi mảng dữ liệu trả về rỗng (`rows.length === 0`): Hiển thị hàng bảng rỗng với icon và thông báo: *"Chưa có dữ liệu nào được ghi nhận trong khoảng thời gian đã chọn."*.
3. **Trạng thái Lỗi API (Error State)**:
   - **Mã lỗi 401 (Unauthorized)**: Tự động kích hoạt cơ chế refresh token của `apiClient` (đã được làm vững ở Phase 4B). Nếu refresh thất bại, chuyển hướng về `/login`.
   - **Mã lỗi 403 (Forbidden)**: Hiển thị thông báo quyền hạn: *"Bạn không có quyền truy cập dữ liệu báo cáo này."* (Tuyệt đối không logout user).
   - **Mã lỗi 500 hoặc Mất mạng (Network Error)**: Hiển thị banner cảnh báo màu đỏ kèm nút *"Thử lại (Retry)"*.
4. **Trạng thái Thành công (Success State)**:
   - Render đầy đủ các thẻ KPI và bảng dữ liệu, các giá trị số được định dạng chuẩn tiếng Việt.

---

## 13. KIỂM TOÁN THIẾT KẾ ĐÁP ỨNG (RESPONSIVE DESIGN AUDIT)

Kiểm toán giao diện CSS hiện tại của Django Dashboard cho thấy các quy chuẩn đáp ứng bắt buộc phải bảo toàn khi chuyển sang React:

1. **Giao diện Máy tính (Desktop > 900px)**:
   - Bảng dữ liệu hiển thị dạng Table truyền thống với tiêu đề cố định (Sticky Header `top: 0; z-index: 10`).
   - Các cột chỉ số ma trận hiển thị ô chéo `.diagonal-cell` đầy đủ 2 giá trị.
   - 4 Thẻ KPI Kế toán dàn hàng ngang dạng lưới CSS Grid `repeat(auto-fit, minmax(220px, 1fr))`.
2. **Giao diện Máy tính bảng (Tablet 641px - 900px)**:
   - Bảng dữ liệu cho phép cuộn ngang mượt mà (`overflow-x: auto`) trong thẻ `.table-wrapper`.
   - Lưới KPI co giãn thành 2 cột.
3. **Giao diện Di động (Mobile <= 640px)**:
   - **Ẩn toàn bộ `<table>`**: Áp dụng quy tắc `.desktop-table-container { display: none !important; }`.
   - **Hiển thị danh sách thẻ `.card-list` / `.mobile-cards-container`**: Mỗi dòng dữ liệu được render thành một Card độc lập (`.data-card` hoặc `.acc-card`), hiển thị rõ nhãn và giá trị từng công đoạn.
   - Các form lọc ngày và nhóm nút hành động xếp chồng dọc (`flex-direction: column; width: 100%`).
   - Giữ nguyên các class CSS thuần đã định nghĩa trong `premium.css`, không đưa thêm thư viện CSS bên ngoài.

---

## 14. KIỂM TOÁN BIỂU ĐỒ & TRỰC QUAN HÓA (CHART / VISUALIZATION AUDIT)

1. **Hiện trạng trong Django Dashboard**:
   - **KHÔNG CÓ thư viện biểu đồ nào (No Chart.js, No ApexCharts, No Highcharts, No Canvas)** đang được sử dụng trong mã nguồn legacy.
   - Mọi trực quan hóa hiện tại đều được thể hiện thông qua:
     - Các ô số liệu phân màu (Badge, status pills).
     - Thanh tiến độ phần trăm bằng CSS thuần (`.progress-bar-wrap` và `.progress-bar-fill`).
     - Bảng ma trận ô chéo chia góc bằng linear-gradient CSS.
2. **Kế hoạch cho React (Phase 4C)**:
   - Giai đoạn đầu di chuyển Dashboard: Tái hiện trung thực 100% giao diện hiện hữu bằng Vanilla CSS.
   - **Tuyệt đối KHÔNG cài đặt thêm thư viện biểu đồ (như `recharts` hay `chart.js`) trong Phase 4C-0**.
   - Nếu trong tương lai người dùng yêu cầu trực quan hóa biểu đồ cột/tròn cho số liệu sản xuất, việc lựa chọn thư viện biểu đồ nhẹ (như Recharts hoặc Chart.js) sẽ được trình duyệt và phê duyệt ở một pha riêng biệt.

---

## 15. KẾ HOẠCH KIỂM THỬ (TEST PLAN)

### 15.1. Kiểm thử Backend & API hiện có (Automated Tests)
- Đảm bảo toàn bộ 13 API tests hiện hữu tiếp tục vượt qua 100%:
  - `Working.api.tests.WorkingAPITestCase.test_dashboard_access`: Kiểm tra chặn role `BASIC` và cấp quyền role `PREMIUM` truy cập `/api/v1/working/dashboards/cut/`.
  - `Accounting.api.tests.AccountingAPITests.test_accounting_dashboard`: Kiểm tra dữ liệu và cấu trúc response của `/api/v1/accounting/dashboard/`.
  - `Accounting.api.tests.AccountingAPITests.test_team_revenue`: Kiểm tra dữ liệu báo cáo doanh thu tổ xưởng.
- *Ghi chú về lỗi kiểm thử phát hiện trong quá trình audit:*
  - Phát hiện test `Accounting.tests.AccountingTests.test_team_revenue_pagination_5_per_page` trong suite tổng 85 tests bị lỗi do test case sử dụng ngày giả lập trong tương lai (từ ngày 3 đến ngày 12 của tháng hiện tại), trong khi view legacy mặc định chỉ lọc dữ liệu từ đầu tháng đến ngày hiện tại (`today = September 2nd`). Lỗi này thuộc về dữ liệu fixture của test cũ và không làm ảnh hưởng đến tính đúng đắn của REST API.

### 15.2. Kiểm thử React Frontend (Phase 4C)
- Kiểm thử tích hợp Component bằng Vitest / React Testing Library:
  - Render thẻ KPI với số liệu giả lập.
  - Kiểm tra tính toán % của Progress Bar.
  - Kiểm tra mở/đóng modal thanh toán và validate số tiền nhập.
  - Kiểm tra hiển thị banner thông báo khi API trả về 403 Forbidden.
  - Kiểm tra trạng thái rỗng khi không có bản ghi nào.

### 15.3. Kiểm thử xác minh thủ công (Manual Verification Checklist)
1. Đăng nhập tài khoản `QUAN_LY`:
   - Truy cập `/dashboard`: Giao diện hiển thị đầy đủ, không lỗi console.
   - Chuyển đổi giữa các tab Cắt, May, KCS, Hoàn thiện, Kho, Kế toán: Dữ liệu tải đúng tương ứng.
   - Thay đổi khoảng ngày lọc: Dữ liệu cập nhật chính xác.
2. Đăng nhập tài khoản `KE_TOAN`:
   - Mở modal ghi nhận thanh toán: Gửi thành công, số tiền chưa thanh toán giảm tương ứng.
3. Đăng nhập tài khoản `BASIC` / `NHA_CAT`:
   - Không nhìn thấy menu Dashboard trên Sidebar; nếu gõ trực tiếp `/dashboard` trên URL sẽ được chuyển hướng an toàn về `/working`.
4. Kiểm tra trên thiết bị di động (màn hình < 640px):
   - Bảng chuyển đổi thành danh sách Card hiển thị đầy đủ thông tin, không bị vỡ khung.

---

## 16. PHÂN TÍCH RỦI RO (RISK ASSESSMENT)

| STT | Rủi ro tiềm ẩn (Risk) | Mức độ | Hậu quả | Biện pháp giảm thiểu (Mitigation) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **R-1** | **Bất đồng bộ cấu trúc dữ liệu Dashboard Sản xuất** | **CAO** | API `/dashboards/*` hiện tại chỉ trả số liệu tổng hợp theo mã hàng, không đủ để vẽ bảng chi tiết từng dòng báo cáo kèm số lũy kế như template Django cũ. | **Tách rõ 2 lựa chọn kiến trúc:** Hoặc nâng cấp API để trả về danh sách dòng chi tiết (kèm mode detailed), hoặc thống nhất React Dashboard hiển thị bảng tổng hợp mã hàng (Executive Summary) và để bảng chi tiết ở trang Nhật ký `/working`. |
| **R-2** | **Hiệu năng tính toán lũy kế (Cumulative Calculation)** | **TRUNG BÌNH** | Hàm `_calculate_cumulative_totals_*` quét toàn bộ bảng dữ liệu từ đầu đến cuối để cộng dồn, có thể chậm khi số lượng báo cáo tăng lên hàng vạn dòng. | Giữ nguyên việc tính toán ở backend; nếu cần bảng chi tiết, bổ sung index database cho cặp `(created_at, id)`. |
| **R-3** | **Xung đột phiên làm việc và Refresh Token khi load nhiều widget** | **THẤP** | Trang Dashboard có thể gọi đồng thời nhiều request API (KPIs, bảng biểu, danh sách), gây nguy cơ refresh token nhiều lần. | Đã được giải quyết triệt để ở Phase 4B bằng cơ chế `refreshTokenPromise` concurrency lock trong `apiClient`. |
| **R-4** | **Phụ thuộc vào giao diện Mobile Card** | **TRUNG BÌNH** | Nếu quên xử lý responsive, bảng dữ liệu lớn với các ô chéo sẽ bị vỡ tràn màn hình trên mobile. | Kế thừa nguyên vẹn media queries `@media (max-width: 900px)` và cấu trúc Card view của `premium.css`. |

---

## 17. ĐỀ XUẤT PHẠM VI MIGRATION PHASE 4C (MIGRATION SCOPE PROPOSAL)

Để đảm bảo quá trình di chuyển an toàn, có thể kiểm chứng độc lập và không làm gián đoạn hệ thống đang vận hành:

### 17.1. PHẠM VI THỰC HIỆN TRONG PHASE 4C (IN-SCOPE):
1. **Module 1: Dashboard Kế Toán (`Accounting Dashboard`)**:
   - Xây dựng Component React hoàn chỉnh thay thế `Accounting/templates/accounting/dashboard.html`.
   - Kết nối trực tiếp vào các REST API đã sẵn sàng 100%:
     - `GET /api/v1/accounting/dashboard/` (KPIs và bảng công nợ).
     - `POST /api/v1/accounting/payments/` (Ghi nhận thanh toán).
     - `DELETE /api/v1/accounting/payments/{id}/` (Xóa thanh toán).
   - Tái hiện đầy đủ 4 thẻ KPI, thanh tiến độ %, bảng công nợ, modal ghi nhận và modal lịch sử.
2. **Module 2: Dashboard Cân Đối Kho (`Inventory Summary`)**:
   - Xây dựng Component React hiển thị bảng cân đối kho vật tư.
   - Kết nối vào REST API `GET /api/v1/inventory/summary/`.
3. **Module 3: Khung điều hướng & Tóm tắt Sản Xuất (`Production Executive Summary`)**:
   - Thanh Tab chuyển đổi giữa các phân hệ.
   - Bộ lọc khoảng thời gian.
   - Các bảng chỉ số tóm tắt tiến độ Cắt, May, KCS, Hoàn thiện kết nối vào `/api/v1/working/dashboards/*`.
4. **Module 4: Trạng thái Loading / Error / Mobile Card View**:
   - Hoàn thiện responsive 100% trên cả Desktop, Tablet và Mobile.

### 17.2. NGOÀI PHẠM VI PHASE 4C (OUT-OF-SCOPE):
- KHÔNG xóa bỏ các view Django và template cũ (`dashboard_*.html`, `dashboard.html`). Hệ thống Django cũ tiếp tục hoạt động song song làm đối chứng (fallback).
- KHÔNG di chuyển các form nhập liệu quy trình sản xuất (`cut_web`, `web`, `kcs_web`, `finishing_web`) — các màn hình này thuộc về Phase 4D / 4E.
- KHÔNG cài đặt thêm thư viện giao diện (Tailwind, Bootstrap, MUI) hoặc thư viện quản lý state (Redux).
- KHÔNG thay đổi schema cơ sở dữ liệu hoặc tạo file migration mới.

---

## 18. TRÌNH TỰ TRIỂN KHAI KHUYẾN NGHỊ (RECOMMENDED IMPLEMENTATION SEQUENCE)

Kế hoạch từng bước cho pha triển khai tiếp theo (Phase 4C):

```text
BƯỚC 1: XÁC LẬP TẦNG API CLIENT DASHBOARD (Dashboard API Client Services)
  - Tạo file `frontend/src/api/dashboard.js` đóng gói các hàm gọi API:
    + `fetchAccountingDashboard(maHang)`
    + `fetchInventorySummary(filters)`
    + `fetchProductionDashboard(module, dateRange)`
    + `createPayment(data)`
    + `deletePayment(id)`
  - Xác minh tích hợp JWT Bearer Token tự động từ `apiClient`.

BƯỚC 2: TRIỂN KHAI CÁC COMPONENT NỀN TẢNG (Shared Dashboard Components)
  - Xây dựng `<DashboardNavTabs />` hỗ trợ chuyển tab mượt mà.
  - Xây dựng `<DashboardDateFilter />` quản lý khoảng ngày.
  - Xây dựng `<KPICard />` và `<ProgressBar />`.
  - Xây dựng `<DiagonalCell />` định kiểu ma trận chéo bằng Vanilla CSS.

BƯỚC 3: TRIỂN KHAI PHÂN HỆ DASHBOARD KẾ TOÁN (Accounting Dashboard Migration)
  - Xây dựng `<AccountingSummaryTable />` hiển thị danh sách sản phẩm, đơn giá, xuất hàng, nợ đọng.
  - Xây dựng `<PaymentCreateModal />` cho phép nhập và gửi thanh toán qua API.
  - Xây dựng `<PaymentHistoryModal />` hiển thị chi tiết các lần thanh toán kèm thao tác xóa.
  - Kết nối hoàn chỉnh với `AccountingDashboardAPIView`.

BƯỚC 4: TRIỂN KHAI PHÂN HỆ CÂN ĐỐI KHO (Inventory Summary Integration)
  - Xây dựng `<InventorySummaryTable />` hiển thị số liệu nhập - xuất - tồn.
  - Kết nối với `InventorySummaryAPIView`.

BƯỚC 5: TRIỂN KHAI PHÂN HỆ TỔNG HỢP SẢN XUẤT (Production Summary Dashboard)
  - Tích hợp 4 tab: Cắt, May, KCS, Hoàn thiện.
  - Render bảng tiến độ theo mã hàng và màu sắc từ `/api/v1/working/dashboards/*`.
  - Tích hợp badge thông báo số đơn ngoại lệ hoàn thiện đang treo.

BƯỚC 6: KIỂM TOÁN ĐÁP ỨNG DI ĐỘNG & BẢO MẬT (Responsive & Security Hardening)
  - Tái hiện cấu trúc Mobile Card View cho cả bảng sản xuất và bảng kế toán.
  - Khóa quyền truy cập đối với các vai trò không được phép (BASIC, NHA_CAT, KCS, HOAN_THIEN).
  - Kiểm thử xử lý lỗi 401 (refresh token) và 403 (cảnh báo không có quyền).

BƯỚC 7: NGHIỆM THU & ĐỐI SOÁT DỮ LIỆU (Verification & Regression Check)
  - Chạy `npm run build` kiểm tra 0 lỗi bundle.
  - Chạy `python manage.py check` và `makemigrations --check`.
  - Chạy toàn bộ backend test suite.
  - Đối chiếu số liệu hiển thị trên React SPA với Django Template cũ để đảm bảo khớp 100%.
```

---

## 19. KẾT LUẬN MỨC ĐỘ SẴN SÀNG (MIGRATION READINESS VERDICT)

# VERDICT: READY WITH CONDITIONS (SẴN SÀNG CÓ ĐIỀU KIỆN)

### Căn cứ đánh giá:
1. **Điều kiện đã sẵn sàng (Ready Factors)**:
   - Kiến trúc nền tảng React 18, React Router v6, Application Shell, hệ thống xác thực JWT và Token Refresh Guard của Phase 4A & Phase 4B đang hoạt động ổn định và tin cậy 100%.
   - Phân hệ **Dashboard Kế Toán (`Accounting`)** đã có đầy đủ 100% REST API (`/api/v1/accounting/dashboard/`, `/api/v1/accounting/payments/`), logic tính toán tập trung ở backend service, phân quyền chuẩn mực, có thể chuyển đổi sang React ngay lập tức mà không cần chỉnh sửa backend.
   - Phân hệ **Cân Đối Kho (`Inventory`)** đã có sẵn API `GET /api/v1/inventory/summary/`.
2. **Các điều kiện bắt buộc phải tuân thủ trước/khi triển khai (Conditions to Proceed)**:
   - **Điều kiện 1**: Thống nhất định hướng hiển thị của Dashboard Sản Xuất (`Working`): Trong Phase 4C, Dashboard Sản Xuất trên React sẽ hiển thị dạng **Executive Summary** (Tổng hợp sản lượng theo mã hàng/màu và các chỉ số tiến độ) dựa trên API hiện có của Phase 3D. Nếu muốn hiển thị chi tiết từng dòng báo cáo kèm ô chéo lũy kế như template cũ, cần phải thiết kế thêm endpoint chi tiết riêng trong backend ở pha tiếp theo.
   - **Điều kiện 2**: Tuyệt đối không xóa bỏ hoặc ngắt kết nối các view Django template legacy (`/dashboard/*`, `/accounting/`). Toàn bộ URL cũ phải tiếp tục hoạt động song song để làm nguồn đối chứng chân lý (Source of Truth).
   - **Điều kiện 3**: Bộ lọc đa cột dạng Excel (hiện tại do `excel_filter.js` xử lý) sẽ được chuyển đổi thành React Client-side filtering trên tập dữ liệu đã fetch, không tạo thêm endpoint backend phụ trợ không cần thiết.

---
*(Tài liệu này được lập hoàn toàn dựa trên việc kiểm toán trực tiếp mã nguồn của repository, không thay đổi bất kỳ dòng mã logic nào của hệ thống, tuân thủ tuyệt đối quy định dừng lại tại Phase 4C-0).*
