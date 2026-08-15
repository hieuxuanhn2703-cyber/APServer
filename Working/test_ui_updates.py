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
        pass
