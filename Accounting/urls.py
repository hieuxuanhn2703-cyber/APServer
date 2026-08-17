from django.urls import path
from . import views

app_name = "accounting"

urlpatterns = [
    path("", views.accounting_dashboard_view, name="dashboard"),
    path("xuat-hang/", views.export_entry_view, name="export_entry"),
    path("xuat-hang/edit/<int:row_id>/", views.export_edit_view, name="export_edit"),
    path("xuat-hang/delete/<int:row_id>/", views.export_delete_view, name="export_delete"),
    path("don-gia/", views.price_management_view, name="price_management"),
    path("export-excel/", views.accounting_export_excel_view, name="export_excel"),
]
