import datetime
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from Working.models import (
    AppUser,
    Product,
    ProductColor,
    ProductSize,
    CutReport,
    ProcessReport,
    KcsReport,
    FinishingReport,
    DefectReturnReport,
    SampleTakeReport
)

class WorkingAPITestCase(APITestCase):
    def setUp(self):
        self.premium_user = AppUser.objects.create(
            account="admin1",
            password="password123",
            name="Admin",
            role="PREMIUM",
            is_approved=True
        )
        self.basic_user = AppUser.objects.create(
            account="basic1",
            password="password123",
            name="Basic Worker",
            role="BASIC",
            is_approved=True
        )
        self.cut_user = AppUser.objects.create(
            account="cut1",
            password="password123",
            name="Cut Worker",
            role="NHA_CAT",
            is_approved=True
        )
        self.finishing_user = AppUser.objects.create(
            account="finishing1",
            password="password123",
            name="Finishing Worker",
            role="HOAN_THIEN",
            is_approved=True
        )
        self.quan_ly_user = AppUser.objects.create(
            account="quanly1",
            password="password123",
            name="Manager",
            role="QUAN_LY",
            is_approved=True
        )
        self.ke_toan_user = AppUser.objects.create(
            account="ketoan1",
            password="password123",
            name="Accountant",
            role="KE_TOAN",
            is_approved=True
        )
        self.kcs_user = AppUser.objects.create(
            account="kcs1",
            password="password123",
            name="KCS Worker",
            role="KCS",
            is_approved=True
        )
        self.kho_user = AppUser.objects.create(
            account="kho1",
            password="password123",
            name="Warehouse Worker",
            role="KHO",
            is_approved=True
        )

        self.login_url = reverse('api:token_obtain_pair')

    def _get_token(self, account, password):
        resp = self.client.post(self.login_url, {"account": account, "password": password})
        return resp.data['access']

    def test_product_config_crud_permissions(self):
        admin_token = self._get_token('admin1', 'password123')
        basic_token = self._get_token('basic1', 'password123')

        # Admin can create product
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + admin_token)
        url = reverse('api:config-products-list')
        resp = self.client.post(url, {"name": "Test Product"})
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # Basic cannot create product
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + basic_token)
        resp = self.client.post(url, {"name": "Test Product 2"})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        # Basic can read product
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_tracking_report_creation_and_owner_isolation(self):
        cut_token = self._get_token('cut1', 'password123')
        basic_token = self._get_token('basic1', 'password123')

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + cut_token)
        url = reverse('api:reports-cut-list')
        resp = self.client.post(url, {
            "ngay_lam_viec": datetime.date.today(),
            "ma_hang": "A",
            "mau": "Red",
            "size": "M",
            "cat_chinh": 100
        })
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        cut_report_id = resp.data['id']

        # Verify nguoi_nhap is automatically set to cut_user
        report = CutReport.objects.get(id=cut_report_id)
        self.assertEqual(report.nguoi_nhap.id, self.cut_user.id)

        # Try to edit as basic worker (should fail)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + basic_token)
        url_detail = reverse('api:reports-cut-detail', args=[cut_report_id])
        resp = self.client.patch(url_detail, {"cat_chinh": 200})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        # Try to edit as the owner (should pass)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + cut_token)
        resp = self.client.patch(url_detail, {"cat_chinh": 200})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        
        # Admin can also edit
        admin_token = self._get_token('admin1', 'password123')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + admin_token)
        resp = self.client.patch(url_detail, {"cat_chinh": 300})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_defect_receive_action(self):
        finishing_token = self._get_token('finishing1', 'password123')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + finishing_token)
        
        # Create a defect return
        url = reverse('api:exceptions-defects-list')
        resp = self.client.post(url, {
            "ngay_tra": datetime.date.today(),
            "ma_hang": "A",
            "mau": "Red",
            "so_luong_tra": 10
        })
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        defect_id = resp.data['id']
        
        # Receive action
        receive_url = reverse('api:exceptions-defects-receive', args=[defect_id])
        
        # Try receiving 15 (exceeds 10)
        resp = self.client.post(receive_url, {"quantity": 15})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Try receiving 4 (valid)
        resp = self.client.post(receive_url, {"quantity": 4, "ghi_chu": "Lần 1"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['so_luong_nhan_lai'], 4)
        
        # Try receiving 7 (exceeds remaining 6)
        resp = self.client.post(receive_url, {"quantity": 7})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_dashboard_access(self):
        admin_token = self._get_token('admin1', 'password123')
        basic_token = self._get_token('basic1', 'password123')
        
        url = reverse('api:dashboard-cut')
        
        # Basic worker cannot see dashboard
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + basic_token)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        
        # Admin can see dashboard
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + admin_token)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_appuser_security(self):
        admin_token = self._get_token('admin1', 'password123')
        
        # Test that user list does not expose passwords
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + admin_token)
        url = reverse('api:users-list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        
        if len(resp.data.get('results', [])) > 0:
            first_user = resp.data['results'][0]
            self.assertNotIn('password', first_user)
            
        # Test modifying sensitive fields by non-admin
        basic_token = self._get_token('basic1', 'password123')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + basic_token)
        url_detail = reverse('api:users-detail', args=[self.basic_user.id])
        resp = self.client.patch(url_detail, {"role": "PREMIUM", "is_approved": True})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN) # Basic cannot access users endpoint

    def test_strict_role_isolation_for_creation(self):
        basic_token = self._get_token('basic1', 'password123')
        
        # Basic worker tries to create CutReport (should fail, needs NHA_CAT)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + basic_token)
        url = reverse('api:reports-cut-list')
        resp = self.client.post(url, {
            "ngay_lam_viec": datetime.date.today(),
            "ma_hang": "B",
            "mau": "Blue",
            "size": "M",
            "cat_chinh": 10
        })
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_nguoi_nhap_spoofing(self):
        cut_token = self._get_token('cut1', 'password123')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + cut_token)
        url = reverse('api:reports-cut-list')
        resp = self.client.post(url, {
            "ngay_lam_viec": datetime.date.today(),
            "ma_hang": "C",
            "mau": "Green",
            "size": "M",
            "cat_chinh": 10,
            "nguoi_nhap": self.admin_user.id if hasattr(self, 'admin_user') else self.premium_user.id
        })
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        cut_report_id = resp.data['id']
        
        # Verify nguoi_nhap is the actual authenticated user, NOT the spoofed one
        report = CutReport.objects.get(id=cut_report_id)
        self.assertEqual(report.nguoi_nhap.id, self.cut_user.id)

    def test_dashboard_permissions_and_ke_toan_access(self):
        """
        GAP-PROD-02 & Section 12/23:
        Verify all 5 dashboard endpoints reject unauthenticated (401),
        allow PREMIUM, QUAN_LY, and KE_TOAN (200),
        and reject worker roles BASIC, KHO, NHA_CAT, KCS, HOAN_THIEN (403).
        """
        dashboard_urls = [
            reverse('api:dashboard-cut'),
            reverse('api:dashboard-process'),
            reverse('api:dashboard-kcs'),
            reverse('api:dashboard-finishing'),
            reverse('api:dashboard-tracking'),
        ]

        # 1. Unauthenticated -> 401
        self.client.credentials()
        for url in dashboard_urls:
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED, f"Unauthenticated should get 401 on {url}")

        # 2. Authorized roles -> 200
        authorized_users = [
            ('admin1', 'PREMIUM'),
            ('quanly1', 'QUAN_LY'),
            ('ketoan1', 'KE_TOAN'),
        ]
        for account, role_name in authorized_users:
            token = self._get_token(account, 'password123')
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
            for url in dashboard_urls:
                resp = self.client.get(url)
                self.assertEqual(
                    resp.status_code,
                    status.HTTP_200_OK,
                    f"Role {role_name} should get 200 on {url}, got {resp.status_code}"
                )

        # 3. Unauthorized worker roles -> 403
        unauthorized_users = [
            ('basic1', 'BASIC'),
            ('kho1', 'KHO'),
            ('cut1', 'NHA_CAT'),
            ('kcs1', 'KCS'),
            ('finishing1', 'HOAN_THIEN'),
        ]
        for account, role_name in unauthorized_users:
            token = self._get_token(account, 'password123')
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
            for url in dashboard_urls:
                resp = self.client.get(url)
                self.assertEqual(
                    resp.status_code,
                    status.HTTP_403_FORBIDDEN,
                    f"Role {role_name} should get 403 on {url}, got {resp.status_code}"
                )

    def test_tracking_dashboard_data_shape_and_calculations(self):
        """
        GAP-PROD-01 & Section 23:
        Verify tracking API data shape, 7 stages, order quantities, completed values,
        and remaining calculations including negative balances.
        """
        p1 = Product.objects.create(name="TRACK_PROD_1")
        c1 = ProductColor.objects.create(product=p1, name="Do", quantity=1000)
        c2 = ProductColor.objects.create(product=p1, name="Xanh", quantity=500)

        # Process report exceeding order quantity for Do: nhan_btp = 600 + 500 = 1100 > 1000
        ProcessReport.objects.create(
            nguoi_nhap=self.basic_user,
            ngay_lam_viec=datetime.date.today(),
            ma_hang="TRACK_PROD_1",
            mau="Do",
            xuong=1,
            to=1,
            nhan_btp=600,
            vao_chuyen=550,
            giua_chuyen=500,
            ra_chuyen=450,
            thu_hoa=400,
            la_thanh_pham=350,
            nhap_hoan_thien=300
        )
        ProcessReport.objects.create(
            nguoi_nhap=self.basic_user,
            ngay_lam_viec=datetime.date.today(),
            ma_hang="TRACK_PROD_1",
            mau="Do",
            xuong=1,
            to=2,
            nhan_btp=500,
            vao_chuyen=400,
            giua_chuyen=300,
            ra_chuyen=200,
            thu_hoa=100,
            la_thanh_pham=50,
            nhap_hoan_thien=20
        )

        admin_token = self._get_token('admin1', 'password123')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + admin_token)
        url = reverse('api:dashboard-tracking')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # Locate the specific item in tracking data
        items = [i for i in resp.data if i['ma_hang'] == "TRACK_PROD_1" and i['mau'] == "Do"]
        self.assertEqual(len(items), 1)
        item = items[0]

        # Verify order quantity
        self.assertEqual(item['so_luong'], 1000)

        # Stage 1: nhan_btp -> lam = 1100, con = 1000 - 1100 = -100 (negative balance verified)
        self.assertEqual(item['nhan_btp']['lam'], 1100)
        self.assertEqual(item['nhan_btp']['con'], -100)

        # Stage 2: vao_chuyen -> lam = 950, con = 50
        self.assertEqual(item['vao_chuyen']['lam'], 950)
        self.assertEqual(item['vao_chuyen']['con'], 50)

        # Stage 3: giua_chuyen -> lam = 800, con = 200
        self.assertEqual(item['giua_chuyen']['lam'], 800)
        self.assertEqual(item['giua_chuyen']['con'], 200)

        # Stage 4: ra_chuyen -> lam = 650, con = 350
        self.assertEqual(item['ra_chuyen']['lam'], 650)
        self.assertEqual(item['ra_chuyen']['con'], 350)

        # Stage 5: thu_hoa -> lam = 500, con = 500
        self.assertEqual(item['thu_hoa']['lam'], 500)
        self.assertEqual(item['thu_hoa']['con'], 500)

        # Stage 6: la_thanh_pham -> lam = 400, con = 600
        self.assertEqual(item['la_thanh_pham']['lam'], 400)
        self.assertEqual(item['la_thanh_pham']['con'], 600)

        # Stage 7: nhap_hoan_thien -> lam = 320, con = 680
        self.assertEqual(item['nhap_hoan_thien']['lam'], 320)
        self.assertEqual(item['nhap_hoan_thien']['con'], 680)

        # Verify legacy flat keys compatibility
        self.assertEqual(item['nhan_btp_nhap'], 1100)
        self.assertEqual(item['nhan_btp_con'], -100)
        self.assertEqual(item['nhap_hoan_thien_nhap'], 320)
        self.assertEqual(item['nhap_hoan_thien_con'], 680)

    def test_tracking_dashboard_filters(self):
        """
        Verify tracking API filtering by ma_hang, mau, and both.
        """
        p1 = Product.objects.create(name="FILTER_P1")
        ProductColor.objects.create(product=p1, name="Red", quantity=100)
        ProductColor.objects.create(product=p1, name="Blue", quantity=200)

        p2 = Product.objects.create(name="FILTER_P2")
        ProductColor.objects.create(product=p2, name="Red", quantity=300)

        admin_token = self._get_token('admin1', 'password123')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + admin_token)
        url = reverse('api:dashboard-tracking')

        # Filter by ma_hang
        resp = self.client.get(f"{url}?ma_hang=FILTER_P1")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        for item in resp.data:
            self.assertEqual(item['ma_hang'], "FILTER_P1")
        self.assertEqual({i['mau'] for i in resp.data}, {"Red", "Blue"})

        # Filter by mau
        resp = self.client.get(f"{url}?mau=Blue")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]['ma_hang'], "FILTER_P1")
        self.assertEqual(resp.data[0]['mau'], "Blue")

        # Filter by both ma_hang and mau
        resp = self.client.get(f"{url}?ma_hang=FILTER_P2&mau=Red")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]['ma_hang'], "FILTER_P2")
        self.assertEqual(resp.data[0]['mau'], "Red")

    def test_cumulative_totals_activity_log_cut(self):
        """
        GAP-PROD-03:
        Verify CutReport cumulative totals with ?with_totals=true
        and backwards compatibility when omitted.
        """
        p = Product.objects.create(name="CUMUL_CUT")
        ProductColor.objects.create(product=p, name="Navy", quantity=2000)

        # Create reports chronologically
        r1 = CutReport.objects.create(
            nguoi_nhap=self.cut_user,
            ngay_lam_viec=datetime.date(2026, 9, 1),
            ma_hang="CUMUL_CUT",
            mau="Navy",
            size="M",
            cat_chinh=100,
            cat_lot=80,
            cat_mex=50,
            cat_bong=40
        )
        r2 = CutReport.objects.create(
            nguoi_nhap=self.cut_user,
            ngay_lam_viec=datetime.date(2026, 9, 2),
            ma_hang="CUMUL_CUT",
            mau="Navy",
            size="M",
            cat_chinh=50,
            cat_lot=40,
            cat_mex=30,
            cat_bong=20
        )
        r3 = CutReport.objects.create(
            nguoi_nhap=self.cut_user,
            ngay_lam_viec=datetime.date(2026, 9, 3),
            ma_hang="CUMUL_CUT",
            mau="Navy",
            size="M",
            cat_chinh=25,
            cat_lot=20,
            cat_mex=10,
            cat_bong=5
        )

        admin_token = self._get_token('admin1', 'password123')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + admin_token)
        url = reverse('api:reports-cut-list')

        # 1. Without with_totals: standard response without cumulative fields
        resp = self.client.get(f"{url}?ma_hang=CUMUL_CUT")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        results = resp.data['results']
        self.assertGreaterEqual(len(results), 3)
        self.assertNotIn('cumulative', results[0])
        self.assertNotIn('tong_don_hang', results[0])

        # 2. With with_totals=true: contains cumulative fields and tong_don_hang
        resp_totals = self.client.get(f"{url}?ma_hang=CUMUL_CUT&with_totals=true")
        self.assertEqual(resp_totals.status_code, status.HTTP_200_OK)
        results_totals = {r['id']: r for r in resp_totals.data['results']}

        # Verify r1: cumulative = 100, 80, 50, 40
        data_r1 = results_totals[r1.id]
        self.assertEqual(data_r1['cumulative']['cat_chinh'], 100)
        self.assertEqual(data_r1['cumulative']['cat_lot'], 80)
        self.assertEqual(data_r1['cumulative']['cat_mex'], 50)
        self.assertEqual(data_r1['cumulative']['cat_bong'], 40)
        self.assertEqual(data_r1['tong_don_hang'], 2000)

        # Verify r2: cumulative = 150, 120, 80, 60
        data_r2 = results_totals[r2.id]
        self.assertEqual(data_r2['cumulative']['cat_chinh'], 150)
        self.assertEqual(data_r2['cumulative']['cat_lot'], 120)
        self.assertEqual(data_r2['cumulative']['cat_mex'], 80)
        self.assertEqual(data_r2['cumulative']['cat_bong'], 60)

        # Verify r3: cumulative = 175, 140, 90, 65
        data_r3 = results_totals[r3.id]
        self.assertEqual(data_r3['cumulative']['cat_chinh'], 175)
        self.assertEqual(data_r3['cumulative']['cat_lot'], 140)
        self.assertEqual(data_r3['cumulative']['cat_mex'], 90)
        self.assertEqual(data_r3['cumulative']['cat_bong'], 65)

    def test_cumulative_totals_activity_log_process(self):
        """
        GAP-PROD-03:
        Verify ProcessReport cumulative totals with grouping boundary (ma_hang, mau, xuong, to).
        """
        p = Product.objects.create(name="CUMUL_PROD")
        ProductColor.objects.create(product=p, name="Den", quantity=1500)

        # Group 1: (CUMUL_PROD, Den, X1, T1)
        r1 = ProcessReport.objects.create(
            nguoi_nhap=self.basic_user,
            ngay_lam_viec=datetime.date(2026, 9, 1),
            ma_hang="CUMUL_PROD",
            mau="Den",
            xuong=1,
            to=1,
            nhan_btp=100,
            vao_chuyen=90,
            giua_chuyen=80,
            ra_chuyen=70,
            thu_hoa=60,
            la_thanh_pham=50,
            nhap_hoan_thien=40
        )
        r2 = ProcessReport.objects.create(
            nguoi_nhap=self.basic_user,
            ngay_lam_viec=datetime.date(2026, 9, 2),
            ma_hang="CUMUL_PROD",
            mau="Den",
            xuong=1,
            to=1,
            nhan_btp=50,
            vao_chuyen=40,
            giua_chuyen=30,
            ra_chuyen=20,
            thu_hoa=10,
            la_thanh_pham=10,
            nhap_hoan_thien=10
        )

        # Group 2: different xuong -> (CUMUL_PROD, Den, X2, T1)
        r3 = ProcessReport.objects.create(
            nguoi_nhap=self.basic_user,
            ngay_lam_viec=datetime.date(2026, 9, 3),
            ma_hang="CUMUL_PROD",
            mau="Den",
            xuong=2,
            to=1,
            nhan_btp=30,
            vao_chuyen=25,
            giua_chuyen=20,
            ra_chuyen=15,
            thu_hoa=10,
            la_thanh_pham=5,
            nhap_hoan_thien=5
        )

        admin_token = self._get_token('admin1', 'password123')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + admin_token)
        url = reverse('api:reports-process-list')

        resp = self.client.get(f"{url}?ma_hang=CUMUL_PROD&with_totals=true")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        results = {r['id']: r for r in resp.data['results']}

        # r1
        self.assertEqual(results[r1.id]['cumulative']['nhan_btp'], 100)
        self.assertEqual(results[r1.id]['cumulative']['nhap_hoan_thien'], 40)

        # r2 (same group as r1) -> 100 + 50 = 150, 40 + 10 = 50
        self.assertEqual(results[r2.id]['cumulative']['nhan_btp'], 150)
        self.assertEqual(results[r2.id]['cumulative']['nhap_hoan_thien'], 50)

        # r3 (different group: X2) -> strictly 30 and 5 (does NOT accumulate with X1)
        self.assertEqual(results[r3.id]['cumulative']['nhan_btp'], 30)
        self.assertEqual(results[r3.id]['cumulative']['nhap_hoan_thien'], 5)

    def test_cumulative_totals_activity_log_kcs_and_finishing(self):
        """
        GAP-PROD-03:
        Verify KCS and Finishing reports cumulative totals with ?with_totals=true.
        """
        p = Product.objects.create(name="CUMUL_KF")
        ProductColor.objects.create(product=p, name="Trang", quantity=800)

        # KCS Reports
        k1 = KcsReport.objects.create(
            nguoi_nhap=self.kcs_user,
            ngay_lam_viec=datetime.date(2026, 9, 1),
            ma_hang="CUMUL_KF",
            mau="Trang",
            qua_tay=100,
            dat=90,
            loi=10,
            tong_dat=90
        )
        k2 = KcsReport.objects.create(
            nguoi_nhap=self.kcs_user,
            ngay_lam_viec=datetime.date(2026, 9, 2),
            ma_hang="CUMUL_KF",
            mau="Trang",
            qua_tay=60,
            dat=55,
            loi=5,
            tong_dat=55
        )

        # Finishing Reports
        f1 = FinishingReport.objects.create(
            nguoi_nhap=self.finishing_user,
            ngay_lam_viec=datetime.date(2026, 9, 1),
            ma_hang="CUMUL_KF",
            mau="Trang",
            the_bai=80,
            gap_hang=70,
            treo_dong_thung=60
        )
        f2 = FinishingReport.objects.create(
            nguoi_nhap=self.finishing_user,
            ngay_lam_viec=datetime.date(2026, 9, 2),
            ma_hang="CUMUL_KF",
            mau="Trang",
            the_bai=40,
            gap_hang=30,
            treo_dong_thung=20
        )

        admin_token = self._get_token('admin1', 'password123')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + admin_token)

        # Test KCS with totals
        kcs_url = reverse('api:reports-kcs-list')
        resp_kcs = self.client.get(f"{kcs_url}?ma_hang=CUMUL_KF&with_totals=true")
        self.assertEqual(resp_kcs.status_code, status.HTTP_200_OK)
        kcs_results = {r['id']: r for r in resp_kcs.data['results']}
        self.assertEqual(kcs_results[k1.id]['cumulative']['qua_tay'], 100)
        self.assertEqual(kcs_results[k1.id]['cumulative']['tong_dat'], 90)
        self.assertEqual(kcs_results[k2.id]['cumulative']['qua_tay'], 160)
        self.assertEqual(kcs_results[k2.id]['cumulative']['tong_dat'], 145)

        # Test Finishing with totals
        finishing_url = reverse('api:reports-finishing-list')
        resp_fin = self.client.get(f"{finishing_url}?ma_hang=CUMUL_KF&with_totals=true")
        self.assertEqual(resp_fin.status_code, status.HTTP_200_OK)
        fin_results = {r['id']: r for r in resp_fin.data['results']}
        self.assertEqual(fin_results[f1.id]['cumulative']['the_bai'], 80)
        self.assertEqual(fin_results[f1.id]['cumulative']['treo_dong_thung'], 60)
        self.assertEqual(fin_results[f2.id]['cumulative']['the_bai'], 120)
        self.assertEqual(fin_results[f2.id]['cumulative']['treo_dong_thung'], 80)
        self.assertEqual(fin_results[f2.id]['tong_don_hang'], 800)


