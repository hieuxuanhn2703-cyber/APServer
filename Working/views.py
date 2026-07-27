from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied

from .forms import ProcessForm, load_config
from .models import ProcessReport
from .auth_utils import verify_credentials, get_current_user, login_required, SESSION_KEY

HEADERS = [
    "Thời gian", "Mã hàng", "Màu", "Cỡ", "Nhận BTP", "Vào chuyền",
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
            request.session[SESSION_KEY] = user.id
            request.session["display_name"] = user.name
            return redirect("web")
        else:
            error = "Tài khoản hoặc mật khẩu không đúng."

    return render(request, "login.html", {"error": error})


def logout_view(request):
    request.session.flush()
    return redirect("login")


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
    })


# ---------- Danh sách dữ liệu (chỉ của người đang đăng nhập) ----------

@login_required
def list_view(request):
    current_user = get_current_user(request)

    reports = ProcessReport.objects.filter(nguoi_nhap=current_user)  # đã sắp xếp -created_at theo Meta.ordering
    table_rows = [_report_to_row(r) for r in reports]

    return render(request, "list.html", {
        "table_rows": table_rows,
        "headers": HEADERS,
        "display_name": current_user.name if current_user else "",
    })


# ---------- Sửa dữ liệu (chỉ dòng của chính người đăng nhập) ----------

@login_required
def edit_view(request, row_id):
    current_user = get_current_user(request)
    report = get_object_or_404(ProcessReport, pk=row_id)

    if report.nguoi_nhap_id != current_user.id:
        raise PermissionDenied("Bạn không có quyền sửa dữ liệu này.")

    if request.method == "POST":
        form = ProcessForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            report.ma_hang = data["ma_hang"]
            report.mau = data["mau"]
            report.size = data["co"]
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