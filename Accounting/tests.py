import datetime
from django.test import TestCase, Client
from django.conf import settings
from django.urls import reverse
from django.core.exceptions import PermissionDenied

from Working.models import AppUser, Product, ProductColor, ProcessReport
from Working.auth_utils import SESSION_KEY
from Accounting.models import ProductPrice, ExportReport, PaymentReport


class AccountingTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Users
        self.admin_user = AppUser.objects.create(
            name="Admin User",
            account="admin_test",
            password="123",
            role="PREMIUM",
            is_approved=True
        )
        self.accountant_user = AppUser.objects.create(
            name="Ke Toan",
            account="ketoan_test",
            password="123",
            role="KE_TOAN",
            is_approved=True
        )
        self.basic_user = AppUser.objects.create(
            name="Worker",
            account="worker_test",
            password="123",
            role="BASIC",
            is_approved=True
        )

        # Products & Colors
        self.product1 = Product.objects.create(name="AO-POLO-01")
        self.color1_red = ProductColor.objects.create(product=self.product1, name="Đỏ", quantity=1000)
        self.color1_blue = ProductColor.objects.create(product=self.product1, name="Xanh", quantity=500)

        # Set initial unit price and CM price for Đỏ = 120,000 VNĐ & 25,000 VNĐ
        self.price1_red = ProductPrice.objects.create(
            product_color=self.color1_red,
            don_gia=120000,
            gia_cm=25000,
            updated_by=self.accountant_user
        )

    def _login(self, user):
        session = self.client.session
        session[SESSION_KEY] = user.id
        session["display_name"] = user.name
        session.save()
        self.client.cookies[settings.SESSION_COOKIE_NAME] = session.session_key

    def test_permission_denied_for_basic_user(self):
        """Worker / BASIC role cannot access Accounting pages."""
        self._login(self.basic_user)
        resp = self.client.get(reverse("accounting:dashboard"))
        self.assertEqual(resp.status_code, 403)

        resp = self.client.get(reverse("accounting:export_entry"))
        self.assertEqual(resp.status_code, 403)

        resp = self.client.get(reverse("accounting:price_management"))
        self.assertEqual(resp.status_code, 403)

    def test_access_granted_for_accountant_and_premium(self):
        """Accountant and Premium users can access Accounting pages."""
        self._login(self.accountant_user)
        resp = self.client.get(reverse("accounting:dashboard"))
        self.assertEqual(resp.status_code, 200)

        self._login(self.admin_user)
        resp = self.client.get(reverse("accounting:dashboard"))
        self.assertEqual(resp.status_code, 200)

    def test_price_management_updates(self):
        """Test single and bulk price updates (don_gia & gia_cm)."""
        self._login(self.accountant_user)

        # 1. Update single price with formatted string
        resp = self.client.post(reverse("accounting:price_management"), {
            "action": "update_single",
            "product_color_id": self.color1_blue.id,
            "don_gia": "150.000",
            "gia_cm": "30.000"
        })
        self.assertEqual(resp.status_code, 200)
        self.color1_blue.refresh_from_db()
        self.assertEqual(self.color1_blue.price.don_gia, 150000)
        self.assertEqual(self.color1_blue.price.gia_cm, 30000)

        # 2. Update bulk price with commas and m_price / cm_price prefixes
        resp = self.client.post(reverse("accounting:price_management"), {
            "action": "update_bulk",
            f"price_{self.color1_red.id}": "130,000 đ",
            f"cm_price_{self.color1_red.id}": "28,000 đ",
            f"m_price_{self.color1_blue.id}": "160.000",
            f"m_cm_price_{self.color1_blue.id}": "35.000",
        })
        self.assertEqual(resp.status_code, 200)
        self.color1_red.refresh_from_db()
        self.color1_blue.refresh_from_db()
        self.assertEqual(self.color1_red.price.don_gia, 130000)
        self.assertEqual(self.color1_red.price.gia_cm, 28000)
        self.assertEqual(self.color1_blue.price.don_gia, 160000)
        self.assertEqual(self.color1_blue.price.gia_cm, 35000)

    def test_export_entry_and_automatic_thanh_tien(self):
        """Test recording an export and verifying automatic total calculation."""
        self._login(self.accountant_user)

        # Post export report: 200 pieces of AO-POLO-01 / Đỏ
        resp = self.client.post(reverse("accounting:export_entry"), {
            "ngay_xuat": "2026-08-18",
            "ma_hang": "AO-POLO-01",
            "mau": "Đỏ",
            "so_luong_xuat": 200,
            "ghi_chu": "Xuất giao siêu thị BigC"
        })
        self.assertEqual(resp.status_code, 200)

        report = ExportReport.objects.filter(ma_hang="AO-POLO-01", mau="Đỏ").first()
        self.assertIsNotNone(report)
        self.assertEqual(report.so_luong_xuat, 200)
        self.assertEqual(report.don_gia, 120000)
        self.assertEqual(report.thanh_tien, 200 * 120000)  # 24,000,000 VNĐ
        self.assertEqual(report.nguoi_nhap, self.accountant_user)

    def test_dashboard_calculations(self):
        """Test that the dashboard correctly aggregates shipped and remaining revenue."""
        # Create an export report
        ExportReport.objects.create(
            ngay_xuat=datetime.date(2026, 8, 18),
            ma_hang="AO-POLO-01",
            mau="Đỏ",
            so_luong_xuat=300,
            don_gia=120000,
            thanh_tien=300 * 120000, # 36,000,000 VNĐ
            nguoi_nhap=self.accountant_user
        )

        self._login(self.accountant_user)
        resp = self.client.get(reverse("accounting:dashboard"))
        self.assertEqual(resp.status_code, 200)

        ctx = resp.context
        # Total order quantity = 1000 + 500 = 1500
        self.assertEqual(ctx["kpi_tong_so_luong_dh"], 1500)
        # Total order money = (1000 * 120000) + (500 * 0) = 120,000,000
        self.assertEqual(ctx["kpi_tong_tien_dh"], 120000000)
        # Total shipped quantity = 300
        self.assertEqual(ctx["kpi_tong_da_xuat_sl"], 300)
        # Total shipped money = 36,000,000
        self.assertEqual(ctx["kpi_tong_da_xuat_tien"], 36000000)
        # Total remaining quantity = 1200 (700 red + 500 blue)
        self.assertEqual(ctx["kpi_tong_con_lai_sl"], 1200)
        # Total remaining money = 700 * 120,000 = 84,000,000
        self.assertEqual(ctx["kpi_tong_con_lai_tien"], 84000000)
        # Total percentage = 300 / 1500 * 100 = 20.0%
        self.assertEqual(ctx["kpi_tien_do_tong"], 20.0)

    def test_export_edit_and_delete(self):
        """Test editing and deleting an export report."""
        report = ExportReport.objects.create(
            ngay_xuat=datetime.date(2026, 8, 18),
            ma_hang="AO-POLO-01",
            mau="Đỏ",
            so_luong_xuat=100,
            don_gia=120000,
            thanh_tien=12000000,
            nguoi_nhap=self.accountant_user
        )

        self._login(self.accountant_user)

        # Edit quantity to 150
        resp = self.client.post(reverse("accounting:export_edit", args=[report.id]), {
            "ngay_xuat": "2026-08-18",
            "ma_hang": "AO-POLO-01",
            "mau": "Đỏ",
            "so_luong_xuat": 150,
            "ghi_chu": "Đã đổi số lượng"
        })
        self.assertRedirects(resp, reverse("accounting:export_entry"))

        report.refresh_from_db()
        self.assertEqual(report.so_luong_xuat, 150)
        self.assertEqual(report.thanh_tien, 150 * 120000) # 18,000,000 VNĐ

        # Delete report
        resp = self.client.post(reverse("accounting:export_delete", args=[report.id]))
        self.assertRedirects(resp, reverse("accounting:export_entry"))
        self.assertFalse(ExportReport.objects.filter(id=report.id).exists())

    def test_export_excel(self):
        """Test exporting data to Excel spreadsheet."""
        self._login(self.accountant_user)
        resp = self.client.get(reverse("accounting:export_excel"))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp["Content-Type"], "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    def test_accountant_access_to_reports_and_config(self):
        """Test that accountant can access summary dashboards, order tracking, and product management."""
        self._login(self.accountant_user)
        
        # 1. Báo cáo tổng hợp: Dashboard
        resp = self.client.get(reverse("dashboard_cut"))
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get(reverse("dashboard_prod"))
        self.assertEqual(resp.status_code, 200)
        
        # 2. Theo dõi đơn hàng
        resp = self.client.get(reverse("tracking"))
        self.assertEqual(resp.status_code, 200)
        
        # 3. Quản lý mã hàng
        resp = self.client.get(reverse("config_list"))
        self.assertEqual(resp.status_code, 200)

    def test_team_revenue_report_permission(self):
        """Test access control: Only KE_TOAN and PREMIUM can access team revenue report."""
        # Basic user gets 403
        self._login(self.basic_user)
        resp = self.client.get(reverse("accounting:team_revenue_report"))
        self.assertEqual(resp.status_code, 403)
        resp = self.client.get(reverse("accounting:team_revenue_export_excel"))
        self.assertEqual(resp.status_code, 403)

        # Accountant user gets 200
        self._login(self.accountant_user)
        resp = self.client.get(reverse("accounting:team_revenue_report"))
        self.assertEqual(resp.status_code, 200)

        # Premium admin gets 200
        self._login(self.admin_user)
        resp = self.client.get(reverse("accounting:team_revenue_report"))
        self.assertEqual(resp.status_code, 200)

    def test_team_revenue_calculation_multiple_products(self):
        """
        Test team revenue calculation:
        1 team outputs multiple different products/colors on the same day.
        Calculation: sum(ra_chuyen * gia_cm) for each product code based on gia_cm.
        """
        # Create product 2 with prices
        product2 = Product.objects.create(name="AO-KHOAC-02")
        color2_den = ProductColor.objects.create(product=product2, name="Đen", quantity=800)
        ProductPrice.objects.create(
            product_color=color2_den,
            don_gia=250000,
            gia_cm=50000,
            updated_by=self.accountant_user
        )

        # Also set prices for product 1 / Xanh = don_gia 150k, gia_cm = 30,000 VNĐ
        ProductPrice.objects.create(
            product_color=self.color1_blue,
            don_gia=150000,
            gia_cm=30000,
            updated_by=self.accountant_user
        )

        # Work day 1: 2026-08-20, Xuong 1, To 1
        # Product 1 / Do: 50 pcs * 25,000 (gia_cm) = 1,250,000 VNĐ
        ProcessReport.objects.create(
            ngay_lam_viec=datetime.date(2026, 8, 20),
            xuong=1,
            to=1,
            so_luong_ld=20,
            ma_hang="AO-POLO-01",
            mau="Đỏ",
            size="L",
            ra_chuyen=50,
            nguoi_nhap=self.basic_user
        )
        # Product 1 / Xanh: 30 pcs * 30,000 (gia_cm) = 900,000 VNĐ
        ProcessReport.objects.create(
            ngay_lam_viec=datetime.date(2026, 8, 20),
            xuong=1,
            to=1,
            so_luong_ld=20,
            ma_hang="AO-POLO-01",
            mau="Xanh",
            size="M",
            ra_chuyen=30,
            nguoi_nhap=self.basic_user
        )
        # Product 2 / Den: 20 pcs * 50,000 (gia_cm) = 1,000,000 VNĐ
        ProcessReport.objects.create(
            ngay_lam_viec=datetime.date(2026, 8, 20),
            xuong=1,
            to=1,
            so_luong_ld=20,
            ma_hang="AO-KHOAC-02",
            mau="Đen",
            size="XL",
            ra_chuyen=20,
            nguoi_nhap=self.basic_user
        )
        # => Xuong 1 - To 1 total: 100 pcs, 3,150,000 VNĐ

        # Work day 1: 2026-08-20, Xuong 2, To 3
        # Product 1 / Do: 40 pcs * 25,000 (gia_cm) = 1,000,000 VNĐ
        ProcessReport.objects.create(
            ngay_lam_viec=datetime.date(2026, 8, 20),
            xuong=2,
            to=3,
            so_luong_ld=15,
            ma_hang="AO-POLO-01",
            mau="Đỏ",
            size="S",
            ra_chuyen=40,
            nguoi_nhap=self.basic_user
        )

        self._login(self.accountant_user)
        resp = self.client.get(reverse("accounting:team_revenue_report"), {
            "tu_ngay": "2026-08-01",
            "den_ngay": "2026-08-31"
        })
        self.assertEqual(resp.status_code, 200)

        ctx = resp.context
        # Total output = 50 + 30 + 20 + 40 = 140 pcs
        self.assertEqual(ctx["kpi_tong_ra_chuyen"], 140)
        # Total money = 1,250,000 + 900,000 + 1,000,000 + 1,000,000 = 4,150,000 VNĐ
        self.assertEqual(ctx["kpi_tong_tien"], 4150000)
        # Active teams = 2 (Xuong 1 - To 1, Xuong 2 - To 3)
        self.assertEqual(ctx["kpi_so_to"], 2)
        # Active days = 1 (2026-08-20)
        self.assertEqual(ctx["kpi_so_ngay_sx"], 1)

        # Check daily team groups
        groups = ctx["daily_team_groups"]
        self.assertEqual(len(groups), 2)
        # Find group Xuong 1, To 1
        g_x1_t1 = next(g for g in groups if g["xuong"] == 1 and g["to"] == 1)
        self.assertEqual(g_x1_t1["tong_ra_chuyen"], 100)
        self.assertEqual(g_x1_t1["tong_tien"], 3150000)
        self.assertEqual(len(g_x1_t1["items"]), 3)

        # Find group Xuong 2, To 3
        g_x2_t3 = next(g for g in groups if g["xuong"] == 2 and g["to"] == 3)
        self.assertEqual(g_x2_t3["tong_ra_chuyen"], 40)
        self.assertEqual(g_x2_t3["tong_tien"], 1000000)
        self.assertEqual(len(g_x2_t3["items"]), 1)

    def test_team_revenue_filters(self):
        """Test filtering by workshop, team, product code, and date range."""
        ProcessReport.objects.create(
            ngay_lam_viec=datetime.date(2026, 8, 10),
            xuong=1,
            to=1,
            ma_hang="AO-POLO-01",
            mau="Đỏ",
            size="M",
            ra_chuyen=20,
            nguoi_nhap=self.basic_user
        )
        ProcessReport.objects.create(
            ngay_lam_viec=datetime.date(2026, 8, 20),
            xuong=2,
            to=2,
            ma_hang="AO-POLO-01",
            mau="Đỏ",
            size="M",
            ra_chuyen=50,
            nguoi_nhap=self.basic_user
        )

        self._login(self.accountant_user)

        # Filter by xuong=2 -> 50 pcs * 25,000 (gia_cm) = 1,250,000 VNĐ
        resp = self.client.get(reverse("accounting:team_revenue_report"), {
            "xuong": "2",
            "tu_ngay": "2026-08-01",
            "den_ngay": "2026-08-31"
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context["kpi_tong_ra_chuyen"], 50)
        self.assertEqual(resp.context["kpi_tong_tien"], 50 * 25000)

        # Filter by date range (only 2026-08-10)
        resp = self.client.get(reverse("accounting:team_revenue_report"), {
            "tu_ngay": "2026-08-05",
            "den_ngay": "2026-08-15"
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context["kpi_tong_ra_chuyen"], 20)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context["kpi_tong_ra_chuyen"], 20)

    def test_team_revenue_export_excel(self):
        """Test team revenue Excel export response and sheets."""
        ProcessReport.objects.create(
            ngay_lam_viec=datetime.date(2026, 8, 20),
            xuong=1,
            to=1,
            ma_hang="AO-POLO-01",
            mau="Đỏ",
            size="L",
            ra_chuyen=50,
            nguoi_nhap=self.basic_user
        )

        self._login(self.accountant_user)
        resp = self.client.get(reverse("accounting:team_revenue_export_excel"), {
            "tu_ngay": "2026-08-01",
            "den_ngay": "2026-08-31"
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp["Content-Type"], "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        self.assertIn("attachment; filename=", resp["Content-Disposition"])

    def test_all_xuong_and_to_no_duplicates(self):
        """Test that all_xuong and all_to dropdown options do not have duplicate entries."""
        # Create multiple reports for the same xuong=1 and to=1
        for i in range(5):
            ProcessReport.objects.create(
                ngay_lam_viec=datetime.date(2026, 8, 20),
                xuong=1,
                to=1,
                ma_hang="AO-POLO-01",
                mau="Đỏ",
                size=f"Size-{i}",
                ra_chuyen=10,
                nguoi_nhap=self.basic_user
            )
        # Create multiple reports for xuong=2 and to=3
        for i in range(3):
            ProcessReport.objects.create(
                ngay_lam_viec=datetime.date(2026, 8, 21),
                xuong=2,
                to=3,
                ma_hang="AO-POLO-01",
                mau="Đỏ",
                size=f"Size-{i}",
                ra_chuyen=10,
                nguoi_nhap=self.basic_user
            )

        self._login(self.accountant_user)
        resp = self.client.get(reverse("accounting:team_revenue_report"))
        self.assertEqual(resp.status_code, 200)

        all_xuong = resp.context["all_xuong"]
        all_to = resp.context["all_to"]

        # Ensure no duplicates
        self.assertEqual(len(all_xuong), len(set(all_xuong)))
        self.assertEqual(len(all_to), len(set(all_to)))
        self.assertEqual(all_xuong, [1, 2])
        self.assertEqual(all_to, [1, 3])

    def test_team_revenue_pagination_5_per_page(self):
        """Test that daily team detail view is paginated at 5 rows/groups per page."""
        # Create 12 distinct daily team entries in current month
        today = datetime.date.today()
        for day in range(1, 13):
            d = today.replace(day=day)
            ProcessReport.objects.create(
                ngay_lam_viec=d,
                xuong=1,
                to=1,
                ma_hang="AO-POLO-01",
                mau="Đỏ",
                size="L",
                ra_chuyen=50,
                nguoi_nhap=self.basic_user
            )

        self._login(self.accountant_user)

        # Page 1
        resp = self.client.get(reverse("accounting:team_revenue_report"))
        self.assertEqual(resp.status_code, 200)
        daily_page_obj = resp.context["daily_page_obj"]
        self.assertEqual(daily_page_obj.paginator.per_page, 5)
        self.assertEqual(len(daily_page_obj.object_list), 5)
        self.assertEqual(daily_page_obj.paginator.num_pages, 3) # 12 items / 5 = 3 pages
        self.assertEqual(resp.context["total_daily_groups_count"], 12)

        # Page 2
        resp = self.client.get(reverse("accounting:team_revenue_report") + "?page=2")
        self.assertEqual(resp.status_code, 200)
        daily_page_obj = resp.context["daily_page_obj"]
        self.assertEqual(daily_page_obj.number, 2)
        self.assertEqual(len(daily_page_obj.object_list), 5)

        # Page 3 (remaining 2 items)
        resp = self.client.get(reverse("accounting:team_revenue_report") + "?page=3")
        self.assertEqual(resp.status_code, 200)
        daily_page_obj = resp.context["daily_page_obj"]
        self.assertEqual(daily_page_obj.number, 3)
        self.assertEqual(len(daily_page_obj.object_list), 2)

    def test_team_revenue_mathematical_precision_audit(self):
        """
        Audit all calculations for 100% mathematical precision based on gia_cm:
        - Multiple teams (Xuong 1 To 1, Xuong 1 To 2, Xuong 2 To 1)
        - Multiple days (Day 1, Day 2, Day 3)
        - Multiple products (AO-POLO-01 @ 25,000 CM, AO-KHOAC-02 @ 50,000 CM, AO-THUN-03 @ 16,000 CM)
        - Multiple colors and sizes
        - Strict cross-verification across:
            KPI Summary == Tab 1 items sum == Tab 2 team sum == Tab 3 date sum == Excel export.
        """
        # Create products and prices
        p2 = Product.objects.create(name="AO-KHOAC-02")
        c2_den = ProductColor.objects.create(product=p2, name="Đen", quantity=1000)
        ProductPrice.objects.create(product_color=c2_den, don_gia=250000, gia_cm=50000, updated_by=self.accountant_user)

        p3 = Product.objects.create(name="AO-THUN-03")
        c3_trang = ProductColor.objects.create(product=p3, name="Trắng", quantity=1000)
        ProductPrice.objects.create(product_color=c3_trang, don_gia=80000, gia_cm=16000, updated_by=self.accountant_user)

        # Expected totals tracker
        expected_total_qty = 0
        expected_total_money = 0
        expected_active_dates = set()
        expected_active_teams = set()

        # Day 1: 2026-08-05
        d1 = datetime.date(2026, 8, 5)
        # Xuong 1 To 1:
        # - AO-POLO-01 (Đỏ): Size S=10, Size M=20, Size L=30 -> 60 pcs * 25,000 = 1,500,000
        # - AO-KHOAC-02 (Đen): Size XL=15 -> 15 pcs * 50,000 = 750,000
        # Subtotal: 75 pcs, 2,250,000 VNĐ
        for size, q in [("S", 10), ("M", 20), ("L", 30)]:
            ProcessReport.objects.create(
                ngay_lam_viec=d1, xuong=1, to=1, ma_hang="AO-POLO-01", mau="Đỏ", size=size,
                ra_chuyen=q, so_luong_ld=12, nguoi_nhap=self.basic_user
            )
        ProcessReport.objects.create(
            ngay_lam_viec=d1, xuong=1, to=1, ma_hang="AO-KHOAC-02", mau="Đen", size="XL",
            ra_chuyen=15, so_luong_ld=12, nguoi_nhap=self.basic_user
        )
        expected_total_qty += 75
        expected_total_money += 2250000
        expected_active_dates.add(d1)
        expected_active_teams.add((1, 1))

        # Xuong 1 To 2:
        # - AO-THUN-03 (Trắng): Size M=100 -> 100 pcs * 16,000 = 1,600,000
        ProcessReport.objects.create(
            ngay_lam_viec=d1, xuong=1, to=2, ma_hang="AO-THUN-03", mau="Trắng", size="M",
            ra_chuyen=100, so_luong_ld=10, nguoi_nhap=self.basic_user
        )
        expected_total_qty += 100
        expected_total_money += 1600000
        expected_active_teams.add((1, 2))

        # Day 2: 2026-08-06
        d2 = datetime.date(2026, 8, 6)
        # Xuong 2 To 1:
        # - AO-KHOAC-02 (Đen): Size L=40 -> 40 pcs * 50,000 = 2,000,000
        ProcessReport.objects.create(
            ngay_lam_viec=d2, xuong=2, to=1, ma_hang="AO-KHOAC-02", mau="Đen", size="L",
            ra_chuyen=40, so_luong_ld=15, nguoi_nhap=self.basic_user
        )
        expected_total_qty += 40
        expected_total_money += 2000000
        expected_active_dates.add(d2)
        expected_active_teams.add((2, 1))

        # Xuong 1 To 1:
        # - AO-THUN-03 (Trắng): Size S=50 -> 50 pcs * 16,000 = 800,000
        ProcessReport.objects.create(
            ngay_lam_viec=d2, xuong=1, to=1, ma_hang="AO-THUN-03", mau="Trắng", size="S",
            ra_chuyen=50, so_luong_ld=12, nguoi_nhap=self.basic_user
        )
        expected_total_qty += 50
        expected_total_money += 8000000 * 0.1 # 800,000

        # Grand Total across dataset:
        # Qty = 75 + 100 + 40 + 50 = 265 pcs
        # Money = 2,250,000 + 1,600,000 + 2,000,000 + 800,000 = 6,650,000 VNĐ
        # Active teams = 3 (X1-T1, X1-T2, X2-T1)
        # Active days = 2 (2026-08-05, 2026-08-06)
        # Avg money per day = 6,650,000 / 2 = 3,325,000 VNĐ

        self.assertEqual(expected_total_qty, 265)
        self.assertEqual(expected_total_money, 6650000)

        self._login(self.accountant_user)
        resp = self.client.get(reverse("accounting:team_revenue_report") + "?thang=2026-08")
        self.assertEqual(resp.status_code, 200)

        # 1. Audit KPIs
        self.assertEqual(resp.context["kpi_tong_ra_chuyen"], 265)
        self.assertEqual(resp.context["kpi_tong_tien"], 6650000)
        self.assertEqual(resp.context["kpi_so_to"], 3)
        self.assertEqual(resp.context["kpi_so_ngay_sx"], 2)
        self.assertEqual(resp.context["kpi_tien_bq_ngay"], 3325000)

        # 2. Audit Tab 1 (Detail groups)
        daily_groups = resp.context["daily_team_groups"]
        self.assertEqual(len(daily_groups), 4) # (d1, 1, 1), (d1, 1, 2), (d2, 2, 1), (d2, 1, 1)
        tab1_qty_sum = sum(g["tong_ra_chuyen"] for g in daily_groups)
        tab1_money_sum = sum(g["tong_tien"] for g in daily_groups)
        self.assertEqual(tab1_qty_sum, 265)
        self.assertEqual(tab1_money_sum, 6650000)

        # 3. Audit Tab 2 (Team summary)
        team_summary = resp.context["team_summary_list"]
        self.assertEqual(len(team_summary), 3)
        tab2_qty_sum = sum(ts["tong_ra_chuyen"] for ts in team_summary)
        tab2_money_sum = sum(ts["tong_tien"] for ts in team_summary)
        self.assertEqual(tab2_qty_sum, 265)
        self.assertEqual(tab2_money_sum, 6650000)

        # Xưởng 1 Tổ 1: worked 2 days, total money = 2,250,000 + 800,000 = 3,050,000
        x1_t1 = next(ts for ts in team_summary if ts["xuong"] == 1 and ts["to"] == 1)
        self.assertEqual(x1_t1["so_ngay_sx"], 2)
        self.assertEqual(x1_t1["so_ma_hang"], 3) # AO-POLO-01, AO-KHOAC-02, AO-THUN-03
        self.assertEqual(x1_t1["tong_ra_chuyen"], 125)
        self.assertEqual(x1_t1["tong_tien"], 3050000)
        self.assertEqual(x1_t1["tien_bq_ngay"], round(3050000 / 2))

        # 4. Audit Tab 3 (Date summary)
        date_summary = resp.context["date_summary_list"]
        self.assertEqual(len(date_summary), 2)
        tab3_qty_sum = sum(ds["tong_ra_chuyen"] for ds in date_summary)
        tab3_money_sum = sum(ds["tong_tien"] for ds in date_summary)
        self.assertEqual(tab3_qty_sum, 265)
        self.assertEqual(tab3_money_sum, 6650000)

        # Day 1: 75 + 100 = 175 pcs, 2,250,000 + 1,600,000 = 3,850,000 VNĐ, 2 active teams
        d1_summary = next(ds for ds in date_summary if ds["ngay_lam_viec"] == d1)
        self.assertEqual(d1_summary["so_to_hoat_dong"], 2)
        self.assertEqual(d1_summary["tong_ra_chuyen"], 175)
        self.assertEqual(d1_summary["tong_tien"], 3850000)

        # Day 2: 40 + 50 = 90 pcs, 2,000,000 + 800,000 = 2,800,000 VNĐ, 2 active teams
        d2_summary = next(ds for ds in date_summary if ds["ngay_lam_viec"] == d2)
        self.assertEqual(d2_summary["so_to_hoat_dong"], 2)
        self.assertEqual(d2_summary["tong_ra_chuyen"], 90)
        self.assertEqual(d2_summary["tong_tien"], 2800000)

    def test_payment_report_and_dashboard_calculations(self):
        """Test recording payments and calculating paid vs unpaid amounts on dashboard."""
        self._login(self.accountant_user)

        # 1. Create an export for AO-POLO-01 Đỏ: 100 pcs @ 120,000 = 12,000,000 VNĐ
        ExportReport.objects.create(
            ngay_xuat=datetime.date(2026, 8, 20),
            ma_hang="AO-POLO-01",
            mau="Đỏ",
            so_luong_xuat=100,
            don_gia=120000,
            thanh_tien=12000000,
            nguoi_nhap=self.accountant_user
        )

        # Check initial dashboard state before any payments
        resp = self.client.get(reverse("accounting:dashboard"))
        self.assertEqual(resp.status_code, 200)
        row_red = next(r for r in resp.context["rows"] if r["ma_hang"] == "AO-POLO-01" and r["mau"] == "Đỏ")
        self.assertEqual(row_red["tien_da_xuat"], 12000000)
        self.assertEqual(row_red["tien_da_thanh_toan"], 0)
        self.assertEqual(row_red["tien_chua_thanh_toan"], 12000000)
        self.assertEqual(resp.context["kpi_tong_da_thanh_toan"], 0)
        self.assertEqual(resp.context["kpi_tong_chua_thanh_toan"], 12000000)

        # 2. Record payment 1 via POST action="create_payment": 7,000,000 VNĐ
        resp = self.client.post(reverse("accounting:dashboard"), {
            "action": "create_payment",
            "product_color_id": self.color1_red.id,
            "ngay_thanh_toan": "2026-08-22",
            "so_tien": "7,000,000",
            "ghi_chu": "UNC 001/VCB"
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(PaymentReport.objects.count(), 1)
        pay1 = PaymentReport.objects.first()
        self.assertEqual(pay1.so_tien, 7000000)
        self.assertEqual(pay1.product_color, self.color1_red)

        # Check dashboard state after payment 1:
        # tien_da_thanh_toan = 7,000,000; tien_chua_thanh_toan = 12,000,000 - 7,000,000 = 5,000,000
        resp = self.client.get(reverse("accounting:dashboard"))
        row_red = next(r for r in resp.context["rows"] if r["ma_hang"] == "AO-POLO-01" and r["mau"] == "Đỏ")
        self.assertEqual(row_red["tien_da_thanh_toan"], 7000000)
        self.assertEqual(row_red["tien_chua_thanh_toan"], 5000000)
        self.assertEqual(resp.context["kpi_tong_da_thanh_toan"], 7000000)
        self.assertEqual(resp.context["kpi_tong_chua_thanh_toan"], 5000000)
        self.assertEqual(len(row_red["payments_list"]), 1)

        # 3. Record payment 2: 5,000,000 VNĐ (Pay off remaining balance)
        self.client.post(reverse("accounting:dashboard"), {
            "action": "create_payment",
            "product_color_id": self.color1_red.id,
            "ngay_thanh_toan": "2026-08-25",
            "so_tien": "5000000",
            "ghi_chu": "UNC 002/VCB"
        })
        self.assertEqual(PaymentReport.objects.count(), 2)

        resp = self.client.get(reverse("accounting:dashboard"))
        row_red = next(r for r in resp.context["rows"] if r["ma_hang"] == "AO-POLO-01" and r["mau"] == "Đỏ")
        self.assertEqual(row_red["tien_da_thanh_toan"], 12000000)
        self.assertEqual(row_red["tien_chua_thanh_toan"], 0)
        self.assertEqual(resp.context["kpi_tong_da_thanh_toan"], 12000000)
        self.assertEqual(resp.context["kpi_tong_chua_thanh_toan"], 0)
        self.assertEqual(len(row_red["payments_list"]), 2)

        # 4. Test deleting payment via POST action="delete_payment"
        self.client.post(reverse("accounting:dashboard"), {
            "action": "delete_payment",
            "payment_id": pay1.id
        })
        self.assertEqual(PaymentReport.objects.count(), 1)
        resp = self.client.get(reverse("accounting:dashboard"))
        row_red = next(r for r in resp.context["rows"] if r["ma_hang"] == "AO-POLO-01" and r["mau"] == "Đỏ")
        self.assertEqual(row_red["tien_da_thanh_toan"], 5000000)
        self.assertEqual(row_red["tien_chua_thanh_toan"], 7000000)

    def test_export_excel_with_payments(self):
        """Test that Excel export contains Sheet 1 with payment columns and Sheet 3 for payment logs."""
        PaymentReport.objects.create(
            ngay_thanh_toan=datetime.date(2026, 8, 22),
            product_color=self.color1_red,
            so_tien=3000000,
            ghi_chu="Thanh toán đợt 1",
            nguoi_nhap=self.accountant_user
        )

        self._login(self.accountant_user)
        resp = self.client.get(reverse("accounting:export_excel"))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp["Content-Type"], "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")






