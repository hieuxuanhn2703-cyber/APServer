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
    path("dashboard/", views.premium_dashboard_view, name="premium_dashboard"),
    
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
]