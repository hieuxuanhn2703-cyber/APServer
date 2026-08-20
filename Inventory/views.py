import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Sum, Q
from .models import MaterialReceipt, MaterialIssue
from .forms import MaterialReceiptForm, MaterialIssueForm
from Working.models import AppUser
from Working.forms import load_config
from Working.views import get_current_user

def is_authorized(user):
    return user and user.role in ["KHO", "PREMIUM", "QUAN_LY", "KE_TOAN"]

def _clean_options(raw_list):
    cleaned = []
    for item in raw_list:
        if item is not None:
            s = str(item).strip()
            if s and s not in cleaned:
                cleaned.append(s)
    def sort_key(v):
        try:
            return (0, int(v))
        except ValueError:
            return (1, v.lower())
    cleaned.sort(key=sort_key)
    return cleaned

def parse_date_range(start_str, end_str):
    s = None
    e = None
    if start_str:
        try:
            s = datetime.date.fromisoformat(start_str)
        except (ValueError, TypeError):
            pass
    if end_str:
        try:
            e = datetime.date.fromisoformat(end_str)
        except (ValueError, TypeError):
            pass
    return s, e

def _get_cascade_options(base_qs, active_filters, current_col_key, val_field):
    qs = base_qs
    for key, (lookup, vals) in active_filters.items():
        if key != current_col_key and vals:
            qs = qs.filter(**{lookup: vals})
    return list(qs.values_list(val_field, flat=True).distinct())


def get_inventory_summary_data(filter_ma_hang=None, filter_mau=None, filter_ten_vat_tu=None, filter_don_vi=None):
    """
    Tính toán bảng tổng hợp cân đối tất cả nguyên vật liệu có trong kho:
    Thực nhận, Thực xuất, Còn lại (theo mã, màu, tên vật tư, đơn vị)
    """
    receipt_qs = MaterialReceipt.objects.all()
    issue_qs = MaterialIssue.objects.all()

    if filter_ma_hang:
        receipt_qs = receipt_qs.filter(ma_hang__in=filter_ma_hang)
        issue_qs = issue_qs.filter(ma_hang__in=filter_ma_hang)
    if filter_mau:
        receipt_qs = receipt_qs.filter(mau__in=filter_mau)
        issue_qs = issue_qs.filter(mau__in=filter_mau)
    if filter_ten_vat_tu:
        receipt_qs = receipt_qs.filter(ten_vat_tu__in=filter_ten_vat_tu)
        issue_qs = issue_qs.filter(ten_vat_tu__in=filter_ten_vat_tu)
    if filter_don_vi:
        receipt_qs = receipt_qs.filter(don_vi__in=filter_don_vi)
        issue_qs = issue_qs.filter(don_vi__in=filter_don_vi)

    receipts = receipt_qs.values('ma_hang', 'mau', 'ten_vat_tu', 'don_vi').annotate(
        tong_nhap_kien=Sum('so_luong_kien'),
        tong_nhap_so_luong=Sum('so_luong')
    )
    issues = issue_qs.values('ma_hang', 'mau', 'ten_vat_tu', 'don_vi').annotate(
        tong_xuat_kien=Sum('so_luong_kien'),
        tong_xuat_so_luong=Sum('so_luong')
    )

    summary_map = {}
    
    for r in receipts:
        d_vi = r['don_vi'] or 'm'
        key = (r['ma_hang'], r['mau'], r['ten_vat_tu'], d_vi)
        summary_map[key] = {
            'ma_hang': r['ma_hang'],
            'mau': r['mau'],
            'ten_vat_tu': r['ten_vat_tu'],
            'don_vi': d_vi,
            'nhap_kien': r['tong_nhap_kien'] or 0,
            'nhap_so_luong': r['tong_nhap_so_luong'] or 0.0,
            'xuat_kien': 0,
            'xuat_so_luong': 0.0,
        }

    for i in issues:
        d_vi = i['don_vi'] or 'm'
        key = (i['ma_hang'], i['mau'], i['ten_vat_tu'], d_vi)
        if key not in summary_map:
            summary_map[key] = {
                'ma_hang': i['ma_hang'],
                'mau': i['mau'],
                'ten_vat_tu': i['ten_vat_tu'],
                'don_vi': d_vi,
                'nhap_kien': 0,
                'nhap_so_luong': 0.0,
                'xuat_kien': 0,
                'xuat_so_luong': 0.0,
            }
        summary_map[key]['xuat_kien'] = i['tong_xuat_kien'] or 0
        summary_map[key]['xuat_so_luong'] = i['tong_xuat_so_luong'] or 0.0

    results = []
    for key, data in summary_map.items():
        data['con_lai_kien'] = data['nhap_kien'] - data['xuat_kien']
        data['con_lai_so_luong'] = data['nhap_so_luong'] - data['xuat_so_luong']
        data['has_stock'] = (data['con_lai_kien'] > 0 or data['con_lai_so_luong'] > 0)
        results.append(data)

    results.sort(key=lambda x: (x['ma_hang'], x['mau'], x['ten_vat_tu'], x['don_vi']))
    return results


# ==============================================================================
# BẢNG 1: BẢNG TỔNG HỢP TẤT CẢ NGUYÊN VẬT LIỆU CÓ TRONG KHO (KÈM NÚT XUẤT)
# ==============================================================================

def inventory_summary_view(request):
    """
    1. Bảng tổng hợp tất cả các nguyên vật liệu có trong kho
    (Cân đối Thực nhận - Thực xuất - Còn lại, cột Thao tác có nút Xuất, nếu hết thì ẩn đi)
    """
    user = get_current_user(request)
    if not is_authorized(user):
        raise PermissionDenied("Bạn không có quyền truy cập trang này.")
    
    summary_filter_ma_hang = [v for v in request.GET.getlist('summary_filter_ma_hang') if v]
    summary_filter_mau = [v for v in request.GET.getlist('summary_filter_mau') if v]
    summary_filter_ten_vat_tu = [v for v in request.GET.getlist('summary_filter_ten_vat_tu') if v]
    summary_filter_don_vi = [v for v in request.GET.getlist('summary_filter_don_vi') if v]

    # Danh sách options cho bộ lọc
    r_ma = list(MaterialReceipt.objects.values_list('ma_hang', flat=True).distinct())
    i_ma = list(MaterialIssue.objects.values_list('ma_hang', flat=True).distinct())
    opt_ma_hang = sorted(list(set(r_ma + i_ma)))

    r_mau = list(MaterialReceipt.objects.values_list('mau', flat=True).distinct())
    i_mau = list(MaterialIssue.objects.values_list('mau', flat=True).distinct())
    opt_mau = sorted(list(set(r_mau + i_mau)))

    r_vt = list(MaterialReceipt.objects.values_list('ten_vat_tu', flat=True).distinct())
    i_vt = list(MaterialIssue.objects.values_list('ten_vat_tu', flat=True).distinct())
    opt_ten_vat_tu = sorted(list(set(r_vt + i_vt)))

    r_dv = list(MaterialReceipt.objects.values_list('don_vi', flat=True).distinct())
    i_dv = list(MaterialIssue.objects.values_list('don_vi', flat=True).distinct())
    opt_don_vi = sorted(list(set(r_dv + i_dv)))

    summary_data = get_inventory_summary_data(
        filter_ma_hang=summary_filter_ma_hang,
        filter_mau=summary_filter_mau,
        filter_ten_vat_tu=summary_filter_ten_vat_tu,
        filter_don_vi=summary_filter_don_vi
    )

    excel_filter_config = {
        "summary": {
            "page_param": "page",
            "columns": {
                "0": {"param": "summary_filter_ma_hang", "title": "Mã hàng", "options": _clean_options(opt_ma_hang), "selected": summary_filter_ma_hang},
                "1": {"param": "summary_filter_mau", "title": "Màu", "options": _clean_options(opt_mau), "selected": summary_filter_mau},
                "2": {"param": "summary_filter_ten_vat_tu", "title": "Tên vật tư", "options": _clean_options(opt_ten_vat_tu), "selected": summary_filter_ten_vat_tu},
                "3": {"param": "summary_filter_don_vi", "title": "Đơn vị", "options": _clean_options(opt_don_vi), "selected": summary_filter_don_vi},
            }
        }
    }

    has_filter = bool(summary_filter_ma_hang or summary_filter_mau or summary_filter_ten_vat_tu or summary_filter_don_vi)

    return render(request, "Inventory/summary.html", {
        "user": user,
        "inventory_summary_data": summary_data,
        "summary_data": summary_data,
        "excel_filter_config": excel_filter_config,
        "has_filter": has_filter,
    })


# ==============================================================================
# BẢNG 2: BẢNG LỊCH SỬ NHẬP NGUYÊN VẬT LIỆU (20 DÒNG / TRANG)
# ==============================================================================

def receipt_history_view(request):
    """
    2. Bảng lịch sử nhập nguyên vật liệu, lưu lại tất cả những lần nhập nguyên vật liệu (20 dòng / trang)
    Hỗ trợ lọc ngày (từ ngày - đến ngày) và lọc cột Excel (Mã hàng, Màu, Tên vật tư, Đơn vị, Người nhập)
    """
    user = get_current_user(request)
    if not is_authorized(user):
        raise PermissionDenied("Bạn không có quyền truy cập trang này.")

    receipt_start_date = request.GET.get('receipt_start_date', '')
    receipt_end_date = request.GET.get('receipt_end_date', '')
    receipt_s, receipt_e = parse_date_range(receipt_start_date, receipt_end_date)

    receipt_base_qs = MaterialReceipt.objects.select_related('nguoi_nhap').all()
    if receipt_s:
        receipt_base_qs = receipt_base_qs.filter(ngay_nhap__gte=receipt_s)
    if receipt_e:
        receipt_base_qs = receipt_base_qs.filter(ngay_nhap__lte=receipt_e)

    receipt_filter_ma_hang = [v for v in request.GET.getlist('receipt_filter_ma_hang') if v]
    receipt_filter_mau = [v for v in request.GET.getlist('receipt_filter_mau') if v]
    receipt_filter_ten_vat_tu = [v for v in request.GET.getlist('receipt_filter_ten_vat_tu') if v]
    receipt_filter_don_vi = [v for v in request.GET.getlist('receipt_filter_don_vi') if v]
    receipt_filter_nguoi_nhap = [v for v in request.GET.getlist('receipt_filter_nguoi_nhap') if v]

    receipt_filters = {
        'ma_hang': ('ma_hang__in', receipt_filter_ma_hang),
        'mau': ('mau__in', receipt_filter_mau),
        'ten_vat_tu': ('ten_vat_tu__in', receipt_filter_ten_vat_tu),
        'don_vi': ('don_vi__in', receipt_filter_don_vi),
        'nguoi_nhap': ('nguoi_nhap__name__in', receipt_filter_nguoi_nhap),
    }

    opt_ma_hang = _get_cascade_options(receipt_base_qs, receipt_filters, 'ma_hang', 'ma_hang')
    opt_mau = _get_cascade_options(receipt_base_qs, receipt_filters, 'mau', 'mau')
    opt_ten_vat_tu = _get_cascade_options(receipt_base_qs, receipt_filters, 'ten_vat_tu', 'ten_vat_tu')
    opt_don_vi = _get_cascade_options(receipt_base_qs, receipt_filters, 'don_vi', 'don_vi')
    opt_nguoi_nhap = _get_cascade_options(receipt_base_qs, receipt_filters, 'nguoi_nhap', 'nguoi_nhap__name')

    receipt_qs = receipt_base_qs
    if receipt_filter_ma_hang:
        receipt_qs = receipt_qs.filter(ma_hang__in=receipt_filter_ma_hang)
    if receipt_filter_mau:
        receipt_qs = receipt_qs.filter(mau__in=receipt_filter_mau)
    if receipt_filter_ten_vat_tu:
        receipt_qs = receipt_qs.filter(ten_vat_tu__in=receipt_filter_ten_vat_tu)
    if receipt_filter_don_vi:
        receipt_qs = receipt_qs.filter(don_vi__in=receipt_filter_don_vi)
    if receipt_filter_nguoi_nhap:
        receipt_qs = receipt_qs.filter(nguoi_nhap__name__in=receipt_filter_nguoi_nhap)

    receipt_qs = receipt_qs.order_by('-ngay_nhap', '-created_at')

    excel_filter_config = {
        "receipt": {
            "page_param": "page",
            "columns": {
                "1": {"param": "receipt_filter_ma_hang", "title": "Mã hàng", "options": _clean_options(opt_ma_hang), "selected": receipt_filter_ma_hang},
                "2": {"param": "receipt_filter_mau", "title": "Màu", "options": _clean_options(opt_mau), "selected": receipt_filter_mau},
                "3": {"param": "receipt_filter_ten_vat_tu", "title": "Tên vật tư", "options": _clean_options(opt_ten_vat_tu), "selected": receipt_filter_ten_vat_tu},
                "4": {"param": "receipt_filter_don_vi", "title": "Đơn vị", "options": _clean_options(opt_don_vi), "selected": receipt_filter_don_vi},
                "7": {"param": "receipt_filter_nguoi_nhap", "title": "Người nhập", "options": _clean_options(opt_nguoi_nhap), "selected": receipt_filter_nguoi_nhap},
            }
        }
    }

    paginator = Paginator(receipt_qs, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    has_filter = bool(
        receipt_start_date or receipt_end_date or
        receipt_filter_ma_hang or receipt_filter_mau or
        receipt_filter_ten_vat_tu or receipt_filter_don_vi or receipt_filter_nguoi_nhap
    )

    return render(request, "Inventory/receipt_history.html", {
        "user": user,
        "page_obj": page_obj,
        "excel_filter_config": excel_filter_config,
        "receipt_start_date": receipt_start_date,
        "receipt_end_date": receipt_end_date,
        "has_filter": has_filter,
    })


# ==============================================================================
# BẢNG 3: BẢNG LỊCH SỬ XUẤT NGUYÊN VẬT LIỆU (20 DÒNG / TRANG)
# ==============================================================================

def issue_history_view(request):
    """
    3. Bảng lịch sử xuất nguyên vật liệu, lưu lại tất cả những lần xuất nguyên vật liệu (20 dòng / trang)
    Hỗ trợ lọc ngày (từ ngày - đến ngày) và lọc cột Excel (Mã hàng, Màu, Tên vật tư, Đơn vị, Người nhận, Người xuất)
    """
    user = get_current_user(request)
    if not is_authorized(user):
        raise PermissionDenied("Bạn không có quyền truy cập trang này.")

    issue_start_date = request.GET.get('issue_start_date', '')
    issue_end_date = request.GET.get('issue_end_date', '')
    issue_s, issue_e = parse_date_range(issue_start_date, issue_end_date)

    issue_base_qs = MaterialIssue.objects.select_related('nguoi_xuat').all()
    if issue_s:
        issue_base_qs = issue_base_qs.filter(ngay_xuat__gte=issue_s)
    if issue_e:
        issue_base_qs = issue_base_qs.filter(ngay_xuat__lte=issue_e)

    issue_filter_ma_hang = [v for v in request.GET.getlist('issue_filter_ma_hang') if v]
    issue_filter_mau = [v for v in request.GET.getlist('issue_filter_mau') if v]
    issue_filter_ten_vat_tu = [v for v in request.GET.getlist('issue_filter_ten_vat_tu') if v]
    issue_filter_don_vi = [v for v in request.GET.getlist('issue_filter_don_vi') if v]
    issue_filter_nguoi_nhan = [v for v in request.GET.getlist('issue_filter_nguoi_nhan') if v]
    issue_filter_nguoi_xuat = [v for v in request.GET.getlist('issue_filter_nguoi_xuat') if v]

    issue_filters = {
        'ma_hang': ('ma_hang__in', issue_filter_ma_hang),
        'mau': ('mau__in', issue_filter_mau),
        'ten_vat_tu': ('ten_vat_tu__in', issue_filter_ten_vat_tu),
        'don_vi': ('don_vi__in', issue_filter_don_vi),
        'nguoi_nhan': ('nguoi_nhan__in', issue_filter_nguoi_nhan),
        'nguoi_xuat': ('nguoi_xuat__name__in', issue_filter_nguoi_xuat),
    }

    opt_ma_hang = _get_cascade_options(issue_base_qs, issue_filters, 'ma_hang', 'ma_hang')
    opt_mau = _get_cascade_options(issue_base_qs, issue_filters, 'mau', 'mau')
    opt_ten_vat_tu = _get_cascade_options(issue_base_qs, issue_filters, 'ten_vat_tu', 'ten_vat_tu')
    opt_don_vi = _get_cascade_options(issue_base_qs, issue_filters, 'don_vi', 'don_vi')
    opt_nguoi_nhan = _get_cascade_options(issue_base_qs, issue_filters, 'nguoi_nhan', 'nguoi_nhan')
    opt_nguoi_xuat = _get_cascade_options(issue_base_qs, issue_filters, 'nguoi_xuat', 'nguoi_xuat__name')

    issue_qs = issue_base_qs
    if issue_filter_ma_hang:
        issue_qs = issue_qs.filter(ma_hang__in=issue_filter_ma_hang)
    if issue_filter_mau:
        issue_qs = issue_qs.filter(mau__in=issue_filter_mau)
    if issue_filter_ten_vat_tu:
        issue_qs = issue_qs.filter(ten_vat_tu__in=issue_filter_ten_vat_tu)
    if issue_filter_don_vi:
        issue_qs = issue_qs.filter(don_vi__in=issue_filter_don_vi)
    if issue_filter_nguoi_nhan:
        issue_qs = issue_qs.filter(nguoi_nhan__in=issue_filter_nguoi_nhan)
    if issue_filter_nguoi_xuat:
        issue_qs = issue_qs.filter(nguoi_xuat__name__in=issue_filter_nguoi_xuat)

    issue_qs = issue_qs.order_by('-ngay_xuat', '-created_at')

    excel_filter_config = {
        "issue": {
            "page_param": "page",
            "columns": {
                "1": {"param": "issue_filter_ma_hang", "title": "Mã hàng", "options": _clean_options(opt_ma_hang), "selected": issue_filter_ma_hang},
                "2": {"param": "issue_filter_mau", "title": "Màu", "options": _clean_options(opt_mau), "selected": issue_filter_mau},
                "3": {"param": "issue_filter_ten_vat_tu", "title": "Tên vật tư", "options": _clean_options(opt_ten_vat_tu), "selected": issue_filter_ten_vat_tu},
                "4": {"param": "issue_filter_don_vi", "title": "Đơn vị", "options": _clean_options(opt_don_vi), "selected": issue_filter_don_vi},
                "7": {"param": "issue_filter_nguoi_nhan", "title": "Người nhận", "options": _clean_options(opt_nguoi_nhan), "selected": issue_filter_nguoi_nhan},
                "8": {"param": "issue_filter_nguoi_xuat", "title": "Người xuất", "options": _clean_options(opt_nguoi_xuat), "selected": issue_filter_nguoi_xuat},
            }
        }
    }

    paginator = Paginator(issue_qs, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    has_filter = bool(
        issue_start_date or issue_end_date or
        issue_filter_ma_hang or issue_filter_mau or
        issue_filter_ten_vat_tu or issue_filter_don_vi or issue_filter_nguoi_nhan or issue_filter_nguoi_xuat
    )

    return render(request, "Inventory/issue_history.html", {
        "user": user,
        "page_obj": page_obj,
        "excel_filter_config": excel_filter_config,
        "issue_start_date": issue_start_date,
        "issue_end_date": issue_end_date,
        "has_filter": has_filter,
    })


# ==============================================================================
# BIỂU MẪU GHI NHẬN NHẬP KHO
# ==============================================================================

def receipt_web_view(request):
    """
    Biểu Mẫu Ghi Nhận Nhập Kho
    """
    user = get_current_user(request)
    if not is_authorized(user):
        raise PermissionDenied("Bạn không có quyền truy cập trang này.")

    success = False
    if request.method == "POST":
        form = MaterialReceiptForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.nguoi_nhap = user
            report.save()
            return redirect("inventory_summary")
    else:
        form = MaterialReceiptForm()

    return render(request, "Inventory/receipt_web.html", {
        "form": form,
        "user": user,
        "config": load_config(),
        "success": success,
    })


# ==============================================================================
# THAO TÁC XUẤT KHO (TỪ NÚT XUẤT TRÊN BẢNG TỔNG HỢP)
# ==============================================================================

def quick_issue_view(request):
    user = get_current_user(request)
    if not is_authorized(user):
        raise PermissionDenied("Bạn không có quyền thực hiện thao tác này.")

    if request.method == "POST":
        ma_hang = request.POST.get("ma_hang", "").strip()
        mau = request.POST.get("mau", "").strip()
        ten_vat_tu = request.POST.get("ten_vat_tu", "").strip()
        don_vi = request.POST.get("don_vi", "m").strip() or "m"
        ngay_xuat_str = request.POST.get("ngay_xuat", "").strip()
        so_luong_kien_str = request.POST.get("so_luong_kien", "0").strip()
        so_luong_str = request.POST.get("so_luong", "0").strip()
        nguoi_nhan = request.POST.get("nguoi_nhan", "").strip()

        ngay_xuat = datetime.date.today()
        if ngay_xuat_str:
            try:
                ngay_xuat = datetime.date.fromisoformat(ngay_xuat_str)
            except (ValueError, TypeError):
                pass

        try:
            so_luong_kien = max(0, int(so_luong_kien_str or 0))
        except (ValueError, TypeError):
            so_luong_kien = 0

        try:
            so_luong = max(0.0, float(so_luong_str or 0))
        except (ValueError, TypeError):
            so_luong = 0.0

        if don_vi == "chiếc":
            if so_luong <= 0 or not float(so_luong).is_integer():
                so_luong = int(so_luong) if float(so_luong).is_integer() and so_luong > 0 else 0

        if ma_hang and mau and ten_vat_tu and nguoi_nhan and (so_luong_kien > 0 or so_luong > 0):
            MaterialIssue.objects.create(
                ngay_xuat=ngay_xuat,
                ma_hang=ma_hang,
                mau=mau,
                ten_vat_tu=ten_vat_tu,
                so_luong_kien=so_luong_kien,
                so_luong=so_luong,
                don_vi=don_vi,
                nguoi_nhan=nguoi_nhan,
                nguoi_xuat=user
            )

        next_url = request.POST.get("next") or request.META.get('HTTP_REFERER') or reverse('inventory_summary')
        return redirect(next_url)

    return redirect('inventory_summary')


# ==============================================================================
# SỬA / XÓA PHIẾU NHẬP (CHỈ QUẢN LÝ / ADMIN MỚI CÓ QUYỀN)
# ==============================================================================

def receipt_edit_view(request, row_id):
    user = get_current_user(request)
    if not user or user.role not in ["PREMIUM", "QUAN_LY"]:
        raise PermissionDenied("Chỉ quản lý mới có quyền chỉnh sửa phiếu nhập kho.")
    
    report = get_object_or_404(MaterialReceipt, id=row_id)

    if request.method == "POST":
        form = MaterialReceiptForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            return redirect("inventory_receipt_history")
    else:
        form = MaterialReceiptForm(instance=report)

    return render(request, "Inventory/receipt_edit.html", {
        "form": form,
        "report": report,
        "user": user,
        "config": load_config(),
    })

def receipt_delete_view(request, row_id):
    user = get_current_user(request)
    if not user or user.role not in ["PREMIUM", "QUAN_LY"]:
        raise PermissionDenied("Chỉ quản lý mới có quyền xóa phiếu nhập kho.")
        
    report = get_object_or_404(MaterialReceipt, id=row_id)
    report.delete()
    return redirect("inventory_receipt_history")


# ==============================================================================
# SỬA / XÓA PHIẾU XUẤT (CHỈ QUẢN LÝ / ADMIN MỚI CÓ QUYỀN)
# ==============================================================================

def issue_edit_view(request, row_id):
    user = get_current_user(request)
    if not user or user.role not in ["PREMIUM", "QUAN_LY"]:
        raise PermissionDenied("Chỉ quản lý mới có quyền chỉnh sửa phiếu xuất kho.")
    
    report = get_object_or_404(MaterialIssue, id=row_id)

    if request.method == "POST":
        form = MaterialIssueForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            return redirect("inventory_issue_history")
    else:
        form = MaterialIssueForm(instance=report)

    return render(request, "Inventory/issue_edit.html", {
        "form": form,
        "report": report,
        "user": user,
        "config": load_config(),
    })

def issue_delete_view(request, row_id):
    user = get_current_user(request)
    if not user or user.role not in ["PREMIUM", "QUAN_LY"]:
        raise PermissionDenied("Chỉ quản lý mới có quyền xóa phiếu xuất kho.")
        
    report = get_object_or_404(MaterialIssue, id=row_id)
    report.delete()
    next_url = request.META.get('HTTP_REFERER') or reverse('inventory_issue_history')
    return redirect(next_url)
