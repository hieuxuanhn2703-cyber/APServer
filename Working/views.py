from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
import openpyxl
from django.core.exceptions import PermissionDenied

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
        report.size,
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
def pending_accounts_view(request):
    current_user = get_current_user(request)
    if current_user.role != "PREMIUM":
        raise PermissionDenied("Chỉ quản trị viên cấp cao mới có quyền truy cập trang này.")
        
    pending_users = AppUser.objects.filter(is_approved=False).order_by("-id")
    return render(request, "pending_accounts.html", {
        "pending_users": pending_users,
        "display_name": current_user.name
    })


@login_required
def approve_account_view(request, user_id):
    current_user = get_current_user(request)
    if current_user.role != "PREMIUM":
        raise PermissionDenied("Chỉ quản trị viên cấp cao mới có quyền duyệt tài khoản.")
        
    user_to_approve = get_object_or_404(AppUser, pk=user_id)
    user_to_approve.is_approved = True
    user_to_approve.save()
    
    return redirect("pending_accounts")


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
            product, _ = Product.objects.get_or_create(name=name)
            
            if colors:
                color_list = [c.strip() for c in colors.split(',') if c.strip()]
                for color_name in color_list:
                    color_obj, _ = ProductColor.objects.get_or_create(product=product, name=color_name)
                    for size_name in sizes:
                        ProductSize.objects.get_or_create(color=color_obj, name=size_name)
                        
        return redirect("config_list")
        
    return render(request, "config_add.html", {
        "type": "product",
        "default_sizes": ["XS", "S", "M", "L", "XL", "XXL", "XXXL"]
    })

@login_required
def config_add_color_view(request, product_id):
    current_user = get_current_user(request)
    if current_user.role != "PREMIUM":
        raise PermissionDenied("Chỉ quản trị viên cấp cao mới có quyền truy cập trang này.")
        
    product = get_object_or_404(Product, pk=product_id)
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        if name:
            ProductColor.objects.get_or_create(product=product, name=name)
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
                size=data["co"],
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
            report.size = data["co"]
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
            "co": report.size,
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