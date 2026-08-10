# HƯỚNG DẪN SỬ DỤNG HỆ THỐNG QUẢN LÝ TIẾN ĐỘ SẢN XUẤT VÀ HOÀN THIỆN

Chào mừng bạn đến với Hệ thống Quản lý và Theo dõi Tiến độ. Hệ thống được chia làm 4 cấp độ quyền hạn (Role) với các chức năng tương ứng nhằm đảm bảo tính bảo mật và thuận tiện trong quá trình làm việc.

---

## I. DÀNH CHO TẤT CẢ NGƯỜI DÙNG

### 1. Đăng ký & Đăng nhập
- **Đăng ký:** Truy cập vào trang Đăng nhập, chọn **"Chưa có tài khoản? Đăng ký ngay"**. Điền Họ tên, Tên tài khoản, Mật khẩu và chọn đúng Vai trò (Sản xuất, Hoàn thiện, hoặc Quản lý). 
- **Lưu ý:** Tài khoản mới tạo ra sẽ ở trạng thái *Chờ duyệt*. Bạn cần báo cho Admin (quyền PREMIUM) phê duyệt thì mới có thể đăng nhập.
- **Đăng nhập:** Nhập Tên tài khoản và Mật khẩu. Bạn sẽ được tự động chuyển hướng vào màn hình làm việc tương ứng với quyền của mình.

### 2. Đổi mật khẩu
- Khi đã đăng nhập, ở tất cả các trang làm việc chính, bạn sẽ thấy nút **"Đổi mật khẩu"** màu xanh (bên cạnh nút Đăng xuất). 
- Bạn có thể vào đó để tự đổi mật khẩu cá nhân bất cứ lúc nào.

---

## II. HƯỚNG DẪN DÀNH CHO NHÂN VIÊN SẢN XUẤT (Quyền BASIC)

Nhân viên Sản xuất là người trực tiếp nhập liệu số lượng các công đoạn sản xuất.

- **Thêm Báo Cáo:** Tại trang chính, chọn **Mã Hàng -> Màu -> Cỡ**. Nhập chính xác số lượng cho từng công đoạn (Tổ cắt, Nhận BTP, Vào chuyền...). (Tổ và Xưởng mặc định là 0, yêu cầu phải nhập khác 0). Ấn nút **Lưu dữ liệu**.
- **Xem Dữ liệu:** Bạn chỉ được phép nhìn thấy những dữ liệu **Sản xuất** do chính bạn đã nhập. Bạn không thể xem dữ liệu Hoàn thiện hay dữ liệu của người khác.
- **Lưu ý:** Để đảm bảo tính toàn vẹn dữ liệu, nhân viên Sản xuất **không có quyền Sửa hay Xóa** dữ liệu sau khi đã ấn Lưu. Nếu nhập sai, vui lòng báo lại cho Quản lý.

---

## III. HƯỚNG DẪN DÀNH CHO NHÂN VIÊN HOÀN THIỆN (Quyền HOAN_THIEN)

Tương tự như Sản xuất, nhưng dành riêng cho quy trình Hoàn thiện.

- **Thêm Báo Cáo:** Nhập số lượng cho các công đoạn: Nhận chuyền, Nhặt chỉ, Ủi, Gập bao gói, KCS. Ấn nút **Lưu dữ liệu**.
- **Xem Dữ liệu:** Bạn chỉ được phép xem các báo cáo **Hoàn thiện** do chính bạn nhập. 
- **Lưu ý:** Nhân viên Hoàn thiện **không có quyền Sửa hay Xóa** dữ liệu sau khi đã ấn Lưu. Nếu nhập sai, vui lòng báo lại cho Quản lý.

---

## IV. HƯỚNG DẪN DÀNH CHO QUẢN LÝ (Quyền QUAN_LY)

Tài khoản Quản lý được cấp quyền xem và chỉnh sửa dữ liệu toàn hệ thống, cũng như xem báo cáo tổng hợp.

### 1. Bảng Điều Khiển (Dashboard) & Thống Kê
- Ngay khi đăng nhập, Quản lý sẽ thấy **Dashboard Dữ Liệu**, nơi hiển thị hai bảng lớn: **Danh sách Sản xuất** và **Danh sách Hoàn thiện** của toàn bộ công nhân viên.
- **Lọc Dữ Liệu:** Quản lý có thể lọc dữ liệu theo khoảng thời gian (Từ ngày - Đến ngày) độc lập cho từng bảng Sản xuất và bảng Hoàn thiện.
- **Xuất Excel:** Ấn nút **Xuất Excel** để tải dữ liệu về máy. Hệ thống sẽ chỉ xuất các dữ liệu nằm trong khoảng thời gian đã lọc.

### 2. Quản Lý Dữ Liệu
- Quản lý có thể ấn nút **Nhập DL Sản xuất** hoặc **Nhập DL Hoàn thiện** ngay trên Dashboard để tự mình nhập số liệu nếu cần.
- Quản lý có toàn quyền **Sửa** hoặc **Xóa** bất kỳ báo cáo nào của bất kỳ ai nếu phát hiện có sai sót.
- Quản lý có thể thêm mới, sửa, xóa cấu trúc **Mã hàng - Màu - Cỡ** (Cấu hình mã hàng).

*(Lưu ý: Quản lý không có quyền tác động đến các Tài khoản trên hệ thống).*

---

## V. HƯỚNG DẪN DÀNH CHO ADMIN (Quyền PREMIUM)

Admin (Cao cấp) là người quản trị cao nhất của hệ thống, nắm giữ quyền hạn về mặt nhân sự và cấu hình.

### 1. Dashboard Dành Riêng Cho Admin
- Admin cũng có quyền truy cập **Dashboard** để xem, Sửa, Xóa, Lọc ngày và Xuất Excel toàn bộ dữ liệu Sản xuất & Hoàn thiện giống như Quản lý.
- Tuy nhiên, Admin sẽ không có nút tự nhập liệu (để tránh nhầm lẫn vai trò).

### 2. Quản Lý Tài Khoản
- Chỉ Admin mới thấy nút **Quản lý Tài khoản**.
- **Phê duyệt / Khóa:** Admin duyệt các tài khoản mới đăng ký để họ có thể đăng nhập, hoặc khóa các tài khoản vi phạm/nghỉ việc.
- **Xóa Vĩnh Viễn:** Admin có quyền ấn nút **Xóa** để loại bỏ vĩnh viễn một tài khoản khỏi hệ thống.

---

*Hệ thống được thiết kế tối ưu hoá riêng biệt, đảm bảo tính thuận tiện, không yêu cầu người dùng phải hiểu biết sâu về máy tính vẫn có thể sử dụng dễ dàng trên cả Điện thoại di động lẫn PC.*
