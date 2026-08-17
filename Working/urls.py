from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("change-password/", views.change_password_view, name="change_password"),
    path("register/", views.register_view, name="register"),
    path("manage-accounts/", views.manage_accounts_view, name="manage_accounts"),
    path("toggle-account/<int:user_id>/", views.toggle_account_view, name="toggle_account"),
    path("delete-account/<int:user_id>/", views.delete_account_view, name="delete_account"),
    path("dashboard/", views.dashboard_cut_view, name="premium_dashboard"),
    path("dashboard/cut/", views.dashboard_cut_view, name="dashboard_cut"),
    path("dashboard/prod/", views.dashboard_prod_view, name="dashboard_prod"),
    path("dashboard/kcs/", views.dashboard_kcs_view, name="dashboard_kcs"),
    path("dashboard/finishing/", views.dashboard_finishing_view, name="dashboard_finishing"),
    
    path("config/", views.config_list_view, name="config_list"),
    path("config/product/add/", views.config_add_product_view, name="config_add_product"),
    path("config/color/add/<int:product_id>/", views.config_add_color_view, name="config_add_color"),
    path("config/color/edit/<int:color_id>/", views.config_edit_color_view, name="config_edit_color"),
    path("config/size/add/<int:color_id>/", views.config_add_size_view, name="config_add_size"),
    path("config/product/delete/<int:product_id>/", views.config_delete_product_view, name="config_delete_product"),
    path("config/color/delete/<int:color_id>/", views.config_delete_color_view, name="config_delete_color"),
    path("config/size/delete/<int:size_id>/", views.config_delete_size_view, name="config_delete_size"),
    
    path("export-excel/", views.export_excel_view, name="export_excel"),
    
    path("", views.web_view, name="web"),
    path("list/", views.list_view, name="list"),
    path("edit/<int:row_id>/", views.edit_view, name="edit"),
    path("delete/<int:row_id>/", views.delete_report_view, name="delete_report"),
    path("tracking/", views.tracking_view, name="tracking"),
    path("tracking/export/", views.tracking_export_excel_view, name="tracking_export_excel"),
    
    # Quy trình hoàn thiện
    path("finishing/", views.finishing_web_view, name="finishing_web"),
    path("finishing/list/", views.finishing_list_view, name="finishing_list"),
    path("finishing/edit/<int:row_id>/", views.finishing_edit_view, name="finishing_edit"),
    path("finishing/delete/<int:row_id>/", views.finishing_delete_report_view, name="finishing_delete_report"),
    path("finishing/export-excel/", views.finishing_export_excel_view, name="finishing_export_excel"),
    
    # Quy trình hoàn thiện - Các thao tác ngoại lệ
    path("finishing/ngoai-le/", views.finishing_ngoai_le_view, name="finishing_ngoai_le"),
    path("finishing/tra-hang/nhan-lai/<int:row_id>/", views.defect_receive_back_view, name="defect_receive_back"),
    path("finishing/lay-mau/nhan-lai/<int:row_id>/", views.sample_receive_back_view, name="sample_receive_back"),
    
    # Quy trình KCS
    path("kcs/", views.kcs_web_view, name="kcs_web"),
    path("kcs/list/", views.kcs_list_view, name="kcs_list"),
    path("kcs/edit/<int:row_id>/", views.kcs_edit_view, name="kcs_edit"),
    path("kcs/delete/<int:row_id>/", views.kcs_delete_report_view, name="kcs_delete_report"),
    path("kcs/export-excel/", views.kcs_export_excel_view, name="kcs_export_excel"),
    
    # Quy trình Cắt
    path("cut/", views.cut_web_view, name="cut_web"),
    path("cut/list/", views.cut_list_view, name="cut_list"),
    path("cut/edit/<int:row_id>/", views.cut_edit_view, name="cut_edit"),
    path("cut/delete/<int:row_id>/", views.cut_delete_report_view, name="cut_delete_report"),
    path("cut/export-excel/", views.cut_export_excel_view, name="cut_export_excel"),
]