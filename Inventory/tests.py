import datetime
from django.test import TestCase, Client
from django.urls import reverse
from django.template.loader import render_to_string
from Working.models import AppUser, Product, ProductColor
from Inventory.models import MaterialReceipt, MaterialIssue
from Inventory.forms import MaterialReceiptForm, MaterialIssueForm
from Inventory.views import (
    get_inventory_summary_data,
    _clean_options,
    parse_date_range,
    _get_cascade_options,
)


class InventoryComprehensiveTests(TestCase):
    def setUp(self):
        self.client = Client(HTTP_HOST='127.0.0.1')

        # 1. Khởi tạo người dùng các role
        self.premium_user = AppUser.objects.create(
            account="admin_vip", password="123", name="Quản Trị Viên", role="PREMIUM", is_approved=True
        )
        self.quanly_user = AppUser.objects.create(
            account="manager_user", password="123", name="Quản Lý", role="QUAN_LY", is_approved=True
        )
        self.kho_user = AppUser.objects.create(
            account="kho_staff", password="123", name="Thủ Kho", role="KHO", is_approved=True
        )
        self.ketoan_user = AppUser.objects.create(
            account="ketoan_staff", password="123", name="Kế Toán", role="KE_TOAN", is_approved=True
        )
        self.basic_user = AppUser.objects.create(
            account="staff_prod", password="123", name="NV Sản Xuất", role="BASIC", is_approved=True
        )
        self.unapproved_user = AppUser.objects.create(
            account="newbie", password="123", name="NV Mới", role="BASIC", is_approved=False
        )

        # 2. Khởi tạo cấu hình mã hàng & màu
        self.product_at1 = Product.objects.create(name="AT1")
        self.color_black = ProductColor.objects.create(product=self.product_at1, name="Đen", quantity=500)
        self.color_white = ProductColor.objects.create(product=self.product_at1, name="Trắng", quantity=300)

        self.product_at2 = Product.objects.create(name="AT2")
        self.color_red = ProductColor.objects.create(product=self.product_at2, name="Đỏ", quantity=200)

        # 3. Tạo sẵn một số dữ liệu nhập và xuất
        self.receipt1 = MaterialReceipt.objects.create(
            ngay_nhap=datetime.date(2026, 8, 1),
            ma_hang="AT1",
            mau="Đen",
            ten_vat_tu="Vải chính",
            so_luong_kien=10,
            so_luong=100.5,
            don_vi="m",
            nguoi_nhap=self.kho_user
        )
        self.receipt2 = MaterialReceipt.objects.create(
            ngay_nhap=datetime.date(2026, 8, 2),
            ma_hang="AT1",
            mau="Đen",
            ten_vat_tu="Vải lót",
            so_luong_kien=5,
            so_luong=50.0,
            don_vi="y",
            nguoi_nhap=self.kho_user
        )
        self.issue1 = MaterialIssue.objects.create(
            receipt=self.receipt1,
            ngay_xuat=datetime.date(2026, 8, 3),
            ma_hang="AT1",
            mau="Đen",
            ten_vat_tu="Vải chính",
            so_luong_kien=3,
            so_luong=30.0,
            don_vi="m",
            nguoi_nhan="NV Sản Xuất",
            nguoi_xuat=self.kho_user
        )

    def _login(self, user):
        from django.conf import settings
        session = self.client.session
        session['user_id'] = user.id
        session['display_name'] = user.name
        session.save()
        self.client.cookies[settings.SESSION_COOKIE_NAME] = session.session_key

    # ==============================================================================
    # 1. MODEL & SUMMARY CALCULATION LOGIC TESTS
    # ==============================================================================
    def test_model_str_and_relationships(self):
        """Kiểm tra __str__ và quan hệ của MaterialReceipt & MaterialIssue"""
        self.assertIn("AT1", str(self.receipt1))
        self.assertIn("Vải chính", str(self.receipt1))
        self.assertIn("100.5 m", str(self.receipt1))
        self.assertEqual(self.receipt1.nguoi_nhap, self.kho_user)

        self.assertIn("AT1", str(self.issue1))
        self.assertIn("30.0 m", str(self.issue1))
        self.assertEqual(self.issue1.nguoi_nhan, "NV Sản Xuất")
        self.assertEqual(self.issue1.nguoi_xuat, self.kho_user)
        self.assertEqual(self.issue1.receipt, self.receipt1)

    def test_summary_calculation_and_grouping(self):
        """Kiểm tra logic tổng hợp tồn kho, tính Thực nhận - Thực xuất - Còn lại"""
        summary = get_inventory_summary_data()
        self.assertEqual(len(summary), 2)  # AT1-Đen-Vải chính (m) và AT1-Đen-Vải lót (y)

        # Tìm dòng Vải chính
        row_main = next(r for r in summary if r["ten_vat_tu"] == "Vải chính")
        self.assertEqual(row_main["nhap_kien"], 10)
        self.assertEqual(row_main["nhap_so_luong"], 100.5)
        self.assertEqual(row_main["don_vi"], "m")
        self.assertEqual(row_main["xuat_kien"], 3)
        self.assertEqual(row_main["xuat_so_luong"], 30.0)
        self.assertEqual(row_main["con_lai_kien"], 7)
        self.assertEqual(row_main["con_lai_so_luong"], 70.5)

        # Tìm dòng Vải lót (chưa xuất lần nào)
        row_lining = next(r for r in summary if r["ten_vat_tu"] == "Vải lót")
        self.assertEqual(row_lining["nhap_kien"], 5)
        self.assertEqual(row_lining["xuat_kien"], 0)
        self.assertEqual(row_lining["con_lai_kien"], 5)
        self.assertEqual(row_lining["con_lai_so_luong"], 50.0)
        self.assertEqual(row_lining["don_vi"], "y")

    def test_summary_filters(self):
        """Kiểm tra lọc bảng tổng hợp theo mã hàng, màu, tên vật tư, đơn vị"""
        res_ma = get_inventory_summary_data(filter_ma_hang=["AT1"])
        self.assertEqual(len(res_ma), 2)

        res_none = get_inventory_summary_data(filter_ma_hang=["AT_NON_EXISTENT"])
        self.assertEqual(len(res_none), 0)

        res_vt = get_inventory_summary_data(filter_ten_vat_tu=["Vải chính"])
        self.assertEqual(len(res_vt), 1)
        self.assertEqual(res_vt[0]["ten_vat_tu"], "Vải chính")

        res_dv = get_inventory_summary_data(filter_don_vi=["m"])
        self.assertEqual(len(res_dv), 1)
        self.assertEqual(res_dv[0]["don_vi"], "m")

    def test_helpers_clean_options_and_date_range(self):
        """Kiểm tra các hàm helper lọc Excel và parse ngày"""
        opts = _clean_options([" 10 ", "2", "1", "10", None, "   ", "Đỏ", "Xanh"])
        self.assertEqual(opts, ["1", "2", "10", "Xanh", "Đỏ"])

        s, e = parse_date_range("2026-08-01", "2026-08-15")
        self.assertEqual(s, datetime.date(2026, 8, 1))
        self.assertEqual(e, datetime.date(2026, 8, 15))

        s_bad, e_bad = parse_date_range("invalid-date", "")
        self.assertIsNone(s_bad)
        self.assertIsNone(e_bad)

    # ==============================================================================
    # 2. RECEIPT FORM & ENTRY TESTS (INCLUDING UNIT VALIDATION)
    # ==============================================================================
    def test_receipt_form_validation_and_unit(self):
        """Kiểm tra form nhập kho hợp lệ và không hợp lệ (bao gồm đơn vị chiếc)"""
        # 1. Hợp lệ với đơn vị mét (cho phép số thập phân)
        form_m = MaterialReceiptForm(data={
            "ngay_nhap": "2026-08-19",
            "ma_hang": "AT1",
            "mau": "Đen",
            "ten_vat_tu": "Chỉ may",
            "so_luong_kien": 20,
            "don_vi": "m",
            "so_luong": 200.5,
        })
        self.assertTrue(form_m.is_valid())

        # 2. Hợp lệ với đơn vị chiếc (số nguyên dương)
        form_chiec_valid = MaterialReceiptForm(data={
            "ngay_nhap": "2026-08-19",
            "ma_hang": "AT1",
            "mau": "Đen",
            "ten_vat_tu": "Cúc áo",
            "so_luong_kien": 1,
            "don_vi": "chiếc",
            "so_luong": 50,
        })
        self.assertTrue(form_chiec_valid.is_valid())

        # 3. Không hợp lệ với đơn vị chiếc (số thập phân)
        form_chiec_float = MaterialReceiptForm(data={
            "ngay_nhap": "2026-08-19",
            "ma_hang": "AT1",
            "mau": "Đen",
            "ten_vat_tu": "Cúc áo",
            "so_luong_kien": 1,
            "don_vi": "chiếc",
            "so_luong": 50.5,
        })
        self.assertFalse(form_chiec_float.is_valid())
        self.assertIn("so_luong", form_chiec_float.errors)

        # 4. Không hợp lệ với đơn vị chiếc (số âm hoặc 0)
        form_chiec_zero = MaterialReceiptForm(data={
            "ngay_nhap": "2026-08-19",
            "ma_hang": "AT1",
            "mau": "Đen",
            "ten_vat_tu": "Cúc áo",
            "so_luong_kien": 1,
            "don_vi": "chiếc",
            "so_luong": 0,
        })
        self.assertFalse(form_chiec_zero.is_valid())
        self.assertIn("so_luong", form_chiec_zero.errors)

        # 5. Sai mã hàng
        form_invalid_ma = MaterialReceiptForm(data={
            "ngay_nhap": "2026-08-19",
            "ma_hang": "KHONG_TON_TAI",
            "mau": "Đen",
            "ten_vat_tu": "Vải",
            "so_luong_kien": 1,
            "don_vi": "m",
            "so_luong": 10.0,
        })
        self.assertFalse(form_invalid_ma.is_valid())
        self.assertIn("ma_hang", form_invalid_ma.errors)

        # 6. Sai màu so với mã hàng (AT2 chỉ có Đỏ, không có Đen)
        form_invalid_color = MaterialReceiptForm(data={
            "ngay_nhap": "2026-08-19",
            "ma_hang": "AT2",
            "mau": "Đen",
            "ten_vat_tu": "Vải",
            "so_luong_kien": 1,
            "don_vi": "m",
            "so_luong": 10.0,
        })
        self.assertFalse(form_invalid_color.is_valid())
        self.assertIn("mau", form_invalid_color.errors)

    def test_receipt_web_view_post_and_redirect(self):
        """Thủ kho POST nhập nguyên liệu thành công và chuyển hướng tới tổng hợp kho"""
        self._login(self.kho_user)
        res = self.client.post(reverse("inventory_receipt_web"), {
            "ngay_nhap": "2026-08-19",
            "ma_hang": "AT1",
            "mau": "Trắng",
            "ten_vat_tu": "Khóa kéo",
            "so_luong_kien": 15,
            "don_vi": "chiếc",
            "so_luong": 150,
        })
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, reverse("inventory_summary"))
        created = MaterialReceipt.objects.filter(ten_vat_tu="Khóa kéo").first()
        self.assertIsNotNone(created)
        self.assertEqual(created.nguoi_nhap, self.kho_user)
        self.assertEqual(created.don_vi, "chiếc")
        self.assertEqual(created.so_luong, 150.0)

    # ==============================================================================
    # 3. ISSUE & QUICK ISSUE TESTS
    # ==============================================================================
    def test_issue_form_fields_and_unit(self):
        """Form xuất có các trường hợp lệ bao gồm don_vi và nguoi_nhan là text input"""
        # Hợp lệ với mét
        form_m = MaterialIssueForm(data={
            "ngay_xuat": "2026-08-19",
            "ma_hang": "AT1",
            "mau": "Đen",
            "ten_vat_tu": "Vải chính",
            "so_luong_kien": 2,
            "don_vi": "m",
            "so_luong": 20.5,
            "nguoi_nhan": "Tổ Cắt",
        })
        self.assertTrue(form_m.is_valid())

        # Không hợp lệ với chiếc nếu số lẻ
        form_chiec_invalid = MaterialIssueForm(data={
            "ngay_xuat": "2026-08-19",
            "ma_hang": "AT1",
            "mau": "Đen",
            "ten_vat_tu": "Khóa kéo",
            "so_luong_kien": 2,
            "don_vi": "chiếc",
            "so_luong": 20.5,
            "nguoi_nhan": "Tổ Cắt",
        })
        self.assertFalse(form_chiec_invalid.is_valid())
        self.assertIn("so_luong", form_chiec_invalid.errors)

    def test_quick_issue_success(self):
        """Xuất kho nhanh từ modal với tên người nhận và đơn vị hợp lệ"""
        self._login(self.kho_user)
        post_data = {
            "ma_hang": "AT1",
            "mau": "Đen",
            "ten_vat_tu": "Vải chính",
            "don_vi": "m",
            "ngay_xuat": "2026-08-19",
            "so_luong_kien": "2",
            "so_luong": "20.5",
            "nguoi_nhan": "Tổ Cắt",
        }
        res = self.client.post(reverse("inventory_quick_issue"), post_data, HTTP_REFERER=reverse("inventory_summary"))
        self.assertEqual(res.status_code, 302)

        # Kiểm tra bản ghi xuất được tạo
        latest_issue = MaterialIssue.objects.filter(nguoi_nhan="Tổ Cắt").order_by("-id").first()
        self.assertIsNotNone(latest_issue)
        self.assertEqual(latest_issue.so_luong_kien, 2)
        self.assertEqual(latest_issue.so_luong, 20.5)
        self.assertEqual(latest_issue.don_vi, "m")
        self.assertEqual(latest_issue.nguoi_nhan, "Tổ Cắt")
        self.assertEqual(latest_issue.nguoi_xuat, self.kho_user)

    def test_quick_issue_chiec_integer_handling(self):
        """Xuất kho nhanh với đơn vị chiếc: số nguyên hợp lệ"""
        self._login(self.kho_user)
        post_data = {
            "ma_hang": "AT1",
            "mau": "Đen",
            "ten_vat_tu": "Khóa kéo",
            "don_vi": "chiếc",
            "ngay_xuat": "2026-08-19",
            "so_luong_kien": "1",
            "so_luong": "50",
            "nguoi_nhan": "Anh Nam",
        }
        res = self.client.post(reverse("inventory_quick_issue"), post_data, HTTP_REFERER=reverse("inventory_summary"))
        self.assertEqual(res.status_code, 302)

        issue_chiec = MaterialIssue.objects.filter(nguoi_nhan="Anh Nam").first()
        self.assertIsNotNone(issue_chiec)
        self.assertEqual(issue_chiec.don_vi, "chiếc")
        self.assertEqual(issue_chiec.so_luong, 50.0)

    def test_quick_issue_invalid_user_or_zero_qty(self):
        """Xuất kho không có tên người nhận hoặc số lượng 0 không tạo phiếu xuất"""
        self._login(self.kho_user)
        initial_count = MaterialIssue.objects.count()

        # Người nhận để trống
        self.client.post(reverse("inventory_quick_issue"), {
            "ma_hang": "AT1",
            "mau": "Đen",
            "ten_vat_tu": "Vải chính",
            "don_vi": "m",
            "ngay_xuat": "2026-08-19",
            "so_luong_kien": "2",
            "so_luong": "20.5",
            "nguoi_nhan": "",
        })
        self.assertEqual(MaterialIssue.objects.count(), initial_count)

        # Số lượng 0
        self.client.post(reverse("inventory_quick_issue"), {
            "ma_hang": "AT1",
            "mau": "Đen",
            "ten_vat_tu": "Vải chính",
            "don_vi": "m",
            "ngay_xuat": "2026-08-19",
            "so_luong_kien": "0",
            "so_luong": "0",
            "nguoi_nhan": "Tổ Cắt",
        })
        self.assertEqual(MaterialIssue.objects.count(), initial_count)

    # ==============================================================================
    # 4. HISTORY, PAGINATION & FILTERING TESTS
    # ==============================================================================
    def test_receipt_history_pagination_and_filters(self):
        """Kiểm tra phân trang 20 dòng và lọc theo ngày / cột của lịch sử nhập"""
        # Tạo thêm 25 phiếu nhập để kiểm tra phân trang
        for i in range(25):
            MaterialReceipt.objects.create(
                ngay_nhap=datetime.date(2026, 8, 10),
                ma_hang="AT1",
                mau="Trắng",
                ten_vat_tu=f"Vật tư {i}",
                so_luong_kien=1,
                so_luong=10.0,
                don_vi="m",
                nguoi_nhap=self.kho_user
            )

        self._login(self.kho_user)

        # Trang 1 có 20 bản ghi
        res1 = self.client.get(reverse("inventory_receipt_history") + "?page=1")
        self.assertEqual(res1.status_code, 200)
        self.assertEqual(len(res1.context["page_obj"]), 20)

        # Trang 2 có 7 bản ghi (2 + 25 = 27 tổng)
        res2 = self.client.get(reverse("inventory_receipt_history") + "?page=2")
        self.assertEqual(res2.status_code, 200)
        self.assertEqual(len(res2.context["page_obj"]), 7)

        # Lọc theo ngày
        res_date = self.client.get(reverse("inventory_receipt_history") + "?receipt_start_date=2026-08-01&receipt_end_date=2026-08-05")
        self.assertEqual(len(res_date.context["page_obj"]), 2)

        # Lọc theo cột mã hàng
        res_col = self.client.get(reverse("inventory_receipt_history") + "?receipt_filter_mau=Trắng")
        self.assertEqual(len(res_col.context["page_obj"]), 20)

        # Lọc theo cột đơn vị
        res_dv = self.client.get(reverse("inventory_receipt_history") + "?receipt_filter_don_vi=m")
        self.assertEqual(len(res_dv.context["page_obj"]), 20)

    def test_issue_history_pagination_and_filters(self):
        """Kiểm tra phân trang 20 dòng và lọc theo người nhận / người xuất của lịch sử xuất"""
        for i in range(25):
            MaterialIssue.objects.create(
                ngay_xuat=datetime.date(2026, 8, 10),
                ma_hang="AT1",
                mau="Đen",
                ten_vat_tu=f"Vật tư xuất {i}",
                so_luong_kien=1,
                so_luong=5.0,
                don_vi="m",
                nguoi_nhan="NV Sản Xuất",
                nguoi_xuat=self.kho_user
            )

        self._login(self.kho_user)
        res = self.client.get(reverse("inventory_issue_history") + "?page=1")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.context["page_obj"]), 20)

        # Lọc theo người nhận
        res_user = self.client.get(reverse("inventory_issue_history") + "?issue_filter_nguoi_nhan=NV Sản Xuất")
        self.assertEqual(res_user.status_code, 200)
        self.assertEqual(len(res_user.context["page_obj"]), 20)

        # Lọc theo đơn vị
        res_dv = self.client.get(reverse("inventory_issue_history") + "?issue_filter_don_vi=m")
        self.assertEqual(res_dv.status_code, 200)
        self.assertEqual(len(res_dv.context["page_obj"]), 20)

    # ==============================================================================
    # 5. EDIT & DELETE PERMISSION TESTS (QUAN_LY / PREMIUM ONLY)
    # ==============================================================================
    def test_receipt_edit_and_delete_permissions(self):
        """Chỉ PREMIUM và QUAN_LY mới có quyền sửa/xóa phiếu nhập. KHO, KE_TOAN, BASIC bị cấm (403)"""
        # 1. KHO thử sửa -> 403
        self._login(self.kho_user)
        res_kho = self.client.get(reverse("inventory_receipt_edit", args=[self.receipt1.id]))
        self.assertEqual(res_kho.status_code, 403)

        res_kho_del = self.client.post(reverse("inventory_receipt_delete", args=[self.receipt1.id]))
        self.assertEqual(res_kho_del.status_code, 403)

        # 2. KE_TOAN thử sửa -> 403
        self._login(self.ketoan_user)
        res_kt = self.client.get(reverse("inventory_receipt_edit", args=[self.receipt1.id]))
        self.assertEqual(res_kt.status_code, 403)

        # 3. QUAN_LY sửa thành công -> 200 / 302
        self._login(self.quanly_user)
        res_mgr = self.client.post(reverse("inventory_receipt_edit", args=[self.receipt1.id]), {
            "ngay_nhap": "2026-08-01",
            "ma_hang": "AT1",
            "mau": "Đen",
            "ten_vat_tu": "Vải chính đã sửa",
            "so_luong_kien": 12,
            "don_vi": "m",
            "so_luong": 120.0,
        })
        self.assertEqual(res_mgr.status_code, 302)
        self.receipt1.refresh_from_db()
        self.assertEqual(self.receipt1.ten_vat_tu, "Vải chính đã sửa")
        self.assertEqual(self.receipt1.so_luong_kien, 12)
        self.assertEqual(self.receipt1.so_luong, 120.0)

        # 4. PREMIUM xóa thành công
        self._login(self.premium_user)
        res_del = self.client.post(reverse("inventory_receipt_delete", args=[self.receipt1.id]))
        self.assertEqual(res_del.status_code, 302)
        self.assertFalse(MaterialReceipt.objects.filter(id=self.receipt1.id).exists())

    def test_issue_edit_and_delete_permissions(self):
        """Chỉ PREMIUM và QUAN_LY mới có quyền sửa/xóa phiếu xuất. KHO, KE_TOAN bị cấm (403)"""
        # 1. KHO thử sửa -> 403
        self._login(self.kho_user)
        res_kho = self.client.get(reverse("inventory_issue_edit", args=[self.issue1.id]))
        self.assertEqual(res_kho.status_code, 403)

        # 2. QUAN_LY sửa thành công
        self._login(self.quanly_user)
        res_mgr = self.client.post(reverse("inventory_issue_edit", args=[self.issue1.id]), {
            "ngay_xuat": "2026-08-03",
            "ma_hang": "AT1",
            "mau": "Đen",
            "ten_vat_tu": "Vải chính",
            "so_luong_kien": 4,
            "don_vi": "m",
            "so_luong": 40.0,
            "nguoi_nhan": "Tổ Cắt Đã Sửa",
        })
        self.assertEqual(res_mgr.status_code, 302)
        self.issue1.refresh_from_db()
        self.assertEqual(self.issue1.so_luong_kien, 4)
        self.assertEqual(self.issue1.so_luong, 40.0)
        self.assertEqual(self.issue1.nguoi_nhan, "Tổ Cắt Đã Sửa")

        # 3. PREMIUM xóa thành công
        self._login(self.premium_user)
        res_del = self.client.post(reverse("inventory_issue_delete", args=[self.issue1.id]))
        self.assertEqual(res_del.status_code, 302)
        self.assertFalse(MaterialIssue.objects.filter(id=self.issue1.id).exists())

    # ==============================================================================
    # 6. ROLE MATRIX & SIDEBAR VISIBILITY TESTS
    # ==============================================================================
    def test_role_access_matrix(self):
        """Kiểm tra quyền truy cập các trang kho theo ma trận vai trò"""
        urls = [
            reverse("inventory_summary"),
            reverse("inventory_receipt_history"),
            reverse("inventory_issue_history"),
            reverse("dashboard_kho"),
        ]

        # 1. Cho phép: PREMIUM, QUAN_LY, KHO, KE_TOAN
        for user in [self.premium_user, self.quanly_user, self.kho_user, self.ketoan_user]:
            self._login(user)
            for u in urls:
                res = self.client.get(u)
                self.assertEqual(res.status_code, 200, f"User {user.role} failed to access {u}")

        # 2. Từ chối: BASIC (403 PermissionDenied)
        self._login(self.basic_user)
        for u in urls:
            res = self.client.get(u)
            self.assertEqual(res.status_code, 403, f"User {self.basic_user.role} should be denied access to {u}")

        # 3. Chưa duyệt: UNAPPROVED (302 Redirect to Login)
        self._login(self.unapproved_user)
        for u in urls:
            res = self.client.get(u)
            self.assertEqual(res.status_code, 302, f"Unapproved user should be redirected to login from {u}")

    def test_sidebar_rendering_per_role(self):
        """Kiểm tra hiển thị menu sidebar theo từng vai trò"""
        # PREMIUM: Thấy 3 bảng kho, ẨN "Ghi Nhận Nhập Kho"
        html_p = render_to_string("sidebar.html", {"user": self.premium_user})
        self.assertIn("Tổng Hợp Kho", html_p)
        self.assertIn("Lịch Sử Nhập Kho", html_p)
        self.assertIn("Lịch Sử Xuất Kho", html_p)
        self.assertNotIn("Ghi Nhận Nhập Kho", html_p)

        # KE_TOAN: Thấy 3 bảng kho, ẨN "Ghi Nhận Nhập Kho"
        html_kt = render_to_string("sidebar.html", {"user": self.ketoan_user})
        self.assertIn("Tổng Hợp Kho", html_kt)
        self.assertIn("Lịch Sử Nhập Kho", html_kt)
        self.assertIn("Lịch Sử Xuất Kho", html_kt)
        self.assertNotIn("Ghi Nhận Nhập Kho", html_kt)

        # KHO: Thấy 3 bảng kho + HIỆN "Ghi Nhận Nhập Kho"
        html_k = render_to_string("sidebar.html", {"user": self.kho_user})
        self.assertIn("Tổng Hợp Kho", html_k)
        self.assertIn("Ghi Nhận Nhập Kho", html_k)

        # QUAN_LY: Thấy 3 bảng kho + HIỆN "Ghi Nhận Nhập Kho"
        html_ql = render_to_string("sidebar.html", {"user": self.quanly_user})
        self.assertIn("Tổng Hợp Kho", html_ql)
        self.assertIn("Ghi Nhận Nhập Kho", html_ql)

        # BASIC: Không thấy menu KHO VẬT TƯ
        html_b = render_to_string("sidebar.html", {"user": self.basic_user})
        self.assertNotIn("KHO VẬT TƯ", html_b)

    def test_history_table_action_column_visibility(self):
        """Cột thao tác (Sửa/Xóa) chỉ hiển thị cho PREMIUM và QUAN_LY trên bảng lịch sử"""
        # KHO xem lịch sử nhập -> Không có cột Thao tác
        self._login(self.kho_user)
        res_kho = self.client.get(reverse("inventory_receipt_history"))
        html_kho = res_kho.content.decode("utf-8")
        self.assertNotIn("<th style=\"border: 1px solid #cbd5e1; padding: 10px 8px; text-align: center; width: 120px;\">Thao tác</th>", html_kho)

        # QUAN_LY xem lịch sử nhập -> CÓ cột Thao tác
        self._login(self.quanly_user)
        res_ql = self.client.get(reverse("inventory_receipt_history"))
        html_ql = res_ql.content.decode("utf-8")
        self.assertIn("Thao tác", html_ql)

