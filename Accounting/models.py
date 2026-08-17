from django.db import models
import datetime


class ProductPrice(models.Model):
    """
    Lưu đơn giá (VNĐ/cái) cho từng (Mã hàng, Màu sắc).
    Liên kết 1-1 với ProductColor của app Working.
    """
    product_color = models.OneToOneField(
        'Working.ProductColor',
        on_delete=models.CASCADE,
        related_name='price',
        verbose_name='Mã & Màu sản phẩm'
    )
    don_gia = models.PositiveBigIntegerField('Đơn giá (VNĐ)', default=0)
    updated_by = models.ForeignKey(
        'Working.AppUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='updated_prices',
        verbose_name='Người cập nhật'
    )
    updated_at = models.DateTimeField('Cập nhật lần cuối', auto_now=True)

    class Meta:
        verbose_name = 'Đơn giá sản phẩm'
        verbose_name_plural = 'Đơn giá sản phẩm'
        ordering = ['product_color__product__name', 'product_color__name']

    def __str__(self):
        return f"{self.product_color} - {self.don_gia:,.0f} VNĐ"


class ExportReport(models.Model):
    """
    Lưu thông tin từng đợt xuất hàng của Kế toán.
    Tự động tính thành tiền = số lượng xuất * đơn giá tại thời điểm xuất.
    """
    ngay_xuat = models.DateField('Ngày xuất hàng', default=datetime.date.today)
    ma_hang = models.CharField('Mã hàng', max_length=255)
    mau = models.CharField('Màu sắc', max_length=255)
    so_luong_xuat = models.PositiveIntegerField('Số lượng xuất', default=0)
    don_gia = models.PositiveBigIntegerField('Đơn giá tại thời điểm xuất (VNĐ)', default=0)
    thanh_tien = models.PositiveBigIntegerField('Thành tiền (VNĐ)', default=0)
    ghi_chu = models.CharField('Ghi chú', max_length=500, blank=True, default='')
    
    nguoi_nhap = models.ForeignKey(
        'Working.AppUser',
        on_delete=models.PROTECT,
        related_name='export_reports',
        verbose_name='Người nhập'
    )
    created_at = models.DateTimeField('Thời gian tạo', auto_now_add=True)
    updated_at = models.DateTimeField('Cập nhật lần cuối', auto_now=True)

    class Meta:
        verbose_name = 'Phiếu xuất hàng'
        verbose_name_plural = 'Phiếu xuất hàng'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.thanh_tien and self.so_luong_xuat and self.don_gia:
            self.thanh_tien = self.so_luong_xuat * self.don_gia
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Xuất {self.so_luong_xuat} cái {self.ma_hang}-{self.mau} ({self.ngay_xuat}) - {self.thanh_tien:,.0f} VNĐ"
