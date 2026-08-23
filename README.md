# Tài liệu Mô tả Hệ thống Process Monitoring & Kế Toán & Quản Lý Kho May Mặc

Đây là hệ thống toàn diện về quản lý và giám sát tiến độ quy trình sản xuất may mặc **(Cắt – May Sản Xuất – KCS – Hoàn Thiện)**, phân hệ quản lý **Kho Nguyên Vật Liệu (Nhập – Xuất – Tồn Kho)** và phân hệ **Kế toán & Tài chính (Đơn giá, Phiếu xuất hàng, Doanh thu đơn hàng, Báo cáo Doanh thu Tổ/Xưởng theo ngày)**. 

Hệ thống cho phép nhân viên từng bộ phận ghi nhận sản lượng theo thời gian thực, thủ kho quản lý xuất nhập tồn vật tư, kế toán theo dõi đơn giá và số tiền làm được của từng tổ/xưởng, cấp quản lý và ban giám đốc theo dõi toàn diện tiến độ, truy xuất báo cáo đa chiều và xuất file Excel chuẩn hóa.

Hệ thống được phát triển bằng **Django** (Python) và sử dụng cơ sở dữ liệu **MySQL/SQLite**. Giao diện được tối ưu hóa hiển thị trên cả máy tính (Full-width) lẫn điện thoại di động (Mobile-friendly).

---

## 1. Phân quyền & Quản lý Tài khoản (RBAC)

Hệ thống phân chia người dùng thành **8 vai trò (Role)** chặt chẽ và độc lập:

| Vai trò | Mã Role | Quyền hạn & Chức năng chính | Giao diện |
|---|---|---|---|
| **Sản xuất** | `BASIC` | Nhập & xem lịch sử báo cáo May/Sản xuất (50 bản ghi gần nhất). | Giao diện đơn, tối ưu cho công nhân. |
| **Nhà cắt** | `NHA_CAT` | Nhập & xem lịch sử báo cáo Cắt (Cắt chính/lót/Mex/bông). | Giao diện đơn, tối ưu cho tổ cắt. |
| **KCS** | `KCS` | Nhập & xem lịch sử báo cáo KCS (Qua tay, Đạt, Lỗi, Tổng đạt). | Giao diện đơn, tối ưu cho KCS. |
| **Hoàn thiện** | `HOAN_THIEN` | Nhập báo cáo Hoàn thiện & Ghi nhận/theo dõi ngoại lệ (Trả hàng lỗi, Lấy mẫu từng lần). | Giao diện đơn, có tab ngoại lệ. |
| **Kho** | `KHO` | Nhập kho vật tư, xuất kho nhanh, quản lý lịch sử nhập/xuất và theo dõi tồn kho nguyên vật liệu. | Có Sidebar điều hướng chuyên dụng. |
| **Kế toán** | `KE_TOAN` | Quản lý đơn giá, lập phiếu xuất hàng, theo dõi doanh thu đơn hàng & tiền làm được của từng tổ/xưởng theo ngày; xem Báo cáo tổng hợp, Tracking và Quản lý mã hàng. | Có Sidebar điều hướng tài chính. |
| **Quản lý** | `QUAN_LY` | Xem Dashboard 4 bảng sản xuất, tự nhập liệu 4 bộ phận, quản lý Kho, Quản lý Mã hàng, xem Tracking & xuất Excel. | Có Sidebar điều hướng toàn diện. |
| **Admin** | `PREMIUM` | Quản trị cấp cao: Toàn quyền truy cập tất cả các phân hệ (Sản xuất, Kho, Kế toán, Quản trị người dùng, Cấu hình hệ thống). | Có Sidebar đầy đủ quyền cao nhất. |

### Các tính năng liên quan đến tài khoản:
- **Đăng ký & Phê duyệt**: Người dùng đăng ký mới sẽ ở trạng thái *Chờ duyệt*. Chỉ Admin (`PREMIUM`) mới có quyền phê duyệt, phân quyền, khóa hoặc xóa tài khoản.
- **Đổi mật khẩu**: Mọi tài khoản đều có thể tự đổi mật khẩu với nút thao tác thuận tiện.
- **Bảo mật & Tự động điều hướng**: Mọi trang đều yêu cầu xác thực đăng nhập (`@login_required`). Khi chưa đăng nhập, tự động chuyển hướng về `/login/`. Sau khi đăng nhập, hệ thống tự động đưa người dùng đến trang làm việc tương ứng với vai trò.

---

## 2. Phân Hệ Kế Toán & Quản Lý Doanh Thu (`Accounting`)

Phân hệ dành riêng cho vai trò **Kế toán (`KE_TOAN`)** và **Ban Giám đốc (`PREMIUM`)** với bảo mật tuyệt đối về dữ liệu tài chính (các role khác bị chặn `403 Forbidden`).

### 2.1 Quản Lý Đơn Giá Xuất Hàng (`/accounting/don-gia/`)
- Thiết lập đơn giá (VNĐ/cái) cho từng cặp `(Mã hàng, Màu sắc)`.
- Hỗ trợ nhập định dạng tiền tệ thông minh (tự động định dạng dấu phẩy `,` phân cách hàng nghìn khi gõ: ví dụ `150,000`).
- Hỗ trợ **cập nhật đơn giá từng dòng** hoặc **Lưu toàn bộ đơn giá** cùng một lúc.
- Hiển thị người cập nhật và thời gian cập nhật gần nhất.

### 2.2 Nhập Phiếu Xuất Hàng & Tính Tiền Tự Động (`/accounting/xuat-hang/`)
- Lập phiếu xuất hàng: **Ngày xuất**, **Mã hàng**, **Màu sắc**, **Số lượng xuất**, **Ghi chú**.
- **Tính tiền thời gian thực (Real-time Preview)**: Tự động tra cứu đơn giá và hiển thị ngay **Thành tiền (VNĐ)** trước khi lưu.
- Lưu lịch sử chi tiết, hỗ trợ **Sửa** (`/accounting/xuat-hang/<id>/sua/`) và **Xóa** phiếu xuất.

### 2.3 Dashboard Theo Dõi Xuất Hàng & Tồn Đọng (`/accounting/`)
- **3 Thẻ KPI tổng quan**: Tổng Giá Trị Đơn Hàng, Tổng Tiền Đã Xuất, Giá Trị Hàng Chưa Xuất.
- **Bảng Chi Tiết Tiến Độ Xuất Hàng & Tồn Đọng**: Hiển thị trọn vẹn full-width màn hình với định dạng tiền tệ chuyên nghiệp.
- **Bộ lọc & Xuất Excel**: Lọc theo mã hàng và xuất file Excel chuẩn gồm 2 sheet.

### 2.4 Báo Cáo Doanh Thu Tổ / Xưởng Theo Ngày (`/accounting/bao-cao-to-xuong/`)
- **Nguyên tắc tính toán chính xác**:
  $$\text{Doanh thu} = \sum (\text{Sản lượng Ra Chuyền} \times \text{Đơn giá của từng mã hàng/màu sắc})$$
- **Tính năng nổi bật**:
  - **Xử lý đa sản phẩm trong ngày**: Nếu trong 1 ngày, 1 tổ ra chuyền nhiều mã hàng hoặc màu sắc khác nhau, từng mặt hàng sẽ được nhân với đơn giá riêng và cộng dồn chính xác.
  - **Tự động reset theo chu kỳ tháng**: Mặc định hiển thị dữ liệu từ **ngày 01 của tháng hiện tại đến ngày hôm nay**. Sang tháng mới, số liệu tự động reset về 0 cho tháng mới.
  - **Nút chọn nhanh kỳ tháng**: Nút **"Tháng này"** và **"Tháng trước"** giúp chuyển đổi xem số liệu kỳ kế toán chỉ với 1 click.
  - **Thanh lọc siêu gọn (Inline Toolbar)**: Tích hợp đầy đủ bộ lọc *Từ ngày, Đến ngày, Xưởng, Tổ, Mã hàng* cùng các nút *Lọc, Đặt lại, Xuất Excel* trên 1 dòng duy nhất.
  - **4 Thẻ KPI thống kê**: Tổng doanh thu làm được, Tổng hàng ra chuyền, Quy mô sản xuất, Doanh thu bình quân/ngày.
  - **3 Tab hiển thị độc lập**:
    1. *Tab 1 - Chi Tiết Theo Ngày & Tổ*: Phân trang chuẩn **5 hàng (5 ca tổ/ngày) mỗi trang** kèm thanh điều hướng trang bảo toàn bộ lọc.
    2. *Tab 2 - Tổng Hợp Theo Tổ / Xưởng*: Bảng tổng hợp số ngày làm việc, số mã hàng, tổng sản lượng, tổng tiền và tiền bình quân/ngày của từng tổ trong tháng.
    3. *Tab 3 - Tổng Hợp Theo Ngày*: Bảng theo dõi dòng tiền và sản lượng ra chuyền toàn xưởng theo từng ngày.
  - **Xuất Excel Đa Sheet (`/accounting/bao-cao-to-xuong/export-excel/`)**: Tải file `.xlsx` gồm **3 Sheet chuẩn hóa** (*Chi Tiết Ngày & Tổ*, *Tổng Hợp Tổ Xưởng*, *Tổng Hợp Theo Ngày*) có định dạng tiền tệ, màu sắc và border chỉn chu.

---

## 3. Phân Hệ Quản Lý Kho Nguyên Vật Liệu (`Inventory`)

Phân hệ dành cho **Thủ kho (`KHO`)**, **Quản lý (`QUAN_LY`)**, **Kế toán (`KE_TOAN`)** và **Admin (`PREMIUM`)**.

### 3.1 Nhập Kho Nguyên Vật Liệu (`/inventory/nhap/`)
- Nhập thông tin: Ngày nhập, Mã hàng, Màu, Tên vật tư, Đơn vị tính (cuộn, kg, chiếc, mét...), Số lượng kiện, Số lượng chi tiết, Người nhập.
- Xem danh sách và lịch sử nhập kho (`/inventory/lich-su-nhap/`) có phân trang 20 dòng/trang, hỗ trợ sửa/xóa phiếu nhập.

### 3.2 Xuất Kho Nguyên Vật Liệu & Xuất Kho Nhanh (`/inventory/quick-issue/`)
- Cho phép xuất kho nguyên vật liệu theo từng lần phát sinh hoặc thao tác xuất kho nhanh ngay từ bảng tổng hợp tồn kho.
- Xem danh sách và lịch sử xuất kho (`/inventory/lich-su-xuat/`) có phân trang 20 dòng/trang.

### 3.3 Tổng Hợp Tồn Kho Vật Tư (`/inventory/tong-hop/`)
- Tự động tổng hợp lượng Nhập – Xuất – Tồn kho của từng loại vật tư theo từng Mã hàng và Màu sắc.
- Cảnh báo tồn kho an toàn và hỗ trợ xuất báo cáo Excel kho vật tư.

---

## 4. Quản Lý Báo Cáo Sản Xuất (4 Quy trình)

Hệ thống có **4 luồng dữ liệu sản xuất độc lập**:

### 4.1 Quy trình Cắt (`/cut/`)
- Ghi nhận: **Cắt chính, Cắt lót, Cắt Mex, Cắt bông** theo Mã hàng & Màu sắc.

### 4.2 Quy trình May Sản Xuất (`/`)
- Ghi nhận: Xưởng, Tổ, **Số lượng LĐ**.
- Các công đoạn: Nhận BTP, Vào chuyền, Giữa chuyền, Ra chuyền, Thu hóa, Là thành phẩm, Nhập hoàn thiện.

### 4.3 Quy trình KCS (`/kcs/`)
- Ghi nhận: Xưởng, Tổ.
- Các chỉ số: **Qua tay, Đạt, Lỗi, Tổng đạt**.

### 4.4 Quy trình Hoàn Thiện & Nghiệp Vụ Ngoại Lệ (`/finishing/`)
- Ghi nhận sản lượng: **Thẻ bài, Gấp hàng, Treo/Đóng thùng**.
- **Quản lý ngoại lệ (`/finishing/ngoai-le/`)**:
  - Dành cho: **Hoàn thiện (`HOAN_THIEN`)**, **Quản lý (`QUAN_LY`)** và **Admin (`PREMIUM`)**.
  - Ghi nhận: Trả hàng lỗi / sửa về tổ may và Lấy mẫu kiểm định.
  - **Theo dõi nhận lại từng lần**: Ghi nhận số lượng nhận trả từng đợt, tự động tính lũy kế và ẩn khi đã nhận đủ 100%.

---

## 5. Dashboard Báo Cáo Tổng Hợp Dữ Liệu (`/dashboard/`)

Dành cho Quản lý (`QUAN_LY`), Admin (`PREMIUM`) và Kế toán (`KE_TOAN`).

- **4 Tab tổng hợp độc lập**: **Tổng hợp Cắt** (`/dashboard/cut/`) → **Tổng hợp May** (`/dashboard/prod/`) → **Tổng hợp KCS** (`/dashboard/kcs/`) → **Tổng hợp Hoàn thiện** (`/dashboard/finishing/`).
- **Quy tắc tính ô Ngày / Tổng**: Số Tổng ở góc dưới ô chéo là **tổng lũy kế** tính đến thời điểm của lần nhập đó.
- **Bộ lọc dạng Excel đa tầng trên từng cột**: Nút `[▼]` hỗ trợ tìm kiếm, lọc nhiều giá trị, lọc liên tầng (Cascading) và bảo toàn bộ lọc khi chuyển trang.
- **Lọc thời gian & Xuất Excel**: Bộ lọc ngày độc lập và nút xuất file Excel theo đúng dữ liệu đang lọc.

---

## 6. Tracking Đơn Hàng (`/tracking/`)

Bảng theo dõi tổng hợp tiến độ vòng đời toàn bộ đơn hàng theo từng `(Mã hàng, Màu sắc)`:
- Số lượng đặt hàng, số lượng lũy kế qua từng công đoạn (Cắt, May, KCS, Hoàn thiện, Đã xuất), số lượng tồn đọng.
- Hỗ trợ lọc nâng cao và xuất báo cáo Excel.

---

## 7. Quản Lý Cấu Hình Mã Hàng (`/config/`)

- Cấu trúc: `Product (Mã hàng)` → `ProductColor (Màu + Số lượng Đơn hàng)`.
- Thêm mã hàng mới, thêm màu hàng loạt, chỉnh sửa số lượng đơn hàng linh hoạt.
- Dữ liệu cấu hình làm gốc cho danh mục chọn Mã – Màu và tính toán tiến độ ở tất cả các khâu.

---

## 8. Công Nghệ & Kiểm Thử Tự Động

- **Backend**: Python 3.x, Django 6.x.
- **Database**: SQLite (phát triển) / MySQL (triển khai thực tế).
- **Frontend**: HTML5, CSS3 hiện đại, Vanilla JavaScript (không phụ thuộc framework nặng, tốc độ phản hồi cực nhanh).
- **Thư viện xử lý Excel**: `openpyxl`.
- **Kiểm thử tự động**: Bộ test suite toàn diện với **66/66 tests PASS 100%** bao phủ toàn bộ phân quyền, tính toán doanh thu tổ xưởng, xuất nhập kho, phiếu xuất hàng và bộ lọc báo cáo.
