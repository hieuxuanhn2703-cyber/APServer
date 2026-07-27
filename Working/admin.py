from django.contrib import admin
from .models import ProcessReport, AppUser
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