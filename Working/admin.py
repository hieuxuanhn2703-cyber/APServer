from django.contrib import admin
from .models import ProcessReport, AppUser, CutReport, FinishingReport, KcsReport, DefectReturnReport, SampleTakeReport, DefectReceiveLog, SampleReceiveLog
# p.x.hieu
# Xinchao2026
@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "account")
    search_fields = ("name", "account")


@admin.register(ProcessReport)
class ProcessReportAdmin(admin.ModelAdmin):
    list_display = ("id", "ma_hang", "mau", "size", "nguoi_nhap", "created_at")
    list_filter = ("ma_hang", "mau", "nguoi_nhap")
    search_fields = ("ma_hang", "mau", "size")

@admin.register(CutReport)
class CutReportAdmin(admin.ModelAdmin):
    list_display = ("id", "ma_hang", "mau", "nguoi_nhap", "created_at")
    list_filter = ("ma_hang", "mau", "nguoi_nhap")
    search_fields = ("ma_hang", "mau")

@admin.register(FinishingReport)
class FinishingReportAdmin(admin.ModelAdmin):
    list_display = ("id", "ma_hang", "mau", "nguoi_nhap", "created_at")
    list_filter = ("ma_hang", "mau", "nguoi_nhap")
    search_fields = ("ma_hang", "mau")

@admin.register(KcsReport)
class KcsReportAdmin(admin.ModelAdmin):
    list_display = ("id", "ma_hang", "mau", "nguoi_nhap", "created_at")
    list_filter = ("ma_hang", "mau", "nguoi_nhap")
    search_fields = ("ma_hang", "mau")

@admin.register(DefectReturnReport)
class DefectReturnReportAdmin(admin.ModelAdmin):
    list_display = ("id", "ma_hang", "mau", "so_luong_tra", "so_luong_nhan_lai", "nguoi_nhap", "created_at")
    list_filter = ("ma_hang", "mau", "nguoi_nhap")
    search_fields = ("ma_hang", "mau")

@admin.register(SampleTakeReport)
class SampleTakeReportAdmin(admin.ModelAdmin):
    list_display = ("id", "ma_hang", "mau", "nguoi_lay", "so_luong_lay", "so_luong_nhan_lai", "nguoi_nhap", "created_at")
    list_filter = ("ma_hang", "mau", "nguoi_lay", "nguoi_nhap")
    search_fields = ("ma_hang", "mau", "nguoi_lay")

@admin.register(DefectReceiveLog)
class DefectReceiveLogAdmin(admin.ModelAdmin):
    list_display = ("id", "report", "ngay_nhan", "so_luong", "nguoi_nhap", "created_at")
    list_filter = ("ngay_nhan", "nguoi_nhap")

@admin.register(SampleReceiveLog)
class SampleReceiveLogAdmin(admin.ModelAdmin):
    list_display = ("id", "report", "ngay_nhan", "so_luong", "nguoi_nhap", "created_at")
    list_filter = ("ngay_nhan", "nguoi_nhap")