from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from Accounting.models import ProductPrice, ExportReport, PaymentReport
from Accounting.api.serializers import (
    ProductPriceSerializer, 
    ExportReportSerializer, 
    PaymentReportSerializer
)
from Accounting.api.permissions import IsAccountingTeam, IsAppUser
from Accounting.services import get_dashboard_data, get_team_revenue_data


class ProductPriceViewSet(viewsets.ModelViewSet):
    """
    Quản lý bảng giá xuất và giá CM.
    Mọi user đều có thể xem (ReadOnly cho KCS/Nha_cat/To_Truong).
    Chỉ QUAN_LY, KE_TOAN mới có quyền sửa/tạo (nếu cần qua form thay vì signal).
    """
    queryset = ProductPrice.objects.select_related('product_color', 'product_color__product', 'updated_by').all()
    serializer_class = ProductPriceSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['product_color__product__name', 'product_color__name']
    ordering_fields = ['product_color__product__name', 'updated_at']
    ordering = ['product_color__product__name', 'product_color__name']
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAppUser()]
        return [IsAccountingTeam()]


class ExportReportViewSet(viewsets.ModelViewSet):
    """
    Quản lý Phiếu Xuất Hàng (Chỉ Kế Toán & Quản Lý).
    """
    queryset = ExportReport.objects.select_related('nguoi_nhap').all()
    serializer_class = ExportReportSerializer
    permission_classes = [IsAccountingTeam]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['ma_hang', 'mau']
    search_fields = ['ma_hang', 'mau', 'ghi_chu']
    ordering_fields = ['ngay_xuat', 'created_at']
    ordering = ['-created_at']


class PaymentReportViewSet(viewsets.ModelViewSet):
    """
    Quản lý Phiếu Thanh Toán (Chỉ Kế Toán & Quản Lý).
    """
    queryset = PaymentReport.objects.select_related('product_color', 'product_color__product', 'nguoi_nhap').all()
    serializer_class = PaymentReportSerializer
    permission_classes = [IsAccountingTeam]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['product_color', 'product_color__product__name']
    search_fields = ['product_color__product__name', 'ghi_chu']
    ordering_fields = ['ngay_thanh_toan', 'created_at']
    ordering = ['-created_at']


class AccountingDashboardAPIView(APIView):
    """
    Trả về dữ liệu tổng hợp cho Dashboard Kế Toán.
    """
    permission_classes = [IsAccountingTeam]

    def get(self, request, *args, **kwargs):
        selected_ma_hang = request.query_params.get('ma_hang', '')
        data = get_dashboard_data(selected_ma_hang=selected_ma_hang)
        return Response(data)


class TeamRevenueAPIView(APIView):
    """
    Trả về dữ liệu báo cáo doanh thu Tổ/Xưởng.
    """
    permission_classes = [IsAccountingTeam]

    def get(self, request, *args, **kwargs):
        data = get_team_revenue_data(request.query_params)
        return Response(data)
