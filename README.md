# Tài liệu Mô tả Hệ thống Process Monitoring

Đây là hệ thống quản lý và giám sát tiến độ quy trình **Cắt – Sản xuất – KCS – Hoàn thiện**, cho phép nhân viên từng bộ phận nhập báo cáo sản lượng, và cấp quản lý theo dõi toàn diện, xuất báo cáo cũng như quản trị cấu trúc sản phẩm và nhân sự.

Hệ thống được phát triển bằng **Django** (Python) và sử dụng cơ sở dữ liệu **MySQL**.

---

## 1. Phân quyền & Quản lý Tài khoản (RBAC)

Hệ thống phân chia người dùng thành **6 vai trò (Role)** chặt chẽ và độc lập:

| Vai trò | Mã | Quyền hạn |
|---|---|---|
| **Sản xuất** | `BASIC` | Nhập & xem báo cáo Sản xuất của chính mình. Không sửa/xóa. |
| **Nhà cắt** | `NHA_CAT` | Nhập & xem báo cáo Cắt (Mã hàng, Màu, Cắt chính/lót/Mex/bông) của chính mình. Không cần nhập Xưởng/Tổ. Không sửa/xóa. |
| **KCS** | `KCS` | Nhập & xem báo cáo KCS (Mã hàng, Màu, Xưởng, Tổ, Qua tay, Đạt, Lỗi, Tổng đạt) của chính mình. Không sửa/xóa. |
| **Hoàn thiện** | `HOAN_THIEN` | Nhập & xem báo cáo Hoàn thiện (Thẻ bài, Gấp hàng, Treo/Đóng thùng) của chính mình. Không sửa/xóa. |
| **Quản lý** | `QUAN_LY` | Xem Dashboard 4 bảng (Sản xuất, Hoàn thiện, KCS, Cắt), tự nhập liệu cho cả 4 bộ phận, sửa/xóa mọi báo cáo, xuất Excel, quản lý Mã hàng, xem Tracking. Không quản lý tài khoản. |
| **Admin** | `PREMIUM` | Toàn quyền như Quản lý, cộng thêm **Quản trị Tài khoản** (Phê duyệt, Khóa, Xóa người dùng). |

### Các tính năng liên quan đến tài khoản:
- **Đăng ký & Phê duyệt**: Người dùng đăng ký sẽ ở trạng thái *Chờ duyệt*. Chỉ Admin mới có thể duyệt, khóa hoặc xóa tài khoản.
- **Đổi mật khẩu**: Mọi tài khoản đều có thể tự đổi mật khẩu.
- **Bảo mật phân quyền**: Mọi URL đều được kiểm tra quyền chính xác (HTTP 403 nếu sai quyền, redirect về Login nếu chưa đăng nhập).

---

## 2. Quản lý Báo cáo Tiến độ (4 bộ phận)

Hệ thống có **4 luồng dữ liệu độc lập** với giao diện nhập liệu, danh sách, sửa, xóa và xuất Excel riêng:

### 2.1 Sản xuất (`/`)
Các công đoạn: Nhận BTP, Vào chuyền, Giữa chuyền, Ra chuyền, Thu hóa, Là TP, Nhập HT.

### 2.2 Tổ Cắt (`/cut/`)
Các công đoạn: **Cắt chính, Cắt lót, Cắt Mex, Cắt bông**. Không yêu cầu nhập Xưởng/Tổ.

### 2.3 KCS (`/kcs/`)
Các chỉ số: **Qua tay, Đạt, Lỗi, Tổng đạt**. Có Xưởng và Tổ. Thứ tự cột bảng: Mã hàng → Màu → Xưởng → Tổ.

### 2.4 Hoàn thiện (`/finishing/`)
Các công đoạn: **Thẻ bài, Gấp hàng, Treo/Đóng thùng**.

### Tính năng chung:
- **Cascade Dropdown**: Chọn Mã hàng → tự hiện danh sách Màu tương ứng theo cấu hình.
- **Thời gian nhập tự động**: Cột "Ngày nhập" ghi lại đúng thời điểm thực tế (`dd/mm/yyyy hh:mm:ss`) theo giờ Việt Nam (Asia/Ho_Chi_Minh) khi người dùng ấn Lưu — không cho phép chỉnh sửa.
- **Responsive**: Dạng Bảng cuộn ngang trên máy tính, dạng Thẻ (Card) trên điện thoại.

---

## 3. Dashboard Tổng hợp (`/dashboard/`)

Dành cho Quản lý (`QUAN_LY`) và Admin (`PREMIUM`).

- **4 bảng tổng hợp độc lập**: Sản xuất, Hoàn thiện, KCS, Cắt — mỗi bảng hiển thị số liệu tổng hợp theo (Mã hàng, Màu) với cột Ngày và cột Tổng cộng dồn.
- **Bộ lọc thời gian riêng biệt**: Lọc theo ngày cho từng bảng, các bảng khác không bị ảnh hưởng.
- **Phân trang độc lập**: Tham số `p1`, `p2`, `p3`, `p4` — chuyển trang bảng này không mất trạng thái bảng kia.
- **Xuất Excel từng bảng**: Lấy đúng dữ liệu theo bộ lọc đang áp dụng.
- **Nút nhập liệu nhanh** (top-bar): Nhập DL Cắt, Nhập DL Sản xuất, Nhập DL KCS, Nhập DL Hoàn thiện, Theo dõi Đơn hàng, Quản lý Mã hàng.

---

## 4. Tracking Đơn hàng (`/tracking/`)

Bảng theo dõi tổng hợp trạng thái toàn bộ đơn hàng theo (Mã hàng, Màu):
- Số lượng đơn hàng, tiến độ qua từng công đoạn, số lượng còn lại.
- Hỗ trợ xuất Excel.

---

## 5. Quản lý Cấu hình Sản phẩm (`/config/`)

Cấu trúc phân cấp: `Product (Mã hàng)` → `ProductColor (Màu + Số lượng)`.

- **Thêm Mã hàng**: Form nhập Tên mã hàng + Màu hàng loạt (cách nhau bằng dấy phẩy) + Số lượng.
- **Sửa/Xóa màu**: Có thể chỉnh sửa tên màu và số lượng bất kỳ lúc nào.
- **Xóa an toàn**: Xóa Mã hàng sẽ xóa toàn bộ màu liên quan, nhưng không ảnh hưởng dữ liệu báo cáo lịch sử.

---

## 6. Công nghệ & Cấu trúc mã nguồn chính

- **Backend**: Python 3.14, Django 6.x.
- **Database**: MySQL (có thể dùng SQLite cho dev).
- **Múi giờ**: Asia/Ho_Chi_Minh — toàn bộ thời gian nhập liệu đều chính xác theo giờ Việt Nam.
- **Models chính (`models.py`)**:
  - `AppUser`: Phân quyền 6 roles, trạng thái phê duyệt.
  - `Product`, `ProductColor`: Cấu trúc Mã hàng – Màu.
  - `ProcessReport`: Dữ liệu Sản xuất.
  - `FinishingReport`: Dữ liệu Hoàn thiện.
  - `KcsReport`: Dữ liệu KCS.
  - `CutReport`: Dữ liệu Tổ Cắt.
- **Giao diện (`templates/`)**: HTML/CSS thuần túy, 100% Mobile-Friendly.
- **Kiểm thử tự động**: 16 unit tests bao phủ toàn bộ luồng phân quyền, nhập liệu, CRUD, xuất Excel và lọc theo thời gian.
