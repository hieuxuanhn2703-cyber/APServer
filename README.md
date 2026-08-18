# Tài liệu Mô tả Hệ thống Process Monitoring & Kế Toán

Đây là hệ thống quản lý, giám sát tiến độ quy trình sản xuất may mặc **(Cắt – May Sản Xuất – KCS – Hoàn thiện)** và phân hệ quản lý **Kế toán & Tài chính (Đơn giá, Phiếu xuất hàng, Doanh thu và Tồn đọng)**. Hệ thống cho phép nhân viên từng bộ phận ghi nhận sản lượng, kế toán lập phiếu xuất và theo dõi giá trị tiền hàng, cấp quản lý và ban giám đốc theo dõi toàn diện tiến độ, xuất báo cáo và quản trị nhân sự.

Hệ thống được phát triển bằng **Django** (Python) và sử dụng cơ sở dữ liệu **MySQL/SQLite**. Giao diện được tối ưu hóa hiển thị trên cả máy tính (Full-width) lẫn điện thoại di động (Mobile-friendly).

---

## 1. Phân quyền & Quản lý Tài khoản (RBAC)

Hệ thống phân chia người dùng thành **7 vai trò (Role)** chặt chẽ và độc lập:

| Vai trò | Mã Role | Quyền hạn & Chức năng chính | Giao diện |
|---|---|---|---|
| **Sản xuất** | `BASIC` | Nhập & xem lịch sử báo cáo May/Sản xuất (50 bản ghi gần nhất). | Giao diện đơn, không có Sidebar. |
| **Nhà cắt** | `NHA_CAT` | Nhập & xem lịch sử báo cáo Cắt (Cắt chính/lót/Mex/bông). | Giao diện đơn, không có Sidebar. |
| **KCS** | `KCS` | Nhập & xem lịch sử báo cáo KCS (Qua tay, Đạt, Lỗi, Tổng đạt). | Giao diện đơn, không có Sidebar. |
| **Hoàn thiện** | `HOAN_THIEN` | Nhập báo cáo Hoàn thiện & Ghi nhận/theo dõi ngoại lệ (Trả hàng lỗi, Lấy mẫu từng lần). | Giao diện đơn, không có Sidebar. |
| **Kế toán** | `KE_TOAN` | Quản lý đơn giá xuất, lập phiếu xuất hàng, theo dõi doanh thu & tiền hàng tồn đọng; xem Báo cáo tổng hợp, Tracking đơn hàng và Quản lý mã hàng. | Có Sidebar điều hướng chuyên dụng. |
| **Quản lý** | `QUAN_LY` | Xem Dashboard 4 bảng sản xuất, tự nhập liệu 4 bộ phận, quản lý Mã hàng, xem Tracking & xuất Excel. | Có Sidebar điều hướng toàn diện. |
| **Admin** | `PREMIUM` | Quản trị cấp cao: Xem toàn bộ Dashboard sản xuất & Kế toán, Quản lý Hệ thống (Tài khoản, Mã hàng, Đơn giá), xem Tracking. | Có Sidebar đầy đủ quyền cao nhất. |

### Các tính năng liên quan đến tài khoản:
- **Đăng ký & Phê duyệt**: Người dùng đăng ký mới sẽ ở trạng thái *Chờ duyệt*. Chỉ Admin (`PREMIUM`) mới có quyền phê duyệt, khóa hoặc xóa tài khoản.
- **Đổi mật khẩu**: Mọi tài khoản đều có thể tự đổi mật khẩu. Giao diện có nút "Quay lại" thông minh.
- **Bảo mật & Tự động điều hướng**: Mọi trang trong hệ thống đều yêu cầu đăng nhập. Khi chưa đăng nhập, hệ thống tự động chuyển hướng về `/login/`. Sau khi đăng nhập, hệ thống tự động đưa người dùng đến trang đích phù hợp với vai trò của mình.

---

## 2. Phân Hệ Kế Toán & Quản Lý Doanh Thu (`Accounting`)

Phân hệ dành riêng cho vai trò **Kế toán (`KE_TOAN`)** và **Ban Giám đốc (`PREMIUM`)** với tính năng bảo mật tuyệt đối về dữ liệu tài chính (các role sản xuất khác bị chặn 403 Forbidden).

### 2.1 Quản Lý Đơn Giá Xuất Hàng (`/accounting/don-gia/`)
- Thiết lập đơn giá (VNĐ/cái) cho từng cặp `(Mã hàng, Màu sắc)`.
- Hỗ trợ nhập định dạng tiền tệ thông minh (tự động thêm dấu phẩy `,` phân cách hàng nghìn khi gõ: ví dụ `150,000`).
- Hỗ trợ **cập nhật đơn giá đơn lẻ** hoặc **Lưu toàn bộ đơn giá** cùng một lúc.
- Hiển thị người cập nhật và thời gian cập nhật gần nhất.

### 2.2 Nhập Phiếu Xuất Hàng & Tính Tiền Tự Động (`/accounting/xuat-hang/`)
- Lập phiếu xuất hàng gồm: **Ngày xuất**, **Mã hàng**, **Màu sắc**, **Số lượng xuất**, **Ghi chú**.
- **Tính tiền thời gian thực (Real-time Preview)**: Khi chọn mã hàng, màu sắc và gõ số lượng, hệ thống tự động lấy đơn giá tương ứng và tính ngay **Thành tiền (VNĐ)** trước khi bấm lưu.
- Lưu lại lịch sử chi tiết từng lần xuất hàng, hỗ trợ **Sửa** (`/accounting/xuat-hang/<id>/sua/`) và **Xóa** phiếu xuất.

### 2.3 Dashboard Theo Dõi Xuất Hàng & Tồn Đọng (`/accounting/`)
- **3 Thẻ KPI tổng quan**:
  1. **Tổng Giá Trị Đơn Hàng**: Tổng số lượng và tổng thành tiền toàn bộ đơn hàng đặt may.
  2. **Tổng Tiền Đã Xuất**: Doanh thu hàng đã giao cùng % tiến độ giao hàng.
  3. **Giá Trị Hàng Chưa Xuất**: Số lượng và tổng tiền hàng còn tồn đọng cần giao tiếp.
- **Bảng Chi Tiết Tiến Độ Xuất Hàng & Tồn Đọng**:
  - Thiết kế tiêu đề 2 tầng chuyên nghiệp, hiển thị trọn vẹn 100% độ rộng màn hình (không cần cuộn ngang).
  - Cột dữ liệu: Mã hàng, Màu, Số lượng ĐH, Đơn giá, Thành tiền ĐH, SL xuất, Tiền đã xuất, SL còn lại, Tiền còn lại, % Tiến độ.
  - Định dạng số tiền có dấu phẩy `,` rõ ràng (ví dụ: `33,000,000 VNĐ`).
- **Bộ lọc Mã hàng**: Lọc nhanh theo mã hàng có nút xóa lọc tiện lợi.
- **Xuất Báo Cáo Excel**: Xuất file Excel chuẩn hóa gồm 2 sheet (*Tổng hợp theo dõi* & *Chi tiết từng phiếu xuất*).

---

## 3. Quản Lý Báo Cáo Sản Xuất (4 Quy trình)

Hệ thống có **4 luồng dữ liệu độc lập** với giao diện nhập liệu và danh sách lịch sử riêng:

### 3.1 Quy trình Cắt (`/cut/`)
- Ghi nhận: **Cắt chính, Cắt lót, Cắt Mex, Cắt bông** theo Mã hàng & Màu sắc.

### 3.2 Quy trình May Sản Xuất (`/`)
- Ghi nhận: Xưởng, Tổ, **Số lượng LĐ**.
- Các công đoạn: Nhận BTP, Vào chuyền, Giữa chuyền, Ra chuyền, Thu hóa, Là thành phẩm, Nhập hoàn thiện.

### 3.3 Quy trình KCS (`/kcs/`)
- Ghi nhận: Xưởng, Tổ.
- Các chỉ số: **Qua tay, Đạt, Lỗi, Tổng đạt**.

### 3.4 Quy trình Hoàn Thiện & Nghiệp Vụ Ngoại Lệ (`/finishing/`)
- Ghi nhận sản lượng: **Thẻ bài, Gấp hàng, Treo/Đóng thùng**.
- **Quản lý ngoại lệ (`/finishing/ngoai-le/`)**:
  - Dành cho: **Hoàn thiện (`HOAN_THIEN`)**, **Quản lý (`QUAN_LY`)** và **Cao cấp / Admin (`PREMIUM`)**.
  - Ghi nhận: Trả hàng lỗi / sửa về tổ sản xuất và Lấy mẫu (cho KCS, Kỹ thuật, Lãnh đạo, Khách hàng...).
  - **Theo dõi nhận lại từng lần**: Ghi nhận số lượng nhận trả từng đợt (`/finishing/tra-hang/nhan-lai/<id>/`, `/finishing/lay-mau/nhan-lai/<id>/`).
  - **Lọc thông minh**: Hỗ trợ chuyển đổi nhanh giữa chế độ "Đang treo (chờ nhận lại)" và "Xem tất cả lịch sử".
  - **Truy cập nhanh**: Tích hợp trực tiếp trên **Sidebar menu** (mục Báo Cáo Tổng Hợp & Quy Trình Sản Xuất) và nút truy cập kèm badge đếm số lượng đang treo trên **Bảng Tổng Hợp Hoàn Thiện** (`/dashboard/finishing/`).

---

## 4. Dashboard Báo Cáo Tổng Hợp Dữ Liệu (`/dashboard/`)

Dành cho Quản lý (`QUAN_LY`), Admin (`PREMIUM`) và Kế toán (`KE_TOAN`).

- **4 Tab tổng hợp độc lập**: **Tổng hợp Cắt** (`/dashboard/cut/`) → **Tổng hợp Sản Xuất** (`/dashboard/prod/`) → **Tổng hợp KCS** (`/dashboard/kcs/`) → **Tổng hợp Hoàn Thiện** (`/dashboard/finishing/`).
- **Quy tắc tính ô Ngày / Tổng**: Số Tổng ở góc dưới ô chéo là **tổng lũy kế** tính đến thời điểm của lần nhập đó.
- **Bộ lọc Excel đa tầng trên từng cột**: Nút `[▼]` hỗ trợ tìm kiếm, lọc nhiều giá trị, lọc liên tầng (Cascading) và bảo toàn bộ lọc khi chuyển trang.
- **Lọc thời gian & Xuất Excel**: Bộ lọc ngày độc lập và nút xuất file Excel theo đúng dữ liệu đang lọc.

---

## 5. Tracking Đơn Hàng (`/tracking/`)

Bảng theo dõi tổng hợp tiến độ vòng đời toàn bộ đơn hàng theo từng `(Mã hàng, Màu sắc)`:
- Số lượng đặt hàng, số lượng lũy kế qua từng công đoạn (Cắt, May, KCS, Hoàn thiện, Đã xuất), số lượng tồn đọng.
- Hỗ trợ lọc nâng cao và xuất báo cáo Excel.

---

## 6. Quản Lý Cấu Hình Mã Hàng (`/config/`)

- Cấu trúc: `Product (Mã hàng)` → `ProductColor (Màu + Số lượng Đơn hàng)`.
- Thêm mã hàng mới, thêm màu hàng loạt, chỉnh sửa số lượng đơn hàng linh hoạt.
- Dữ liệu cấu hình làm gốc cho danh mục chọn Mã – Màu và tính toán tiến độ ở tất cả các khâu.

---

## 7. Công Nghệ & Cấu Trúc Mã Nguồn

- **Backend**: Python 3.x, Django 6.x.
- **Database**: SQLite (phát triển) / MySQL (triển khai thực tế).
- **Frontend**: HTML5, CSS3 hiện đại, Vanilla JavaScript (không phụ thuộc framework nặng, tải trang tức thì).
- **Thư viện xử lý Excel**: `openpyxl`.
- **Kiểm thử tự động**: Bộ test suite toàn diện với **36/36 tests PASS 100%** bao phủ phân quyền, tính toán doanh thu, xuất nhập hàng và lọc báo cáo.
