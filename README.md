# Tài liệu Mô tả Hệ thống Process Monitoring

Đây là hệ thống quản lý và giám sát tiến độ quy trình sản xuất và hoàn thiện, cho phép công nhân/nhân viên nhập báo cáo sản lượng qua từng công đoạn, và quản lý cấp cao theo dõi, xuất báo cáo cũng như quản trị cấu trúc sản phẩm và nhân sự.

Hệ thống được phát triển bằng **Django** (Python) và sử dụng cơ sở dữ liệu **SQLite** / **MySQL**.

---

## 1. Phân quyền và Quản lý Tài khoản (RBAC)

Hệ thống chia người dùng làm 4 cấp độ quyền chính, được thiết kế chặt chẽ và độc lập:

1. **Tài khoản Sản xuất (BASIC)**: Chỉ có quyền nhập và xem các báo cáo về công đoạn **Sản xuất** do chính mình tạo ra. Không có quyền sửa/xóa dữ liệu.
2. **Tài khoản Hoàn thiện (HOAN_THIEN)**: Chỉ có quyền nhập và xem các báo cáo về công đoạn **Hoàn thiện** do chính mình tạo ra. Không có quyền sửa/xóa dữ liệu.
3. **Tài khoản Quản lý (QUAN_LY)**: Có quyền xem, thao tác (sửa/xóa) trên toàn bộ dữ liệu Sản xuất và Hoàn thiện của tất cả mọi người. Có quyền xem Dashboard, xuất Excel, quản lý mã hàng và tự nhập liệu. Không có quyền can thiệp vào tài khoản người dùng khác.
4. **Tài khoản Admin (PREMIUM)**: Quyền lực cao nhất. Sở hữu mọi quyền hạn của Quản lý, cộng thêm quyền **Quản trị Tài khoản** (Phê duyệt, Khóa, và Xóa vĩnh viễn người dùng).

### Các tính năng liên quan đến tài khoản:
- **Đăng ký & Phê duyệt**: Người dùng đăng ký sẽ ở trạng thái chờ duyệt. Chỉ Admin mới có thể duyệt, khóa hoặc xóa tài khoản.
- **Đổi mật khẩu**: Mọi tài khoản đều có thể tự thay đổi mật khẩu của mình một cách an toàn.
- **Bảo mật tuyệt đối**: Tất cả các URL đều được phân quyền chính xác bằng mã HTTP (403 Forbidden đối với hành vi truy cập sai quyền). Chưa đăng nhập sẽ bị đẩy về trang Login.

---

## 2. Quản lý Báo cáo Tiến độ (Process Reports)

Hệ thống có hai luồng dữ liệu riêng biệt: Dữ liệu Sản xuất và Dữ liệu Hoàn thiện.

- **Nhập liệu Động**: 
  - Người dùng chọn cấu hình sản phẩm: `Mã Hàng -> Màu -> Cỡ`. Dropdown này được tải bất đồng bộ: chọn Mã hàng sẽ tự hiện Màu tương ứng, v.v.
  - Các công đoạn có nhiều thông số (Nhận chuyền, Nhặt chỉ, Tổ cắt, v.v.). Đặc biệt Xưởng và Tổ bắt buộc phải nhập khác 0.
- **Xem danh sách**: Giao diện Responsive. Dạng Bảng trên máy tính và dạng Thẻ (Card) trên điện thoại.
- **Dashboard (Bảng điều khiển)**:
  - Nơi Quản lý và Admin có cái nhìn tổng quan. 
  - **Lọc Dữ liệu Độc lập**: Bảng Sản xuất và Hoàn thiện có công cụ lọc thời gian (Từ ngày - Đến ngày) hoàn toàn riêng biệt.
- **Xuất Excel**: Chức năng xuất dữ liệu báo cáo `.xlsx` linh hoạt, lấy đúng dữ liệu theo bộ lọc thời gian đang áp dụng.

---

## 3. Quản lý Cấu hình Sản phẩm (Mã Hàng - Màu - Cỡ)

Dữ liệu sản phẩm được lưu trong CSDL dưới dạng cây phân cấp: `Product` -> `ProductColor` -> `ProductSize`. Tính năng này dành cho QUAN_LY và PREMIUM.

- **Thêm Mã hàng siêu tốc**: Một form duy nhất cho phép nhập Tên Mã Hàng, nhập hàng loạt Màu (cách nhau bằng dấu phẩy), và chọn nhanh các Cỡ chung (XS, S, M, L, XL, XXL, XXXL).
- **Tuỳ biến sâu**: Có thể vào từng Mã hàng để thêm Màu mới, vào từng Màu để thêm Cỡ mới bất kỳ lúc nào.
- **Xoá an toàn (Cascade Delete)**: Xoá Mã hàng sẽ dọn dẹp Màu/Cỡ bên trong. Dữ liệu này độc lập với dữ liệu báo cáo, nên xoá cấu hình không làm mất báo cáo lịch sử.

---

## 4. Công nghệ & Cấu trúc mã nguồn chính
- **Backend**: Python 3, Django Web Framework.
- **Models chính (`models.py`)**:
  - `AppUser`: Phân quyền với 4 roles và trạng thái duyệt.
  - `Product`, `ProductColor`, `ProductSize`: Lưu cấu trúc mã hàng.
  - `ProcessReport` & `FinishingReport`: Bảng dữ liệu tương ứng cho Sản xuất và Hoàn thiện.
- **Giao diện (`templates/`)**: Sử dụng HTML/CSS thuần túy. Giao diện tối giản, trực quan, 100% Mobile-Friendly.
- **Kiểm thử (Automated Tests)**: Hệ thống được bao phủ bởi 15 unit tests tự động, đặc biệt là bài test vét cạn 36 kịch bản (Ma trận 4 Roles x 9 URL Routes) đảm bảo chặt chẽ tuyệt đối về bảo mật phân quyền.
