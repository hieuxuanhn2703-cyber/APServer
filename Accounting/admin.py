from django.contrib import admin
from .models import ProductPrice, ExportReport, PaymentReport


@admin.register(ProductPrice)
class ProductPriceAdmin(admin.ModelAdmin):
    list_display = ("product_color", "don_gia", "gia_cm", "updated_by", "updated_at")
    search_fields = ("product_color__product__name", "product_color__name")
    list_filter = ("product_color__product",)


@admin.register(ExportReport)
class ExportReportAdmin(admin.ModelAdmin):
    list_display = ("ngay_xuat", "ma_hang", "mau", "so_luong_xuat", "don_gia", "thanh_tien", "nguoi_nhap", "created_at")
    search_fields = ("ma_hang", "mau", "ghi_chu", "nguoi_nhap__name", "nguoi_nhap__account")
    list_filter = ("ngay_xuat", "ma_hang")


@admin.register(PaymentReport)
class PaymentReportAdmin(admin.ModelAdmin):
    list_display = ("ngay_thanh_toan", "product_color", "so_tien", "ghi_chu", "nguoi_nhap", "created_at")
    search_fields = ("product_color__product__name", "product_color__name", "ghi_chu", "nguoi_nhap__name", "nguoi_nhap__account")
    list_filter = ("ngay_thanh_toan", "product_color__product")

