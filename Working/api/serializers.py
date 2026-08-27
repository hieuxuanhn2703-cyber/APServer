from rest_framework import serializers
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

class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['id', 'name', 'account', 'role', 'is_approved']
        read_only_fields = ['account', 'role'] # To avoid basic users modifying these

class AppUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['id', 'name', 'account', 'password', 'role', 'is_approved']
        extra_kwargs = {
            'password': {'write_only': True}
        }

class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = ['id', 'color', 'name']

class ProductColorSerializer(serializers.ModelSerializer):
    sizes = ProductSizeSerializer(many=True, read_only=True)
    
    class Meta:
        model = ProductColor
        fields = ['id', 'product', 'name', 'quantity', 'sizes']

class ProductSerializer(serializers.ModelSerializer):
    colors = ProductColorSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'colors']

class CutReportSerializer(serializers.ModelSerializer):
    nguoi_nhap_name = serializers.CharField(source='nguoi_nhap.name', read_only=True)

    class Meta:
        model = CutReport
        fields = [
            'id', 'ngay_lam_viec', 'ma_hang', 'mau', 'size',
            'cat_chinh', 'cat_lot', 'cat_mex', 'cat_bong',
            'nguoi_nhap', 'nguoi_nhap_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['nguoi_nhap', 'created_at', 'updated_at']

class ProcessReportSerializer(serializers.ModelSerializer):
    nguoi_nhap_name = serializers.CharField(source='nguoi_nhap.name', read_only=True)

    class Meta:
        model = ProcessReport
        fields = [
            'id', 'ngay_lam_viec', 'xuong', 'to', 'so_luong_ld',
            'ma_hang', 'mau', 'size', 'nhan_btp', 'vao_chuyen',
            'giua_chuyen', 'ra_chuyen', 'thu_hoa', 'la_thanh_pham', 'nhap_hoan_thien',
            'nguoi_nhap', 'nguoi_nhap_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['nguoi_nhap', 'created_at', 'updated_at']

class KcsReportSerializer(serializers.ModelSerializer):
    nguoi_nhap_name = serializers.CharField(source='nguoi_nhap.name', read_only=True)

    class Meta:
        model = KcsReport
        fields = [
            'id', 'ngay_lam_viec', 'xuong', 'to', 'ma_hang', 'mau', 'size',
            'qua_tay', 'dat', 'loi', 'tong_dat',
            'nguoi_nhap', 'nguoi_nhap_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['nguoi_nhap', 'created_at', 'updated_at']

class FinishingReportSerializer(serializers.ModelSerializer):
    nguoi_nhap_name = serializers.CharField(source='nguoi_nhap.name', read_only=True)

    class Meta:
        model = FinishingReport
        fields = [
            'id', 'ngay_lam_viec', 'ma_hang', 'mau', 'size',
            'the_bai', 'gap_hang', 'treo_dong_thung',
            'nguoi_nhap', 'nguoi_nhap_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['nguoi_nhap', 'created_at', 'updated_at']

class DefectReceiveLogSerializer(serializers.ModelSerializer):
    nguoi_nhap_name = serializers.CharField(source='nguoi_nhap.name', read_only=True)

    class Meta:
        model = DefectReceiveLog
        fields = ['id', 'report', 'ngay_nhan', 'so_luong', 'nguoi_nhap', 'nguoi_nhap_name', 'ghi_chu', 'created_at']
        read_only_fields = ['nguoi_nhap', 'report', 'created_at']

class DefectReturnReportSerializer(serializers.ModelSerializer):
    nguoi_nhap_name = serializers.CharField(source='nguoi_nhap.name', read_only=True)
    receive_logs = DefectReceiveLogSerializer(many=True, read_only=True)
    so_luong_treo = serializers.ReadOnlyField()

    class Meta:
        model = DefectReturnReport
        fields = [
            'id', 'ngay_tra', 'ma_hang', 'mau', 'xuong', 'to',
            'so_luong_tra', 'so_luong_nhan_lai', 'so_luong_treo',
            'nguoi_nhap', 'nguoi_nhap_name', 'created_at', 'updated_at',
            'receive_logs'
        ]
        read_only_fields = ['nguoi_nhap', 'so_luong_nhan_lai', 'created_at', 'updated_at']

class SampleReceiveLogSerializer(serializers.ModelSerializer):
    nguoi_nhap_name = serializers.CharField(source='nguoi_nhap.name', read_only=True)

    class Meta:
        model = SampleReceiveLog
        fields = ['id', 'report', 'ngay_nhan', 'so_luong', 'nguoi_nhap', 'nguoi_nhap_name', 'ghi_chu', 'created_at']
        read_only_fields = ['nguoi_nhap', 'report', 'created_at']

class SampleTakeReportSerializer(serializers.ModelSerializer):
    nguoi_nhap_name = serializers.CharField(source='nguoi_nhap.name', read_only=True)
    receive_logs = SampleReceiveLogSerializer(many=True, read_only=True)
    so_luong_treo = serializers.ReadOnlyField()

    class Meta:
        model = SampleTakeReport
        fields = [
            'id', 'ngay_lay', 'ma_hang', 'mau', 'nguoi_lay',
            'so_luong_lay', 'so_luong_nhan_lai', 'so_luong_treo',
            'nguoi_nhap', 'nguoi_nhap_name', 'created_at', 'updated_at',
            'receive_logs'
        ]
        read_only_fields = ['nguoi_nhap', 'so_luong_nhan_lai', 'created_at', 'updated_at']
