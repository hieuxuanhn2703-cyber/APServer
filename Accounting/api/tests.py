from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from Working.models import AppUser, Product, ProductColor
from Accounting.models import ProductPrice, ExportReport, PaymentReport
import datetime

class AccountingAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        self.manager = AppUser.objects.create(
            account='manager1', name='Manager', password='testpassword', role='QUAN_LY', is_approved=True
        )
        self.accountant = AppUser.objects.create(
            account='acc1', name='Accountant', password='testpassword', role='KE_TOAN', is_approved=True
        )
        self.worker = AppUser.objects.create(
            account='worker1', name='Worker', password='testpassword', role='TO_TRUONG', is_approved=True
        )

        # Create basic data
        self.product = Product.objects.create(name='Ao-Polo')
        self.color = ProductColor.objects.create(product=self.product, name='Xanh', quantity=100)
        
        self.price = ProductPrice.objects.create(
            product_color=self.color, don_gia=50000, gia_cm=10000, updated_by=self.manager
        )
        
        self.export = ExportReport.objects.create(
            ma_hang='Ao-Polo', mau='Xanh', so_luong_xuat=10, don_gia=50000, 
            thanh_tien=500000, nguoi_nhap=self.manager
        )
        
        self.payment = PaymentReport.objects.create(
            product_color=self.color, so_tien=200000, nguoi_nhap=self.manager
        )

    def test_authentication_required(self):
        # Unauthenticated access should be denied
        response = self.client.get('/api/v1/accounting/prices/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        response = self.client.get('/api/v1/accounting/exports/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_permission_read_prices(self):
        # Any authenticated user can read prices
        self.client.force_authenticate(user=self.worker)
        response = self.client.get('/api/v1/accounting/prices/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if 'results' in response.data:
            self.assertEqual(len(response.data['results']), 1)
        else:
            self.assertEqual(len(response.data), 1)

    def test_permission_write_exports(self):
        # Only accounting/manager can access exports
        self.client.force_authenticate(user=self.worker)
        response = self.client.get('/api/v1/accounting/exports/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        self.client.force_authenticate(user=self.accountant)
        response = self.client.get('/api/v1/accounting/exports/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if 'results' in response.data:
            self.assertEqual(len(response.data['results']), 1)
        else:
            self.assertEqual(len(response.data), 1)

    def test_create_export_report(self):
        self.client.force_authenticate(user=self.accountant)
        data = {
            'ngay_xuat': str(datetime.date.today()),
            'ma_hang': 'Ao-Polo',
            'mau': 'Xanh',
            'so_luong_xuat': 20,
            'don_gia': 50000
        }
        response = self.client.post('/api/v1/accounting/exports/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['thanh_tien'], 1000000)
        self.assertEqual(response.data['nguoi_nhap_name'], 'Accountant')

    def test_accounting_dashboard(self):
        self.client.force_authenticate(user=self.manager)
        response = self.client.get('/api/v1/accounting/dashboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if the structure is correct
        self.assertIn('rows', response.data)
        self.assertIn('kpi', response.data)
        self.assertIn('payments_by_pc', response.data)
        
        # Validate data aggregation
        rows = response.data['rows']
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row['ma_hang'], 'Ao-Polo')
        self.assertEqual(row['tong_so_luong'], 100)
        self.assertEqual(row['da_xuat'], 10)
        self.assertEqual(row['tien_da_thanh_toan'], 200000)

    def test_team_revenue(self):
        self.client.force_authenticate(user=self.accountant)
        response = self.client.get('/api/v1/accounting/team-revenue/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify structure
        self.assertIn('daily_team_groups', response.data)
        self.assertIn('team_summary_list', response.data)
        self.assertIn('date_summary_list', response.data)
        self.assertIn('kpi_tong_tien', response.data)

    def test_payment_create_and_delete(self):
        self.client.force_authenticate(user=self.accountant)
        
        # 1. Create a payment
        pay_data = {
            'ngay_thanh_toan': str(datetime.date.today()),
            'product_color': self.color.id,
            'so_tien': 150000,
            'ghi_chu': 'Dot 2 test'
        }
        create_resp = self.client.post('/api/v1/accounting/payments/', pay_data)
        self.assertEqual(create_resp.status_code, status.HTTP_201_CREATED)
        new_pay_id = create_resp.data['id']
        self.assertEqual(create_resp.data['so_tien'], 150000)
        self.assertEqual(create_resp.data['product_name'], 'Ao-Polo')
        
        # 2. Verify dashboard reflects updated paid amount (200000 + 150000 = 350000)
        dash_resp = self.client.get('/api/v1/accounting/dashboard/')
        self.assertEqual(dash_resp.status_code, status.HTTP_200_OK)
        row = dash_resp.data['rows'][0]
        self.assertEqual(row['tien_da_thanh_toan'], 350000)
        
        # 3. Delete the newly created payment
        del_resp = self.client.delete(f'/api/v1/accounting/payments/{new_pay_id}/')
        self.assertEqual(del_resp.status_code, status.HTTP_204_NO_CONTENT)
        
        # 4. Verify dashboard returns to previous state (200000)
        dash_resp2 = self.client.get('/api/v1/accounting/dashboard/')
        self.assertEqual(dash_resp2.status_code, status.HTTP_200_OK)
        row2 = dash_resp2.data['rows'][0]
        self.assertEqual(row2['tien_da_thanh_toan'], 200000)

    def test_payment_permissions(self):
        # Worker cannot create or delete payments (HTTP 403)
        self.client.force_authenticate(user=self.worker)
        
        pay_data = {
            'ngay_thanh_toan': str(datetime.date.today()),
            'product_color': self.color.id,
            'so_tien': 100000
        }
        create_resp = self.client.post('/api/v1/accounting/payments/', pay_data)
        self.assertEqual(create_resp.status_code, status.HTTP_403_FORBIDDEN)
        
        del_resp = self.client.delete(f'/api/v1/accounting/payments/{self.payment.id}/')
        self.assertEqual(del_resp.status_code, status.HTTP_403_FORBIDDEN)

