from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from Inventory.models import MaterialReceipt, MaterialIssue
from Inventory.services import get_inventory_summary_data
from .serializers import MaterialReceiptSerializer, MaterialIssueSerializer
from .permissions import InventoryAccessPolicy, IsInventoryViewer
from ProcessMonitoring.api.permissions import IsAuthenticatedAppUser

class MaterialReceiptViewSet(viewsets.ModelViewSet):
    """
    CRUD API for MaterialReceipt.
    - KHO, PREMIUM, QUAN_LY, KE_TOAN can GET and POST.
    - PREMIUM, QUAN_LY can PUT, PATCH, DELETE.
    """
    queryset = MaterialReceipt.objects.select_related('nguoi_nhap').all().order_by('-created_at')
    serializer_class = MaterialReceiptSerializer
    permission_classes = [IsAuthenticatedAppUser, InventoryAccessPolicy]

    def perform_create(self, serializer):
        serializer.save(nguoi_nhap=self.request.user)

class MaterialIssueViewSet(viewsets.ModelViewSet):
    """
    CRUD API for MaterialIssue.
    - KHO, PREMIUM, QUAN_LY, KE_TOAN can GET and POST.
    - PREMIUM, QUAN_LY can PUT, PATCH, DELETE.
    """
    queryset = MaterialIssue.objects.select_related('nguoi_xuat', 'receipt').all().order_by('-created_at')
    serializer_class = MaterialIssueSerializer
    permission_classes = [IsAuthenticatedAppUser, InventoryAccessPolicy]

    def perform_create(self, serializer):
        serializer.save(nguoi_xuat=self.request.user)

class InventorySummaryAPIView(APIView):
    """
    Read-only endpoint that returns computed inventory stock.
    Supports query parameters: ma_hang, mau, ten_vat_tu, don_vi.
    """
    permission_classes = [IsAuthenticatedAppUser, IsInventoryViewer]

    def get(self, request, *args, **kwargs):
        filter_ma_hang = request.query_params.getlist('ma_hang')
        filter_mau = request.query_params.getlist('mau')
        filter_ten_vat_tu = request.query_params.getlist('ten_vat_tu')
        filter_don_vi = request.query_params.getlist('don_vi')

        data = get_inventory_summary_data(
            filter_ma_hang=filter_ma_hang if filter_ma_hang else None,
            filter_mau=filter_mau if filter_mau else None,
            filter_ten_vat_tu=filter_ten_vat_tu if filter_ten_vat_tu else None,
            filter_don_vi=filter_don_vi if filter_don_vi else None
        )
        return Response(data)
