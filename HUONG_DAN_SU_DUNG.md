# HƯỚNG DẪN SỬ DỤNG HỆ THỐNG QUẢN LÝ TIẾN ĐỘ SẢN XUẤT & KẾ TOÁN

Chào mừng bạn đến với Hệ thống Quản lý và Giám sát Tiến độ **Cắt – May Sản Xuất – KCS – Hoàn Thiện & Kế Toán Xuất Hàng**. Hệ thống được thiết kế tối ưu trên cả máy tính lẫn điện thoại di động, phân chia thành **7 vai trò (Role)** với các quyền hạn độc lập nhằm bảo mật thông tin và tối ưu thao tác công việc.

> 🕒 **Lưu ý về thời gian & Định dạng số:**
> - Hệ thống tự động ghi nhận thời gian nhập liệu (`dd/mm/yyyy hh:mm:ss`) theo **giờ Việt Nam** ngay khi người dùng ấn **Lưu dữ liệu**.
> - Mọi số tiền và số lượng lớn đều được định dạng dấu phẩy `,` phân cách hàng nghìn (ví dụ: `150,000`, `33,000,000 VNĐ`) để dễ quan sát và tránh nhầm lẫn.

---

## I. HƯỚNG DẪN CHUNG CHO TẤT CẢ NGƯỜI DÙNG

### 1. Đăng Ký & Đăng Nhập
- **Đăng ký tài khoản:** Tại màn hình Đăng nhập → bấm **"Chưa có tài khoản? Đăng ký ngay"** → Nhập Họ tên, Tên tài khoản, Mật khẩu và chọn đúng **Vai trò** của bạn.
- **Phê duyệt:** Tài khoản đăng ký mới sẽ ở trạng thái *Chờ duyệt*. Vui lòng liên hệ Quản trị viên (Admin) để được kích hoạt.
- **Đăng nhập:** Nhập Tên tài khoản và Mật khẩu (có thể bấm biểu tượng con mắt để xem mật khẩu). Sau khi đăng nhập thành công, hệ thống sẽ **tự động chuyển hướng** đến trang làm việc tương ứng với quyền hạn của bạn.
- **Bảo mật truy cập:** Mọi đường dẫn trong hệ thống đều yêu cầu đăng nhập. Nếu chưa đăng nhập hoặc phiên làm việc hết hạn, hệ thống sẽ tự động chuyển hướng về trang Đăng nhập (`/login/`).

### 2. Đổi Mật Khẩu
- Mọi người dùng đều có thể tự đổi mật khẩu tài khoản bất kỳ lúc nào.
- Đối với nhân viên sản xuất (Cắt, May, KCS, Hoàn thiện): Nút đổi mật khẩu nằm ở góc trên thanh công cụ.
- Đối với Quản lý, Kế toán và Admin: Chức năng Đổi mật khẩu nằm ở phần chân thanh menu **Sidebar** (bên trái màn hình).

---

## II. HƯỚNG DẪN BỘ PHẬN KẾ TOÁN (Quyền KE_TOAN)

Kế toán có thanh điều hướng Sidebar riêng biệt để quản trị tài chính, đơn giá và theo dõi doanh thu xuất hàng.

### 1. Quản Lý Đơn Giá Xuất Hàng (`/accounting/don-gia/`)
- **Mục đích:** Thiết lập đơn giá bán/xuất hàng (VNĐ/cái) cho từng cặp Mã hàng và Màu sắc.
- **Cách thao tác:**
  1. Mở menu Sidebar → Chọn **Quản lý Đơn Giá**.
  2. Tại bảng danh sách Mã – Màu:
     - Gõ đơn giá trực tiếp vào ô tương ứng (hệ thống tự động định dạng dấu phẩy khi gõ, ví dụ nhập `150000` sẽ hiển thị `150,000`).
     - Bấm nút **Lưu** ở cuối dòng để cập nhật đơn giá cho dòng đó.
     - Hoặc có thể nhập đơn giá cho nhiều dòng rồi bấm nút **Lưu Tất Cả Đơn Giá** ở góc trên để cập nhật hàng loạt cùng lúc.
  3. Cột *Thời gian cập nhật* và *Người cập nhật* sẽ tự động ghi nhận lại lần sửa mới nhất.

### 2. Nhập Phiếu Xuất Hàng (`/accounting/xuat-hang/`)
- **Mục đích:** Lập phiếu khi xuất hàng đi và theo dõi tổng tiền xuất.
- **Cách thao tác:**
  1. Mở menu Sidebar → Chọn **Nhập Xuất Hàng**.
  2. Điền thông tin vào form:
     - **Ngày xuất:** Chọn ngày thực tế xuất hàng.
     - **Mã hàng & Màu sắc:** Chọn mã hàng và màu tương ứng.
     - **Số lượng xuất:** Nhập số lượng hàng xuất đi.
     - **Tính tiền tự động (Real-time):** Ngay khi chọn Mã - Màu và gõ số lượng, hệ thống sẽ tự động hiển thị **Đơn giá hiện tại** và tính ngay **Thành tiền dự tính (VNĐ)**.
     - **Ghi chú:** Điền thêm thông tin giao hàng, khách hàng, xe chở (nếu có).
  3. Bấm **Lưu Phiếu Xuất Hàng**.
  4. Lịch sử phiếu xuất sẽ xuất hiện ngay ở bảng danh sách bên cạnh. Kế toán có thể bấm **Sửa** hoặc **Xóa** phiếu xuất nếu có sai sót.

### 3. Dashboard Doanh Thu & Tồn Đọng (`/accounting/`)
- **Mục đích:** Bức tranh toàn cảnh về tiến độ xuất hàng và giá trị tiền của từng mã hàng.
- **3 Thẻ KPI trên cùng:**
  - **Tổng Giá Trị Đơn Hàng:** Tổng số lượng & tổng tiền đơn hàng khách đặt.
  - **Tổng Tiền Đã Xuất:** Doanh thu số hàng đã thực tế giao đi cùng % tiến độ hoàn thành.
  - **Giá Trị Hàng Chưa Xuất:** Tổng số lượng & tổng tiền của số hàng còn tồn đọng cần giao tiếp.
- **Bảng Chi Tiết Tiến Độ Xuất Hàng & Tồn Đọng:**
  - Hiển thị đầy đủ thông tin: *Số lượng ĐH, Đơn giá, Thành tiền ĐH, SL đã xuất, Doanh thu đã xuất, SL còn lại, Tiền còn lại, % Tiến độ*.
  - Bảng hiển thị full màn hình rộng, không cần cuộn ngang.
- **Lọc Mã Hàng:** Chọn mã hàng để xem chi tiết từng mã, có nút **Xóa lọc** tiện dụng.
- **Xuất Báo Cáo Excel:** Bấm nút **Xuất Excel** để tải về bảng kê theo dõi gồm 2 sheet (*Tổng hợp số liệu & Chi tiết từng phiếu xuất*).

### 4. Báo Cáo Tổng Hợp & Quản Lý Mã Hàng
- Kế toán có thể xem **Tổng hợp dữ liệu sản xuất** (`/dashboard/cut/`), **Theo dõi Đơn hàng** (`/tracking/`) và xem danh sách **Quản lý Mã hàng** (`/config/`) trên thanh Sidebar.

---

## III. HƯỚNG DẪN NHÂN VIÊN MAY SẢN XUẤT (Quyền BASIC)

- **Trang làm việc:** Màn hình chính (`/`).
- **Thêm Báo Cáo:**
  1. Chọn **Mã Hàng** → Chọn **Màu**.
  2. Nhập **Xưởng**, **Tổ** và **Số lượng LĐ**.
  3. Nhập số lượng các công đoạn: *Nhận BTP, Vào chuyền, Giữa chuyền, Ra chuyền, Thu hóa, Là thành phẩm, Nhập hoàn thiện*.
  4. Bấm **Lưu dữ liệu**.
- **Xem Lịch Sử:** Bấm nút **Xem danh sách đã nhập** để xem lại 50 báo cáo gần nhất do chính mình nhập.
- *Lưu ý: Công nhân không có quyền sửa/xóa sau khi đã lưu. Nếu nhập nhầm hãy báo Quản lý.*

---

## IV. HƯỚNG DẪN BỘ PHẬN TỔ CẮT (Quyền NHA_CAT)

- **Trang làm việc:** Màn hình Nhập Báo Cáo Cắt (`/cut/`).
- **Thêm Báo Cáo:**
  1. Chọn **Mã Hàng** → Chọn **Màu**.
  2. Nhập số lượng các công đoạn: **Cắt chính, Cắt lót, Cắt Mex, Cắt bông**.
  3. Bấm **Lưu dữ liệu**. *(Không cần nhập Xưởng/Tổ).*
- **Xem Lịch Sử:** Bấm **Xem danh sách đã nhập** để xem 50 báo cáo mới nhất.

---

## V. HƯỚNG DẪN BỘ PHẬN KCS (Quyền KCS)

- **Trang làm việc:** Màn hình Nhập Báo Cáo KCS (`/kcs/`).
- **Thêm Báo Cáo:**
  1. Chọn **Mã Hàng** → Chọn **Màu**.
  2. Nhập **Xưởng**, **Tổ**.
  3. Nhập số liệu kiểm tra chất lượng: **Qua tay, Đạt, Lỗi, Tổng đạt**.
  4. Bấm **Lưu dữ liệu**.
- **Xem Lịch Sử:** Bấm **Xem danh sách đã nhập** để xem 50 bản ghi gần nhất.

---

## VI. HƯỚNG DẪN BỘ PHẬN HOÀN THIỆN (Quyền HOAN_THIEN)

- **Trang làm việc:** Màn hình Nhập Báo Cáo Hoàn Thiện (`/finishing/`).
- **Thao tác sản lượng chuẩn:**
  1. Chọn **Mã Hàng** → Chọn **Màu**.
  2. Nhập số lượng: **Thẻ bài, Gấp hàng, Treo/Đóng thùng**.
  3. Bấm **Lưu dữ liệu**.
- **Nghiệp Vụ Ngoại Lệ (Trả hàng lỗi & Lấy mẫu) (`/finishing/ngoai-le/`):**
  - Ghi nhận số lượng xuất trả về các tổ may để sửa lỗi hoặc đưa đi lấy mẫu kiểm định.
  - **Theo dõi nhận lại từng lần:** Bấm vào phiếu để nhập số lượng nhận lại sau khi tổ may đã sửa xong.
  - Hệ thống tự động tính lũy kế số lượng đã nhận lại và số lượng còn thiếu. Khi đã nhận đủ 100%, bản ghi sẽ tự động được ẩn khỏi danh sách chờ.

---

## VII. HƯỚNG DẪN CẤP QUẢN LÝ (Quyền QUAN_LY)

Quản lý xưởng có toàn quyền theo dõi và giám sát tiến độ toàn bộ các khâu trên thanh Sidebar:

### 1. Dashboard Tổng Hợp Sản Xuất (`/dashboard/`)
- Gồm 4 Tab: **Tổng hợp Cắt** (`/dashboard/cut/`) → **Tổng hợp May** (`/dashboard/prod/`) → **Tổng hợp KCS** (`/dashboard/kcs/`) → **Tổng hợp Hoàn thiện** (`/dashboard/finishing/`).
- **Quy tắc ô Ngày / Tổng:** Hiển thị sản lượng ngày và tổng lũy kế tính đến thời điểm ghi nhận.
- **Bộ lọc dạng Excel trên cột:** Bấm `[▼]` tại các cột *Người nhập, Mã hàng, Màu, Xưởng, Tổ* để tìm kiếm và lọc dữ liệu đa tầng.
- **Bộ lọc ngày độc lập & Xuất Excel:** Lọc khoảng thời gian và tải file Excel tổng hợp trực tiếp.

### 2. Quản Lý & Điều Chỉnh Dữ Liệu
- Quản lý có quyền **Sửa** hoặc **Xóa** bất kỳ báo cáo nào của nhân viên từ cả 4 quy trình sản xuất khi có sai sót.

### 3. Cấu Hình Mã Hàng (`/config/`)
- Thêm Mã hàng mới, thêm danh sách Màu sắc và Số lượng đơn hàng khách đặt.
- Chỉnh sửa số lượng hoặc xóa màu/mã hàng khi cần thiết.

### 4. Tracking Đơn Hàng (`/tracking/`)
- Xem tiến độ xuyên suốt của từng mã hàng từ Cắt ➔ May ➔ KCS ➔ Hoàn thiện ➔ Xuất hàng và xuất Excel theo dõi.

---

## VIII. HƯỚNG DẪN QUẢN TRỊ VIÊN ADMIN (Quyền PREMIUM)

Tài khoản `PREMIUM` là quản trị cấp cao nhất, nắm toàn quyền điều hành hệ thống:

1. **Xem toàn bộ Dashboard & Báo Cáo:** Xem được cả Dashboard Sản Xuất (`/dashboard/`), Dashboard Kế Toán Doanh Thu (`/accounting/`) và Tracking Đơn Hàng (`/tracking/`).
2. **Quản Lý Người Dùng (`/manage-accounts/`):**
   - **Phê duyệt:** Kích hoạt tài khoản mới đăng ký.
   - **Phân quyền:** Chuyển đổi vai trò của người dùng sang *Sản xuất, Nhà cắt, KCS, Hoàn thiện, Kế toán, Quản lý, hoặc Admin*.
   - **Khóa / Mở khóa:** Vô hiệu hóa hoặc cấp lại quyền đăng nhập.
   - **Xóa tài khoản:** Xóa vĩnh viễn tài khoản không còn làm việc.
3. **Quản trị Cấu hình & Đơn giá:** Cùng với Kế toán quản trị danh mục sản phẩm, màu sắc và bảng đơn giá toàn công ty.
