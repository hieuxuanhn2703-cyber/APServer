from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Working.api.views import (
    AppUserViewSet,
    ProductViewSet,
    ProductColorViewSet,
    ProductSizeViewSet,
    CutReportViewSet,
    ProcessReportViewSet,
    KcsReportViewSet,
    FinishingReportViewSet,
    DefectReturnReportViewSet,
    SampleTakeReportViewSet,
    DashboardCutAPIView,
    DashboardProcessAPIView,
    DashboardKcsAPIView,
    DashboardFinishingAPIView,
    DashboardTrackingAPIView
)

router = DefaultRouter()
router.register(r'users', AppUserViewSet, basename='users')
router.register(r'config/products', ProductViewSet, basename='config-products')
router.register(r'config/colors', ProductColorViewSet, basename='config-colors')
router.register(r'config/sizes', ProductSizeViewSet, basename='config-sizes')
router.register(r'reports/cut', CutReportViewSet, basename='reports-cut')
router.register(r'reports/process', ProcessReportViewSet, basename='reports-process')
router.register(r'reports/kcs', KcsReportViewSet, basename='reports-kcs')
router.register(r'reports/finishing', FinishingReportViewSet, basename='reports-finishing')
router.register(r'exceptions/defects', DefectReturnReportViewSet, basename='exceptions-defects')
router.register(r'exceptions/samples', SampleTakeReportViewSet, basename='exceptions-samples')

urlpatterns = [
    path('', include(router.urls)),
    path('dashboards/cut/', DashboardCutAPIView.as_view(), name='dashboard-cut'),
    path('dashboards/process/', DashboardProcessAPIView.as_view(), name='dashboard-process'),
    path('dashboards/kcs/', DashboardKcsAPIView.as_view(), name='dashboard-kcs'),
    path('dashboards/finishing/', DashboardFinishingAPIView.as_view(), name='dashboard-finishing'),
    path('dashboards/tracking/', DashboardTrackingAPIView.as_view(), name='dashboard-tracking'),
]
