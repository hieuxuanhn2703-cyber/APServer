from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MaterialReceiptViewSet, MaterialIssueViewSet, InventorySummaryAPIView

app_name = 'inventory_api'

router = DefaultRouter()
router.register(r'receipts', MaterialReceiptViewSet, basename='receipts')
router.register(r'issues', MaterialIssueViewSet, basename='issues')

urlpatterns = [
    path('summary/', InventorySummaryAPIView.as_view(), name='summary'),
    path('', include(router.urls)),
]
