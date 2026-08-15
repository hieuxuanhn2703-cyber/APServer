# HƯỚNG DẪN SỬ DỤNG HỆ THỐNG QUẢN LÝ TIẾN ĐỘ SẢN XUẤT

Chào mừng bạn đến với Hệ thống Quản lý và Theo dõi Tiến độ Cắt – Sản xuất – KCS – Hoàn thiện. Hệ thống được phân chia thành **6 vai trò (Role)** với các chức năng tương ứng nhằm đảm bảo tính bảo mật và thuận tiện trong quá trình làm việc. Giao diện hệ thống được thiết kế đặc biệt dễ dàng thao tác trên màn hình điện thoại.

> **Lưu ý về thời gian:** Hệ thống tự động ghi nhận thời gian nhập liệu (`dd/mm/yyyy hh:mm:ss`) theo **giờ Việt Nam** ngay khi người dùng ấn **Lưu dữ liệu**. Thông tin này không thể chỉnh sửa thủ công, đảm bảo tính chính xác và trung thực của dữ liệu.

---

## I. DÀNH CHO TẤT CẢ NGƯỜI DÙNG

### 1. Đăng ký & Đăng nhập
- **Đăng ký:** Truy cập trang Đăng nhập → chọn **"Chưa có tài khoản? Đăng ký ngay"** → Điền Họ tên, Tên tài khoản, Mật khẩu và chọn đúng **Vai trò** phù hợp với bộ phận của bạn.
- **Lưu ý:** Tài khoản mới sẽ ở trạng thái *Chờ duyệt*. Bạn cần báo cho Admin phê duyệt thì mới có thể đăng nhập.
- **Đăng nhập:** Nhập Tên tài khoản và Mật khẩu (có thể bấm biểu tượng con mắt để xem mật khẩu). Hệ thống tự chuyển hướng vào màn hình làm việc đúng với vai trò của bạn.
- **Bảo mật truy cập:** Trường hợp người dùng **chưa đăng nhập** mà truy cập vào bất kỳ đường dẫn nào trên hệ thống, hệ thống sẽ **tự động chuyển hướng về trang Đăng nhập (`/login/`)**.

### 2. Đổi mật khẩu
- Khi đã đăng nhập, bạn có thể tự đổi mật khẩu.
- Đối với nhân viên sản xuất, nhà cắt, KCS và hoàn thiện: Nút đổi mật khẩu nằm trực tiếp ở góc trên trang.
- Đối với Quản lý và Admin (Premium): Chức năng Đổi mật khẩu nằm trong thanh menu Sidebar trượt từ bên trái.
- Có nút quay lại dễ dàng ở màn hình đổi mật khẩu nếu muốn hủy bỏ.

---

## II. HƯỚNG DẪN NHÂN VIÊN SẢN XUẤT (Quyền BASIC)

Trang làm việc chính: Màn hình **Nhập Báo Cáo Sản Xuất**

- **Thêm Báo Cáo:**
  1. Chọn **Mã Hàng** → danh sách **Màu** sẽ tự hiện ra, chọn Màu.
  2. Nhập **Xưởng**, **Tổ** (bắt buộc, không được bằng 0) và **Số lượng LĐ**.
  3. Nhập số lượng các công đoạn: Nhận BTP, Vào chuyền, Giữa chuyền, Ra chuyền, Thu hóa, Là TP, Nhập HT.
  4. Ấn **Lưu dữ liệu**.
- **Xem Danh sách:** Bấm **Xem danh sách đã nhập** để xem lại **50 báo cáo mới nhất** do chính bạn đã nhập. Để quay lại nhập liệu, hãy bấm nút **+ Nhập Mới** trên góc phải.
- **Lưu ý:** Nhân viên Sản xuất **không có quyền Sửa hay Xóa** sau khi đã lưu. Nếu nhập sai, vui lòng báo Quản lý. Hệ thống không có thanh Sidebar để tối đa diện tích màn hình.

---

## III. HƯỚNG DẪN TỔ CẮT (Quyền NHA_CAT)

Trang làm việc chính: Màn hình **Nhập Báo Cáo Cắt**

- **Thêm Báo Cáo:**
  1. Chọn **Mã Hàng** → chọn **Màu**.
  2. Nhập số lượng các công đoạn cắt: **Cắt chính, Cắt lót, Cắt Mex, Cắt bông**.
  3. Ấn **Lưu dữ liệu**. *(Không cần nhập Xưởng hay Tổ.)*
- **Xem Danh sách:** Bấm **Xem danh sách đã nhập** để xem lại 50 báo cáo mới nhất do chính bạn đã nhập.
- **Lưu ý:** Nhà cắt **không có quyền Sửa hay Xóa** sau khi đã lưu. Nếu nhập sai, vui lòng báo Quản lý. Không có thanh Sidebar.

---

## IV. HƯỚNG DẪN NHÂN VIÊN KCS (Quyền KCS)

Trang làm việc chính: Màn hình **Nhập Báo Cáo KCS**

- **Thêm Báo Cáo:**
  1. Chọn **Mã Hàng** → chọn **Màu**.
  2. Nhập **Xưởng**, **Tổ**.
  3. Nhập số liệu kiểm tra: **Qua tay, Đạt, Lỗi, Tổng đạt**.
  4. Ấn **Lưu dữ liệu**.
- **Xem Danh sách:** Bấm **Xem danh sách đã nhập** để xem 50 báo cáo mới nhất do chính bạn đã nhập.
- **Lưu ý:** Nhân viên KCS **không có quyền Sửa hay Xóa** sau khi đã lưu. Nếu nhập sai, vui lòng báo Quản lý. Không có thanh Sidebar.

---

## V. HƯỚNG DẪN NHÂN VIÊN HOÀN THIỆN (Quyền HOAN_THIEN)

Trang làm việc chính: Màn hình **Nhập Báo Cáo Hoàn Thiện**

- **Thêm Báo Cáo:**
  1. Chọn **Mã Hàng** → chọn **Màu**.
  2. Nhập số lượng: **Thẻ bài, Gấp hàng, Treo/Đóng thùng**.
  3. Ấn **Lưu dữ liệu**.
- **Xem Danh sách:** Bấm **Xem danh sách đã nhập** để xem 50 báo cáo mới nhất.
- **Lưu ý:** Nhân viên Hoàn thiện **không có quyền Sửa hay Xóa** sau khi đã lưu. Nếu nhập sai, vui lòng báo Quản lý. Không có thanh Sidebar.

---

## VI. HƯỚNG DẪN QUẢN LÝ (Quyền QUAN_LY)

Quản lý có thể nhìn thấy thanh menu mở rộng (Sidebar) bên trái màn hình với đầy đủ chức năng.

### 1. Bảng Điều Khiển — Dashboard (`/dashboard/`)
Ngay khi đăng nhập, Quản lý thấy **Dashboard Dữ Liệu** với **4 bảng tổng hợp độc lập** hiển thị đầy đủ thông tin trên màn hình rộng mà không cần kéo ngang:

| Thứ tự | Bảng | Nội dung |
|---|---|---|
| 1 | **Tổng hợp Cắt** | Số liệu tổng hợp từng (Mã hàng, Màu) của tổ Cắt (Cắt chính, Cắt lót, Cắt Mex, Cắt bông), có cột Tổng SL đơn hàng |
| 2 | **Tổng hợp Sản xuất** | Số liệu tổng hợp từng (Mã hàng, Màu) của bộ phận Sản xuất (không hiển thị cột Thời gian, có cột Số lượng LĐ) |
| 3 | **Tổng hợp KCS** | Số liệu tổng hợp từng (Mã hàng, Màu) của bộ phận KCS (Xưởng, Tổ, Qua tay, Đạt, Lỗi, Tổng đạt) |
| 4 | **Tổng hợp Hoàn thiện** | Số liệu tổng hợp từng (Mã hàng, Màu) của bộ phận Hoàn thiện (Thẻ bài, Gấp hàng, Treo/Đóng thùng) |

- **Lọc thời gian độc lập**: Mỗi bảng có bộ lọc riêng (Từ ngày – Đến ngày). Lọc bảng này không ảnh hưởng bảng kia.
- **Quy tắc tính ô Ngày / Tổng (Lũy kế theo thời gian)**: Số Tổng ở góc dưới ô chéo là **tổng lũy kế** của lần nhập đó cộng với tất cả các lần nhập trước đó. Khi có các lần nhập mới sau đó, giá trị Tổng của lần nhập cũ vẫn giữ nguyên không đổi.
- **Bộ lọc dạng Excel trên từng cột (Lọc liên tầng, Toàn bộ dữ liệu & Giữ lọc khi đổi trang)**: Các cột **Người nhập, Mã hàng, Màu, Xưởng, Tổ** đều có nút lọc `[▼]` giống Excel.
- **Xuất Excel**: Ấn nút **Xuất Excel** của từng bảng để tải file dữ liệu đã lọc trên Dashboard.
- **Phân trang**: Mỗi bảng hiển thị tối đa **10 hàng dữ liệu** trên một trang.

### 2. Các chức năng trên Sidebar
Quản lý có thể truy cập nhanh trên Sidebar:
- **BÁO CÁO TỔNG HỢP**: Tổng hợp dữ liệu (Dashboard) & Theo dõi Đơn hàng (Tracking).
- **QUY TRÌNH SẢN XUẤT**: Cho phép Quản lý tự thao tác **Nhập DL Cắt, Sản xuất, KCS, Hoàn thiện**.
- **HỆ THỐNG & QUẢN TRỊ**: Quản lý Mã hàng & Màu sắc.

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

Tài khoản `PREMIUM` là quản trị viên hệ thống. Role này sẽ tập trung vào xem báo cáo tổng quan và quản trị người dùng, **không thực hiện nhập liệu quy trình sản xuất**. Trên Sidebar, mục "Quy trình sản xuất" sẽ không được hiển thị.

Admin có quyền hạn xem Dashboard như Quản lý, và có thêm đặc quyền:

### Quản Lý Người Dùng (`/manage-accounts/`) (Trên Sidebar)
- **Phê duyệt**: Duyệt tài khoản mới đăng ký để họ có thể đăng nhập.
- **Phân quyền**: Thay đổi vai trò (Role) của từng tài khoản.
- **Khóa/Mở**: Tạm thời khóa hoặc mở khóa quyền đăng nhập.
- **Xóa vĩnh viễn**: Xóa tài khoản không còn sử dụng khỏi hệ thống.
