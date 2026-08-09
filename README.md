# Tài liệu Mô tả Hệ thống Process Monitoring

Đây là hệ thống quản lý và giám sát tiến độ sản xuất, cho phép công nhân/nhân viên nhập báo cáo sản lượng qua từng công đoạn, và quản lý cấp cao theo dõi, duyệt tài khoản cũng như quản lý cấu trúc sản phẩm.

Hệ thống được phát triển bằng **Django** (Python) và sử dụng cơ sở dữ liệu **MySQL**.

---

## 1. Phân quyền và Quản lý Tài khoản

Hệ thống chia người dùng làm 2 cấp độ quyền chính:
- **Tài khoản Cơ bản (BASIC)**: Dành cho nhân viên bình thường. Chỉ có thể nhập báo cáo, xem và chỉnh sửa các báo cáo **do chính mình tạo ra**.
- **Tài khoản Cao cấp (PREMIUM)**: Dành cho Quản lý. Có thể xem, sửa dữ liệu của **tất cả mọi người**. Ngoài ra còn được cấp các quyền quản trị hệ thống.

### Các tính năng liên quan đến tài khoản:
- **Đăng ký tài khoản**: Người dùng có thể tự đăng ký tài khoản (kèm xác nhận mật khẩu 2 lần). Tài khoản mới tạo sẽ ở trạng thái **Chờ duyệt** và chưa thể đăng nhập.
- **Phê duyệt tài khoản**: Quản lý (PREMIUM) có trang riêng để xét duyệt các tài khoản mới. Khi được phê duyệt, nhân viên mới có thể đăng nhập vào hệ thống.
- **Bảo mật**: Các trang đều yêu cầu phải đăng nhập (`@login_required`), nếu chưa đăng nhập sẽ bị đẩy về trang Login.

---

## 2. Quản lý Báo cáo Tiến độ (Process Reports)

Đây là tính năng cốt lõi của hệ thống để thu thập dữ liệu sản xuất.

- **Nhập liệu**: 
  - Người dùng chọn cấu hình sản phẩm: `Mã Hàng -> Màu -> Cỡ`. Các menu thả xuống (Dropdown) này được thiết kế **động**, chọn Mã hàng sẽ tự hiện Màu tương ứng, chọn Màu sẽ hiện Cỡ tương ứng.
  - Điền số lượng vào các công đoạn: Tổ (bắt buộc), Nhận BTP, Vào chuyền, Giữa chuyền, Ra chuyền, Thu hóa, Là thành phẩm, KCS, Nhập hoàn thiện.
- **Xem danh sách báo cáo**:
  - Danh sách được hiển thị dưới dạng Bảng (trên máy tính) hoặc Thẻ Card (trên điện thoại).
  - Nhân viên chỉ thấy báo cáo của mình, Quản lý thấy của tất cả mọi người.
- **Sửa báo cáo**: Cho phép cập nhật lại số liệu nếu nhập sai.
- **Xuất Excel**: Tài khoản PREMIUM có một nút "Xuất Excel" để tải toàn bộ dữ liệu lịch sử báo cáo về máy dưới dạng file chuẩn `.xlsx` (sử dụng thư viện `openpyxl`).

---

## 3. Quản lý Cấu hình Sản phẩm (Mã Hàng - Màu - Cỡ)

Thay vì lưu file tĩnh, dữ liệu sản phẩm được lưu trong CSDL dưới dạng cây phân cấp: `Product` -> `ProductColor` -> `ProductSize`. Tính năng này **chỉ dành cho tài khoản PREMIUM**.

- **Thêm Mã hàng siêu tốc**: Một form duy nhất cho phép Quản lý nhập Tên Mã Hàng, nhập hàng loạt Màu (cách nhau bằng dấu phẩy), và chọn nhanh các Cỡ chung bằng các nút bấm (XS, S, M, L, XL, XXL, XXXL).
- **Tuỳ biến sâu**: Có thể vào từng Mã hàng để thêm Màu mới, vào từng Màu để thêm Cỡ mới bất kỳ lúc nào.
- **Xoá an toàn**: 
  - Xoá Mã hàng sẽ tự dọn dẹp các Màu và Cỡ bên trong (Cascade Delete).
  - Dữ liệu cấu hình độc lập với dữ liệu báo cáo: Việc xoá một Mã hàng khỏi hệ thống để không ai chọn được nữa sẽ **không làm mất** các báo cáo lịch sử mà công nhân đã nhập trước đó.

---

## 4. Công nghệ & Cấu trúc mã nguồn chính
- **Backend**: Python 3, Django Web Framework.
- **Database**: MySQL (kết nối qua `mysqlclient`).
- **Models chính (`models.py`)**:
  - `AppUser`: Lưu thông tin tài khoản (Tên, Tài khoản, Mật khẩu, Quyền, Trạng thái duyệt).
  - `Product`, `ProductColor`, `ProductSize`: Lưu cấu trúc mã hàng.
  - `ProcessReport`: Lưu báo cáo tiến độ sản xuất thực tế.
- **Giao diện (`templates/`)**: Sử dụng HTML/CSS thuần (Responsive, tương thích tốt với cả giao diện di động lẫn máy tính bàn). Các bảng được thiết kế tự cuộn ngang khi màn hình nhỏ.
- **Forms (`forms.py`)**: Hàm `load_config()` làm nhiệm vụ móc nối dữ liệu bảng Product để trả về cấu trúc động cho Javascript ở trang Nhập liệu.
