from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Accounting.api.views import (
    ProductPriceViewSet,
    ExportReportViewSet,
    PaymentReportViewSet,
    AccountingDashboardAPIView,
    TeamRevenueAPIView,
)

router = DefaultRouter()
router.register(r'prices', ProductPriceViewSet, basename='api-price')
router.register(r'exports', ExportReportViewSet, basename='api-export')
router.register(r'payments', PaymentReportViewSet, basename='api-payment')

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', AccountingDashboardAPIView.as_view(), name='api-accounting-dashboard'),
    path('team-revenue/', TeamRevenueAPIView.as_view(), name='api-team-revenue'),
]
