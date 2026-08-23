# HƯỚNG DẪN SỬ DỤNG HỆ THỐNG QUẢN LÝ TIẾN ĐỘ SẢN XUẤT, KHO & KẾ TOÁN

Chào mừng bạn đến với Hệ thống Quản lý và Giám sát Tiến độ **Cắt – May Sản Xuất – KCS – Hoàn Thiện – Kho Vật Tư & Kế Toán Tài Chính**. Hệ thống được thiết kế tối ưu trên cả máy tính lẫn điện thoại di động, phân chia thành **8 vai trò (Role)** với các quyền hạn độc lập nhằm bảo mật thông tin và tối ưu thao tác công việc.

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
- Đối với Quản lý, Kế toán, Thủ kho và Admin: Chức năng Đổi mật khẩu nằm ở phần chân thanh menu **Sidebar** (bên trái màn hình).

---

## II. HƯỚNG DẪN BỘ PHẬN KẾ TOÁN (Quyền KE_TOAN)

Kế toán có thanh điều hướng Sidebar riêng biệt để quản trị tài chính, đơn giá và theo dõi doanh thu.

### 1. Quản Lý Đơn Giá Xuất Hàng (`/accounting/don-gia/`)
- **Mục đích:** Thiết lập đơn giá (VNĐ/cái) cho từng cặp Mã hàng và Màu sắc.
- **Cách thao tác:**
  1. Mở menu Sidebar → Chọn **Quản lý Đơn Giá**.
  2. Tại bảng danh sách Mã – Màu:
     - Gõ đơn giá trực tiếp vào ô tương ứng (hệ thống tự động định dạng dấu phẩy khi gõ, ví dụ nhập `150000` sẽ hiển thị `150,000`).
     - Bấm nút **Lưu** ở cuối dòng để cập nhật đơn giá cho dòng đó.
     - Hoặc có thể nhập đơn giá cho nhiều dòng rồi bấm nút **Lưu Tất Cả Đơn Giá** ở góc trên để cập nhật hàng loạt cùng lúc.
  3. Cột *Thời gian cập nhật* và *Người cập nhật* sẽ tự động ghi nhận lại lần sửa mới nhất.

### 2. Báo Cáo Doanh Thu Tổ / Xưởng Theo Ngày (`/accounting/bao-cao-to-xuong/`)
- **Mục đích:** Tính toán chính xác số tiền làm được của từng tổ / xưởng theo từng ngày dựa trên sản lượng hàng ra chuyền nhân với đơn giá.
- **Công thức:**
  $$\text{Doanh thu} = \sum (\text{Số lượng hàng Ra Chuyền} \times \text{Đơn giá mã hàng/màu})$$
- **Tính năng nổi bật:**
  - **Tự động tính theo tháng:** Mặc định hệ thống tự động tổng hợp từ **ngày 01 của tháng hiện tại đến ngày hôm nay**. Sang tháng mới, hệ thống tự động reset về 0 cho tháng mới.
  - **Nút chọn nhanh tháng:** Bấm **"Tháng này"** hoặc **"Tháng trước"** trên thanh công cụ để xem số liệu từng kỳ kế toán chỉ với 1 click.
  - **Thanh lọc siêu gọn:** Đầy đủ các tiêu chí lọc (*Từ ngày, Đến ngày, Xưởng, Tổ, Mã hàng*) nằm gọn trên 1 dòng duy nhất.
  - **4 Thẻ KPI thống kê đầu trang:**
    - 💰 *Tổng Doanh Thu Làm Được (VNĐ)*
    - 📦 *Tổng Hàng Ra Chuyền (Cái)*
    - 🏭 *Quy Mô Sản Xuất (Số tổ tham gia & Số ca tổ/ngày)*
    - 📈 *Bình Quân Tiền / Ngày (VNĐ/ngày)*
  - **3 Tab xem linh hoạt:**
    1. **📋 Chi Tiết Theo Ngày & Tổ:** Hiển thị từng ca làm việc của tổ trong ngày với bảng chi tiết từng mã/màu. Phân trang chuẩn **5 ca/trang** kèm thanh chuyển trang tiện lợi.
    2. **🏭 Tổng Hợp Theo Tổ / Xưởng:** Bảng tổng kết số ngày làm việc, số mã hàng, tổng sản lượng, tổng tiền và doanh thu bình quân/ngày của từng tổ trong tháng.
    3. **📅 Tổng Hợp Theo Ngày:** Thống kê sản lượng và dòng tiền ra chuyền của toàn nhà máy theo từng ngày.
  - **Xuất Báo Cáo Excel Đa Sheet:** Bấm nút **Xuất Excel** để tải về file Excel `.xlsx` gồm **3 Sheet chuẩn hóa** (*Chi Tiết Ngày & Tổ*, *Tổng Hợp Tổ Xưởng*, *Tổng Hợp Theo Ngày*) có định dạng số tiền và đường viền chuyên nghiệp.

### 3. Nhập Phiếu Xuất Hàng (`/accounting/xuat-hang/`)
- **Mục đích:** Lập phiếu khi xuất hàng đi và theo dõi tổng tiền xuất.
- **Cách thao tác:**
  1. Mở menu Sidebar → Chọn **Nhập Xuất Hàng**.
  2. Điền thông tin vào form: Ngày xuất, Mã hàng, Màu sắc, Số lượng xuất, Ghi chú.
  3. **Tính tiền tự động (Real-time):** Ngay khi chọn Mã - Màu và gõ số lượng, hệ thống sẽ tự động hiển thị **Đơn giá hiện tại** và tính ngay **Thành tiền dự tính (VNĐ)**.
  4. Bấm **Lưu Phiếu Xuất Hàng**. Lịch sử phiếu xuất có thể bấm **Sửa** hoặc **Xóa** nếu cần.

### 4. Dashboard Doanh Thu & Tồn Đọng (`/accounting/`)
- **Mục đích:** Bức tranh toàn cảnh về tiến độ xuất hàng và giá trị tiền của từng mã hàng (Tổng giá trị đơn hàng, Tổng tiền đã xuất, Giá trị hàng chưa xuất).
- Bấm **Xuất Excel** để tải về bảng kê theo dõi gồm 2 sheet.

---

## III. HƯỚNG DẪN BỘ PHẬN KHO NGUYÊN VẬT LIỆU (Quyền KHO)

Thủ kho có giao diện Sidebar chuyên dụng để quản lý toàn bộ vòng đời vật tư trong nhà máy.

### 1. Nhập Kho Nguyên Vật Liệu (`/inventory/nhap/`)
- **Cách thao tác:**
  1. Mở menu Sidebar → Chọn **Nhập Kho**.
  2. Điền thông tin: Ngày nhập, Mã hàng, Màu sắc, Tên vật tư (Vải chính, Vải lót, Mex, Chỉ may, Khóa kéo, Cúc...), Đơn vị tính (Cuộn, Kg, Chiếc, Mét...), Số lượng kiện, Số lượng chi tiết.
  3. Bấm **Lưu Phiếu Nhập**.

### 2. Xem Lịch Sử Nhập / Xuất Kho
- **Lịch sử nhập kho (`/inventory/lich-su-nhap/`):** Xem danh sách tất cả các phiếu nhập, phân trang 20 dòng/trang, có quyền Sửa/Xóa phiếu nhập.
- **Lịch sử xuất kho (`/inventory/lich-su-xuat/`):** Xem chi tiết các lần xuất kho vật tư cho các bộ phận sản xuất.

### 3. Bảng Tổng Hợp Tồn Kho Vật Tư (`/inventory/tong-hop/`)
- Theo dõi số lượng Nhập – Xuất – Tồn kho của từng mã vật tư.
- Hỗ trợ thao tác **Xuất kho nhanh** trực tiếp từ bảng tồn kho.

---

## IV. HƯỚNG DẪN NHÂN VIÊN MAY SẢN XUẤT (Quyền BASIC)

- **Trang làm việc:** Màn hình chính (`/`).
- **Thao tác nhập báo cáo:**
  1. Chọn **Mã Hàng** → Chọn **Màu**.
  2. Nhập **Xưởng**, **Tổ** và **Số lượng LĐ**.
  3. Nhập số lượng các công đoạn: *Nhận BTP, Vào chuyền, Giữa chuyền, Ra chuyền, Thu hóa, Là thành phẩm, Nhập hoàn thiện*.
  4. Bấm **Lưu dữ liệu**.
- **Xem Lịch Sử:** Bấm nút **Xem danh sách đã nhập** để xem lại 50 báo cáo gần nhất do chính mình nhập.

---

## V. HƯỚNG DẪN BỘ PHẬN TỔ CẮT (Quyền NHA_CAT)

- **Trang làm việc:** Màn hình Nhập Báo Cáo Cắt (`/cut/`).
- **Thao tác nhập báo cáo:**
  1. Chọn **Mã Hàng** → Chọn **Màu**.
  2. Nhập số lượng các công đoạn: **Cắt chính, Cắt lót, Cắt Mex, Cắt bông**.
  3. Bấm **Lưu dữ liệu**.
- **Xem Lịch Sử:** Bấm **Xem danh sách đã nhập** để xem 50 báo cáo mới nhất.

---

## VI. HƯỚNG DẪN BỘ PHẬN KCS (Quyền KCS)

- **Trang làm việc:** Màn hình Nhập Báo Cáo KCS (`/kcs/`).
- **Thao tác nhập báo cáo:**
  1. Chọn **Mã Hàng** → Chọn **Màu**.
  2. Nhập **Xưởng**, **Tổ**.
  3. Nhập số liệu kiểm tra chất lượng: **Qua tay, Đạt, Lỗi, Tổng đạt**.
  4. Bấm **Lưu dữ liệu**.
- **Xem Lịch Sử:** Bấm **Xem danh sách đã nhập** để xem 50 bản ghi gần nhất.

---

## VII. HƯỚNG DẪN BỘ PHẬN HOÀN THIỆN (Quyền HOAN_THIEN)

- **Trang làm việc:** Màn hình Nhập Báo Cáo Hoàn Thiện (`/finishing/`).
- **Thao tác sản lượng chuẩn:**
  1. Chọn **Mã Hàng** → Chọn **Màu**.
  2. Nhập số lượng: **Thẻ bài, Gấp hàng, Treo/Đóng thùng**.
  3. Bấm **Lưu dữ liệu**.
- **Nghiệp Vụ Ngoại Lệ (Trả hàng lỗi & Lấy mẫu) (`/finishing/ngoai-le/`):**
  - Ghi nhận số lượng xuất trả về các tổ may để sửa lỗi hoặc đưa đi lấy mẫu kiểm định.
  - **Theo dõi nhận lại từng lần:** Bấm vào phiếu để nhập số lượng nhận lại sau khi tổ may đã sửa xong.
  - Tự động tính lũy kế và tự động ẩn khỏi danh sách chờ khi đã nhận đủ 100%.

---

## VIII. HƯỚNG DẪN CẤP QUẢN LÝ (Quyền QUAN_LY)

Quản lý xưởng có toàn quyền theo dõi và giám sát tiến độ toàn bộ các khâu trên thanh Sidebar:

### 1. Dashboard Tổng Hợp Sản Xuất (`/dashboard/`)
- Gồm 4 Tab: **Tổng hợp Cắt** (`/dashboard/cut/`) → **Tổng hợp May** (`/dashboard/prod/`) → **Tổng hợp KCS** (`/dashboard/kcs/`) → **Tổng hợp Hoàn thiện** (`/dashboard/finishing/`).
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

## IX. HƯỚNG DẪN QUẢN TRỊ VIÊN ADMIN (Quyền PREMIUM)

Tài khoản `PREMIUM` là quản trị cấp cao nhất, nắm toàn quyền điều hành hệ thống:

1. **Xem toàn bộ Dashboard & Báo Cáo:** Xem được Dashboard Sản Xuất (`/dashboard/`), Dashboard Doanh Thu Xuất Hàng (`/accounting/`), Báo Cáo Doanh Thu Tổ/Xưởng (`/accounting/bao-cao-to-xuong/`), Kho Vật Tư (`/inventory/tong-hop/`) và Tracking Đơn Hàng (`/tracking/`).
2. **Quản Lý Người Dùng (`/manage-accounts/`):**
   - **Phê duyệt:** Kích hoạt tài khoản mới đăng ký.
   - **Phân quyền:** Chuyển đổi vai trò của người dùng sang *Sản xuất, Nhà cắt, KCS, Hoàn thiện, Kho, Kế toán, Quản lý, hoặc Admin*.
   - **Khóa / Mở khóa:** Vô hiệu hóa hoặc cấp lại quyền đăng nhập.
   - **Xóa tài khoản:** Xóa vĩnh viễn tài khoản không còn làm việc.
3. **Quản trị Cấu hình & Đơn giá:** Cùng với Kế toán quản trị danh mục sản phẩm, màu sắc và bảng đơn giá toàn công ty.
