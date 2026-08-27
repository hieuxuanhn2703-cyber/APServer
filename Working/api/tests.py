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
