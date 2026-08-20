from django.db import models
import datetime

UNIT_CHOICES = [
    ("m", "m"),
    ("y", "y"),
    ("chiếc", "chiếc"),
]

class MaterialReceipt(models.Model):
    # Phiếu nhập nguyên liệu
    ngay_nhap = models.DateField("Ngày nhập", default=datetime.date.today)
    ma_hang = models.CharField("Mã hàng", max_length=255, null=False)
    mau = models.CharField("Màu", max_length=255, null=False)
    ten_vat_tu = models.CharField("Tên vật tư", max_length=255, null=False)
    
    so_luong_kien = models.PositiveIntegerField("Số lượng kiện/cây", default=0)
    so_luong = models.FloatField("Số lượng", default=0.0)
    don_vi = models.CharField("Đơn vị", max_length=20, choices=UNIT_CHOICES, default="m")

    # Người ghi nhận dữ liệu
    nguoi_nhap = models.ForeignKey(
        "Working.AppUser",
        on_delete=models.PROTECT,
        related_name="material_receipts",
        verbose_name="Người nhập",
    )

    created_at = models.DateTimeField("Thời gian nhập", auto_now_add=True)
    updated_at = models.DateTimeField("Cập nhật lần cuối", auto_now=True)

    class Meta:
        verbose_name = "Phiếu nhập nguyên liệu"
        verbose_name_plural = "Phiếu nhập nguyên liệu"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Nhập {self.ten_vat_tu} - {self.ma_hang} ({self.so_luong_kien} kiện, {self.so_luong} {self.don_vi})"


class MaterialIssue(models.Model):
    # Phiếu xuất nguyên liệu
    receipt = models.ForeignKey(
        MaterialReceipt,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="issues",
        verbose_name="Phiếu nhập gốc"
    )
    ngay_xuat = models.DateField("Ngày xuất", default=datetime.date.today)
    ma_hang = models.CharField("Mã hàng", max_length=255, null=False)
    mau = models.CharField("Màu", max_length=255, null=False)
    ten_vat_tu = models.CharField("Tên vật tư", max_length=255, null=False)
    
    so_luong_kien = models.PositiveIntegerField("Số lượng kiện/cây", default=0)
    so_luong = models.FloatField("Số lượng", default=0.0)
    don_vi = models.CharField("Đơn vị", max_length=20, choices=UNIT_CHOICES, default="m")
    
    # Người nhận (tên chữ)
    nguoi_nhan = models.CharField("Người nhận", max_length=255, null=False)

    # Người xuất (ghi nhận dữ liệu)
    nguoi_xuat = models.ForeignKey(
        "Working.AppUser",
        on_delete=models.PROTECT,
        related_name="material_issues",
        verbose_name="Người xuất",
    )

    created_at = models.DateTimeField("Thời gian nhập", auto_now_add=True)
    updated_at = models.DateTimeField("Cập nhật lần cuối", auto_now=True)

    class Meta:
        verbose_name = "Phiếu xuất nguyên liệu"
        verbose_name_plural = "Phiếu xuất nguyên liệu"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Xuất {self.ten_vat_tu} - {self.ma_hang} cho {self.nguoi_nhan} ({self.so_luong_kien} kiện, {self.so_luong} {self.don_vi})"
