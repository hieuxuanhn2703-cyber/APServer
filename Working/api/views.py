from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
import datetime

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
    SampleTakeReport,
    DefectReceiveLog,
    SampleReceiveLog
)

from Working.api.serializers import (
    AppUserSerializer,
    AppUserCreateSerializer,
    ProductSerializer,
    ProductColorSerializer,
    ProductSizeSerializer,
    CutReportSerializer,
    ProcessReportSerializer,
    KcsReportSerializer,
    FinishingReportSerializer,
    DefectReturnReportSerializer,
    SampleTakeReportSerializer
)

from Working.api.permissions import (
    IsAppUser,
    IsAdminOrManager,
    IsBasicWorker,
    IsFinishingWorker,
    IsKcsWorker,
    IsCutWorker,
    IsOwnerOrAdmin
)

class AppUserViewSet(viewsets.ModelViewSet):
    queryset = AppUser.objects.all().order_by('id')
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['role', 'is_approved']
    
    def get_permissions(self):
        # Only Admins and Managers can manage accounts
        return [IsAdminOrManager()]
        
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return AppUserCreateSerializer
        return AppUserSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('name')
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['name']
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAppUser()]
        return [IsAdminOrManager()]

class ProductColorViewSet(viewsets.ModelViewSet):
    queryset = ProductColor.objects.all().order_by('name')
    serializer_class = ProductColorSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['product', 'name']
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAppUser()]
        return [IsAdminOrManager()]

class ProductSizeViewSet(viewsets.ModelViewSet):
    queryset = ProductSize.objects.all().order_by('name')
    serializer_class = ProductSizeSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['color', 'name']
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAppUser()]
        return [IsAdminOrManager()]

class BaseTrackingViewSet(viewsets.ModelViewSet):
    """
    Base ViewSet cho các báo cáo quy trình
    Tự động điền nguoi_nhap và kiểm tra Owner
    """
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    
    def perform_create(self, serializer):
        serializer.save(nguoi_nhap=self.request.user)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAppUser()]
        elif self.action == 'create':
            return [self.create_permission_class()]
        else:
            # Update/Delete requires Owner or Admin
            return [IsOwnerOrAdmin()]
            
    def create_permission_class(self):
        return IsAppUser()

class CutReportViewSet(BaseTrackingViewSet):
    queryset = CutReport.objects.all().select_related('nguoi_nhap').order_by('-created_at')
    serializer_class = CutReportSerializer
    filterset_fields = ['ngay_lam_viec', 'ma_hang', 'mau']
    
    def create_permission_class(self):
        return IsCutWorker()

class ProcessReportViewSet(BaseTrackingViewSet):
    queryset = ProcessReport.objects.all().select_related('nguoi_nhap').order_by('-created_at')
    serializer_class = ProcessReportSerializer
    filterset_fields = ['ngay_lam_viec', 'xuong', 'to', 'ma_hang', 'mau']
    
    def create_permission_class(self):
        return IsBasicWorker()

class KcsReportViewSet(BaseTrackingViewSet):
    queryset = KcsReport.objects.all().select_related('nguoi_nhap').order_by('-created_at')
    serializer_class = KcsReportSerializer
    filterset_fields = ['ngay_lam_viec', 'xuong', 'to', 'ma_hang', 'mau']
    
    def create_permission_class(self):
        return IsKcsWorker()

class FinishingReportViewSet(BaseTrackingViewSet):
    queryset = FinishingReport.objects.all().select_related('nguoi_nhap').order_by('-created_at')
    serializer_class = FinishingReportSerializer
    filterset_fields = ['ngay_lam_viec', 'ma_hang', 'mau']
    
    def create_permission_class(self):
        return IsFinishingWorker()

class DefectReturnReportViewSet(BaseTrackingViewSet):
    queryset = DefectReturnReport.objects.all().select_related('nguoi_nhap').prefetch_related('receive_logs', 'receive_logs__nguoi_nhap').order_by('-created_at')
    serializer_class = DefectReturnReportSerializer
    filterset_fields = ['ngay_tra', 'ma_hang', 'mau', 'xuong', 'to']
    
    def create_permission_class(self):
        return IsFinishingWorker()

    @action(detail=True, methods=['post'], permission_classes=[IsFinishingWorker])
    def receive(self, request, pk=None):
        report = self.get_object()
        quantity = request.data.get('quantity')
        ghi_chu = request.data.get('ghi_chu', '')
        
        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            return Response({'error': 'Số lượng không hợp lệ.'}, status=status.HTTP_400_BAD_REQUEST)
            
        if quantity <= 0:
            return Response({'error': 'Số lượng phải lớn hơn 0.'}, status=status.HTTP_400_BAD_REQUEST)
            
        if quantity > report.so_luong_treo:
            return Response({'error': f'Số lượng nhận lại vượt quá số lượng treo ({report.so_luong_treo}).'}, status=status.HTTP_400_BAD_REQUEST)
            
        # Update report
        report.so_luong_nhan_lai += quantity
        report.save()
        
        # Create log
        DefectReceiveLog.objects.create(
            report=report,
            ngay_nhan=datetime.date.today(),
            so_luong=quantity,
            nguoi_nhap=request.user,
            ghi_chu=ghi_chu
        )
        
        return Response({'status': 'success', 'so_luong_nhan_lai': report.so_luong_nhan_lai, 'so_luong_treo': report.so_luong_treo})

class SampleTakeReportViewSet(BaseTrackingViewSet):
    queryset = SampleTakeReport.objects.all().select_related('nguoi_nhap').prefetch_related('receive_logs', 'receive_logs__nguoi_nhap').order_by('-created_at')
    serializer_class = SampleTakeReportSerializer
    filterset_fields = ['ngay_lay', 'ma_hang', 'mau', 'nguoi_lay']
    
    def create_permission_class(self):
        return IsFinishingWorker()

    @action(detail=True, methods=['post'], permission_classes=[IsFinishingWorker])
    def receive(self, request, pk=None):
        report = self.get_object()
        quantity = request.data.get('quantity')
        ghi_chu = request.data.get('ghi_chu', '')
        
        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            return Response({'error': 'Số lượng không hợp lệ.'}, status=status.HTTP_400_BAD_REQUEST)
            
        if quantity <= 0:
            return Response({'error': 'Số lượng phải lớn hơn 0.'}, status=status.HTTP_400_BAD_REQUEST)
            
        if quantity > report.so_luong_treo:
            return Response({'error': f'Số lượng nhận lại vượt quá số lượng treo ({report.so_luong_treo}).'}, status=status.HTTP_400_BAD_REQUEST)
            
        # Update report
        report.so_luong_nhan_lai += quantity
        report.save()
        
        # Create log
        SampleReceiveLog.objects.create(
            report=report,
            ngay_nhan=datetime.date.today(),
            so_luong=quantity,
            nguoi_nhap=request.user,
            ghi_chu=ghi_chu
        )
        
        return Response({'status': 'success', 'so_luong_nhan_lai': report.so_luong_nhan_lai, 'so_luong_treo': report.so_luong_treo})

from rest_framework.views import APIView
from Working.services import (
    get_cut_dashboard_data,
    get_process_dashboard_data,
    get_kcs_dashboard_data,
    get_finishing_dashboard_data
)

class DashboardCutAPIView(APIView):
    permission_classes = [IsAdminOrManager]
    
    def get(self, request):
        data = get_cut_dashboard_data(
            start_date=request.query_params.get('start_date'),
            end_date=request.query_params.get('end_date'),
            ma_hangs=request.query_params.getlist('ma_hang'),
            maus=request.query_params.getlist('mau')
        )
        return Response(data)

class DashboardProcessAPIView(APIView):
    permission_classes = [IsAdminOrManager]
    
    def get(self, request):
        data = get_process_dashboard_data(
            start_date=request.query_params.get('start_date'),
            end_date=request.query_params.get('end_date'),
            ma_hangs=request.query_params.getlist('ma_hang'),
            maus=request.query_params.getlist('mau')
        )
        return Response(data)

class DashboardKcsAPIView(APIView):
    permission_classes = [IsAdminOrManager]
    
    def get(self, request):
        data = get_kcs_dashboard_data(
            start_date=request.query_params.get('start_date'),
            end_date=request.query_params.get('end_date'),
            ma_hangs=request.query_params.getlist('ma_hang'),
            maus=request.query_params.getlist('mau')
        )
        return Response(data)

class DashboardFinishingAPIView(APIView):
    permission_classes = [IsAdminOrManager]
    
    def get(self, request):
        data = get_finishing_dashboard_data(
            start_date=request.query_params.get('start_date'),
            end_date=request.query_params.get('end_date'),
            ma_hangs=request.query_params.getlist('ma_hang'),
            maus=request.query_params.getlist('mau')
        )
        return Response(data)
