import calendar
import datetime
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import PermissionDenied
from django.db.models import Sum
from django.core.paginator import Paginator
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

from Working.models import AppUser, Product, ProductColor, ProcessReport
from Working.auth_utils import get_current_user, login_required
from Working.forms import load_config
from .models import ProductPrice, ExportReport
from .forms import ExportReportForm, load_price_map


def _check_accounting_permission(request):
    user = get_current_user(request)
    if not user:
        return None, redirect("login")
    if user.role not in ["KE_TOAN", "PREMIUM"]:
        raise PermissionDenied("Chỉ tài khoản Kế toán và Quản trị viên mới có quyền truy cập.")
    return user, None


@login_required
def accounting_dashboard_view(request):
    user, redirect_resp = _check_accounting_permission(request)
    if redirect_resp:
        return redirect_resp

    selected_ma_hang = request.GET.get("ma_hang", "").strip()

    # Lấy toàn bộ ProductColor kèm Product và ProductPrice
    colors_qs = ProductColor.objects.select_related("product", "price").all()
    if selected_ma_hang:
        colors_qs = colors_qs.filter(product__name=selected_ma_hang)
    
    colors_qs = colors_qs.order_by("product__name", "name")

    # Lấy tổng số lượng và thành tiền đã xuất nhóm theo (ma_hang, mau)
    export_agg = (
        ExportReport.objects
        .values("ma_hang", "mau")
        .annotate(
            tong_da_xuat=Sum("so_luong_xuat"),
            tong_tien_xuat=Sum("thanh_tien")
        )
    )
    export_map = {
        (item["ma_hang"], item["mau"]): {
            "da_xuat": item["tong_da_xuat"] or 0,
            "tien_xuat": item["tong_tien_xuat"] or 0,
        }
        for item in export_agg
    }

    rows = []
    kpi_tong_tien_dh = 0
    kpi_tong_da_xuat_tien = 0
    kpi_tong_con_lai_tien = 0
    kpi_tong_so_luong_dh = 0
    kpi_tong_da_xuat_sl = 0
    kpi_tong_con_lai_sl = 0

    for pc in colors_qs:
        ma = pc.product.name
        mau = pc.name
        tong_sl = pc.quantity
        don_gia = pc.price.don_gia if hasattr(pc, "price") else 0
        tong_tien = tong_sl * don_gia

        exp_data = export_map.get((ma, mau), {"da_xuat": 0, "tien_xuat": 0})
        da_xuat = exp_data["da_xuat"]
        tien_da_xuat = exp_data["tien_xuat"]
        
        con_lai = max(0, tong_sl - da_xuat)
        tien_con_lai = con_lai * don_gia
        ty_le_xuat = round((da_xuat / tong_sl * 100), 1) if tong_sl > 0 else 0

        rows.append({
            "product_color_id": pc.id,
            "ma_hang": ma,
            "mau": mau,
            "tong_so_luong": tong_sl,
            "don_gia": don_gia,
            "tong_tien": tong_tien,
            "da_xuat": da_xuat,
            "tien_da_xuat": tien_da_xuat,
            "con_lai": con_lai,
            "tien_con_lai": tien_con_lai,
            "ty_le_xuat": ty_le_xuat,
        })

        kpi_tong_so_luong_dh += tong_sl
        kpi_tong_tien_dh += tong_tien
        kpi_tong_da_xuat_sl += da_xuat
        kpi_tong_da_xuat_tien += tien_da_xuat
        kpi_tong_con_lai_sl += con_lai
        kpi_tong_con_lai_tien += tien_con_lai

    kpi_tien_do_tong = round((kpi_tong_da_xuat_sl / kpi_tong_so_luong_dh * 100), 1) if kpi_tong_so_luong_dh > 0 else 0

    # Danh sách các mã hàng để làm bộ lọc
    all_products = Product.objects.all().order_by("name")

    context = {
        "user": user,
        "rows": rows,
        "all_products": all_products,
        "selected_ma_hang": selected_ma_hang,
        "kpi_tong_tien_dh": kpi_tong_tien_dh,
        "kpi_tong_da_xuat_tien": kpi_tong_da_xuat_tien,
        "kpi_tong_con_lai_tien": kpi_tong_con_lai_tien,
        "kpi_tong_so_luong_dh": kpi_tong_so_luong_dh,
        "kpi_tong_da_xuat_sl": kpi_tong_da_xuat_sl,
        "kpi_tong_con_lai_sl": kpi_tong_con_lai_sl,
        "kpi_tien_do_tong": kpi_tien_do_tong,
    }
    return render(request, "accounting/dashboard.html", context)


@login_required
def export_entry_view(request):
    user, redirect_resp = _check_accounting_permission(request)
    if redirect_resp:
        return redirect_resp

    success_msg = None
    last_created_report = None

    if request.method == "POST":
        form = ExportReportForm(request.POST)
        if form.is_valid():
            ma_hang = form.cleaned_data["ma_hang"]
            mau = form.cleaned_data["mau"]
            so_luong_xuat = form.cleaned_data["so_luong_xuat"]
            ngay_xuat = form.cleaned_data["ngay_xuat"]
            ghi_chu = form.cleaned_data["ghi_chu"]

            # Lấy đơn giá hiện hành của mã hàng & màu này
            pc = ProductColor.objects.filter(product__name=ma_hang, name=mau).select_related("price").first()
            don_gia = pc.price.don_gia if (pc and hasattr(pc, "price")) else 0
            thanh_tien = so_luong_xuat * don_gia

            report = ExportReport.objects.create(
                ngay_xuat=ngay_xuat,
                ma_hang=ma_hang,
                mau=mau,
                so_luong_xuat=so_luong_xuat,
                don_gia=don_gia,
                thanh_tien=thanh_tien,
                ghi_chu=ghi_chu,
                nguoi_nhap=user
            )
            last_created_report = report
            success_msg = f"Đã lưu phiếu xuất thành công: {so_luong_xuat:,} cái [{ma_hang} - {mau}] | Đơn giá: {don_gia:,} đ | Tổng tiền: {thanh_tien:,} VNĐ"
            form = ExportReportForm()  # reset form
    else:
        form = ExportReportForm()

    # Danh sách xuất hàng gần đây (50 dòng)
    recent_exports = ExportReport.objects.select_related("nguoi_nhap").all().order_by("-created_at")[:50]

    context = {
        "user": user,
        "form": form,
        "recent_exports": recent_exports,
        "config": load_config(),
        "price_map": load_price_map(),
        "success_msg": success_msg,
        "last_created_report": last_created_report,
    }
    return render(request, "accounting/export_entry.html", context)


def _parse_currency(val):
    if not val:
        return 0
    clean = str(val).replace(".", "").replace(",", "").replace(" ", "").replace("đ", "").replace("VNĐ", "").replace("vnd", "").strip()
    try:
        return max(0, int(clean))
    except (ValueError, TypeError):
        return 0


@login_required
def price_management_view(request):
    user, redirect_resp = _check_accounting_permission(request)
    if redirect_resp:
        return redirect_resp

    success_msg = None

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "update_single":
            color_id = request.POST.get("product_color_id")
            don_gia = _parse_currency(request.POST.get("don_gia"))
            if color_id:
                pc = get_object_or_404(ProductColor, id=color_id)
                price_obj, _ = ProductPrice.objects.get_or_create(product_color=pc)
                price_obj.don_gia = don_gia
                price_obj.updated_by = user
                price_obj.save()
                success_msg = f"Đã lưu đơn giá cho [{pc.product.name} - {pc.name}]: {don_gia:,} VNĐ"
        elif action == "update_bulk":
            updated_count = 0
            # Collect unique color ids and values
            color_prices = {}
            for key, val in request.POST.items():
                if key.startswith("price_") or key.startswith("m_price_"):
                    try:
                        clean_key = key.replace("m_price_", "").replace("price_", "")
                        color_id = int(clean_key)
                        color_prices[color_id] = _parse_currency(val)
                    except Exception:
                        pass

            for color_id, don_gia in color_prices.items():
                try:
                    pc = ProductColor.objects.get(id=color_id)
                    price_obj, _ = ProductPrice.objects.get_or_create(product_color=pc)
                    if price_obj.don_gia != don_gia or not price_obj.id:
                        price_obj.don_gia = don_gia
                        price_obj.updated_by = user
                        price_obj.save()
                        updated_count += 1
                except Exception:
                    pass

            if updated_count > 0:
                success_msg = f"Đã lưu thành công đơn giá cho {updated_count} mặt hàng."
            else:
                success_msg = "Dữ liệu đơn giá đã được cập nhật đồng bộ."

    # Lấy danh sách ProductColor kèm Product & ProductPrice
    colors = ProductColor.objects.select_related("product", "price").all().order_by("product__name", "name")
    
    price_items = []
    for pc in colors:
        don_gia = pc.price.don_gia if hasattr(pc, "price") else 0
        tong_tien = pc.quantity * don_gia
        price_items.append({
            "id": pc.id,
            "ma_hang": pc.product.name,
            "mau": pc.name,
            "quantity": pc.quantity,
            "don_gia": don_gia,
            "tong_tien": tong_tien,
            "updated_at": pc.price.updated_at if hasattr(pc, "price") else None,
            "updated_by": pc.price.updated_by.name if (hasattr(pc, "price") and pc.price.updated_by) else "",
        })

    context = {
        "user": user,
        "price_items": price_items,
        "success_msg": success_msg,
    }
    return render(request, "accounting/price_management.html", context)


@login_required
def export_edit_view(request, row_id):
    user, redirect_resp = _check_accounting_permission(request)
    if redirect_resp:
        return redirect_resp

    report = get_object_or_404(ExportReport, id=row_id)

    if request.method == "POST":
        form = ExportReportForm(request.POST)
        if form.is_valid():
            report.ngay_xuat = form.cleaned_data["ngay_xuat"]
            report.ma_hang = form.cleaned_data["ma_hang"]
            report.mau = form.cleaned_data["mau"]
            report.so_luong_xuat = form.cleaned_data["so_luong_xuat"]
            report.ghi_chu = form.cleaned_data["ghi_chu"]
            
            # Lấy lại đơn giá theo mã và màu mới (nếu có thay đổi)
            pc = ProductColor.objects.filter(product__name=report.ma_hang, name=report.mau).select_related("price").first()
            if pc and hasattr(pc, "price") and pc.price.don_gia > 0:
                report.don_gia = pc.price.don_gia
            
            report.thanh_tien = report.so_luong_xuat * report.don_gia
            report.save()
            return redirect("accounting:export_entry")
    else:
        form = ExportReportForm(initial={
            "ngay_xuat": report.ngay_xuat,
            "ma_hang": report.ma_hang,
            "mau": report.mau,
            "so_luong_xuat": report.so_luong_xuat,
            "ghi_chu": report.ghi_chu,
        })

    context = {
        "user": user,
        "form": form,
        "report": report,
        "config": load_config(),
        "price_map": load_price_map(),
    }
    return render(request, "accounting/export_edit.html", context)


@login_required
def export_delete_view(request, row_id):
    user, redirect_resp = _check_accounting_permission(request)
    if redirect_resp:
        return redirect_resp

    report = get_object_or_404(ExportReport, id=row_id)
    if request.method == "POST":
        report.delete()
    return redirect("accounting:export_entry")


@login_required
def accounting_export_excel_view(request):
    user, redirect_resp = _check_accounting_permission(request)
    if redirect_resp:
        return redirect_resp

    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = 'attachment; filename="BaoCaoKeToan_XuatHang.xlsx"'

    wb = openpyxl.Workbook()
    
    # Sheet 1: Tổng hợp Theo Dõi Xuất Hàng & Doanh Thu
    ws1 = wb.active
    ws1.title = "Theo Dõi Doanh Thu & Xuất Hàng"
    
    headers1 = [
        "STT", "Mã hàng", "Màu sắc", "Tổng đơn hàng (Cái)",
        "Đơn giá (VNĐ)", "Tổng giá trị ĐH (VNĐ)",
        "Đã xuất (Cái)", "Tiền đã xuất (VNĐ)",
        "Còn lại (Cái)", "Tiền còn lại (VNĐ)", "Tiến độ xuất (%)"
    ]
    ws1.append(headers1)

    colors_qs = ProductColor.objects.select_related("product", "price").all().order_by("product__name", "name")
    export_agg = (
        ExportReport.objects
        .values("ma_hang", "mau")
        .annotate(
            tong_da_xuat=Sum("so_luong_xuat"),
            tong_tien_xuat=Sum("thanh_tien")
        )
    )
    export_map = {
        (item["ma_hang"], item["mau"]): {
            "da_xuat": item["tong_da_xuat"] or 0,
            "tien_xuat": item["tong_tien_xuat"] or 0,
        }
        for item in export_agg
    }

    for idx, pc in enumerate(colors_qs, 1):
        ma = pc.product.name
        mau = pc.name
        tong_sl = pc.quantity
        don_gia = pc.price.don_gia if hasattr(pc, "price") else 0
        tong_tien = tong_sl * don_gia

        exp_data = export_map.get((ma, mau), {"da_xuat": 0, "tien_xuat": 0})
        da_xuat = exp_data["da_xuat"]
        tien_da_xuat = exp_data["tien_xuat"]
        con_lai = max(0, tong_sl - da_xuat)
        tien_con_lai = con_lai * don_gia
        ty_le = round((da_xuat / tong_sl * 100), 1) if tong_sl > 0 else 0

        ws1.append([
            idx, ma, mau, tong_sl, don_gia, tong_tien, da_xuat, tien_da_xuat, con_lai, tien_con_lai, f"{ty_le}%"
        ])

    # Sheet 2: Danh Sách Các Đợt Xuất Hàng Chi Tiết
    ws2 = wb.create_sheet(title="Lịch Sử Xuất Hàng Chi Tiết")
    headers2 = [
        "STT", "Ngày xuất", "Mã hàng", "Màu sắc", "Số lượng xuất",
        "Đơn giá (VNĐ)", "Thành tiền (VNĐ)", "Người nhập", "Ghi chú", "Thời gian nhập"
    ]
    ws2.append(headers2)

    exports = ExportReport.objects.select_related("nguoi_nhap").all().order_by("-ngay_xuat", "-created_at")
    for idx, r in enumerate(exports, 1):
        ws2.append([
            idx,
            r.ngay_xuat.strftime("%d/%m/%Y"),
            r.ma_hang,
            r.mau,
            r.so_luong_xuat,
            r.don_gia,
            r.thanh_tien,
            r.nguoi_nhap.name if r.nguoi_nhap else "",
            r.ghi_chu,
            r.created_at.strftime("%d/%m/%Y %H:%M"),
        ])

    # Style cả 2 sheets
    header_fill = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
    header_font = Font(name="Arial", size=11, bold=True, color="FFFFFF")
    thin_border = Border(
        left=Side(style='thin', color='CBD5E1'),
        right=Side(style='thin', color='CBD5E1'),
        top=Side(style='thin', color='CBD5E1'),
        bottom=Side(style='thin', color='CBD5E1')
    )

    for ws in [ws1, ws2]:
        for cell in ws[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        ws.row_dimensions[1].height = 28

        for row in ws.iter_rows(min_row=2):
            for cell in row:
                cell.border = thin_border
                cell.font = Font(name="Arial", size=10)
                if isinstance(cell.value, (int, float)):
                    cell.number_format = '#,##0'

        for col in ws.columns:
            max_len = max(len(str(cell.value or '')) for cell in col)
            col_letter = openpyxl.utils.get_column_letter(col[0].column)
            ws.column_dimensions[col_letter].width = max(max_len + 4, 12)

    wb.save(response)
    return response


def _get_team_revenue_data(request):
    """
    Tính toán doanh thu làm được của từng tổ/xưởng theo ngày dựa trên:
    Doanh thu = Sản lượng ra chuyền * Đơn giá của từng mã hàng/màu sắc.
    Xử lý trường hợp 1 tổ có thể ra chuyền nhiều mã hàng khác nhau trong 1 ngày.
    """
    has_filter_params = any(k in request.GET for k in ["tu_ngay", "den_ngay", "xuong", "to", "ma_hang", "thang"])
    today = datetime.date.today()

    thang_param = request.GET.get("thang", "").strip()
    tu_ngay_str = request.GET.get("tu_ngay", "").strip()
    den_ngay_str = request.GET.get("den_ngay", "").strip()

    tu_ngay = None
    den_ngay = None

    if thang_param:
        try:
            parts = thang_param.split("-")
            y, m = int(parts[0]), int(parts[1])
            tu_ngay = datetime.date(y, m, 1)
            _, last_day = calendar.monthrange(y, m)
            den_ngay = datetime.date(y, m, last_day)
            tu_ngay_str = tu_ngay.strftime("%Y-%m-%d")
            den_ngay_str = den_ngay.strftime("%Y-%m-%d")
        except Exception:
            pass

    if not tu_ngay and not den_ngay:
        if not has_filter_params:
            # Mặc định theo tháng hiện tại: từ ngày 1 đầu tháng đến ngày hiện tại
            # Tự động reset lại từ 0 khi bước sang tháng mới
            tu_ngay = today.replace(day=1)
            den_ngay = today
            tu_ngay_str = tu_ngay.strftime("%Y-%m-%d")
            den_ngay_str = den_ngay.strftime("%Y-%m-%d")
        else:
            if tu_ngay_str:
                try:
                    tu_ngay = datetime.date.fromisoformat(tu_ngay_str)
                except (ValueError, TypeError):
                    pass
            if den_ngay_str:
                try:
                    den_ngay = datetime.date.fromisoformat(den_ngay_str)
                except (ValueError, TypeError):
                    pass

    selected_xuong = request.GET.get("xuong", "").strip()
    selected_to = request.GET.get("to", "").strip()
    selected_ma_hang = request.GET.get("ma_hang", "").strip()

    # 1. Bảng đơn giá từ ProductPrice
    price_map = {}
    product_price_fallback = {}
    for pc in ProductColor.objects.select_related("product", "price").all():
        p_val = pc.price.don_gia if hasattr(pc, "price") else 0
        price_map[(pc.product.name, pc.name)] = p_val
        if p_val > 0 and pc.product.name not in product_price_fallback:
            product_price_fallback[pc.product.name] = p_val

    # 2. Truy vấn ProcessReport có ra chuyền > 0
    qs = ProcessReport.objects.filter(ra_chuyen__gt=0)

    if tu_ngay:
        qs = qs.filter(ngay_lam_viec__gte=tu_ngay)
    if den_ngay:
        qs = qs.filter(ngay_lam_viec__lte=den_ngay)
    if selected_xuong:
        try:
            qs = qs.filter(xuong=int(selected_xuong))
        except (ValueError, TypeError):
            pass
    if selected_to:
        try:
            qs = qs.filter(to=int(selected_to))
        except (ValueError, TypeError):
            pass
    if selected_ma_hang:
        qs = qs.filter(ma_hang=selected_ma_hang)

    reports = qs.order_by("-ngay_lam_viec", "xuong", "to", "ma_hang", "mau", "size")

    # 3. Gom nhóm theo (ngay_lam_viec, xuong, to)
    daily_team_dict = {}

    for r in reports:
        dt_key = (r.ngay_lam_viec, r.xuong, r.to)
        if dt_key not in daily_team_dict:
            daily_team_dict[dt_key] = {
                "ngay_lam_viec": r.ngay_lam_viec,
                "xuong": r.xuong,
                "to": r.to,
                "so_luong_ld": r.so_luong_ld,
                "items_map": {},
                "tong_ra_chuyen": 0,
                "tong_tien": 0,
                "has_missing_price": False,
            }

        group = daily_team_dict[dt_key]
        if r.so_luong_ld and not group["so_luong_ld"]:
            group["so_luong_ld"] = r.so_luong_ld

        item_key = (r.ma_hang, r.mau)
        if item_key not in group["items_map"]:
            don_gia = price_map.get(item_key, product_price_fallback.get(r.ma_hang, 0))
            group["items_map"][item_key] = {
                "ma_hang": r.ma_hang,
                "mau": r.mau,
                "don_gia": don_gia,
                "so_luong": 0,
                "thanh_tien": 0,
                "has_price": (don_gia > 0),
            }

        item = group["items_map"][item_key]
        item["so_luong"] += r.ra_chuyen
        item["thanh_tien"] += r.ra_chuyen * item["don_gia"]

        group["tong_ra_chuyen"] += r.ra_chuyen
        group["tong_tien"] += r.ra_chuyen * item["don_gia"]
        if item["don_gia"] == 0:
            group["has_missing_price"] = True

    daily_team_groups = []
    kpi_tong_tien = 0
    kpi_tong_ra_chuyen = 0
    active_teams_set = set()
    active_dates_set = set()

    for dt_key, group in daily_team_dict.items():
        items_list = list(group["items_map"].values())
        items_list.sort(key=lambda x: (x["ma_hang"], x["mau"]))
        group["items"] = items_list
        group["item_count"] = len(items_list)

        daily_team_groups.append(group)
        kpi_tong_tien += group["tong_tien"]
        kpi_tong_ra_chuyen += group["tong_ra_chuyen"]
        active_teams_set.add((group["xuong"], group["to"]))
        active_dates_set.add(group["ngay_lam_viec"])

    # 4. Tổng hợp theo Xưởng & Tổ
    team_summary_dict = {}
    for g in daily_team_groups:
        team_key = (g["xuong"], g["to"])
        if team_key not in team_summary_dict:
            team_summary_dict[team_key] = {
                "xuong": g["xuong"],
                "to": g["to"],
                "so_ngay_sx": 0,
                "dates": set(),
                "tong_ra_chuyen": 0,
                "tong_tien": 0,
                "ma_hang_set": set(),
            }
        ts = team_summary_dict[team_key]
        ts["dates"].add(g["ngay_lam_viec"])
        ts["tong_ra_chuyen"] += g["tong_ra_chuyen"]
        ts["tong_tien"] += g["tong_tien"]
        for it in g["items"]:
            ts["ma_hang_set"].add(it["ma_hang"])

    team_summary_list = []
    for team_key, ts in team_summary_dict.items():
        so_ngay = len(ts["dates"])
        ts["so_ngay_sx"] = so_ngay
        ts["so_ma_hang"] = len(ts["ma_hang_set"])
        ts["tien_bq_ngay"] = round(ts["tong_tien"] / so_ngay) if so_ngay > 0 else 0
        team_summary_list.append(ts)
    team_summary_list.sort(key=lambda x: (x["xuong"], x["to"]))

    # 5. Tổng hợp theo Ngày
    date_summary_dict = {}
    for g in daily_team_groups:
        d = g["ngay_lam_viec"]
        if d not in date_summary_dict:
            date_summary_dict[d] = {
                "ngay_lam_viec": d,
                "teams_set": set(),
                "tong_ra_chuyen": 0,
                "tong_tien": 0,
            }
        ds = date_summary_dict[d]
        ds["teams_set"].add((g["xuong"], g["to"]))
        ds["tong_ra_chuyen"] += g["tong_ra_chuyen"]
        ds["tong_tien"] += g["tong_tien"]

    date_summary_list = []
    for d, ds in date_summary_dict.items():
        ds["so_to_hoat_dong"] = len(ds["teams_set"])
        date_summary_list.append(ds)
    date_summary_list.sort(key=lambda x: x["ngay_lam_viec"], reverse=True)

    # 6. KPI metrics
    so_ngay_sx = len(active_dates_set)
    kpi_tien_bq_ngay = round(kpi_tong_tien / so_ngay_sx) if so_ngay_sx > 0 else 0
    kpi_so_to = len(active_teams_set)

    # 7. Nhãn chu kỳ & Tháng
    if tu_ngay and den_ngay:
        if tu_ngay.year == den_ngay.year and tu_ngay.month == den_ngay.month:
            ky_thang_label = f"Tháng {tu_ngay.month:02d}/{tu_ngay.year}"
        else:
            ky_thang_label = f"{tu_ngay.strftime('%d/%m/%Y')} - {den_ngay.strftime('%d/%m/%Y')}"
    elif tu_ngay:
        ky_thang_label = f"Từ {tu_ngay.strftime('%d/%m/%Y')}"
    elif den_ngay:
        ky_thang_label = f"Đến {den_ngay.strftime('%d/%m/%Y')}"
    else:
        ky_thang_label = "Toàn bộ thời gian"

    thang_hien_tai_str = today.strftime("%Y-%m")
    thang_truoc_date = (today.replace(day=1) - datetime.timedelta(days=1))
    thang_truoc_str = thang_truoc_date.strftime("%Y-%m")

    # 8. Bộ lọc danh sách (Dùng set và order_by() để loại bỏ hoàn toàn các giá trị trùng lặp)
    all_xuong_raw = ProcessReport.objects.order_by().values_list("xuong", flat=True).distinct()
    all_xuong = sorted(list(set(int(x) for x in all_xuong_raw if x is not None and int(x) > 0)))

    all_to_raw = ProcessReport.objects.order_by().values_list("to", flat=True).distinct()
    all_to = sorted(list(set(int(t) for t in all_to_raw if t is not None and int(t) > 0)))

    all_products = Product.objects.all().order_by("name")

    # 9. Phân trang cho Bảng Chi Tiết Theo Ngày & Tổ (5 hàng / trang)
    total_daily_groups_count = len(daily_team_groups)
    paginator = Paginator(daily_team_groups, 5)
    page_number = request.GET.get("page", 1)
    daily_page_obj = paginator.get_page(page_number)

    return {
        "tu_ngay": tu_ngay_str,
        "den_ngay": den_ngay_str,
        "selected_xuong": selected_xuong,
        "selected_to": selected_to,
        "selected_ma_hang": selected_ma_hang,
        "daily_team_groups": daily_team_groups,
        "daily_page_obj": daily_page_obj,
        "total_daily_groups_count": total_daily_groups_count,
        "team_summary_list": team_summary_list,
        "date_summary_list": date_summary_list,
        "kpi_tong_tien": kpi_tong_tien,
        "kpi_tong_ra_chuyen": kpi_tong_ra_chuyen,
        "kpi_so_to": kpi_so_to,
        "kpi_so_ngay_sx": so_ngay_sx,
        "kpi_tien_bq_ngay": kpi_tien_bq_ngay,
        "all_xuong": all_xuong,
        "all_to": all_to,
        "all_products": all_products,
        "ky_thang_label": ky_thang_label,
        "thang_hien_tai_str": thang_hien_tai_str,
        "thang_truoc_str": thang_truoc_str,
        "thang_param": thang_param,
    }


@login_required
def team_revenue_report_view(request):
    user, redirect_resp = _check_accounting_permission(request)
    if redirect_resp:
        return redirect_resp

    data = _get_team_revenue_data(request)
    data["user"] = user
    return render(request, "accounting/team_revenue_report.html", data)


@login_required
def team_revenue_export_excel_view(request):
    user, redirect_resp = _check_accounting_permission(request)
    if redirect_resp:
        return redirect_resp

    data = _get_team_revenue_data(request)

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    filename = f"BaoCao_DoanhThu_ToXuong_{datetime.date.today().strftime('%Y%m%d')}.xlsx"
    response["Content-Disposition"] = f'attachment; filename="{filename}"'

    wb = openpyxl.Workbook()

    # Style definitions
    header_fill = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
    header_font = Font(name="Arial", size=11, bold=True, color="FFFFFF")
    group_fill = PatternFill(start_color="E0F2FE", end_color="E0F2FE", fill_type="solid")
    group_font = Font(name="Arial", size=10, bold=True, color="0369A1")
    total_fill = PatternFill(start_color="FEF08A", end_color="FEF08A", fill_type="solid")
    total_font = Font(name="Arial", size=11, bold=True, color="854D0E")
    thin_border = Border(
        left=Side(style='thin', color='CBD5E1'),
        right=Side(style='thin', color='CBD5E1'),
        top=Side(style='thin', color='CBD5E1'),
        bottom=Side(style='thin', color='CBD5E1')
    )

    # -------------------------------------------------------------
    # SHEET 1: Chi Tiết Theo Ngày & Tổ
    # -------------------------------------------------------------
    ws1 = wb.active
    ws1.title = "Chi Tiết Ngày & Tổ"

    headers1 = [
        "STT", "Ngày làm việc", "Xưởng", "Tổ", "Mã hàng", "Màu sắc",
        "Số lượng ra chuyền (Cái)", "Đơn giá (VNĐ)", "Thành tiền (VNĐ)", "Trạng thái đơn giá"
    ]
    ws1.append(headers1)

    stt = 1
    for g in data["daily_team_groups"]:
        ngay_str = g["ngay_lam_viec"].strftime("%d/%m/%Y")
        xuong_label = f"Xưởng {g['xuong']}" if g['xuong'] else "Chưa phân xưởng"
        to_label = f"Tổ {g['to']}" if g['to'] else "Chưa phân tổ"

        for it in g["items"]:
            status_dg = "Đã có giá" if it["has_price"] else "CHƯA CÓ ĐƠN GIÁ"
            ws1.append([
                stt,
                ngay_str,
                xuong_label,
                to_label,
                it["ma_hang"],
                it["mau"],
                it["so_luong"],
                it["don_gia"],
                it["thanh_tien"],
                status_dg
            ])
            stt += 1

    # Dòng tổng cộng Sheet 1
    total_row_idx_1 = ws1.max_row + 1
    ws1.append([
        "TỔNG CỘNG", "", "", "", "", "",
        data["kpi_tong_ra_chuyen"], "", data["kpi_tong_tien"], ""
    ])

    # -------------------------------------------------------------
    # SHEET 2: Tổng Hợp Theo Tổ & Xưởng
    # -------------------------------------------------------------
    ws2 = wb.create_sheet(title="Tổng Hợp Tổ Xưởng")
    headers2 = [
        "STT", "Xưởng", "Tổ", "Số ngày làm việc", "Số mã hàng đã làm",
        "Tổng SL ra chuyền (Cái)", "Tổng tiền làm được (VNĐ)", "Tiền bình quân / ngày (VNĐ)"
    ]
    ws2.append(headers2)

    for idx, ts in enumerate(data["team_summary_list"], 1):
        xuong_label = f"Xưởng {ts['xuong']}" if ts['xuong'] else "Chưa phân xưởng"
        to_label = f"Tổ {ts['to']}" if ts['to'] else "Chưa phân tổ"
        ws2.append([
            idx,
            xuong_label,
            to_label,
            ts["so_ngay_sx"],
            ts["so_ma_hang"],
            ts["tong_ra_chuyen"],
            ts["tong_tien"],
            ts["tien_bq_ngay"]
        ])

    # Dòng tổng cộng Sheet 2
    ws2.append([
        "TỔNG CỘNG", "", "", data["kpi_so_ngay_sx"], "",
        data["kpi_tong_ra_chuyen"], data["kpi_tong_tien"], data["kpi_tien_bq_ngay"]
    ])

    # -------------------------------------------------------------
    # SHEET 3: Tổng Hợp Theo Ngày
    # -------------------------------------------------------------
    ws3 = wb.create_sheet(title="Tổng Hợp Theo Ngày")
    headers3 = [
        "STT", "Ngày làm việc", "Số tổ hoạt động",
        "Tổng SL ra chuyền (Cái)", "Tổng tiền làm được (VNĐ)"
    ]
    ws3.append(headers3)

    for idx, ds in enumerate(data["date_summary_list"], 1):
        ws3.append([
            idx,
            ds["ngay_lam_viec"].strftime("%d/%m/%Y"),
            ds["so_to_hoat_dong"],
            ds["tong_ra_chuyen"],
            ds["tong_tien"]
        ])

    # Dòng tổng cộng Sheet 3
    ws3.append([
        "TỔNG CỘNG", "", data["kpi_so_to"],
        data["kpi_tong_ra_chuyen"], data["kpi_tong_tien"]
    ])

    # -------------------------------------------------------------
    # Formatting Style cho cả 3 Sheets
    # -------------------------------------------------------------
    for ws in [ws1, ws2, ws3]:
        # Header formatting
        for cell in ws[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        ws.row_dimensions[1].height = 28

        # Data row formatting
        last_row = ws.max_row
        for r_idx, row in enumerate(ws.iter_rows(min_row=2, max_row=last_row), start=2):
            is_total = (r_idx == last_row)
            ws.row_dimensions[r_idx].height = 22 if is_total else 20
            for cell in row:
                cell.border = thin_border
                if is_total:
                    cell.fill = total_fill
                    cell.font = total_font
                else:
                    cell.font = Font(name="Arial", size=10)

                # Format số tiền và số lượng
                if isinstance(cell.value, (int, float)):
                    cell.number_format = '#,##0'

        # Auto width
        for col in ws.columns:
            max_len = max(len(str(cell.value or '')) for cell in col)
            col_letter = openpyxl.utils.get_column_letter(col[0].column)
            ws.column_dimensions[col_letter].width = max(max_len + 4, 14)

    wb.save(response)
    return response

