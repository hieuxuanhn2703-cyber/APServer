from django.urls import path
from . import views

urlpatterns = [
    # 1. Bảng tổng hợp tất cả các nguyên vật liệu có trong kho
    path('tong-hop/', views.inventory_summary_view, name='inventory_summary'),
    
    # 2. Bảng lịch sử nhập nguyên vật liệu
    path('lich-su-nhap/', views.receipt_history_view, name='inventory_receipt_history'),
    
    # 3. Bảng lịch sử xuất nguyên vật liệu
    path('lich-su-xuat/', views.issue_history_view, name='inventory_issue_history'),
    
    # 4. Biểu Mẫu Ghi Nhận Nhập Kho
    path('nhap/', views.receipt_web_view, name='inventory_receipt_web'),
    path('nhap/edit/<int:row_id>/', views.receipt_edit_view, name='inventory_receipt_edit'),
    path('nhap/delete/<int:row_id>/', views.receipt_delete_view, name='inventory_receipt_delete'),
    
    # Thao tác xuất kho nhanh (từ Bảng 1)
    path('quick-issue/', views.quick_issue_view, name='inventory_quick_issue'),
    path('xuat/edit/<int:row_id>/', views.issue_edit_view, name='inventory_issue_edit'),
    path('xuat/delete/<int:row_id>/', views.issue_delete_view, name='inventory_issue_delete'),
    
    # Aliases
    path('danh-sach-xuat/', views.issue_history_view, name='inventory_issue_list'),
    path('danh-sach/', views.receipt_history_view, name='inventory_material_list'),
]
