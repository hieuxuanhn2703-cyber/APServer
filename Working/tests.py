import datetime
from django.test import TestCase, Client
from django.urls import reverse
from .models import AppUser, Product, ProductColor, ProductSize, ProcessReport, FinishingReport


class ComprehensiveSystemTests(TestCase):
    def setUp(self):
        self.client = Client(HTTP_HOST='127.0.0.1')
        
        # Tạo sẵn các tài khoản với các quyền khác nhau
        self.premium_user = AppUser.objects.create(
            account="admin_vip", password="123", name="Quản Trị Viên", role="PREMIUM", is_approved=True
        )
        self.quanly_user = AppUser.objects.create(
            account="manager_user", password="123", name="Quản Lý", role="QUAN_LY", is_approved=True
        )
        self.basic_user = AppUser.objects.create(
            account="staff_prod", password="123", name="NV Sản Xuất", role="BASIC", is_approved=True
        )
        self.finishing_user = AppUser.objects.create(
            account="staff_fin", password="123", name="NV Hoàn Thiện", role="HOAN_THIEN", is_approved=True
        )
        self.unapproved_user = AppUser.objects.create(
            account="newbie", password="123", name="NV Mới", role="BASIC", is_approved=False
        )
        
        # Tạo cấu hình sản phẩm & màu sắc mẫu
        self.product = Product.objects.create(name="AT01")
        self.color_red = ProductColor.objects.create(product=self.product, name="Đỏ", quantity=100)
        self.color_blue = ProductColor.objects.create(product=self.product, name="Xanh", quantity=200)

        # Tạo báo cáo sản xuất mẫu
        self.prod_report = ProcessReport.objects.create(
            ngay_lam_viec=datetime.date.today(),
            xuong=1,
            to=1,
            ma_hang="AT01",
            mau="Đỏ",
            size="N/A",
            nhan_btp=10,
            vao_chuyen=10,
            giua_chuyen=10,
            ra_chuyen=10,
            thu_hoa=10,
            la_thanh_pham=10,
            kcs=10,
            nhap_hoan_thien=10,
            nguoi_nhap=self.basic_user
        )

        # Tạo báo cáo hoàn thiện mẫu
        self.fin_report = FinishingReport.objects.create(
            ngay_lam_viec=datetime.date.today(),
            ma_hang="AT01",
            mau="Đỏ",
            size="N/A",
            nhan_hang_hoan_thien=10,
            the_bai=10,
            gap_hang=10,
            treo_dong_thung=10,
            nguoi_nhap=self.finishing_user
        )

    def _login_as(self, user):
        session = self.client.session
        session['user_id'] = user.id
        session['display_name'] = user.name
        session.save()

    # ==========================================
    # 1. TEST ĐĂNG KÝ, ĐĂNG NHẬP, PHÂN QUYỀN
    # ==========================================
    def test_registration_flow(self):
        # Đăng ký thành công -> Mặc định chưa duyệt
        response = self.client.post(reverse('register'), {
            'account': 'user_test',
            'name': 'User Test',
            'password': 'pass123',
            'confirm_password': 'pass123'
        })
        self.assertEqual(response.status_code, 200)
        user = AppUser.objects.filter(account='user_test').first()
        self.assertIsNotNone(user)
        self.assertFalse(user.is_approved)

        # Đăng ký trùng username
        res_dup = self.client.post(reverse('register'), {
            'account': 'user_test',
            'name': 'Duplicate',
            'password': 'pass123',
            'confirm_password': 'pass123'
        })
        self.assertContains(res_dup, "Tài khoản này đã tồn tại")

        # Đăng ký mật khẩu không khớp
        res_mismatch = self.client.post(reverse('register'), {
            'account': 'user_mismatch',
            'name': 'Mismatch',
            'password': 'pass1',
            'confirm_password': 'pass2'
        })
        self.assertContains(res_mismatch, "Mật khẩu nhập lại không khớp")

    def test_login_flow(self):
        # 1. Đăng nhập tài khoản chưa duyệt
        res_unapproved = self.client.post(reverse('login'), {'account': 'newbie', 'password': '123'})
        self.assertContains(res_unapproved, "đang chờ quản trị viên phê duyệt")

        # 2. Đăng nhập sai mật khẩu
        res_wrong = self.client.post(reverse('login'), {'account': 'staff_prod', 'password': 'wrong'})
        self.assertContains(res_wrong, "Tài khoản hoặc mật khẩu không đúng")

        # 3. Đăng nhập tài khoản BASIC -> Chuyển hướng về trang nhập sản xuất
        res_basic = self.client.post(reverse('login'), {'account': 'staff_prod', 'password': '123'})
        self.assertRedirects(res_basic, reverse('web'))

        # 4. Đăng nhập tài khoản HOAN_THIEN -> Chuyển hướng về trang nhập hoàn thiện
        res_fin = self.client.post(reverse('login'), {'account': 'staff_fin', 'password': '123'})
        self.assertRedirects(res_fin, reverse('finishing_web'))

        # 5. Đăng nhập tài khoản PREMIUM -> Chuyển hướng thẳng về Dashboard Dữ Liệu
        res_prem = self.client.post(reverse('login'), {'account': 'admin_vip', 'password': '123'})
        self.assertRedirects(res_prem, reverse('premium_dashboard'))

        # 6. Đăng nhập tài khoản QUAN_LY -> Chuyển hướng về Dashboard Dữ Liệu
        res_quanly = self.client.post(reverse('login'), {'account': 'manager_user', 'password': '123'})
        self.assertRedirects(res_quanly, reverse('premium_dashboard'))

    def test_logout(self):
        self._login_as(self.premium_user)
        res = self.client.get(reverse('logout'))
        self.assertRedirects(res, reverse('login'))
        self.assertNotIn('user_id', self.client.session)

    def test_change_password(self):
        self._login_as(self.basic_user)
        
        # Đổi mật khẩu thành công
        res_ok = self.client.post(reverse('change_password'), {
            'old_password': '123',
            'new_password': '456',
            'confirm_password': '456'
        })
        self.assertEqual(res_ok.status_code, 200)
        self.assertTrue(res_ok.context['success'])
        
        # Đổi mật khẩu thất bại (sai pass cũ)
        res_fail1 = self.client.post(reverse('change_password'), {
            'old_password': 'wrong',
            'new_password': '789',
            'confirm_password': '789'
        })
        self.assertIn("Mật khẩu cũ không chính xác", res_fail1.content.decode('utf-8'))
        
        # Đổi mật khẩu thất bại (pass mới không khớp)
        res_fail2 = self.client.post(reverse('change_password'), {
            'old_password': '456',
            'new_password': '789',
            'confirm_password': '999'
        })
        self.assertIn("Mật khẩu mới không khớp", res_fail2.content.decode('utf-8'))


    def test_unauthenticated_access_blocked(self):
        # Chưa đăng nhập truy cập các trang bảo mật đều chuyển về login
        protected_urls = [
            reverse('web'),
            reverse('list'),
            reverse('premium_dashboard'),
            reverse('manage_accounts'),
            reverse('config_list'),
            reverse('tracking'),
            reverse('finishing_web'),
            reverse('finishing_list'),
            reverse('change_password'),
        ]
        for url in protected_urls:
            res = self.client.get(url)
            self.assertRedirects(res, reverse('login'), msg_prefix=f"URL {url} should redirect to login")

    def test_exhaustive_role_permissions(self):
        # Định nghĩa các route cần test
        routes = {
            'web': reverse('web'),
            'list': reverse('list'),
            'finishing_web': reverse('finishing_web'),
            'finishing_list': reverse('finishing_list'),
            'premium_dashboard': reverse('premium_dashboard'),
            'tracking': reverse('tracking'),
            'config_list': reverse('config_list'),
            'manage_accounts': reverse('manage_accounts'),
            'change_password': reverse('change_password'),
        }

        # Cấu hình mong đợi HTTP Status Code cho từng Role
        expected_status = {
            self.basic_user: {
                'web': 200, 'list': 200,
                'finishing_web': 403, 'finishing_list': 403,
                'premium_dashboard': 403, 'tracking': 403,
                'config_list': 403, 'manage_accounts': 403,
                'change_password': 200
            },
            self.finishing_user: {
                'web': 403, 'list': 403,
                'finishing_web': 200, 'finishing_list': 200,
                'premium_dashboard': 403, 'tracking': 403,
                'config_list': 403, 'manage_accounts': 403,
                'change_password': 200
            },
            self.quanly_user: {
                'web': 200, 'list': 200,
                'finishing_web': 200, 'finishing_list': 200,
                'premium_dashboard': 200, 'tracking': 200,
                'config_list': 200, 'manage_accounts': 403,
                'change_password': 200
            },
            self.premium_user: {
                'web': 200, 'list': 200,
                'finishing_web': 200, 'finishing_list': 200,
                'premium_dashboard': 200, 'tracking': 200,
                'config_list': 200, 'manage_accounts': 200,
                'change_password': 200
            }
        }

        # Chạy kiểm thử vét cạn
        for user, permissions in expected_status.items():
            self._login_as(user)
            for route_name, expected_code in permissions.items():
                url = routes[route_name]
                response = self.client.get(url)
                self.assertEqual(
                    response.status_code, 
                    expected_code, 
                    f"User {user.role} accessing {url} returned {response.status_code}, expected {expected_code}"
                )



    # ==========================================
    # 2. TEST DASHBOARD DỮ LIỆU (PREMIUM)
    # ==========================================
    def test_premium_dashboard_view(self):
        self._login_as(self.premium_user)
        res = self.client.get(reverse('premium_dashboard'))
        self.assertEqual(res.status_code, 200)
        self.assertIn("Dashboard Dữ Liệu", res.content.decode('utf-8'))
        self.assertIn("Danh sách Sản xuất", res.content.decode('utf-8'))
        self.assertIn("Danh sách Hoàn thiện", res.content.decode('utf-8'))
        self.assertIn("Quản lý Mã hàng", res.content.decode('utf-8'))
        self.assertIn("Quản lý Tài khoản", res.content.decode('utf-8'))
        self.assertIn("Đăng xuất", res.content.decode('utf-8'))
        
        # Admin (PREMIUM) thì KHÔNG thấy 2 nút nhập dữ liệu ở Dashboard
        self.assertNotIn("Nhập DL Sản xuất", res.content.decode('utf-8'))
        self.assertNotIn("Nhập DL Hoàn thiện", res.content.decode('utf-8'))


    def test_quanly_dashboard_view(self):
        self._login_as(self.quanly_user)
        res = self.client.get(reverse('premium_dashboard'))
        self.assertEqual(res.status_code, 200)
        self.assertIn("Dashboard Dữ Liệu", res.content.decode('utf-8'))
        self.assertNotIn("Quản lý Tài khoản", res.content.decode('utf-8'))
        
        # Quản lý (QUAN_LY) thì CÓ thấy 2 nút nhập dữ liệu ở Dashboard
        self.assertIn("Nhập DL Sản xuất", res.content.decode('utf-8'))
        self.assertIn("Nhập DL Hoàn thiện", res.content.decode('utf-8'))

    def test_dashboard_date_filter(self):
        self._login_as(self.premium_user)
        prod_date = self.prod_report.created_at.strftime('%Y-%m-%d')
        res = self.client.get(f"{reverse('premium_dashboard')}?prod_start_date={prod_date}&prod_end_date={prod_date}&fin_start_date={prod_date}&fin_end_date={prod_date}")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.context['page_prod']), 1)
        self.assertEqual(len(res.context['page_fin']), 1)

        # Lọc ngày trong tương lai -> Không có dữ liệu
        res_empty = self.client.get(f"{reverse('premium_dashboard')}?prod_start_date=2099-01-01&prod_end_date=2099-12-31&fin_start_date=2099-01-01&fin_end_date=2099-12-31")
        self.assertEqual(res_empty.status_code, 200)
        self.assertEqual(len(res_empty.context['page_prod']), 0)
        self.assertEqual(len(res_empty.context['page_fin']), 0)
        self.assertEqual(len(res_empty.context['page_fin']), 0)

    def test_production_validation_zero_xuong_to(self):
        # Kiểm tra Xưởng và Tổ không được bằng 0
        self._login_as(self.basic_user)
        today_str = datetime.date.today().strftime('%Y-%m-%d')
        
        # Test gửi Xưởng = 0, Tổ = 0
        res_zero = self.client.post(reverse('web'), {
            'ngay_lam_viec': today_str,
            'xuong': 0,
            'to': 0,
            'ma_hang': 'AT01',
            'mau': 'Đỏ',
            'co': 'N/A',
        })
        self.assertEqual(res_zero.status_code, 200)
        self.assertFalse(res_zero.context.get('success', False))
        self.assertIn("Vui lòng nhập số xưởng khác 0.", res_zero.content.decode('utf-8'))
        self.assertIn("Vui lòng nhập số tổ khác 0.", res_zero.content.decode('utf-8'))

    def test_production_crud_and_redirects(self):
        # 1. Nhập dữ liệu sản xuất (BASIC)
        self._login_as(self.basic_user)
        today_str = datetime.date.today().strftime('%Y-%m-%d')
        res_post = self.client.post(reverse('web'), {
            'ngay_lam_viec': today_str,
            'xuong': 2,
            'to': 2,
            'ma_hang': 'AT01',
            'mau': 'Đỏ',
            'co': 'N/A',
            'nhan_btp': 20,
            'vao_chuyen': 20,
            'giua_chuyen': 20,
            'ra_chuyen': 20,
            'thu_hoa': 20,
            'la_thanh_pham': 20,
            'kcs': 20,
            'nhap_hoan_thien': 20,
        })
        self.assertEqual(res_post.status_code, 200)
        self.assertTrue(res_post.context['success'])
        new_report = ProcessReport.objects.filter(to=2).first()
        self.assertIsNotNone(new_report)
        self.assertEqual(new_report.xuong, 2)
        
        # Kiểm tra BASIC không thấy nút Xóa/Sửa ở trang list
        res_list = self.client.get(reverse('list'))
        self.assertEqual(res_list.status_code, 200)
        self.assertNotIn("<th>Thao tác</th>", res_list.content.decode('utf-8'))
        
        # Nhưng PREMIUM thì thấy
        self._login_as(self.premium_user)
        res_list_prem = self.client.get(reverse('list'))
        self.assertEqual(res_list_prem.status_code, 200)
        self.assertIn("<th>Thao tác</th>", res_list_prem.content.decode('utf-8'))
        
        # Đăng nhập lại BASIC để chạy tiếp luồng
        self._login_as(self.basic_user)

        # 2. Sửa bởi người tạo (BASIC) -> Chuyển về 'list'
        res_edit_basic = self.client.post(reverse('edit', args=[new_report.id]), {
            'ngay_lam_viec': today_str,
            'xuong': 3,
            'to': 2,
            'ma_hang': 'AT01',
            'mau': 'Đỏ',
            'co': 'N/A',
            'nhan_btp': 30,
            'vao_chuyen': 30,
            'giua_chuyen': 30,
            'ra_chuyen': 30,
            'thu_hoa': 30,
            'la_thanh_pham': 30,
            'kcs': 30,
            'nhap_hoan_thien': 30,
        })
        self.assertRedirects(res_edit_basic, reverse('list'))
        new_report.refresh_from_db()
        self.assertEqual(new_report.nhan_btp, 30)
        self.assertEqual(new_report.xuong, 3)

        # 3. Sửa bởi PREMIUM -> Chuyển về 'premium_dashboard'
        self._login_as(self.premium_user)
        res_edit_prem = self.client.post(reverse('edit', args=[new_report.id]), {
            'ngay_lam_viec': today_str,
            'xuong': 3,
            'to': 2,
            'ma_hang': 'AT01',
            'mau': 'Đỏ',
            'co': 'N/A',
            'nhan_btp': 50,
            'vao_chuyen': 50,
            'giua_chuyen': 50,
            'ra_chuyen': 50,
            'thu_hoa': 50,
            'la_thanh_pham': 50,
            'kcs': 50,
            'nhap_hoan_thien': 50,
        })
        self.assertRedirects(res_edit_prem, reverse('premium_dashboard'))
        new_report.refresh_from_db()
        self.assertEqual(new_report.nhan_btp, 50)

        # 4. Người khác không có quyền sửa (HOAN_THIEN) -> 403
        self._login_as(self.finishing_user)
        res_denied = self.client.post(reverse('edit', args=[new_report.id]), {
            'ngay_lam_viec': today_str,
            'xuong': 3,
            'to': 2,
            'ma_hang': 'AT01',
            'mau': 'Đỏ',
            'co': 'N/A',
        })
        self.assertEqual(res_denied.status_code, 403)

        # 5. Xóa bởi PREMIUM -> Chuyển về 'premium_dashboard'
        self._login_as(self.premium_user)
        res_del = self.client.post(reverse('delete_report', args=[new_report.id]))
        self.assertRedirects(res_del, reverse('premium_dashboard'))
        self.assertFalse(ProcessReport.objects.filter(id=new_report.id).exists())

    # ==========================================
    # 4. TEST QUY TRÌNH HOÀN THIỆN (CRUD & REDIRECTS)
    # ==========================================
    def test_finishing_crud_and_redirects(self):
        # 1. Nhập dữ liệu hoàn thiện (HOAN_THIEN)
        self._login_as(self.finishing_user)
        today_str = datetime.date.today().strftime('%Y-%m-%d')
        res_post = self.client.post(reverse('finishing_web'), {
            'ngay_lam_viec': today_str,
            'ma_hang': 'AT01',
            'mau': 'Đỏ',
            'nhan_hang_hoan_thien': 15,
            'the_bai': 15,
            'gap_hang': 15,
            'treo_dong_thung': 15,
        })
        self.assertEqual(res_post.status_code, 200)
        self.assertTrue(res_post.context['success'])
        new_fin = FinishingReport.objects.filter(nhan_hang_hoan_thien=15).first()
        self.assertIsNotNone(new_fin)
        
        # Kiểm tra HOAN_THIEN không thấy nút Xóa/Sửa ở trang finishing_list
        res_fin_list = self.client.get(reverse('finishing_list'))
        self.assertEqual(res_fin_list.status_code, 200)
        self.assertNotIn("<th>Thao tác</th>", res_fin_list.content.decode('utf-8'))
        
        # Nhưng QUAN_LY (hoặc PREMIUM) thì thấy
        self._login_as(self.quanly_user)
        res_fin_list_quanly = self.client.get(reverse('finishing_list'))
        self.assertEqual(res_fin_list_quanly.status_code, 200)
        self.assertIn("<th>Thao tác</th>", res_fin_list_quanly.content.decode('utf-8'))
        
        # Đăng nhập lại HOAN_THIEN để chạy tiếp luồng
        self._login_as(self.finishing_user)

        # 2. Sửa bởi người tạo (HOAN_THIEN) -> Chuyển về 'finishing_list'
        res_edit_fin = self.client.post(reverse('finishing_edit', args=[new_fin.id]), {
            'ngay_lam_viec': today_str,
            'ma_hang': 'AT01',
            'mau': 'Đỏ',
            'nhan_hang_hoan_thien': 25,
            'the_bai': 25,
            'gap_hang': 25,
            'treo_dong_thung': 25,
        })
        self.assertRedirects(res_edit_fin, reverse('finishing_list'))
        new_fin.refresh_from_db()
        self.assertEqual(new_fin.nhan_hang_hoan_thien, 25)

        # 3. Sửa bởi PREMIUM -> Chuyển về 'premium_dashboard'
        self._login_as(self.premium_user)
        res_edit_prem = self.client.post(reverse('finishing_edit', args=[new_fin.id]), {
            'ngay_lam_viec': today_str,
            'ma_hang': 'AT01',
            'mau': 'Đỏ',
            'nhan_hang_hoan_thien': 35,
            'the_bai': 35,
            'gap_hang': 35,
            'treo_dong_thung': 35,
        })
        self.assertRedirects(res_edit_prem, reverse('premium_dashboard'))
        new_fin.refresh_from_db()
        self.assertEqual(new_fin.nhan_hang_hoan_thien, 35)

        # 4. Người khác không có quyền sửa (BASIC) -> 403
        self._login_as(self.basic_user)
        res_denied = self.client.post(reverse('finishing_edit', args=[new_fin.id]), {
            'ngay_lam_viec': today_str,
            'ma_hang': 'AT01',
            'mau': 'Đỏ',
        })
        self.assertEqual(res_denied.status_code, 403)

        # 5. Xóa bởi PREMIUM -> Chuyển về 'premium_dashboard'
        self._login_as(self.premium_user)
        res_del = self.client.post(reverse('finishing_delete_report', args=[new_fin.id]))
        self.assertRedirects(res_del, reverse('premium_dashboard'))
        self.assertFalse(FinishingReport.objects.filter(id=new_fin.id).exists())

    # ==========================================
    # 5. TEST QUẢN LÝ TÀI KHOẢN & CẤU HÌNH & EXCEL
    # ==========================================
    def test_account_management(self):
        self._login_as(self.premium_user)
        # Xem danh sách
        res = self.client.get(reverse('manage_accounts'))
        self.assertEqual(res.status_code, 200)

        # Phê duyệt tài khoản
        self.client.post(reverse('toggle_account', args=[self.unapproved_user.id]), {'action': 'toggle_status'})
        self.unapproved_user.refresh_from_db()
        self.assertTrue(self.unapproved_user.is_approved)

        # Thay đổi vai trò
        self.client.post(reverse('toggle_account', args=[self.unapproved_user.id]), {'action': 'change_role', 'new_role': 'HOAN_THIEN'})
        self.unapproved_user.refresh_from_db()
        self.assertEqual(self.unapproved_user.role, 'HOAN_THIEN')
        
        # Test quyền xóa tài khoản
        # QUAN_LY truy cập sẽ bị 403
        self._login_as(self.quanly_user)
        res_del_fail = self.client.post(reverse('delete_account', args=[self.unapproved_user.id]))
        self.assertEqual(res_del_fail.status_code, 403)
        
        # PREMIUM xóa thành công
        self._login_as(self.premium_user)
        res_del_ok = self.client.post(reverse('delete_account', args=[self.unapproved_user.id]))
        self.assertRedirects(res_del_ok, reverse('manage_accounts'))
        self.assertFalse(AppUser.objects.filter(id=self.unapproved_user.id).exists())

    def test_config_product_and_color_crud(self):
        self._login_as(self.premium_user)

        # Thêm sản phẩm & màu
        res_add = self.client.post(reverse('config_add_product'), {
            'name': 'AT02',
            'colors': 'Vàng - 60\nTím: 70'
        })
        self.assertRedirects(res_add, reverse('config_list'))
        p2 = Product.objects.get(name='AT02')
        self.assertEqual(p2.colors.count(), 2)

        # Sửa màu sắc & số lượng
        color_yellow = p2.colors.get(name='Vàng')
        res_edit_color = self.client.post(reverse('config_edit_color', args=[color_yellow.id]), {
            'name': 'Vàng Chanh',
            'quantity': 88
        })
        self.assertRedirects(res_edit_color, reverse('config_list'))
        color_yellow.refresh_from_db()
        self.assertEqual(color_yellow.name, 'Vàng Chanh')
        self.assertEqual(color_yellow.quantity, 88)

        # Xóa màu
        self.client.post(reverse('config_delete_color', args=[color_yellow.id]))
        self.assertEqual(p2.colors.count(), 1)

        # Xóa mã hàng
        self.client.post(reverse('config_delete_product', args=[p2.id]))
        self.assertFalse(Product.objects.filter(id=p2.id).exists())

    def test_excel_exports(self):
        self._login_as(self.premium_user)
        
        # 1. Xuất Excel Sản xuất
        res_prod = self.client.get(reverse('export_excel'))
        self.assertEqual(res_prod.status_code, 200)
        self.assertEqual(res_prod['Content-Type'], "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        # 2. Xuất Excel Hoàn thiện
        res_fin = self.client.get(reverse('finishing_export_excel'))
        self.assertEqual(res_fin.status_code, 200)
        self.assertEqual(res_fin['Content-Type'], "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        # 3. Xuất Excel Tracking
        res_track = self.client.get(reverse('tracking_export_excel'))
        self.assertEqual(res_track.status_code, 200)
        self.assertEqual(res_track['Content-Type'], "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
