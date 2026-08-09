# HƯỚNG DẪN SỬ DỤNG HỆ THỐNG QUẢN LÝ TIẾN ĐỘ SẢN XUẤT

Chào mừng bạn đến với Hệ thống Quản lý và Theo dõi Tiến độ Sản xuất. Hệ thống được chia làm 2 cấp độ quyền hạn (Role) với các chức năng tương ứng nhằm đảm bảo tính bảo mật và thuận tiện trong quá trình làm việc.

---

## I. DÀNH CHO TẤT CẢ NGƯỜI DÙNG

### 1. Đăng ký tài khoản
- Truy cập vào trang Đăng nhập, chọn **"Chưa có tài khoản? Đăng ký ngay"**.
- Điền đầy đủ thông tin: Họ tên, Tên tài khoản, Mật khẩu (yêu cầu nhập 2 lần để xác nhận).
- Ấn nút **Đăng ký**.
- **Lưu ý:** Tài khoản mới tạo ra sẽ ở trạng thái *Chờ duyệt*. Bạn cần báo cho Quản lý (người có quyền PREMIUM) để họ phê duyệt tài khoản của bạn trước khi có thể đăng nhập.

### 2. Đăng nhập
- Nhập Tên tài khoản và Mật khẩu.
- Nếu tài khoản đã được quản lý duyệt, bạn sẽ được tự động chuyển hướng vào màn hình làm việc chính.

---

## II. HƯỚNG DẪN DÀNH CHO NHÂN VIÊN (Quyền BASIC)

Nhân viên là người trực tiếp nhập liệu trên hệ thống. 

### 1. Thêm Báo Cáo Sản Lượng Mới
- Tại trang chính (Danh sách), ấn nút **+ Nhập mới**.
- Chọn lần lượt: **Mã Hàng** -> **Màu** -> **Cỡ**. *(Hệ thống sẽ tự động lọc danh sách Màu và Cỡ tương ứng với Mã hàng bạn vừa chọn)*.
- Nhập chính xác số lượng cho từng công đoạn tương ứng (Ví dụ: Tổ cắt, Nhận BTP, KCS...). Các ô không có số lượng có thể để trống (mặc định là 0).
- Ấn nút **Lưu dữ liệu** màu xanh lá. Dữ liệu sẽ lập tức được lưu và hiển thị ra bảng.

### 2. Xem Báo Cáo Của Mình
- Ngay khi đăng nhập thành công, bạn sẽ thấy **Danh sách dữ liệu đã nhập**.
- Với quyền BASIC, bạn **chỉ nhìn thấy các báo cáo do chính bạn nhập**.
- Trên máy tính, danh sách hiển thị dưới dạng Bảng. Trên điện thoại, danh sách sẽ hiển thị dưới dạng Thẻ (Card) rất dễ nhìn và có thể vuốt ngang để xem.

### 3. Sửa / Xoá Báo Cáo (Nếu nhập sai)
- Tại bảng danh sách, bấm vào nút **Sửa** (Màu cam) ở cuối mỗi dòng để sửa lại các số liệu bị sai và ấn **Cập nhật**.
- Hoặc bấm nút **Xóa** (Màu đỏ) để xóa hẳn dòng báo cáo đó đi. Hệ thống sẽ hỏi lại một lần nữa để tránh việc bạn bấm nhầm.

---

## III. HƯỚNG DẪN DÀNH CHO QUẢN LÝ (Quyền PREMIUM)

Tài khoản Quản lý được cấp quyền cao nhất, cho phép theo dõi toàn bộ tiến độ, quản trị danh mục sản phẩm và nhân sự.

### 1. Theo dõi & Quản lý Dữ liệu Toàn hệ thống
- Khác với nhân viên, Quản lý khi truy cập vào **Danh sách dữ liệu** sẽ nhìn thấy **toàn bộ báo cáo của tất cả công nhân viên** đã nhập lên hệ thống.
- Quản lý có quyền ấn nút **Sửa** hoặc **Xoá** bất kỳ dòng báo cáo nào nếu phát hiện có sai sót.

### 2. Quản Lý Tài Khoản (Duyệt & Khóa)
- Ấn nút **Quản lý TK** (Màu xanh lá) trên thanh công cụ.
- Hệ thống sẽ hiển thị danh sách tất cả các tài khoản đang có trên hệ thống (Bao gồm cả các tài khoản đang chờ duyệt và đã duyệt).
- Để cấp quyền cho nhân viên đăng nhập, bạn ấn nút **Phê duyệt** màu xanh lá.
- Để tạm khoá quyền truy cập của một nhân viên đã nghỉ hoặc có vấn đề, bạn ấn nút **Khóa TK** màu đỏ. Nhân viên đó sẽ ngay lập tức không thể đăng nhập được nữa.

### 3. Quản Lý Danh Mục Mã Hàng (Cấu hình)
- Ấn nút **Quản lý Mã hàng** (Màu tím) trên thanh công cụ.
- **Thêm siêu tốc**: Ấn nút **+ Thêm Mã Hàng**. Tại đây, bạn có thể nhập:
  - Tên Mã Hàng (VD: `AT99`)
  - Các Màu: Nhập nhiều màu cùng lúc cách nhau bằng dấu phẩy (VD: `Xanh, Đỏ, Trắng`)
  - Các Cỡ: Chọn nhanh các cỡ chung (XS, S, M, L, XL...) bằng cách nhấp chuột (Nút sẽ hiện màu xanh nước biển khi được chọn).
- Khi ấn **Lưu**, hệ thống sẽ tự tạo ra cấu trúc phân nhánh cho nhân viên chọn.
- **Quản lý chi tiết**: Tại trang danh sách, bạn cũng có thể bấm các nút **+ Thêm Màu** / **+ Thêm Cỡ** lẻ tẻ cho từng dòng, hoặc ấn **Xoá** để dọn dẹp các mã hàng cũ không còn sản xuất. *(Việc xoá sẽ không làm mất các báo cáo lịch sử)*.

### 4. Xuất Báo Cáo Ra Excel
- Tại trang Danh sách, ấn nút **Xuất Excel** (Màu cam).
- Hệ thống sẽ tổng hợp toàn bộ dữ liệu báo cáo của tất cả mọi người và lập tức tải về máy của bạn dưới định dạng tệp tin `DuLieuBaoCao.xlsx`. File này tương thích 100% với phần mềm Microsoft Excel.

---

*Hệ thống được thiết kế tối ưu hoá riêng biệt, đảm bảo tính thuận tiện, không yêu cầu người dùng phải hiểu biết sâu về máy tính vẫn có thể sử dụng dễ dàng trên cả Điện thoại di động lẫn Máy tính bảng / PC.*
