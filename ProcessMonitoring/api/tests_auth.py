from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from Working.models import AppUser
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.views import APIView
from rest_framework.response import Response
from ProcessMonitoring.api.permissions import HasRole, IsAuthenticatedAppUser
from django.urls import path

# Dummy view for testing roles
class DummyRoleView(APIView):
    permission_classes = [IsAuthenticatedAppUser, HasRole(["PREMIUM"])]
    def get(self, request):
        return Response({"status": "premium_ok"})

class AuthTests(APITestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Ensure our dummy view is routable for this test suite
        from ProcessMonitoring.api.urls import urlpatterns
        urlpatterns.append(path('test-premium-role/', DummyRoleView.as_view(), name='test-premium-role'))

    def setUp(self):
        # Create users for testing
        self.basic_user = AppUser.objects.create(
            name="Basic User", account="basic1", password="password123", role="BASIC", is_approved=True
        )
        self.premium_user = AppUser.objects.create(
            name="Premium User", account="premium1", password="password123", role="PREMIUM", is_approved=True
        )
        self.unapproved_user = AppUser.objects.create(
            name="Unapproved", account="unapp1", password="password123", role="BASIC", is_approved=False
        )
        
        self.login_url = reverse('api:token_obtain_pair')
        self.refresh_url = reverse('api:token_refresh')
        self.me_url = reverse('api:user_profile')
        self.test_role_url = reverse('api:test-premium-role')

    def test_valid_login(self):
        response = self.client.post(self.login_url, {"account": "basic1", "password": "password123"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        
        # Verify the access token contains user_id
        token = AccessToken(response.data['access'])
        self.assertEqual(token['user_id'], self.basic_user.id)

    def test_invalid_login(self):
        response = self.client.post(self.login_url, {"account": "basic1", "password": "wrong"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_missing_credentials(self):
        response = self.client.post(self.login_url, {"account": "basic1"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unapproved_user_login(self):
        response = self.client.post(self.login_url, {"account": "unapp1", "password": "password123"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_token_refresh(self):
        # 1. Login to get refresh token
        login_resp = self.client.post(self.login_url, {"account": "basic1", "password": "password123"})
        refresh_token = login_resp.data['refresh']
        
        # 2. Use refresh token
        refresh_resp = self.client.post(self.refresh_url, {"refresh": refresh_token})
        self.assertEqual(refresh_resp.status_code, status.HTTP_200_OK)
        self.assertIn('access', refresh_resp.data)

    def test_invalid_token_refresh(self):
        response = self.client.post(self.refresh_url, {"refresh": "fake_token"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_me_endpoint(self):
        login_resp = self.client.post(self.login_url, {"account": "basic1", "password": "password123"})
        access_token = login_resp.data['access']
        
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.basic_user.id)
        self.assertEqual(response.data['role'], "BASIC")

    def test_unauthenticated_me_endpoint(self):
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_role_based_permissions(self):
        # 1. Test basic user accessing premium view (should fail)
        login_resp = self.client.post(self.login_url, {"account": "basic1", "password": "password123"})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_resp.data['access'])
        resp1 = self.client.get(self.test_role_url)
        self.assertEqual(resp1.status_code, status.HTTP_403_FORBIDDEN)
        
        # 2. Test premium user accessing premium view (should pass)
        login_resp2 = self.client.post(self.login_url, {"account": "premium1", "password": "password123"})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_resp2.data['access'])
        resp2 = self.client.get(self.test_role_url)
        self.assertEqual(resp2.status_code, status.HTTP_200_OK)
