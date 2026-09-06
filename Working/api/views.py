from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.db.models import Sum
import datetime

from Working.services import (
    get_cut_dashboard_data,
    get_process_dashboard_data,
    get_kcs_dashboard_data,
    get_finishing_dashboard_data,
    get_tracking_dashboard_data,
    calculate_cumulative_totals_cut,
    calculate_cumulative_totals_prod,
    calculate_cumulative_totals_kcs,
    calculate_cumulative_totals_finishing,
)

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
    IsProductionDashboardViewer,
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

    def get_queryset(self):
        qs = super().get_queryset()
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            qs = qs.filter(created_at__gte=start_date)
        if end_date:
            qs = qs.filter(created_at__lte=end_date)
        return qs

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.request.query_params.get('with_totals') in ['true', '1', 'True']:
            context['with_totals'] = True
            context['cumulative_map'] = self.get_cumulative_map()
            context['color_map'] = self.get_color_map()
            if hasattr(self, 'get_extra_context'):
                context.update(self.get_extra_context())
        return context

    def get_cumulative_map(self):
        return {}

    def get_color_map(self):
        return {(c.product.name, c.name): c.quantity for c in ProductColor.objects.select_related('product').all()}

class CutReportViewSet(BaseTrackingViewSet):
    queryset = CutReport.objects.all().select_related('nguoi_nhap').order_by('-created_at')
    serializer_class = CutReportSerializer
    filterset_fields = ['ngay_lam_viec', 'ma_hang', 'mau']
    
    def create_permission_class(self):
        return IsCutWorker()

    def get_cumulative_map(self):
        return calculate_cumulative_totals_cut()

class ProcessReportViewSet(BaseTrackingViewSet):
    queryset = ProcessReport.objects.all().select_related('nguoi_nhap').order_by('-created_at')
    serializer_class = ProcessReportSerializer
    filterset_fields = ['ngay_lam_viec', 'xuong', 'to', 'ma_hang', 'mau']
    
    def create_permission_class(self):
        return IsBasicWorker()

    def get_cumulative_map(self):
        return calculate_cumulative_totals_prod()

class KcsReportViewSet(BaseTrackingViewSet):
    queryset = KcsReport.objects.all().select_related('nguoi_nhap').order_by('-created_at')
    serializer_class = KcsReportSerializer
    filterset_fields = ['ngay_lam_viec', 'xuong', 'to', 'ma_hang', 'mau']
    
    def create_permission_class(self):
        return IsKcsWorker()

    def get_cumulative_map(self):
        return calculate_cumulative_totals_kcs()

class FinishingReportViewSet(BaseTrackingViewSet):
    queryset = FinishingReport.objects.all().select_related('nguoi_nhap').order_by('-created_at')
    serializer_class = FinishingReportSerializer
    filterset_fields = ['ngay_lam_viec', 'ma_hang', 'mau']
    
    def create_permission_class(self):
        return IsFinishingWorker()

    def get_cumulative_map(self):
        return calculate_cumulative_totals_finishing()

    def get_extra_context(self):
        prod_nhap_totals = ProcessReport.objects.values('ma_hang', 'mau').annotate(
            total_nhap=Sum('nhap_hoan_thien')
        )
        return {
            'prod_nhap_totals_map': {(row['ma_hang'], row['mau']): row['total_nhap'] for row in prod_nhap_totals}
        }

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

class DashboardCutAPIView(APIView):
    permission_classes = [IsProductionDashboardViewer]
    
    def get(self, request):
        data = get_cut_dashboard_data(
            start_date=request.query_params.get('start_date'),
            end_date=request.query_params.get('end_date'),
            ma_hangs=request.query_params.getlist('ma_hang'),
            maus=request.query_params.getlist('mau')
        )
        return Response(data)

class DashboardProcessAPIView(APIView):
    permission_classes = [IsProductionDashboardViewer]
    
    def get(self, request):
        data = get_process_dashboard_data(
            start_date=request.query_params.get('start_date'),
            end_date=request.query_params.get('end_date'),
            ma_hangs=request.query_params.getlist('ma_hang'),
            maus=request.query_params.getlist('mau')
        )
        return Response(data)

class DashboardKcsAPIView(APIView):
    permission_classes = [IsProductionDashboardViewer]
    
    def get(self, request):
        data = get_kcs_dashboard_data(
            start_date=request.query_params.get('start_date'),
            end_date=request.query_params.get('end_date'),
            ma_hangs=request.query_params.getlist('ma_hang'),
            maus=request.query_params.getlist('mau')
        )
        return Response(data)

class DashboardFinishingAPIView(APIView):
    permission_classes = [IsProductionDashboardViewer]
    
    def get(self, request):
        data = get_finishing_dashboard_data(
            start_date=request.query_params.get('start_date'),
            end_date=request.query_params.get('end_date'),
            ma_hangs=request.query_params.getlist('ma_hang'),
            maus=request.query_params.getlist('mau')
        )
        return Response(data)

class DashboardTrackingAPIView(APIView):
    permission_classes = [IsProductionDashboardViewer]
    
    def get(self, request):
        ma_hangs = request.query_params.getlist('ma_hang')
        if not ma_hangs and request.query_params.get('ma_hang'):
            ma_hangs = [request.query_params.get('ma_hang')]
            
        maus = request.query_params.getlist('mau')
        if not maus and request.query_params.get('mau'):
            maus = [request.query_params.get('mau')]
            
        data = get_tracking_dashboard_data(
            filter_ma_hang=ma_hangs if ma_hangs else None,
            filter_mau=maus if maus else None
        )
        return Response(data)
