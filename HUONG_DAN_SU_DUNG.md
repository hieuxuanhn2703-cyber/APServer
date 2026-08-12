# HƯỚNG DẪN SỬ DỤNG HỆ THỐNG QUẢN LÝ TIẾN ĐỘ SẢN XUẤT

Chào mừng bạn đến với Hệ thống Quản lý và Theo dõi Tiến độ Cắt – Sản xuất – KCS – Hoàn thiện. Hệ thống được phân chia thành **6 vai trò (Role)** với các chức năng tương ứng nhằm đảm bảo tính bảo mật và thuận tiện trong quá trình làm việc.

> **Lưu ý về thời gian:** Hệ thống tự động ghi nhận thời gian nhập liệu (`dd/mm/yyyy hh:mm:ss`) theo **giờ Việt Nam** ngay khi người dùng ấn **Lưu dữ liệu**. Thông tin này không thể chỉnh sửa thủ công, đảm bảo tính chính xác và trung thực của dữ liệu.

---

## I. DÀNH CHO TẤT CẢ NGƯỜI DÙNG

### 1. Đăng ký & Đăng nhập
- **Đăng ký:** Truy cập trang Đăng nhập → chọn **"Chưa có tài khoản? Đăng ký ngay"** → Điền Họ tên, Tên tài khoản, Mật khẩu và chọn đúng **Vai trò** phù hợp với bộ phận của bạn:
  - **Sản xuất** – nhân viên dây chuyền sản xuất
  - **Nhà cắt** – nhân viên tổ cắt
  - **KCS** – nhân viên kiểm tra chất lượng
  - **Hoàn thiện** – nhân viên bộ phận hoàn thiện
  - **Quản lý** – cán bộ quản lý tổng hợp
- **Lưu ý:** Tài khoản mới sẽ ở trạng thái *Chờ duyệt*. Bạn cần báo cho Admin phê duyệt thì mới có thể đăng nhập.
- **Đăng nhập:** Nhập Tên tài khoản và Mật khẩu. Hệ thống tự chuyển hướng vào màn hình làm việc đúng với vai trò của bạn.

### 2. Đổi mật khẩu
Khi đã đăng nhập, bấm nút **"Đổi mật khẩu"** ở góc trên trang để tự đổi mật khẩu cá nhân.

---

## II. HƯỚNG DẪN NHÂN VIÊN SẢN XUẤT (Quyền BASIC)

Trang làm việc: `/` (sau khi đăng nhập)

- **Thêm Báo Cáo:**
  1. Chọn **Mã Hàng** → danh sách **Màu** sẽ tự hiện ra, chọn Màu.
  2. Nhập **Xưởng**, **Tổ** (bắt buộc, không được bằng 0) và **Số lượng LĐ**.
  3. Nhập số lượng các công đoạn: Nhận BTP, Vào chuyền, Giữa chuyền, Ra chuyền, Thu hóa, Là TP, Nhập HT.
  4. Ấn **Lưu dữ liệu**.
- **Xem Danh sách:** Vào `/list/` để xem các báo cáo **do chính bạn** đã nhập.
- **Lưu ý:** Nhân viên Sản xuất **không có quyền Sửa hay Xóa** sau khi đã lưu. Nếu nhập sai, vui lòng báo Quản lý.

---

## III. HƯỚNG DẪN TỔ CẮT (Quyền NHA_CAT)

Trang làm việc: `/cut/`

- **Thêm Báo Cáo:**
  1. Chọn **Mã Hàng** → chọn **Màu**.
  2. Nhập số lượng các công đoạn cắt: **Cắt chính, Cắt lót, Cắt Mex, Cắt bông**.
  3. Ấn **Lưu dữ liệu**. *(Không cần nhập Xưởng hay Tổ.)*
- **Xem Danh sách:** Vào `/cut/list/` để xem các báo cáo cắt do chính bạn nhập.
- **Lưu ý:** Nhà cắt **không có quyền Sửa hay Xóa** sau khi đã lưu. Nếu nhập sai, vui lòng báo Quản lý.

---

## IV. HƯỚNG DẪN NHÂN VIÊN KCS (Quyền KCS)

Trang làm việc: `/kcs/`

- **Thêm Báo Cáo:**
  1. Chọn **Mã Hàng** → chọn **Màu**.
  2. Nhập **Xưởng**, **Tổ**.
  3. Nhập số liệu kiểm tra: **Qua tay, Đạt, Lỗi, Tổng đạt**.
  4. Ấn **Lưu dữ liệu**.
- **Xem Danh sách:** Vào `/kcs/list/` để xem các báo cáo KCS do chính bạn nhập.
  - Cột bảng theo thứ tự: Mã hàng → Màu → Xưởng → Tổ → Cỡ → Qua tay → Đạt → Lỗi → Tổng đạt.
- **Lưu ý:** Nhân viên KCS **không có quyền Sửa hay Xóa** sau khi đã lưu. Nếu nhập sai, vui lòng báo Quản lý.

---

## V. HƯỚNG DẪN NHÂN VIÊN HOÀN THIỆN (Quyền HOAN_THIEN)

Trang làm việc: `/finishing/`

- **Thêm Báo Cáo:**
  1. Chọn **Mã Hàng** → chọn **Màu**.
  2. Nhập số lượng: **Thẻ bài, Gấp hàng, Treo/Đóng thùng**.
  3. Ấn **Lưu dữ liệu**.
- **Xem Danh sách:** Vào `/finishing/list/` để xem các báo cáo hoàn thiện do chính bạn nhập.
- **Lưu ý:** Nhân viên Hoàn thiện **không có quyền Sửa hay Xóa** sau khi đã lưu. Nếu nhập sai, vui lòng báo Quản lý.

---

## VI. HƯỚNG DẪN QUẢN LÝ (Quyền QUAN_LY)

### 1. Bảng Điều Khiển — Dashboard (`/dashboard/`)
Ngay khi đăng nhập, Quản lý thấy **Dashboard Dữ Liệu** với **4 bảng tổng hợp độc lập** (được tối ưu giao diện rộng toàn màn hình trên máy tính, hiển thị đầy đủ các cột mà không cần kéo ngang):

| Thứ tự | Bảng | Nội dung |
|---|---|---|
| 1 | **Tổng hợp Cắt** | Số liệu tổng hợp từng (Mã hàng, Màu) của tổ Cắt (Cắt chính, Cắt lót, Cắt Mex, Cắt bông), có cột Tổng SL đơn hàng |
| 2 | **Tổng hợp Sản xuất** | Số liệu tổng hợp từng (Mã hàng, Màu) của bộ phận Sản xuất (không hiển thị cột Thời gian, có cột Số lượng LĐ) |
| 3 | **Tổng hợp KCS** | Số liệu tổng hợp từng (Mã hàng, Màu) của bộ phận KCS (Xưởng, Tổ, Qua tay, Đạt, Lỗi, Tổng đạt) |
| 4 | **Tổng hợp Hoàn thiện** | Số liệu tổng hợp từng (Mã hàng, Màu) của bộ phận Hoàn thiện (Thẻ bài, Gấp hàng, Treo/Đóng thùng) |

- **Lọc thời gian độc lập**: Mỗi bảng có bộ lọc riêng (Từ ngày – Đến ngày). Lọc bảng này không ảnh hưởng bảng kia.
- **Quy tắc tính ô Ngày / Tổng (Lũy kế theo thời gian)**: Số Tổng ở góc dưới ô chéo là **tổng lũy kế** của lần nhập đó cộng với tất cả các lần nhập trước đó (cùng Mã hàng + Màu). Khi có các lần nhập mới sau đó, giá trị Tổng của lần nhập cũ vẫn giữ nguyên không đổi.
- **Bộ lọc dạng Excel trên từng cột (Desktop)**: Các cột **Người nhập, Mã hàng, Màu, Xưởng, Tổ** trên cả 4 bảng đều có nút lọc `[▼]` giống Excel:
  - Bấm vào nút `[▼]` trên tiêu đề cột để mở popup danh sách các giá trị phân biệt.
  - Hỗ trợ ô **Tìm kiếm**, checkbox **(Chọn tất cả)**, chọn lọc đa giá trị linh hoạt.
  - Hỗ trợ lọc kết hợp nhiều cột cùng lúc trong bảng. Cột đang có bộ lọc sẽ đổi màu cam nổi bật kèm biểu tượng phễu lọc.
  - Bấm **"Áp dụng"** để lọc ngay lập tức trên bảng hoặc **"Xóa lọc"** để bỏ lọc cột đó.
- **Xuất Excel**: Ấn nút **Xuất Excel** của từng bảng để tải file dữ liệu đã lọc.
- **Phân trang**: Mỗi bảng hiển thị tối đa **10 hàng dữ liệu** trên một trang và phân trang độc lập, chuyển trang bảng này không mất trang của bảng kia.

### 2. Nhập Dữ Liệu Nhanh (Top-bar)
Từ Dashboard, Quản lý có thể truy cập nhanh:
- **Nhập DL Cắt** → `/cut/`
- **Nhập DL Sản xuất** → `/`
- **Nhập DL KCS** → `/kcs/`
- **Nhập DL Hoàn thiện** → `/finishing/`
- **Theo dõi Đơn hàng** → `/tracking/`
- **Quản lý Mã hàng** → `/config/`

### 3. Quản Lý & Sửa/Xóa Dữ Liệu
- Quản lý có thể **Sửa** hoặc **Xóa** bất kỳ dòng dữ liệu nào của bất kỳ ai từ cả 4 bộ phận.
- Khi ấn Sửa, hệ thống hiển thị thời gian ghi nhận gốc để đối chiếu.

### 4. Quản Lý Cấu Hình Mã Hàng (`/config/`)
- Thêm Mã hàng mới + các Màu sắc và Số lượng đơn hàng.
- Sửa/Xóa màu và số lượng bất kỳ lúc nào.
- Xóa Mã hàng sẽ xóa toàn bộ Màu liên quan (không ảnh hưởng lịch sử báo cáo).

### 5. Tracking Đơn Hàng (`/tracking/`)
Bảng tổng hợp theo dõi tiến độ toàn bộ đơn hàng theo (Mã hàng, Màu):
- Số lượng đơn, tiến độ từng công đoạn, số lượng còn lại.
- Hỗ trợ xuất Excel.

*(Lưu ý: Quản lý không có quyền can thiệp vào Tài khoản người dùng trên hệ thống.)*

---

## VII. HƯỚNG DẪN ADMIN (Quyền PREMIUM)

Admin có toàn bộ quyền hạn như Quản lý, cộng thêm:

### Quản Lý Người Dùng (`/manage-accounts/`)
- **Phê duyệt**: Duyệt tài khoản mới đăng ký để họ có thể đăng nhập.
- **Phân quyền**: Thay đổi vai trò (Role) của từng tài khoản.
- **Khóa/Mở**: Tạm thời khóa hoặc mở khóa quyền đăng nhập.
- **Xóa vĩnh viễn**: Xóa tài khoản không còn sử dụng khỏi hệ thống.
