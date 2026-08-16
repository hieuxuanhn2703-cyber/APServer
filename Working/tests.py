import datetime
from django.test import TestCase, Client
from django.urls import reverse
from .models import AppUser, Product, ProductColor, ProductSize, ProcessReport, FinishingReport, CutReport, KcsReport


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
            nhap_hoan_thien=10,
            nguoi_nhap=self.basic_user
        )

        # Tạo báo cáo hoàn thiện mẫu
        self.fin_report = FinishingReport.objects.create(
            ngay_lam_viec=datetime.date.today(),
            ma_hang="AT01",
            mau="Đỏ",
            size="N/A",
            the_bai=10,
            gap_hang=10,
            treo_dong_thung=10,
            nguoi_nhap=self.finishing_user
        )

    def _login_as(self, user):
        from django.conf import settings
        session = self.client.session
        session['user_id'] = user.id
        session['display_name'] = user.name
        session.save()
        self.client.cookies[settings.SESSION_COOKIE_NAME] = session.session_key

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
        # Chưa đăng nhập truy cập bất kỳ trang nào đều tự động chuyển về login
        protected_urls = [
            reverse('web'),
            reverse('list'),
            reverse('premium_dashboard'),
            reverse('manage_accounts'),
            reverse('config_list'),
            reverse('config_add_product'),
            reverse('tracking'),
            reverse('tracking_export_excel'),
            reverse('export_excel'),
            reverse('finishing_web'),
            reverse('finishing_list'),
            reverse('finishing_export_excel'),
            reverse('kcs_web'),
            reverse('kcs_list'),
            reverse('kcs_export_excel'),
            reverse('cut_web'),
            reverse('cut_list'),
            reverse('cut_export_excel'),
            reverse('change_password'),
            '/random-protected-path/',
        ]
        for url in protected_urls:
            res = self.client.get(url)
            self.assertRedirects(res, reverse('login'), msg_prefix=f"URL {url} should redirect to login")

        # Session chứa user_id không tồn tại trong database -> Chuyển về login
        self._login_as(self.basic_user)
        session = self.client.session
        session['user_id'] = 999999
        session.save()
        res_invalid = self.client.get(reverse('web'))
        self.assertRedirects(res_invalid, reverse('login'))

        # Session chứa tài khoản chưa được duyệt -> Chuyển về login
        self._login_as(self.unapproved_user)
        res_unapproved = self.client.get(reverse('web'))
        self.assertRedirects(res_unapproved, reverse('login'))

        # Người dùng đã đăng nhập truy cập GET /login/ -> Tự động chuyển về trang chính
        self._login_as(self.basic_user)
        res_logged_basic = self.client.get(reverse('login'))
        self.assertRedirects(res_logged_basic, reverse('web'))

        self._login_as(self.premium_user)
        res_logged_prem = self.client.get(reverse('login'))
        self.assertRedirects(res_logged_prem, reverse('premium_dashboard'))

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
    # 2. TEST DASHBOARD DỮ LIỆU (4 TRANG TỔNG HỢP)
    # ==========================================
    def test_premium_dashboard_view(self):
        self._login_as(self.premium_user)
        
        # 1. Test Dashboard Cắt
        res_cut = self.client.get(reverse('dashboard_cut'))
        self.assertEqual(res_cut.status_code, 200)
        self.assertIn("Tổng Hợp Quy Trình Cắt", res_cut.content.decode('utf-8'))
        self.assertEqual(res_cut.context['page_cut'].paginator.per_page, 50)
        self.assertIn('data-title="Mã hàng"', res_cut.content.decode('utf-8'))
        
        # 2. Test Dashboard Sản xuất
        res_prod = self.client.get(reverse('dashboard_prod'))
        self.assertEqual(res_prod.status_code, 200)
        self.assertIn("Tổng Hợp Quy Trình Sản Xuất", res_prod.content.decode('utf-8'))
        self.assertEqual(res_prod.context['page_prod'].paginator.per_page, 50)
        self.assertNotIn("Thời gian", res_prod.context['prod_headers'])
        self.assertIn("Số lượng LĐ", res_prod.context['prod_headers'])

        # 3. Test Dashboard KCS
        res_kcs = self.client.get(reverse('dashboard_kcs'))
        self.assertEqual(res_kcs.status_code, 200)
        self.assertIn("Tổng Hợp Quy Trình KCS", res_kcs.content.decode('utf-8'))
        self.assertEqual(res_kcs.context['page_kcs'].paginator.per_page, 50)

        # 4. Test Dashboard Hoàn thiện
        res_fin = self.client.get(reverse('dashboard_finishing'))
        self.assertEqual(res_fin.status_code, 200)
        self.assertIn("Tổng Hợp Quy Trình Hoàn Thiện", res_fin.content.decode('utf-8'))
        self.assertEqual(res_fin.context['page_fin'].paginator.per_page, 50)

        # Common checks
        self.assertIn("Quản lý Mã hàng", res_cut.content.decode('utf-8'))
        self.assertIn("Quản lý Tài khoản", res_cut.content.decode('utf-8'))
        self.assertIn("Đăng xuất", res_cut.content.decode('utf-8'))
        self.assertIn("excel_filter.js", res_cut.content.decode('utf-8'))
        self.assertIn("excel-filter-btn", res_cut.content.decode('utf-8'))


    def test_quanly_dashboard_view(self):
        self._login_as(self.quanly_user)
        res = self.client.get(reverse('dashboard_cut'))
        self.assertEqual(res.status_code, 200)
        self.assertNotIn("Quản lý Tài khoản", res.content.decode('utf-8'))
        self.assertIn("Nhập DL Cắt", res.content.decode('utf-8'))
        self.assertIn("Nhập DL Sản xuất", res.content.decode('utf-8'))
        self.assertIn("Nhập DL Hoàn thiện", res.content.decode('utf-8'))

    def test_dashboard_date_filter(self):
        self._login_as(self.premium_user)
        from django.utils import timezone as tz
        prod_date = tz.localtime(self.prod_report.created_at).strftime('%Y-%m-%d')
        fin_date = tz.localtime(self.fin_report.created_at).strftime('%Y-%m-%d')

        # Lọc ngày bảng Sản xuất
        res_p = self.client.get(f"{reverse('dashboard_prod')}?prod_start_date={prod_date}&prod_end_date={prod_date}")
        self.assertEqual(res_p.status_code, 200)
        self.assertEqual(len(res_p.context['page_prod']), 1)

        # Lọc ngày bảng Hoàn thiện
        res_f = self.client.get(f"{reverse('dashboard_finishing')}?fin_start_date={fin_date}&fin_end_date={fin_date}")
        self.assertEqual(res_f.status_code, 200)
        self.assertEqual(len(res_f.context['page_fin']), 1)

        # Lọc ngày trong tương lai -> Không có dữ liệu
        res_empty = self.client.get(f"{reverse('dashboard_prod')}?prod_start_date=2099-01-01&prod_end_date=2099-12-31")
        self.assertEqual(res_empty.status_code, 200)
        self.assertEqual(len(res_empty.context['page_prod']), 0)

    def test_dashboard_cumulative_running_totals(self):
        """
        Kiểm tra giá trị Ngày/Tổng luôn là tổng lũy kế đến thời điểm nhập của bản ghi đó:
        - Lần nhập 1: 300/300
        - Lần nhập 2: 200/500 (bản ghi 1 vẫn giữ nguyên 300/300, không bị cộng dồn thành 300/500)
        """
        self._login_as(self.premium_user)
        import datetime
        from Working.models import CutReport, FinishingReport, KcsReport

        # Xóa các report cũ để test độc lập
        CutReport.objects.all().delete()
        FinishingReport.objects.all().delete()
        KcsReport.objects.all().delete()

        today = datetime.date.today()

        # Tạo 2 báo cáo Cắt liên tiếp cho cùng mã hàng/màu
        cut1 = CutReport.objects.create(
            nguoi_nhap=self.premium_user,
            ngay_lam_viec=today,
            ma_hang="AT01",
            mau="Đỏ",
            cat_chinh=300,
            cat_lot=50,
            cat_mex=40,
            cat_bong=30
        )
        cut2 = CutReport.objects.create(
            nguoi_nhap=self.premium_user,
            ngay_lam_viec=today,
            ma_hang="AT01",
            mau="Đỏ",
            cat_chinh=200,
            cat_lot=100,
            cat_mex=60,
            cat_bong=70
        )

        # Tạo 2 báo cáo Hoàn thiện liên tiếp
        fin1 = FinishingReport.objects.create(
            nguoi_nhap=self.premium_user,
            ngay_lam_viec=today,
            ma_hang="AT01",
            mau="Đỏ",
            the_bai=100,
            gap_hang=80,
            treo_dong_thung=60
        )
        fin2 = FinishingReport.objects.create(
            nguoi_nhap=self.premium_user,
            ngay_lam_viec=today,
            ma_hang="AT01",
            mau="Đỏ",
            the_bai=150,
            gap_hang=120,
            treo_dong_thung=90
        )

        # Tạo 2 báo cáo KCS liên tiếp
        kcs1 = KcsReport.objects.create(
            nguoi_nhap=self.premium_user,
            ngay_lam_viec=today,
            ma_hang="AT01",
            mau="Đỏ",
            xuong=1,
            to=1,
            qua_tay=50,
            dat=45,
            loi=5,
            tong_dat=45
        )
        kcs2 = KcsReport.objects.create(
            nguoi_nhap=self.premium_user,
            ngay_lam_viec=today,
            ma_hang="AT01",
            mau="Đỏ",
            xuong=1,
            to=1,
            qua_tay=70,
            dat=65,
            loi=5,
            tong_dat=65
        )

        # Kiểm tra bảng Cắt
        res_cut = self.client.get(reverse('dashboard_cut'))
        self.assertEqual(res_cut.status_code, 200)
        cut_page = res_cut.context['page_cut']
        cut_dict = {row['row_id']: row for row in cut_page}
        # Bản ghi 1: Ngày 300 / Tổng 300
        self.assertEqual(cut_dict[cut1.id]['cat_chinh_ngay'], 300)
        self.assertEqual(cut_dict[cut1.id]['cat_chinh_tong'], 300)
        # Bản ghi 2: Ngày 200 / Tổng 500
        self.assertEqual(cut_dict[cut2.id]['cat_chinh_ngay'], 200)
        self.assertEqual(cut_dict[cut2.id]['cat_chinh_tong'], 500)

        # Kiểm tra bảng Hoàn thiện
        res_fin = self.client.get(reverse('dashboard_finishing'))
        self.assertEqual(res_fin.status_code, 200)
        fin_page = res_fin.context['page_fin']
        fin_dict = {row['row_id']: row for row in fin_page}
        # Bản ghi 1: 100 / 100
        self.assertEqual(fin_dict[fin1.id]['the_bai_ngay'], 100)
        self.assertEqual(fin_dict[fin1.id]['the_bai_tong'], 100)
        # Bản ghi 2: 150 / 250
        self.assertEqual(fin_dict[fin2.id]['the_bai_ngay'], 150)
        self.assertEqual(fin_dict[fin2.id]['the_bai_tong'], 250)

        # Kiểm tra bảng KCS
        res_kcs = self.client.get(reverse('dashboard_kcs'))
        self.assertEqual(res_kcs.status_code, 200)
        kcs_page = res_kcs.context['page_kcs']
        kcs_dict = {row['row_id']: row for row in kcs_page}
        # Bản ghi 1: 50 / 50
        self.assertEqual(kcs_dict[kcs1.id]['qua_tay_ngay'], 50)
        self.assertEqual(kcs_dict[kcs1.id]['qua_tay_tong'], 50)
        # Bản ghi 2: 70 / 120
        self.assertEqual(kcs_dict[kcs2.id]['qua_tay_ngay'], 70)
        self.assertEqual(kcs_dict[kcs2.id]['qua_tay_tong'], 120)

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
            'so_luong_ld': 15,
            'ma_hang': 'AT01',
            'mau': 'Đỏ',
            'co': 'N/A',
            'nhan_btp': 20,
            'vao_chuyen': 20,
            'giua_chuyen': 20,
            'ra_chuyen': 20,
            'thu_hoa': 20,
            'la_thanh_pham': 20,
            'nhap_hoan_thien': 20,
        })
        self.assertEqual(res_post.status_code, 200)
        self.assertTrue(res_post.context['success'])
        new_report = ProcessReport.objects.filter(to=2).first()
        self.assertIsNotNone(new_report)
        self.assertEqual(new_report.xuong, 2)
        self.assertEqual(new_report.so_luong_ld, 15)
        
        # Kiểm tra trang list hiển thị nút Sửa/Xóa cho bản ghi của chính người dùng
        res_list = self.client.get(reverse('list'))
        self.assertEqual(res_list.status_code, 200)
        self.assertIn("Thao tác", res_list.content.decode('utf-8'))
        self.assertIn(f"href=\"/edit/{new_report.id}/?next=/list/\"", res_list.content.decode('utf-8'))
        
        # PREMIUM cũng thấy
        self._login_as(self.premium_user)
        res_list_prem = self.client.get(reverse('list'))
        self.assertEqual(res_list_prem.status_code, 200)
        self.assertIn("Thao tác", res_list_prem.content.decode('utf-8'))

        # Đăng nhập lại BASIC để chạy tiếp luồng
        self._login_as(self.basic_user)

        # 2. Sửa bởi người tạo (BASIC) -> Chuyển về 'list'
        res_edit_basic = self.client.post(reverse('edit', args=[new_report.id]), {
            'ngay_lam_viec': today_str,
            'xuong': 3,
            'to': 2,
            'so_luong_ld': 25,
            'ma_hang': 'AT01',
            'mau': 'Đỏ',
            'co': 'N/A',
            'nhan_btp': 30,
            'vao_chuyen': 30,
            'giua_chuyen': 30,
            'ra_chuyen': 30,
            'thu_hoa': 30,
            'la_thanh_pham': 30,
            'nhap_hoan_thien': 30,
        })
        self.assertRedirects(res_edit_basic, reverse('list'))
        new_report.refresh_from_db()
        self.assertEqual(new_report.nhan_btp, 30)
        self.assertEqual(new_report.xuong, 3)
        self.assertEqual(new_report.so_luong_ld, 25)

        # 3. Sửa bởi PREMIUM -> Chuyển về 'dashboard_prod'
        self._login_as(self.premium_user)
        res_edit_prem = self.client.post(reverse('edit', args=[new_report.id]), {
            'ngay_lam_viec': today_str,
            'xuong': 3,
            'to': 2,
            'so_luong_ld': 35,
            'ma_hang': 'AT01',
            'mau': 'Đỏ',
            'co': 'N/A',
            'nhan_btp': 50,
            'vao_chuyen': 50,
            'giua_chuyen': 50,
            'ra_chuyen': 50,
            'thu_hoa': 50,
            'la_thanh_pham': 50,
            'nhap_hoan_thien': 50,
        })
        self.assertRedirects(res_edit_prem, reverse('dashboard_prod'))
        new_report.refresh_from_db()
        self.assertEqual(new_report.nhan_btp, 50)
        self.assertEqual(new_report.so_luong_ld, 35)

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

        # 5. Xóa bởi PREMIUM -> Chuyển về 'dashboard_prod'
        self._login_as(self.premium_user)
        res_del = self.client.post(reverse('delete_report', args=[new_report.id]))
        self.assertRedirects(res_del, reverse('dashboard_prod'))
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
            'the_bai': 15,
            'gap_hang': 15,
            'treo_dong_thung': 15,
        })
        self.assertEqual(res_post.status_code, 200)
        self.assertTrue(res_post.context['success'])
        new_fin = FinishingReport.objects.filter(the_bai=15).first()
        self.assertIsNotNone(new_fin)
        
        # Kiểm tra trang finishing_list hiển thị nút Sửa/Xóa cho bản ghi của chính người dùng
        res_fin_list = self.client.get(reverse('finishing_list'))
        self.assertEqual(res_fin_list.status_code, 200)
        self.assertIn("Thao tác", res_fin_list.content.decode('utf-8'))
        self.assertIn(f"href=\"/finishing/edit/{new_fin.id}/?next=/finishing/list/\"", res_fin_list.content.decode('utf-8'))
        
        # PREMIUM và QUAN_LY cũng thấy
        self._login_as(self.premium_user)
        res_fin_list_prem = self.client.get(reverse('finishing_list'))
        self.assertEqual(res_fin_list_prem.status_code, 200)
        self.assertIn("Thao tác", res_fin_list_prem.content.decode('utf-8'))

        self._login_as(self.quanly_user)
        res_fin_list_quanly = self.client.get(reverse('finishing_list'))
        self.assertEqual(res_fin_list_quanly.status_code, 200)
        self.assertIn("Thao tác", res_fin_list_quanly.content.decode('utf-8'))



        
        # Đăng nhập lại HOAN_THIEN để chạy tiếp luồng
        self._login_as(self.finishing_user)

        # 2. Sửa bởi người tạo (HOAN_THIEN) -> Chuyển về 'finishing_list'
        res_edit_fin = self.client.post(reverse('finishing_edit', args=[new_fin.id]), {
            'ngay_lam_viec': today_str,
            'ma_hang': 'AT01',
            'mau': 'Đỏ',
            'the_bai': 25,
            'gap_hang': 25,
            'treo_dong_thung': 25,
        })
        self.assertRedirects(res_edit_fin, reverse('finishing_list'))
        new_fin.refresh_from_db()
        self.assertEqual(new_fin.the_bai, 25)

        # 3. Sửa bởi PREMIUM -> Chuyển về 'dashboard_finishing'
        self._login_as(self.premium_user)
        res_edit_prem = self.client.post(reverse('finishing_edit', args=[new_fin.id]), {
            'ngay_lam_viec': today_str,
            'ma_hang': 'AT01',
            'mau': 'Đỏ',
            'the_bai': 35,
            'gap_hang': 35,
            'treo_dong_thung': 35,
        })
        self.assertRedirects(res_edit_prem, reverse('dashboard_finishing'))
        new_fin.refresh_from_db()
        self.assertEqual(new_fin.the_bai, 35)

        # 4. Người khác không có quyền sửa (BASIC) -> 403
        self._login_as(self.basic_user)
        res_denied = self.client.post(reverse('finishing_edit', args=[new_fin.id]), {
            'ngay_lam_viec': today_str,
            'ma_hang': 'AT01',
            'mau': 'Đỏ',
        })
        self.assertEqual(res_denied.status_code, 403)

        # 5. Xóa bởi PREMIUM -> Chuyển về 'dashboard_finishing'
        self._login_as(self.premium_user)
        res_del = self.client.post(reverse('finishing_delete_report', args=[new_fin.id]))
        self.assertRedirects(res_del, reverse('dashboard_finishing'))
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

        # 4. Xuất Excel KCS
        res_kcs = self.client.get(reverse('kcs_export_excel'))
        self.assertEqual(res_kcs.status_code, 200)
        self.assertEqual(res_kcs['Content-Type'], "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        # 5. Xuất Excel Cắt
        res_cut = self.client.get(reverse('cut_export_excel'))
        self.assertEqual(res_cut.status_code, 200)
        self.assertEqual(res_cut['Content-Type'], "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    def test_cut_and_kcs_crud_flows(self):
        # 1. Tạo user NHA_CAT và KCS
        cut_user = AppUser.objects.create(account="cut_staff", password="123", name="NV Cắt", role="NHA_CAT", is_approved=True)
        kcs_user = AppUser.objects.create(account="kcs_staff", password="123", name="NV KCS", role="KCS", is_approved=True)
        today_str = datetime.date.today().strftime('%Y-%m-%d')

        # 2. Test Quản lý nhập dữ liệu Cắt và KCS
        self._login_as(self.quanly_user)
        res_cut_ql = self.client.post(reverse('cut_web'), {
            'ngay_lam_viec': today_str,
            'ma_hang': 'AT01',
            'mau': 'Đỏ',
            'cat_chinh': 50,
            'cat_lot': 40,
            'cat_mex': 30,
            'cat_bong': 20,
        })
        self.assertEqual(res_cut_ql.status_code, 200)
        self.assertTrue(res_cut_ql.context.get('success', False))
        self.assertEqual(CutReport.objects.filter(nguoi_nhap=self.quanly_user).count(), 1)

        res_kcs_ql = self.client.post(reverse('kcs_web'), {
            'ngay_lam_viec': today_str,
            'xuong': 1,
            'to': 2,
            'ma_hang': 'AT01',
            'mau': 'Đỏ',
            'qua_tay': 15,
            'dat': 14,
            'loi': 1,
            'tong_dat': 14,
        })
        self.assertEqual(res_kcs_ql.status_code, 200)
        self.assertTrue(res_kcs_ql.context.get('success', False))
        self.assertEqual(KcsReport.objects.filter(nguoi_nhap=self.quanly_user).count(), 1)

        # 3. Test NV Cắt nhập dữ liệu và xem list
        self._login_as(cut_user)
        res_cut_post = self.client.post(reverse('cut_web'), {
            'ngay_lam_viec': today_str,
            'ma_hang': 'AT01',
            'mau': 'Đỏ',
            'cat_chinh': 100,
            'cat_lot': 100,
            'cat_mex': 100,
            'cat_bong': 100,
        })
        self.assertEqual(res_cut_post.status_code, 200)
        self.assertTrue(res_cut_post.context.get('success', False))
        cut_report = CutReport.objects.filter(nguoi_nhap=cut_user).first()
        self.assertIsNotNone(cut_report)

        res_cut_list = self.client.get(reverse('cut_list'))
        self.assertEqual(res_cut_list.status_code, 200)

        # 4. Test Sửa dữ liệu Cắt
        res_cut_edit = self.client.post(reverse('cut_edit', args=[cut_report.id]), {
            'ngay_lam_viec': today_str,
            'ma_hang': 'AT01',
            'mau': 'Đỏ',
            'cat_chinh': 120,
            'cat_lot': 110,
            'cat_mex': 105,
            'cat_bong': 100,
        })
        self.assertRedirects(res_cut_edit, reverse('cut_list'))
        cut_report.refresh_from_db()
        self.assertEqual(cut_report.cat_chinh, 120)

        # 5. Test Xóa dữ liệu Cắt
        res_cut_del = self.client.post(reverse('cut_delete_report', args=[cut_report.id]))
        self.assertRedirects(res_cut_del, reverse('cut_list'))
        self.assertFalse(CutReport.objects.filter(id=cut_report.id).exists())

        # 6. Test NV KCS nhập dữ liệu và xem list
        self._login_as(kcs_user)
        res_kcs_post = self.client.post(reverse('kcs_web'), {
            'ngay_lam_viec': today_str,
            'xuong': 1,
            'to': 1,
            'ma_hang': 'AT01',
            'mau': 'Đỏ',
            'qua_tay': 50,
            'dat': 48,
            'loi': 2,
            'tong_dat': 48,
        })
        self.assertEqual(res_kcs_post.status_code, 200)
        self.assertTrue(res_kcs_post.context.get('success', False))
        kcs_report = KcsReport.objects.filter(nguoi_nhap=kcs_user).first()
        self.assertIsNotNone(kcs_report)

        res_kcs_list = self.client.get(reverse('kcs_list'))
        self.assertEqual(res_kcs_list.status_code, 200)

        # 7. Test Sửa dữ liệu KCS
        res_kcs_edit = self.client.post(reverse('kcs_edit', args=[kcs_report.id]), {
            'ngay_lam_viec': today_str,
            'xuong': 1,
            'to': 1,
            'ma_hang': 'AT01',
            'mau': 'Đỏ',
            'qua_tay': 60,
            'dat': 58,
            'loi': 2,
            'tong_dat': 58,
        })
        self.assertRedirects(res_kcs_edit, reverse('kcs_list'))
        kcs_report.refresh_from_db()
        self.assertEqual(kcs_report.qua_tay, 60)

        # 8. Test Xóa dữ liệu KCS
        res_kcs_del = self.client.post(reverse('kcs_delete_report', args=[kcs_report.id]))
        self.assertRedirects(res_kcs_del, reverse('kcs_list'))
        self.assertFalse(KcsReport.objects.filter(id=kcs_report.id).exists())

    def test_dashboard_server_side_column_filters(self):
        self._login_as(self.premium_user)
        today = datetime.date.today()

        # Tạo 60 báo cáo Cắt: 35 cho AT01, 25 cho AT02 -> 2 trang (50, 10)
        CutReport.objects.all().delete()
        for i in range(35):
            CutReport.objects.create(
                ngay_lam_viec=today,
                ma_hang="AT01",
                mau="Đỏ" if i % 2 == 0 else "Xanh",
                cat_chinh=10,
                cat_lot=10,
                cat_mex=10,
                cat_bong=10,
                nguoi_nhap=self.premium_user
            )
        for i in range(25):
            CutReport.objects.create(
                ngay_lam_viec=today,
                ma_hang="AT02",
                mau="Vàng",
                cat_chinh=20,
                cat_lot=20,
                cat_mex=20,
                cat_bong=20,
                nguoi_nhap=self.quanly_user
            )

        # 1. Chưa lọc: tổng 60 bản ghi -> 2 trang (50, 10)
        res_no_filter = self.client.get(reverse('dashboard_cut'))
        self.assertEqual(res_no_filter.status_code, 200)
        page_cut = res_no_filter.context['page_cut']
        self.assertEqual(page_cut.paginator.count, 60)
        self.assertEqual(page_cut.paginator.per_page, 50)
        self.assertEqual(page_cut.paginator.num_pages, 2)
        self.assertEqual(len(page_cut.object_list), 50)

        # 2. Lọc cột Mã hàng = AT01: 35 bản ghi -> 1 trang (35)
        res_filter_at01 = self.client.get(reverse('dashboard_cut') + '?cut_filter_ma_hang=AT01')
        self.assertEqual(res_filter_at01.status_code, 200)
        page_cut_filtered = res_filter_at01.context['page_cut']
        self.assertEqual(page_cut_filtered.paginator.count, 35)
        self.assertEqual(page_cut_filtered.paginator.num_pages, 1)
        self.assertEqual(len(page_cut_filtered.object_list), 35)
        for row in page_cut_filtered.object_list:
            self.assertEqual(row['ma_hang'], 'AT01')

        # 3. Sang trang 2 không lọc
        res_page2 = self.client.get(reverse('dashboard_cut') + '?p4=2')
        self.assertEqual(res_page2.status_code, 200)
        page_cut_p2 = res_page2.context['page_cut']
        self.assertEqual(page_cut_p2.number, 2)
        self.assertEqual(len(page_cut_p2.object_list), 10)

        # 4. Lọc kết hợp nhiều cột: Mã hàng = AT01 VÀ Màu = Đỏ (18 bản ghi -> 1 trang)
        res_multi_filter = self.client.get(reverse('dashboard_cut') + '?cut_filter_ma_hang=AT01&cut_filter_mau=%C4%90%E1%BB%8F')
        self.assertEqual(res_multi_filter.status_code, 200)
        page_cut_multi = res_multi_filter.context['page_cut']
        self.assertEqual(page_cut_multi.paginator.count, 18)
        self.assertEqual(page_cut_multi.paginator.num_pages, 1)
        for row in page_cut_multi.object_list:
            self.assertEqual(row['ma_hang'], 'AT01')
            self.assertEqual(row['mau'], 'Đỏ')

        # 5. Kiểm tra tính năng lọc liên tầng (Cascading Options) trong excel_filter_config
        res_cascade_at01 = self.client.get(reverse('dashboard_cut') + '?cut_filter_ma_hang=AT01')
        cfg_at01 = res_cascade_at01.context['excel_filter_config']['cut']['columns']
        self.assertIn('Đỏ', cfg_at01['4']['options'])
        self.assertIn('Xanh', cfg_at01['4']['options'])
        self.assertNotIn('Vàng', cfg_at01['4']['options'])

        res_cascade_red = self.client.get(reverse('dashboard_cut') + '?cut_filter_mau=%C4%90%E1%BB%8F')
        cfg_red = res_cascade_red.context['excel_filter_config']['cut']['columns']
        self.assertIn('AT01', cfg_red['3']['options'])
        self.assertNotIn('AT02', cfg_red['3']['options'])

        # 6. Test bảng Sản xuất (20 bản ghi) lọc theo Xưởng và Tổ
        ProcessReport.objects.all().delete()
        for i in range(12):
            ProcessReport.objects.create(
                ngay_lam_viec=today,
                xuong=1, to=1,
                ma_hang="AT01", mau="Đỏ", size="N/A",
                nhan_btp=10, vao_chuyen=10, giua_chuyen=10, ra_chuyen=10, thu_hoa=10, la_thanh_pham=10, nhap_hoan_thien=10,
                nguoi_nhap=self.basic_user
            )
        for i in range(8):
            ProcessReport.objects.create(
                ngay_lam_viec=today,
                xuong=2, to=2,
                ma_hang="AT02", mau="Xanh", size="N/A",
                nhan_btp=20, vao_chuyen=20, giua_chuyen=20, ra_chuyen=20, thu_hoa=20, la_thanh_pham=20, nhap_hoan_thien=20,
                nguoi_nhap=self.basic_user
            )
        res_prod_filter = self.client.get(reverse('dashboard_prod') + '?prod_filter_xuong=1&prod_filter_to=1')
        self.assertEqual(res_prod_filter.status_code, 200)
        page_prod = res_prod_filter.context['page_prod']
        self.assertEqual(page_prod.paginator.count, 12)
        self.assertEqual(page_prod.paginator.per_page, 50)
        self.assertEqual(len(page_prod.object_list), 12)

        # 7. Test bảng KCS (15 bản ghi) lọc theo Mã hàng và Xưởng
        KcsReport.objects.all().delete()
        for i in range(15):
            KcsReport.objects.create(
                ngay_lam_viec=today,
                xuong=1 if i < 10 else 2,
                to=1,
                ma_hang="AT01", mau="Đỏ", size="N/A",
                qua_tay=10, dat=10, loi=0, tong_dat=10,
                nguoi_nhap=self.quanly_user
            )
        res_kcs_filter = self.client.get(reverse('dashboard_kcs') + '?kcs_filter_xuong=1')
        self.assertEqual(res_kcs_filter.status_code, 200)
        page_kcs = res_kcs_filter.context['page_kcs']
        self.assertEqual(page_kcs.paginator.count, 10)
        self.assertEqual(page_kcs.paginator.per_page, 50)

        # 8. Test bảng Hoàn thiện (18 bản ghi) lọc theo Màu
        FinishingReport.objects.all().delete()
        for i in range(18):
            FinishingReport.objects.create(
                ngay_lam_viec=today,
                ma_hang="AT01", mau="Đỏ" if i < 14 else "Xanh", size="N/A",
                the_bai=10, gap_hang=10, treo_dong_thung=10,
                nguoi_nhap=self.finishing_user
            )
        res_fin_filter = self.client.get(reverse('dashboard_finishing') + '?fin_filter_mau=%C4%90%E1%BB%8F')
        self.assertEqual(res_fin_filter.status_code, 200)
        page_fin = res_fin_filter.context['page_fin']
        self.assertEqual(page_fin.paginator.count, 14)
        self.assertEqual(page_fin.paginator.per_page, 50)
        self.assertEqual(len(page_fin.object_list), 14)

    def test_tracking_view_with_column_filters(self):
        self._login_as(self.premium_user)
        # Tạo thêm sản phẩm và màu
        p2 = Product.objects.create(name="SM02")
        ProductColor.objects.create(product=p2, name="Trắng", quantity=150)
        ProductColor.objects.create(product=p2, name="Đen", quantity=120)

        # 1. Xem trang tracking không lọc
        res_tracking = self.client.get(reverse('tracking'))
        self.assertEqual(res_tracking.status_code, 200)
        page_tracking = res_tracking.context['tracking_data']
        # Tổng 4 dòng (AT01-Đỏ, AT01-Xanh, SM02-Trắng, SM02-Đen)
        self.assertEqual(len(page_tracking.object_list), 4)

        # 2. Lọc theo Mã hàng SM02
        res_filter_ma = self.client.get(reverse('tracking') + '?tracking_filter_ma_hang=SM02')
        self.assertEqual(res_filter_ma.status_code, 200)
        page_filtered = res_filter_ma.context['tracking_data']
        self.assertEqual(len(page_filtered.object_list), 2)
        for row in page_filtered.object_list:
            self.assertEqual(row['ma_hang'], 'SM02')

        # 3. Lọc theo Màu Đỏ
        res_filter_mau = self.client.get(reverse('tracking') + '?tracking_filter_mau=%C4%90%E1%BB%8F')
        self.assertEqual(res_filter_mau.status_code, 200)
        page_filtered_mau = res_filter_mau.context['tracking_data']
        self.assertEqual(len(page_filtered_mau.object_list), 1)
        self.assertEqual(page_filtered_mau.object_list[0]['ma_hang'], 'AT01')
        self.assertEqual(page_filtered_mau.object_list[0]['mau'], 'Đỏ')

        # 4. Test Xuất Excel tracking có lọc
        res_export = self.client.get(reverse('tracking_export_excel') + '?tracking_filter_ma_hang=SM02')
        self.assertEqual(res_export.status_code, 200)
        self.assertEqual(res_export['Content-Type'], 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


