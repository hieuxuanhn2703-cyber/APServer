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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.context.get('with_totals'):
            cumulative_map = self.context.get('cumulative_map', {})
            color_map = self.context.get('color_map', {})
            totals = cumulative_map.get(instance.id, {})
            data['cumulative'] = {
                'cat_chinh': totals.get('cat_chinh', instance.cat_chinh or 0),
                'cat_lot': totals.get('cat_lot', instance.cat_lot or 0),
                'cat_mex': totals.get('cat_mex', instance.cat_mex or 0),
                'cat_bong': totals.get('cat_bong', instance.cat_bong or 0),
            }
            data['tong_don_hang'] = color_map.get((instance.ma_hang, instance.mau), 0)
        return data

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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.context.get('with_totals'):
            cumulative_map = self.context.get('cumulative_map', {})
            color_map = self.context.get('color_map', {})
            totals = cumulative_map.get(instance.id, {})
            data['cumulative'] = {
                'nhan_btp': totals.get('nhan_btp', instance.nhan_btp or 0),
                'vao_chuyen': totals.get('vao_chuyen', instance.vao_chuyen or 0),
                'giua_chuyen': totals.get('giua_chuyen', instance.giua_chuyen or 0),
                'ra_chuyen': totals.get('ra_chuyen', instance.ra_chuyen or 0),
                'thu_hoa': totals.get('thu_hoa', instance.thu_hoa or 0),
                'la_thanh_pham': totals.get('la_thanh_pham', instance.la_thanh_pham or 0),
                'nhap_hoan_thien': totals.get('nhap_hoan_thien', instance.nhap_hoan_thien or 0),
            }
            data['tong_don_hang'] = color_map.get((instance.ma_hang, instance.mau), 0)
        return data

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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.context.get('with_totals'):
            cumulative_map = self.context.get('cumulative_map', {})
            color_map = self.context.get('color_map', {})
            totals = cumulative_map.get(instance.id, {})
            data['cumulative'] = {
                'qua_tay': totals.get('qua_tay', instance.qua_tay or 0),
                'dat': totals.get('dat', instance.dat or 0),
                'loi': totals.get('loi', instance.loi or 0),
                'tong_dat': totals.get('tong_dat', instance.tong_dat or 0),
            }
            data['tong_don_hang'] = color_map.get((instance.ma_hang, instance.mau), 0)
        return data

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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.context.get('with_totals'):
            cumulative_map = self.context.get('cumulative_map', {})
            color_map = self.context.get('color_map', {})
            prod_nhap_totals_map = self.context.get('prod_nhap_totals_map', {})
            totals = cumulative_map.get(instance.id, {})
            data['cumulative'] = {
                'the_bai': totals.get('the_bai', instance.the_bai or 0),
                'gap_hang': totals.get('gap_hang', instance.gap_hang or 0),
                'treo_dong_thung': totals.get('treo_dong_thung', instance.treo_dong_thung or 0),
            }
            data['tong_don_hang'] = color_map.get((instance.ma_hang, instance.mau), 0)
            data['tong_nhap_hoan_thien'] = prod_nhap_totals_map.get((instance.ma_hang, instance.mau), 0)
        return data

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
