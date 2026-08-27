from rest_framework import serializers
from Inventory.models import MaterialReceipt, MaterialIssue
from Working.models import AppUser

class AppUserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['id', 'name', 'account']

class MaterialReceiptSerializer(serializers.ModelSerializer):
    nguoi_nhap = AppUserBasicSerializer(read_only=True)
    
    class Meta:
        model = MaterialReceipt
        fields = [
            'id', 'ngay_nhap', 'ma_hang', 'mau', 'ten_vat_tu', 
            'so_luong_kien', 'so_luong', 'don_vi', 'nguoi_nhap', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'nguoi_nhap']

    def validate(self, data):
        # Additional backend validation for 'chiếc' unit
        don_vi = data.get('don_vi', 'm')
        so_luong = data.get('so_luong', 0.0)
        
        if don_vi == "chiếc":
            if not float(so_luong).is_integer():
                raise serializers.ValidationError({"so_luong": "Số lượng phải là số nguyên khi đơn vị là 'chiếc'."})
                
        return data

class MaterialIssueSerializer(serializers.ModelSerializer):
    nguoi_xuat = AppUserBasicSerializer(read_only=True)
    
    class Meta:
        model = MaterialIssue
        fields = [
            'id', 'receipt', 'ngay_xuat', 'ma_hang', 'mau', 'ten_vat_tu',
            'so_luong_kien', 'so_luong', 'don_vi', 'nguoi_nhan', 'nguoi_xuat',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'nguoi_xuat']

    def validate(self, data):
        # Additional backend validation for 'chiếc' unit
        don_vi = data.get('don_vi', 'm')
        so_luong = data.get('so_luong', 0.0)
        
        if don_vi == "chiếc":
            if not float(so_luong).is_integer():
                raise serializers.ValidationError({"so_luong": "Số lượng phải là số nguyên khi đơn vị là 'chiếc'."})
                
        return data
