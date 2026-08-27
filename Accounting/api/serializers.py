from rest_framework import serializers
from Accounting.models import ProductPrice, ExportReport, PaymentReport
from Working.models import ProductColor

class ProductPriceSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product_color.product.name', read_only=True)
    color_name = serializers.CharField(source='product_color.name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.name', read_only=True)

    class Meta:
        model = ProductPrice
        fields = [
            'id', 'product_color', 'product_name', 'color_name',
            'don_gia', 'gia_cm', 'updated_by', 'updated_by_name', 'updated_at'
        ]
        read_only_fields = ['updated_by', 'updated_at']

    def update(self, instance, validated_data):
        user = self.context['request'].user
        validated_data['updated_by'] = user
        return super().update(instance, validated_data)


class ExportReportSerializer(serializers.ModelSerializer):
    nguoi_nhap_name = serializers.CharField(source='nguoi_nhap.name', read_only=True)

    class Meta:
        model = ExportReport
        fields = [
            'id', 'ngay_xuat', 'ma_hang', 'mau', 'so_luong_xuat', 
            'don_gia', 'thanh_tien', 'ghi_chu', 'nguoi_nhap', 'nguoi_nhap_name', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['thanh_tien', 'nguoi_nhap', 'created_at', 'updated_at']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['nguoi_nhap'] = user
        return super().create(validated_data)


class PaymentReportSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product_color.product.name', read_only=True)
    color_name = serializers.CharField(source='product_color.name', read_only=True)
    nguoi_nhap_name = serializers.CharField(source='nguoi_nhap.name', read_only=True)

    class Meta:
        model = PaymentReport
        fields = [
            'id', 'ngay_thanh_toan', 'product_color', 'product_name', 'color_name',
            'so_tien', 'ghi_chu', 'nguoi_nhap', 'nguoi_nhap_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['nguoi_nhap', 'created_at', 'updated_at']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['nguoi_nhap'] = user
        return super().create(validated_data)
