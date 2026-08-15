# Tài liệu Mô tả Hệ thống Process Monitoring

Đây là hệ thống quản lý và giám sát tiến độ quy trình **Cắt – Sản xuất – KCS – Hoàn thiện**, cho phép nhân viên từng bộ phận nhập báo cáo sản lượng, và cấp quản lý theo dõi toàn diện, xuất báo cáo cũng như quản trị cấu trúc sản phẩm và nhân sự.

Hệ thống được phát triển bằng **Django** (Python) và sử dụng cơ sở dữ liệu **MySQL/SQLite**. Giao diện được tối ưu hóa cực tốt cho điện thoại di động (Mobile-first).

---

## 1. Phân quyền & Quản lý Tài khoản (RBAC)

Hệ thống phân chia người dùng thành **6 vai trò (Role)** chặt chẽ và độc lập:

| Vai trò | Mã | Quyền hạn |
|---|---|---|
| **Sản xuất** | `BASIC` | Nhập & xem lịch sử báo cáo Sản xuất (50 bản ghi gần nhất). Không có Sidebar. |
| **Nhà cắt** | `NHA_CAT` | Nhập & xem lịch sử báo cáo Cắt (Mã hàng, Màu, Cắt chính/lót/Mex/bông). Không có Sidebar. |
| **KCS** | `KCS` | Nhập & xem lịch sử báo cáo KCS (Qua tay, Đạt, Lỗi, Tổng đạt). Không có Sidebar. |
| **Hoàn thiện** | `HOAN_THIEN` | Nhập & xem lịch sử báo cáo Hoàn thiện (Thẻ bài, Gấp hàng, Treo/Đóng thùng). Không có Sidebar. |
| **Quản lý** | `QUAN_LY` | Quản lý xưởng: Có Sidebar điều hướng. Xem Dashboard 4 bảng, tự nhập liệu cho 4 bộ phận, xem danh sách 50 dòng mới nhất, xuất Excel tại Dashboard, quản lý Mã hàng, xem Tracking. |
| **Admin** | `PREMIUM` | Quản trị cấp cao: Có Sidebar. Chỉ tập trung xem Dashboard, Quản lý Hệ thống (Tài khoản, Mã hàng), xem Tracking. **Không hiển thị các mục Nhập liệu báo cáo**. |

### Các tính năng liên quan đến tài khoản:
- **Đăng ký & Phê duyệt**: Người dùng đăng ký sẽ ở trạng thái *Chờ duyệt*. Chỉ Admin mới có thể duyệt, khóa hoặc xóa tài khoản.
- **Đổi mật khẩu**: Mọi tài khoản đều có thể tự đổi mật khẩu. Có nút "Quay lại" thông minh cho các tài khoản công nhân khi ở trang đổi mật khẩu.
- **Bảo mật & Chuyển hướng tự động**: Mọi trang trong hệ thống đều yêu cầu đăng nhập. Nếu người dùng chưa đăng nhập, hệ thống sẽ **tự động chuyển hướng về trang Login (`/login/`)**.

---

## 2. Quản lý Báo cáo Tiến độ (4 bộ phận)

Hệ thống có **4 luồng dữ liệu độc lập** với giao diện nhập liệu và danh sách lịch sử riêng:

### 2.1 Sản xuất (`/`)
Thông tin chung: Xưởng, Tổ, **Số lượng LĐ**.
Các công đoạn: Nhận BTP, Vào chuyền, Giữa chuyền, Ra chuyền, Thu hóa, Là TP, Nhập HT.

### 2.2 Tổ Cắt (`/cut/`)
Các công đoạn: **Cắt chính, Cắt lót, Cắt Mex, Cắt bông**. Không yêu cầu nhập Xưởng/Tổ.

### 2.3 KCS (`/kcs/`)
Các chỉ số: **Qua tay, Đạt, Lỗi, Tổng đạt**. Có Xưởng và Tổ.

### 2.4 Hoàn thiện (`/finishing/`)
Các công đoạn: **Thẻ bài, Gấp hàng, Treo/Đóng thùng**.

### Tính năng chung:
- **Cascade Dropdown**: Chọn Mã hàng → tự hiện danh sách Màu tương ứng theo cấu hình.
- **Thời gian nhập tự động**: Cột "Ngày nhập" ghi lại đúng thời điểm thực tế theo giờ Việt Nam (Asia/Ho_Chi_Minh) khi người dùng ấn Lưu — không cho phép chỉnh sửa.
- **Giao diện tối ưu Mobile**: Giao diện đăng nhập, đăng ký và form nhập liệu được thiết kế lại tối ưu 100% trên điện thoại. Ô nhập ngày, nhập số lớn dễ thao tác, có nút ẩn/hiện mật khẩu.
- **Danh sách báo cáo tinh gọn**: Tại trang danh sách của các bộ phận, hệ thống giới hạn hiển thị **50 bản ghi mới nhất**, thanh công cụ Header chỉ có nút `+ Nhập Mới` để giao diện đơn giản nhất.

---

## 3. Dashboard Tổng hợp (`/dashboard/`)
 
 Dành cho Quản lý (`QUAN_LY`) và Admin (`PREMIUM`).
 
 - **Khung hiển thị mở rộng (Full-width Desktop)**: Dashboard được thiết kế rộng toàn màn hình máy tính, giúp hiển thị trọn vẹn tất cả các cột mà không cần kéo thanh cuộn ngang (overflow-x).
 - **Thứ tự 4 bảng tổng hợp độc lập**: **Tổng hợp Cắt → Tổng hợp Sản Xuất → Tổng hợp KCS → Tổng hợp Hoàn Thiện**.
 - **Quy tắc tính ô Ngày / Tổng**: Số Tổng ở góc dưới ô chéo là **tổng lũy kế** tính đến thời điểm của lần nhập đó (giá trị lần đó + tất cả các lần trước đó). Khi có thêm lần nhập mới sau này, số Tổng của các lần nhập trước vẫn được giữ nguyên.
 - **Bộ lọc Excel trên từng cột (Lọc liên tầng, Toàn bộ dữ liệu & Giữ lọc khi đổi trang)**: Các cột **Người nhập, Mã hàng, Màu, Xưởng, Tổ** trên cả 4 bảng tổng hợp đều có nút `[▼]` lọc dữ liệu giống hệt Microsoft Excel:
   - **Lọc liên tầng (Cascading)**: Khi lọc một cột bất kỳ (ví dụ Mã hàng), popup của các cột khác (ví dụ Màu) chỉ hiển thị các giá trị thuộc về các dòng đã được lọc.
   - Bấm vào `[▼]` để mở popup danh sách các giá trị thực tế.
   - Tích hợp ô Tìm kiếm nhanh, tùy chọn (Chọn tất cả), chọn lọc đa giá trị linh hoạt.
   - Khi áp dụng, hệ thống **lọc trên toàn bộ cơ sở dữ liệu** và phân trang tối đa 10 hàng/trang.
   - **Khi chuyển trang**, hệ thống **tự động bảo toàn tất cả các bộ lọc cột đang áp dụng**.
 - **Bộ lọc thời gian riêng biệt**: Lọc theo ngày cho từng bảng, các bảng khác không bị ảnh hưởng.
 - **Xuất Excel từng bảng**: Lấy đúng dữ liệu theo bộ lọc đang áp dụng. Dành riêng tại Dashboard.

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

- **Backend**: Python, Django 5.x.
- **Database**: MySQL (có thể dùng SQLite cho dev).
- **Giao diện (`templates/`)**: HTML/CSS thuần túy, 100% Mobile-Friendly (CSS hiện đại, hiệu ứng nổi bật).
- **Kiểm thử tự động**: Tích hợp các unit tests bao phủ luồng phân quyền, nhập liệu, UI controls, và lọc dữ liệu (100% passed).
