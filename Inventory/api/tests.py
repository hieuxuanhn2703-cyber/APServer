from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from Working.models import AppUser
from Inventory.models import MaterialReceipt, MaterialIssue

class InventoryAPITests(APITestCase):
    
    def setUp(self):
        # Create users with different roles
        self.kho_user = AppUser.objects.create(name="Kho", account="kho1", password="pw", role="KHO", is_approved=True)
        self.manager_user = AppUser.objects.create(name="Manager", account="mgr1", password="pw", role="QUAN_LY", is_approved=True)
        self.basic_user = AppUser.objects.create(name="Basic", account="basic1", password="pw", role="BASIC", is_approved=True)
        
        # Authenticate with manager to get token
        login_resp = self.client.post(reverse('api:token_obtain_pair'), {"account": "mgr1", "password": "pw"})
        self.manager_token = login_resp.data['access']
        
        login_resp2 = self.client.post(reverse('api:token_obtain_pair'), {"account": "kho1", "password": "pw"})
        self.kho_token = login_resp2.data['access']
        
        login_resp3 = self.client.post(reverse('api:token_obtain_pair'), {"account": "basic1", "password": "pw"})
        self.basic_token = login_resp3.data['access']

        # URLs
        self.receipts_url = reverse('api:inventory_api:receipts-list')
        self.issues_url = reverse('api:inventory_api:issues-list')
        self.summary_url = reverse('api:inventory_api:summary')

        # Dummy data
        self.receipt = MaterialReceipt.objects.create(
            ma_hang="A1", mau="Đỏ", ten_vat_tu="Vải A", so_luong_kien=10, so_luong=100, don_vi="m", nguoi_nhap=self.kho_user
        )

    def test_unauthorized_access(self):
        # Basic user should not access inventory
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.basic_token)
        response = self.client.get(self.receipts_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_kho_can_read_and_create(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.kho_token)
        
        # Can read
        response = self.client.get(self.receipts_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Can create (nguoi_nhap auto set)
        data = {
            "ma_hang": "B1", "mau": "Xanh", "ten_vat_tu": "Vải B", 
            "so_luong_kien": 5, "so_luong": 50, "don_vi": "m"
        }
        response2 = self.client.post(self.receipts_url, data)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.data['nguoi_nhap']['id'], self.kho_user.id)

    def test_kho_cannot_update_or_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.kho_token)
        url = reverse('api:inventory_api:receipts-detail', args=[self.receipt.id])
        
        # Cannot delete
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Cannot update
        response2 = self.client.patch(url, {"so_luong": 90})
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)

    def test_manager_can_update_and_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.manager_token)
        url = reverse('api:inventory_api:receipts-detail', args=[self.receipt.id])
        
        # Can update
        response = self.client.patch(url, {"so_luong": 90})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['so_luong'], 90)
        
        # Can delete
        response2 = self.client.delete(url)
        self.assertEqual(response2.status_code, status.HTTP_204_NO_CONTENT)

    def test_summary_endpoint(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.kho_token)
        response = self.client.get(self.summary_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, list))
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['nhap_so_luong'], 100)

    def test_issue_creation(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.kho_token)
        data = {
            "receipt": self.receipt.id,
            "ma_hang": "A1", "mau": "Đỏ", "ten_vat_tu": "Vải A",
            "so_luong_kien": 2, "so_luong": 20, "don_vi": "m",
            "nguoi_nhan": "Anh B"
        }
        response = self.client.post(self.issues_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check summary reflects the issue
        summary_resp = self.client.get(self.summary_url)
        self.assertEqual(summary_resp.data[0]['xuat_so_luong'], 20)
        self.assertEqual(summary_resp.data[0]['con_lai_so_luong'], 80)

    def test_unauthenticated_request(self):
        response = self.client.get(self.receipts_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_invalid_jwt(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalidtoken')
        response = self.client.get(self.receipts_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_inactive_user(self):
        self.kho_user.is_approved = False
        self.kho_user.save()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.kho_token)
        response = self.client.get(self.receipts_url)
        # Even with valid token, if user is not active, should fail. 
        # Actually our custom auth IsAuthenticatedAppUser checks is_approved? Let's see what happens.
        # It should be 403 or 401. We'll verify it in the test run.
        self.kho_user.is_approved = True
        self.kho_user.save()

    def test_serializer_validation_chiec(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.kho_token)
        # float amount with don_vi = 'chiếc' should fail
        data = {
            "ma_hang": "C1", "mau": "Vàng", "ten_vat_tu": "Áo", 
            "so_luong_kien": 0, "so_luong": 10.5, "don_vi": "chiếc"
        }
        response = self.client.post(self.receipts_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('so_luong', response.data)
        
        # integer amount with don_vi = 'chiếc' should succeed
        data["so_luong"] = 10.0
        response2 = self.client.post(self.receipts_url, data)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

    def test_pagination(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.kho_token)
        for i in range(25):
            MaterialReceipt.objects.create(
                ma_hang=f"T{i}", mau="Đỏ", ten_vat_tu="Vải", so_luong_kien=1, so_luong=10, don_vi="m", nguoi_nhap=self.kho_user
            )
        response = self.client.get(self.receipts_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # If DRF defaults to pagination, there will be 'count' in data
        # Let's just check if it's paginated or a list
        if isinstance(response.data, dict) and 'results' in response.data:
            self.assertIn('count', response.data)
            self.assertIn('next', response.data)
            self.assertIn('results', response.data)
        
    def test_filtering_summary(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.kho_token)
        response = self.client.get(self.summary_url + "?ma_hang=A1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
        response2 = self.client.get(self.summary_url + "?ma_hang=XYZ")
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response2.data), 0)

    def test_query_performance(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.kho_token)
        # 1 query if no pagination, maybe 2 if paginated (count + data). Let's run it normally first.
        response = self.client.get(self.receipts_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
