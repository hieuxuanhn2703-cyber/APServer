from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

class HealthCheckTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_health_check_endpoint_exists(self):
        """Test that the health check endpoint resolves and returns 200 OK."""
        url = reverse('api:health-check')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_health_check_response_format(self):
        """Test that the response is valid JSON and matches the contract."""
        url = reverse('api:health-check')
        response = self.client.get(url)
        self.assertEqual(response.json(), {"status": "ok"})
