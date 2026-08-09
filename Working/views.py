from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
import openpyxl
from django.core.exceptions import PermissionDenied
from django.db.models import Sum

from .forms import ProcessForm, load_config
from .models import ProcessReport, AppUser, Product, ProductColor, ProductSize
from .auth_utils import verify_credentials, get_current_user, login_required, SESSION_KEY

HEADERS = [
    "Thời gian", "Mã hàng", "Màu", "Cỡ", "Tổ", "Nhận BTP", "Vào chuyền",
    "Giữa chuyền", "Ra chuyền", "Thu hóa", "Là thành phẩm", "KCS",
    "Nhập hoàn thiện", "Người nhập",
]


def _report_to_row(report: ProcessReport):
    """Chuyển 1 đối tượng ProcessReport thành dict phù hợp với template list.html hiện có."""
    values = [
        report.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        report.ma_hang,
        report.mau,
        "N/A",  # Tạm thời ép hiển thị cỡ là N/A
        report.to,
        report.nhan_btp,
        report.vao_chuyen,
        report.giua_chuyen,
        report.ra_chuyen,
        report.thu_hoa,
        report.la_thanh_pham,
        report.kcs,
        report.nhap_hoan_thien,
        report.nguoi_nhap.name,
    ]
    return {
        "row_id": report.id,
        "values": values,
        "pairs": list(zip(HEADERS, values)),
    }


# ---------- Đăng nhập / Đăng xuất ----------

def login_view(request):
    error = None
    if request.method == "POST":
        account = request.POST.get("account", "").strip()
        password = request.POST.get("password", "")

        user = verify_credentials(account, password)
        if user:
            if not user.is_approved:
                error = "Tài khoản của bạn đang chờ quản trị viên phê duyệt."
            else:
                request.session[SESSION_KEY] = user.id
                request.session["display_name"] = user.name
                
                if user.role == "PREMIUM":
                    return redirect("list")
                return redirect("web")
        else:
            error = "Tài khoản hoặc mật khẩu không đúng."

    return render(request, "login.html", {"error": error})


def logout_view(request):
    request.session.flush()
    return redirect("login")


# ---------- Đăng ký & Duyệt tài khoản ----------

def register_view(request):
    error = None
    success = False
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        account = request.POST.get("account", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")
        
        if password != confirm_password:
            error = "Mật khẩu nhập lại không khớp."
        elif AppUser.objects.filter(account=account).exists():
            error = "Tài khoản này đã tồn tại, vui lòng chọn tên khác."
        else:
            AppUser.objects.create(
                name=name,
                account=account,
                password=password,
                is_approved=False
            )
            success = True
            
    return render(request, "register.html", {"error": error, "success": success})


@login_required
def manage_accounts_view(request):
    current_user = get_current_user(request)
    if current_user.role != "PREMIUM":
        raise PermissionDenied("Chỉ quản trị viên cấp cao mới có quyền truy cập trang này.")
        
    all_users = AppUser.objects.exclude(id=current_user.id).order_by("-id")
    return render(request, "manage_accounts.html", {
        "users": all_users,
        "display_name": current_user.name
    })


@login_required
def toggle_account_view(request, user_id):
    current_user = get_current_user(request)
    if current_user.role != "PREMIUM":
        raise PermissionDenied("Chỉ quản trị viên cấp cao mới có quyền duyệt tài khoản.")
        
    user_to_toggle = get_object_or_404(AppUser, id=user_id)
    user_to_toggle.is_approved = not user_to_toggle.is_approved
    user_to_toggle.save()
    return redirect("manage_accounts")


# ---------- Quản lý Cấu hình (PREMIUM) ----------

@login_required
def config_list_view(request):
    current_user = get_current_user(request)
    if current_user.role != "PREMIUM":
        raise PermissionDenied("Chỉ quản trị viên cấp cao mới có quyền truy cập trang này.")
        
    products = Product.objects.prefetch_related('colors__sizes').all()
    return render(request, "config_list.html", {
        "products": products,
        "display_name": current_user.name
    })

@login_required
def config_add_product_view(request):
    current_user = get_current_user(request)
    if current_user.role != "PREMIUM":
        raise PermissionDenied("Chỉ quản trị viên cấp cao mới có quyền truy cập trang này.")
    
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        colors = request.POST.get("colors", "").strip()
        sizes = request.POST.getlist("sizes")
        
        if name:
            if colors:
                # Thay dấu phẩy thành xuống dòng để hỗ trợ cả 2 cách nhập
                color_list = [c.strip() for c in colors.replace(',', '\n').split('\n') if c.strip()]
                parsed_colors = []
                for color_line in color_list:
                    # Hỗ trợ phân cách bằng dấu ':' hoặc '-'
                    parts = color_line.replace('-', ':').split(':')
                    color_name = parts[0].strip()
                    
                    if len(parts) < 2 or not parts[1].strip():
                        return render(request, "config_add.html", {
                            "type": "product",
                            "default_sizes": ["XS", "S", "M", "L", "XL", "XXL", "XXXL"],
                            "error": f"Lỗi: Màu '{color_name}' chưa được nhập số lượng. Vui lòng nhập theo định dạng 'Màu - Số lượng'."
                        })
                    
                    try:
                        quantity = int(parts[1].strip())
                    except ValueError:
                        return render(request, "config_add.html", {
                            "type": "product",
                            "default_sizes": ["XS", "S", "M", "L", "XL", "XXL", "XXXL"],
                            "error": f"Lỗi: Số lượng của màu '{color_name}' không hợp lệ."
                        })
                    parsed_colors.append((color_name, quantity))
                    
                product, _ = Product.objects.get_or_create(name=name)
                for color_name, quantity in parsed_colors:
                    if color_name:
                        color_obj, _ = ProductColor.objects.get_or_create(product=product, name=color_name)
                        color_obj.quantity = quantity
                        color_obj.save()
                        for size_name in sizes:
                            pass # Tạm thời không tạo ProductSize
            else:
                Product.objects.get_or_create(name=name)
                
        return redirect("config_list")
        
    return render(request, "config_add.html", {
        "type": "product",
        "default_sizes": ["N/A"]
    })

@login_required
def config_add_color_view(request, product_id):
    current_user = get_current_user(request)
    if current_user.role != "PREMIUM":
        raise PermissionDenied("Chỉ quản trị viên cấp cao mới có quyền truy cập trang này.")
        
    product = get_object_or_404(Product, pk=product_id)
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        quantity_str = request.POST.get("quantity", "").strip()
        
        if not quantity_str:
            return render(request, "config_add.html", {"type": "color", "parent": product, "error": "Vui lòng nhập số lượng."})
            
        try:
            qty = int(quantity_str)
        except ValueError:
            return render(request, "config_add.html", {"type": "color", "parent": product, "error": "Số lượng không hợp lệ."})
            
        if name:
            color_obj, created = ProductColor.objects.get_or_create(product=product, name=name)
            color_obj.quantity = qty
            color_obj.save()
        return redirect("config_list")
        
    return render(request, "config_add.html", {"type": "color", "parent": product})

@login_required
def config_add_size_view(request, color_id):
    current_user = get_current_user(request)
    if current_user.role != "PREMIUM":
        raise PermissionDenied("Chỉ quản trị viên cấp cao mới có quyền truy cập trang này.")
        
    color = get_object_or_404(ProductColor, pk=color_id)
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        if name:
            # Cho phép nhập nhiều cỡ cùng lúc, cách nhau bằng dấu phẩy
            sizes = [s.strip() for s in name.split(',') if s.strip()]
            for s in sizes:
                ProductSize.objects.get_or_create(color=color, name=s)
        return redirect("config_list")
        
    return render(request, "config_add.html", {"type": "size", "parent": color})

@login_required
def config_delete_product_view(request, product_id):
    current_user = get_current_user(request)
    if current_user.role != "PREMIUM":
        raise PermissionDenied("Chỉ quản trị viên cấp cao mới có quyền truy cập trang này.")
    
    if request.method == "POST":
        product = get_object_or_404(Product, pk=product_id)
        product.delete()
    return redirect("config_list")

@login_required
def config_delete_color_view(request, color_id):
    current_user = get_current_user(request)
    if current_user.role != "PREMIUM":
        raise PermissionDenied("Chỉ quản trị viên cấp cao mới có quyền truy cập trang này.")
    
    if request.method == "POST":
        color = get_object_or_404(ProductColor, pk=color_id)
        color.delete()
    return redirect("config_list")

@login_required
def config_delete_size_view(request, size_id):
    current_user = get_current_user(request)
    if current_user.role != "PREMIUM":
        raise PermissionDenied("Chỉ quản trị viên cấp cao mới có quyền truy cập trang này.")
    
    if request.method == "POST":
        size = get_object_or_404(ProductSize, pk=size_id)
        size.delete()
    return redirect("config_list")


@login_required
def export_excel_view(request):
    current_user = get_current_user(request)
    if current_user.role != "PREMIUM":
        raise PermissionDenied("Chỉ quản trị viên cấp cao mới có quyền xuất dữ liệu.")

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="DuLieuBaoCao.xlsx"'

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Dữ liệu"

    # Ghi headers
    ws.append(HEADERS)

    # Lấy dữ liệu và ghi vào sheet
    reports = ProcessReport.objects.all().order_by("-created_at")
    for report in reports:
        row = _report_to_row(report)
        ws.append(row["values"])

    wb.save(response)
    return response


# ---------- Nhập dữ liệu ----------

@login_required
def web_view(request):
    success = False
    current_user = get_current_user(request)

    if request.method == "POST":
        form = ProcessForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            ProcessReport.objects.create(
                ma_hang=data["ma_hang"],
                mau=data["mau"],
                size="N/A",  # Ép kiểu cỡ là N/A
                to=data.get("to") or 0,
                nhan_btp=data.get("nhan_btp") or 0,
                vao_chuyen=data.get("vao_chuyen") or 0,
                giua_chuyen=data.get("giua_chuyen") or 0,
                ra_chuyen=data.get("ra_chuyen") or 0,
                thu_hoa=data.get("thu_hoa") or 0,
                la_thanh_pham=data.get("la_thanh_pham") or 0,
                kcs=data.get("kcs") or 0,
                nhap_hoan_thien=data.get("nhap_hoan_thien") or 0,
                nguoi_nhap=current_user,
            )
            success = True
            form = ProcessForm()
    else:
        form = ProcessForm()

    return render(request, "web.html", {
        "form": form,
        "success": success,
        "config": load_config(),
        "display_name": current_user.name if current_user else "",
        "is_premium": current_user.role == "PREMIUM" if current_user else False,
    })


# ---------- Danh sách dữ liệu (chỉ của người đang đăng nhập) ----------

@login_required
def list_view(request):
    current_user = get_current_user(request)

    if current_user.role == "PREMIUM":
        reports = ProcessReport.objects.all()
    else:
        reports = ProcessReport.objects.filter(nguoi_nhap=current_user)
        
    table_rows = [_report_to_row(r) for r in reports]

    return render(request, "list.html", {
        "table_rows": table_rows,
        "headers": HEADERS,
        "display_name": current_user.name if current_user else "",
        "is_premium": current_user.role == "PREMIUM" if current_user else False,
    })


# ---------- Sửa dữ liệu (chỉ dòng của chính người đăng nhập) ----------

@login_required
def edit_view(request, row_id):
    current_user = get_current_user(request)
    report = get_object_or_404(ProcessReport, pk=row_id)

    if report.nguoi_nhap_id != current_user.id and current_user.role != "PREMIUM":
        raise PermissionDenied("Bạn không có quyền sửa dữ liệu này.")

    if request.method == "POST":
        form = ProcessForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            report.ma_hang = data["ma_hang"]
            report.mau = data["mau"]
            report.size = "N/A"  # Ép kiểu cỡ là N/A
            report.to = data.get("to") or 0
            report.nhan_btp = data.get("nhan_btp") or 0
            report.vao_chuyen = data.get("vao_chuyen") or 0
            report.giua_chuyen = data.get("giua_chuyen") or 0
            report.ra_chuyen = data.get("ra_chuyen") or 0
            report.thu_hoa = data.get("thu_hoa") or 0
            report.la_thanh_pham = data.get("la_thanh_pham") or 0
            report.kcs = data.get("kcs") or 0
            report.nhap_hoan_thien = data.get("nhap_hoan_thien") or 0
            report.save()
            return redirect("list")
    else:
        initial = {
            "ma_hang": report.ma_hang,
            "mau": report.mau,
            "co": "N/A", # Ép kiểu cỡ là N/A
            "to": report.to,
            "nhan_btp": report.nhan_btp,
            "vao_chuyen": report.vao_chuyen,
            "giua_chuyen": report.giua_chuyen,
            "ra_chuyen": report.ra_chuyen,
            "thu_hoa": report.thu_hoa,
            "la_thanh_pham": report.la_thanh_pham,
            "kcs": report.kcs,
            "nhap_hoan_thien": report.nhap_hoan_thien,
        }
        form = ProcessForm(initial=initial)

    return render(request, "edit.html", {
        "form": form,
        "thoi_gian": report.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "config": load_config(),
        "display_name": current_user.name if current_user else "",
    })

@login_required
def delete_report_view(request, row_id):
    current_user = get_current_user(request)
    report = get_object_or_404(ProcessReport, pk=row_id)

    if report.nguoi_nhap_id != current_user.id and current_user.role != "PREMIUM":
        raise PermissionDenied("Bạn không có quyền xoá dữ liệu này.")

    if request.method == "POST":
        report.delete()
        
    return redirect("list")

def get_tracking_data():
    """Hàm phụ trợ để lấy và tính toán dữ liệu tracking."""
    products = Product.objects.prefetch_related('colors').all()
    
    # Tính tổng tất cả các công đoạn cho từng (Mã hàng, Màu)
    report_sums = ProcessReport.objects.values('ma_hang', 'mau').annotate(
        t_nhan_btp=Sum('nhan_btp'),
        t_vao_chuyen=Sum('vao_chuyen'),
        t_giua_chuyen=Sum('giua_chuyen'),
        t_ra_chuyen=Sum('ra_chuyen'),
        t_thu_hoa=Sum('thu_hoa'),
        t_la_thanh_pham=Sum('la_thanh_pham'),
        t_kcs=Sum('kcs'),
        t_nhap_hoan_thien=Sum('nhap_hoan_thien')
    )
    
    sum_map = {(r['ma_hang'], r['mau']): r for r in report_sums}
    tracking_data = []
    
    for product in products:
        for color in product.colors.all():
            key = (product.name, color.name)
            stats = sum_map.get(key, {})
            qty = color.quantity
            
            def get_val(field_name):
                return stats.get(field_name) or 0
                
            tracking_data.append({
                'ma_hang': product.name,
                'mau': color.name,
                'so_luong': qty,
                'nhan_btp_nhap': get_val('t_nhan_btp'),
                'nhan_btp_con': qty - get_val('t_nhan_btp'),
                'vao_chuyen_vao': get_val('t_vao_chuyen'),
                'vao_chuyen_con': qty - get_val('t_vao_chuyen'),
                'giua_chuyen_ra': get_val('t_giua_chuyen'),
                'giua_chuyen_con': qty - get_val('t_giua_chuyen'),
                'ra_chuyen_ra': get_val('t_ra_chuyen'),
                'ra_chuyen_con': qty - get_val('t_ra_chuyen'),
                'thu_hoa_thu': get_val('t_thu_hoa'),
                'thu_hoa_con': qty - get_val('t_thu_hoa'),
                'la_thanh_pham_lam': get_val('t_la_thanh_pham'),
                'la_thanh_pham_con': qty - get_val('t_la_thanh_pham'),
                'kcs_lam': get_val('t_kcs'),
                'kcs_con': qty - get_val('t_kcs'),
                'nhap_hoan_thien_nhap': get_val('t_nhap_hoan_thien'),
                'nhap_hoan_thien_con': qty - get_val('t_nhap_hoan_thien'),
            })
            
    return tracking_data

@login_required
def tracking_view(request):
    current_user = get_current_user(request)
    if current_user.role != "PREMIUM":
        raise PermissionDenied("Chỉ quản trị viên cấp cao mới có quyền truy cập trang này.")
        
    tracking_data = get_tracking_data()
    
    return render(request, "tracking.html", {
        "tracking_data": tracking_data,
        "display_name": current_user.name
    })

@login_required
def tracking_export_excel_view(request):
    current_user = get_current_user(request)
    if current_user.role != "PREMIUM":
        raise PermissionDenied("Chỉ quản trị viên cấp cao mới có quyền truy cập trang này.")
        
    tracking_data = get_tracking_data()
    
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Tracking"
    
    # Row 1: Headers (Merged cells logic applied implicitly by formatting or explicitly)
    ws.append([
        "Mã hàng", "Màu", "Số lượng", 
        "Nhận BTP", "", 
        "Vào Chuyền", "", 
        "Giữa chuyền", "", 
        "Ra Chuyền", "", 
        "Thu Hoá", "", 
        "Là thành phẩm", "",
        "KCS", "",
        "Nhập Hoàn Thiện", ""
    ])
    
    # Row 2: Sub-headers
    ws.append([
        "", "", "", 
        "Đã Nhập", "Còn lại", 
        "Đã Vào", "Còn lại", 
        "Đã Ra", "Còn Lại", 
        "Đã Ra", "Còn Lại", 
        "Đã Thu", "Còn lại", 
        "Đã Làm", "Còn lại",
        "Đã Làm", "Còn lại",
        "Đã Nhập", "Còn lại"
    ])
    
    # Merge cells for Row 1
    ws.merge_cells("A1:A2")
    ws.merge_cells("B1:B2")
    ws.merge_cells("C1:C2")
    
    for col_start in range(4, 19, 2):
        ws.merge_cells(start_row=1, start_column=col_start, end_row=1, end_column=col_start+1)
        
    # Styling
    from openpyxl.styles import Alignment, Font
    for row in ws.iter_rows(min_row=1, max_row=2):
        for cell in row:
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.font = Font(bold=True)
            
    # Data rows
    for row in tracking_data:
        ws.append([
            row['ma_hang'],
            row['mau'],
            row['so_luong'],
            row['nhan_btp_nhap'], row['nhan_btp_con'],
            row['vao_chuyen_vao'], row['vao_chuyen_con'],
            row['giua_chuyen_ra'], row['giua_chuyen_con'],
            row['ra_chuyen_ra'], row['ra_chuyen_con'],
            row['thu_hoa_thu'], row['thu_hoa_con'],
            row['la_thanh_pham_lam'], row['la_thanh_pham_con'],
            row['kcs_lam'], row['kcs_con'],
            row['nhap_hoan_thien_nhap'], row['nhap_hoan_thien_con']
        ])
        
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = 'attachment; filename="tracking_data.xlsx"'
    wb.save(response)
    return response