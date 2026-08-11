---
name: django-add-new-role-checklist
description: >-
  Checklist and common pitfalls to avoid when adding a new user role (like KCS, Hoàn thiện, Nhà cắt) and its associated models, views, and templates in this Django Process Monitoring project.
---

# Django Add New Role & Department Master Checklist

## Overview
Tài liệu hướng dẫn và danh sách kiểm tra toàn diện các bước cần làm khi tạo một Role (vai trò/bộ phận) mới trong hệ thống Quản lý Tiến độ Sản xuất (Process Monitoring). Tài liệu này được đúc kết từ toàn bộ các lỗi thực tế đã gặp phải trong quá trình tạo role KCS và Nhà cắt (`NHA_CAT`).

---

## 📋 WORKFLOW CHUẨN KHI THÊM ROLE MỚI

### 1. Database & Models (`models.py`)
- [ ] Thêm mã vai trò vào `AppUser.ROLE_CHOICES` (ví dụ `("NHA_CAT", "Nhà cắt")`).
- [ ] Tạo Model báo cáo mới (ví dụ `CutReport`):
  - Kế thừa đúng các trường cơ bản: `ngay_lam_viec`, `ma_hang`, `mau`, `size`, các trường số lượng của công đoạn (`PositiveIntegerField(default=0)`).
  - Khóa ngoại `nguoi_nhap = models.ForeignKey("AppUser", on_delete=models.PROTECT, related_name="...")`.
  - Timestamp: `created_at` (auto_now_add=True) và `updated_at` (auto_now=True).
- [ ] Đăng ký Model trong `admin.py`.
- [ ] Chạy lệnh migration: `python manage.py makemigrations` và `python manage.py migrate`.

---

### 2. Forms (`forms.py`)
- [ ] Tạo Form nhập liệu tương ứng (ví dụ `CutForm(forms.Form)`).
- [ ] Đảm bảo khởi tạo `__init__` nạp cấu hình `self.config = load_config()` để populate choices cho `ma_hang` và `mau`.
- [ ] Hàm `clean()` kiểm tra tính hợp lệ của `ma_hang` và `mau` theo cấu hình.
- [ ] Gán widget `forms.NumberInput(attrs=NUMERIC_FIELD_ATTRS)` cho các trường số.

---

### 3. Views (`views.py`)
- [ ] **Import đầy đủ ở đầu file:** Luôn thêm Model và Form mới vào dòng `from .models import ...` và `from .forms import ...` ở đầu file `views.py` (tránh `NameError`).
- [ ] **Đăng nhập (`login_view`):** Thêm nhánh điều hướng sau đăng nhập:
  ```python
  elif user.role == "NHA_CAT":
      return redirect("cut_web")
  ```
  *(Nếu quên, user sẽ bị điều hướng sang trang `web_view` và dính lỗi 403 Forbidden).*
- [ ] **Đăng ký (`register_view`):** Thêm role mới vào danh sách role hợp lệ:
  ```python
  elif role not in ["BASIC", "HOAN_THIEN", "KCS", "NHA_CAT", "QUAN_LY"]:
  ```
- [ ] **Tạo đủ 5 view chức năng cho Role mới:**
  1. `[role]_web_view`: Nhập liệu. **Bắt buộc truyền `"config": load_config()`** vào context để JavaScript cascade dropdown hoạt động.
  2. `[role]_list_view`: Xem danh sách dữ liệu của chính mình (hoặc toàn bộ nếu là Admin/Quản lý).
  3. `[role]_edit_view`: Sửa dữ liệu. **Bắt buộc truyền `"config": load_config()`** vào context. Điều hướng về `premium_dashboard` nếu là Admin/Quản lý, ngược lại về `[role]_list`.
  4. `[role]_delete_report_view`: Xóa dữ liệu (chỉ người tạo hoặc Admin/Quản lý). Điều hướng về `premium_dashboard` nếu là Admin/Quản lý.
  5. `[role]_export_excel_view`: Xuất Excel theo bộ lọc ngày (`start_date`, `end_date`). Cấp quyền cho cả Role đó, `QUAN_LY` và `PREMIUM`.
- [ ] **Kiểm tra quyền truy cập:** Mọi view nhập/sửa/xóa của bộ phận đều phải cho phép: `[NEW_ROLE, 'PREMIUM', 'QUAN_LY']`.
- [ ] **Cập nhật `premium_dashboard_view`:**
  - Lấy tham số lọc ngày riêng (ví dụ `cut_start_date`, `cut_end_date`).
  - Queryset riêng (ví dụ `cut_qs`).
  - Tính tổng các chỉ số cho từng (Mã hàng, Màu) qua `annotate(Sum(...))`.
  - Phân trang riêng biệt (ví dụ `p4` qua `cut_paginator = Paginator(cut_rows, 20)`).
  - Truyền đầy đủ vào context trả về template.

---

### 4. Routing & URLs (`urls.py`)
- [ ] Khai báo đủ 5 đường dẫn:
  - `path("[role]/", views.[role]_web_view, name="[role]_web")`
  - `path("[role]/list/", views.[role]_list_view, name="[role]_list")`
  - `path("[role]/edit/<int:row_id>/", views.[role]_edit_view, name="[role]_edit")`
  - `path("[role]/delete/<int:row_id>/", views.[role]_delete_report_view, name="[role]_delete_report")`
  - `path("[role]/export-excel/", views.[role]_export_excel_view, name="[role]_export_excel")`

---

### 5. Templates HTML & Giao diện
- [ ] **Tạo 3 template riêng cho Role:** `[role]_web.html`, `[role]_list.html`, `[role]_edit.html`.
  - Chú ý: Ở template nhập liệu và sửa, thẻ JSON config phải viết đúng chuẩn:
    ```html
    {{ config|json_script:"config-data" }}
    ```
- [ ] **Trang Đăng ký (`register.html`):** Thêm `<option value="NHA_CAT">Nhà cắt</option>` vào `<select id="role">`.
- [ ] **Trang Quản lý tài khoản (`manage_accounts.html`):** Thêm `<option value="NHA_CAT">Nhà cắt</option>` vào cả 2 dropdown phân quyền (bản Desktop và Mobile).
- [ ] **Trang Dashboard (`premium_dashboard.html`):**
  - **Menu Top-bar:** Thêm nút "+ Nhập DL [Tên role]" cho `QUAN_LY` và `PREMIUM`.
  - **Bảng tổng hợp mới:** Thêm thẻ `<div class="card">` chứa bảng tổng hợp của role mới.
  - **Đồng bộ Form Lọc & Xóa:** Trong form lọc của TẤT CẢ các bảng, phải chứa đủ các trường hidden của các bảng còn lại để không làm mất bộ lọc và phân trang của nhau khi bấm Lọc hoặc Xóa.
  - **Đồng bộ Phân trang:** Các link Đầu/Trước/Sau/Cuối phải nối đủ tham số phân trang (`p1`, `p2`, `p3`, `p4`) và bộ lọc ngày của toàn bộ các bảng.
  - **Hỗ trợ Mobile:** Tạo thêm `<div class="card-list">` để hiển thị đẹp mắt trên màn hình nhỏ.

---

## ⚠️ DANH SÁCH CÁC LỖI THỰC TẾ & CÁCH PHÒNG TRÁNH (LESSONS LEARNED)

| STT | Lỗi đã gặp | Nguyên nhân gốc rễ | Giải pháp chuẩn |
|---|---|---|---|
| **1** | `NameError: name 'CutReport' is not defined` | Quên import Model/Form mới ở đầu file `views.py`. | Luôn import Model/Form mới vào đầu file `views.py` ngay khi tạo xong. |
| **2** | Đăng nhập bị lỗi `403 Forbidden` | `login_view` chỉ redirect cho các role cũ, role mới bị rơi vào mặc định `redirect("web")` mà `web_view` lại chặn role mới. | Luôn bổ sung nhánh `elif user.role == "NEW_ROLE": return redirect("new_role_web")` trong `login_view`. |
| **3** | Không chọn được Mã hàng & Màu sắc ở form nhập liệu | `views.py` quên truyền `"config": load_config()` vào `context` của `render()`, khiến `cascade_select.js` không đọc được JSON cấu hình. | Bắt buộc truyền `"config": load_config()` ở cả 2 view: `[role]_web_view` và `[role]_edit_view`. |
| **4** | Không có role mới khi Đăng ký / Phân quyền | Quên thêm `<option>` vào `register.html`, `manage_accounts.html` và danh sách role ở `register_view`. | Cập nhật đồng bộ cả 3 vị trí: `register.html`, `manage_accounts.html`, và hàm `register_view`. |
| **5** | Quản lý không thấy nút nhập liệu bộ phận mới | `premium_dashboard.html` chỉ để nút cho Sản xuất và Hoàn thiện, thiếu KCS và Cắt. | Bổ sung đầy đủ các nút nhập liệu cho Quản lý / Admin trên top-bar Dashboard. |
| **6** | Lọc bảng này làm mất lọc / phân trang của bảng kia | Các form lọc GET thiếu các thẻ `<input type="hidden">` lưu trữ tham số ngày và số trang của các bảng khác. | Mỗi form lọc và link phân trang phải chứa đủ tham số của tất cả các bảng trong Dashboard. |
| **7** | `TemplateSyntaxError` (Unclosed tag) | VS Code Auto-formatter tự động bẻ đôi các thẻ template Django `{% if %}` hoặc `{{ variable }}` thành nhiều dòng. | Đảm bảo block tag và in biến nằm trọn vẹn trên 1 dòng duy nhất, không dùng auto-formatter ẩu với file HTML Django. |
| **8** | Xuất Excel không lọc theo khoảng ngày | View `export_excel` không bắt `start_date` / `end_date` từ GET request. | Luôn lấy `request.GET.get('start_date')` và áp dụng `.filter(created_at__date__gte=...)`. |
| **9** | Cột Tổng trên Dashboard hiển thị sai | Dùng `Model.objects.all().annotate()` thay vì QuerySet đã lọc (`qs.values().annotate()`). | Luôn tính toán tổng dựa trên QuerySet đã qua xử lý lọc. |
