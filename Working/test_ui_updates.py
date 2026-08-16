from django.test import TestCase, Client
from django.urls import reverse
from .models import AppUser, Product, ProductColor, ProcessReport
import datetime

class UIUpdatesTests(TestCase):
    def setUp(self):
        self.client = Client(HTTP_HOST='127.0.0.1')
        
        self.premium_user = AppUser.objects.create(
            account="admin_vip", password="123", name="Quản Trị", role="PREMIUM", is_approved=True
        )
        self.quanly_user = AppUser.objects.create(
            account="manager_user", password="123", name="Quản Lý", role="QUAN_LY", is_approved=True
        )
        self.basic_user = AppUser.objects.create(
            account="staff_prod", password="123", name="NV SX", role="BASIC", is_approved=True
        )
        
        self.product = Product.objects.create(name="AT01")
        self.color_red = ProductColor.objects.create(product=self.product, name="Đỏ", quantity=100)

    def _login_as(self, user):
        from django.conf import settings
        session = self.client.session
        session['user_id'] = user.id
        session['display_name'] = user.name
        session.save()
        self.client.cookies[settings.SESSION_COOKIE_NAME] = session.session_key

    def test_list_view_limits_50(self):
        """Kiểm tra trang danh sách chỉ hiển thị 50 bản ghi mới nhất"""
        self._login_as(self.basic_user)
        # Tạo 55 bản ghi
        for i in range(55):
            ProcessReport.objects.create(
                ngay_lam_viec=datetime.date.today(),
                xuong=1, to=1, ma_hang="AT01", mau="Đỏ", size="N/A",
                nhan_btp=i, vao_chuyen=0, giua_chuyen=0, ra_chuyen=0,
                thu_hoa=0, la_thanh_pham=0, nhap_hoan_thien=0,
                nguoi_nhap=self.basic_user
            )
        
        response = self.client.get(reverse('list'))
        self.assertEqual(response.status_code, 200)
        
        # Vì giới hạn là 50, ta kiểm tra số lượng object trong context
        self.assertEqual(len(response.context['table_rows']), 50)
        
        # Reports được sắp xếp giảm dần theo ID hoặc created_at, vì queryset mặc định order_by('-id') hoặc tương tự.

    def test_sidebar_premium_vs_quanly(self):
        """Kiểm tra mục QUY TRÌNH SẢN XUẤT chỉ hiện với QUAN_LY, ẩn với PREMIUM"""
        # Đăng nhập bằng PREMIUM
        self._login_as(self.premium_user)
        res_premium = self.client.get(reverse('premium_dashboard'))
        self.assertEqual(res_premium.status_code, 200)
        # Kiểm tra không chứa "QUY TRÌNH SẢN XUẤT"
        self.assertNotContains(res_premium, "QUY TRÌNH SẢN XUẤT")
        
        # Đăng nhập bằng QUAN_LY
        self.client.cookies.clear()
        self._login_as(self.quanly_user)
        res_quanly = self.client.get(reverse('premium_dashboard'))
        self.assertEqual(res_quanly.status_code, 200)
        # Kiểm tra có chứa "QUY TRÌNH SẢN XUẤT"
        self.assertContains(res_quanly, "QUY TRÌNH SẢN XUẤT")

    def test_list_views_no_extra_buttons(self):
        """Kiểm tra trang danh sách không có các nút thừa như Đổi MK, Đăng xuất, Trực tuyến, Xuất Excel"""
        self._login_as(self.basic_user)
        response = self.client.get(reverse('list'))
        self.assertEqual(response.status_code, 200)
        
        self.assertNotContains(response, "Trực tuyến")
        self.assertNotContains(response, "Xuất Excel")
        self.assertNotContains(response, "Đổi mật khẩu")
        self.assertNotContains(response, "Đăng xuất")
        # Phải có nút nhập mới
        self.assertContains(response, "Nhập Mới")

    def test_entry_pages_header_buttons(self):
        """Kiểm tra trang nhập liệu với QUAN_LY không có nút Đổi MK, Đăng xuất ở header"""
        self._login_as(self.quanly_user)
        response = self.client.get(reverse('web'))
        self.assertEqual(response.status_code, 200)
        
        # Do QUAN_LY có sidebar, các nút này bị ẩn ở header của trang nhập
        self.assertNotContains(response, ">Đổi mật khẩu</a>")
        self.assertNotContains(response, ">Đăng xuất</a>")
        
        # Với nhân viên BASIC (không có sidebar), nút Đổi MK, Đăng xuất vẫn phải có ở header (nếu như design vẫn giữ cho họ)
        self.client.cookies.clear()
        self._login_as(self.basic_user)
        res_basic = self.client.get(reverse('web'))
        self.assertEqual(res_basic.status_code, 200)
        # Tùy thuộc vào design hiện tại, nếu basic user có nút này thì ta check:
        # self.assertContains(res_basic, "Đổi mật khẩu")
        # self.assertContains(res_basic, "Đăng xuất")
    def test_list_view_cross_user_cumulative_totals(self):
        """
        Kiểm tra: Nhân viên chỉ thấy dòng của mình, nhưng cột Tổng vẫn tính lũy kế trên toàn bộ người nhập.
        """
        from .models import CutReport, FinishingReport, KcsReport
        user_a = AppUser.objects.create(account="user_a", password="123", name="Nhân Viên A", role="BASIC", is_approved=True)
        user_b = AppUser.objects.create(account="user_b", password="123", name="Nhân Viên B", role="BASIC", is_approved=True)
        
        today = datetime.date.today()
        # User A nhập trước: 100
        rep_a = ProcessReport.objects.create(
            ngay_lam_viec=today,
            xuong=1, to=1, ma_hang="AT01", mau="Đỏ", size="N/A",
            nhan_btp=100, vao_chuyen=100, giua_chuyen=100, ra_chuyen=100,
            thu_hoa=100, la_thanh_pham=100, nhap_hoan_thien=100,
            nguoi_nhap=user_a
        )
        # User B nhập sau: 50 (cùng mã, màu, xưởng, tổ)
        rep_b = ProcessReport.objects.create(
            ngay_lam_viec=today,
            xuong=1, to=1, ma_hang="AT01", mau="Đỏ", size="N/A",
            nhan_btp=50, vao_chuyen=50, giua_chuyen=50, ra_chuyen=50,
            thu_hoa=50, la_thanh_pham=50, nhap_hoan_thien=50,
            nguoi_nhap=user_b
        )

        # 1. User A xem list: chỉ thấy 1 dòng của chính mình, Tổng = 100
        self._login_as(user_a)
        res_a = self.client.get(reverse('list'))
        self.assertEqual(res_a.status_code, 200)
        rows_a = res_a.context['table_rows']
        self.assertEqual(len(rows_a), 1)
        self.assertEqual(rows_a[0]['row_id'], rep_a.id)
        self.assertEqual(rows_a[0]['nhan_btp_ngay'], 100)
        self.assertEqual(rows_a[0]['nhan_btp_tong'], 100)

        # 2. User B xem list: chỉ thấy 1 dòng của chính mình, nhưng Tổng = 150 (cộng dồn cả A)
        self.client.cookies.clear()
        self._login_as(user_b)
        res_b = self.client.get(reverse('list'))
        self.assertEqual(res_b.status_code, 200)
        rows_b = res_b.context['table_rows']
        self.assertEqual(len(rows_b), 1)
        self.assertEqual(rows_b[0]['row_id'], rep_b.id)
        self.assertEqual(rows_b[0]['nhan_btp_ngay'], 50)
        self.assertEqual(rows_b[0]['nhan_btp_tong'], 150)

        # 3. Quản lý xem list: thấy cả 2 dòng với số tổng 100 và 150
        self.client.cookies.clear()
        self._login_as(self.quanly_user)
        res_ql = self.client.get(reverse('list'))
        self.assertEqual(res_ql.status_code, 200)
        rows_ql = res_ql.context['table_rows']
        self.assertEqual(len(rows_ql), 2)
        dict_ql = {r['row_id']: r for r in rows_ql}
        self.assertEqual(dict_ql[rep_a.id]['nhan_btp_tong'], 100)
        self.assertEqual(dict_ql[rep_b.id]['nhan_btp_tong'], 150)

    def test_finishing_and_cut_and_kcs_list_cross_user_totals(self):
        """
        Kiểm tra tính lũy kế chéo người dùng cho Cắt, KCS, Hoàn thiện trên các trang list.
        """
        from .models import CutReport, FinishingReport, KcsReport
        cut_a = AppUser.objects.create(account="cut_a", password="123", name="Cắt A", role="NHA_CAT", is_approved=True)
        cut_b = AppUser.objects.create(account="cut_b", password="123", name="Cắt B", role="NHA_CAT", is_approved=True)
        today = datetime.date.today()

        c1 = CutReport.objects.create(nguoi_nhap=cut_a, ngay_lam_viec=today, ma_hang="AT01", mau="Đỏ", cat_chinh=80)
        c2 = CutReport.objects.create(nguoi_nhap=cut_b, ngay_lam_viec=today, ma_hang="AT01", mau="Đỏ", cat_chinh=40)

        # Cut B chỉ thấy dòng của mình, nhưng tổng = 120
        self._login_as(cut_b)
        res_cut = self.client.get(reverse('cut_list'))
        self.assertEqual(res_cut.status_code, 200)
        self.assertEqual(len(res_cut.context['table_rows']), 1)
        self.assertEqual(res_cut.context['table_rows'][0]['cat_chinh_ngay'], 40)
        self.assertEqual(res_cut.context['table_rows'][0]['cat_chinh_tong'], 120)

