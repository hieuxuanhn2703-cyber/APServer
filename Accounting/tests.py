import datetime
from django.test import TestCase, Client
from django.conf import settings
from django.urls import reverse
from django.core.exceptions import PermissionDenied

from Working.models import AppUser, Product, ProductColor
from Working.auth_utils import SESSION_KEY
from Accounting.models import ProductPrice, ExportReport


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

        # Set initial unit price for Đỏ = 120,000 VNĐ
        self.price1_red = ProductPrice.objects.create(
            product_color=self.color1_red,
            don_gia=120000,
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
        """Test single and bulk price updates."""
        self._login(self.accountant_user)

        # 1. Update single price with formatted string
        resp = self.client.post(reverse("accounting:price_management"), {
            "action": "update_single",
            "product_color_id": self.color1_blue.id,
            "don_gia": "150.000"
        })
        self.assertEqual(resp.status_code, 200)
        self.color1_blue.refresh_from_db()
        self.assertEqual(self.color1_blue.price.don_gia, 150000)

        # 2. Update bulk price with commas and m_price prefix
        resp = self.client.post(reverse("accounting:price_management"), {
            "action": "update_bulk",
            f"price_{self.color1_red.id}": "130,000 đ",
            f"m_price_{self.color1_blue.id}": "160.000",
        })
        self.assertEqual(resp.status_code, 200)
        self.color1_red.refresh_from_db()
        self.color1_blue.refresh_from_db()
        self.assertEqual(self.color1_red.price.don_gia, 130000)
        self.assertEqual(self.color1_blue.price.don_gia, 160000)

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

