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
from .models import ProductPrice, ExportReport, PaymentReport
from .forms import ExportReportForm, load_price_map
from .services import get_dashboard_data, get_team_revenue_data


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
    success_msg = None
    error_msg = None

    if request.method == "POST":
        action = request.POST.get("action", "").strip()
        if action == "create_payment":
            pc_id = request.POST.get("product_color_id")
            ngay_tt_str = request.POST.get("ngay_thanh_toan")
            so_tien_raw = request.POST.get("so_tien", "0")
            ghi_chu = request.POST.get("ghi_chu", "").strip()

            pc = ProductColor.objects.filter(id=pc_id).select_related("product").first()
            if not pc:
                error_msg = "Không tìm thấy mặt hàng để ghi nhận thanh toán."
            else:
                so_tien = _parse_currency(so_tien_raw)
                if so_tien <= 0:
                    error_msg = "Số tiền thanh toán phải lớn hơn 0 VNĐ."
                else:
                    try:
                        ngay_tt = datetime.date.fromisoformat(ngay_tt_str) if ngay_tt_str else datetime.date.today()
                    except (ValueError, TypeError):
                        ngay_tt = datetime.date.today()

                    PaymentReport.objects.create(
                        ngay_thanh_toan=ngay_tt,
                        product_color=pc,
                        so_tien=so_tien,
                        ghi_chu=ghi_chu,
                        nguoi_nhap=user,
                    )
                    success_msg = f"Đã ghi nhận thanh toán {so_tien:,.0f} VNĐ cho {pc.product.name} — {pc.name} thành công!"
        
        elif action == "delete_payment":
            pay_id = request.POST.get("payment_id")
            pay = PaymentReport.objects.filter(id=pay_id).select_related("product_color__product").first()
            if pay:
                pc_name = f"{pay.product_color.product.name} — {pay.product_color.name}"
                pay.delete()
                success_msg = f"Đã xóa phiếu thanh toán của {pc_name} thành công!"
            else:
                error_msg = "Không tìm thấy phiếu thanh toán cần xóa."

    # Get data from service
    data = get_dashboard_data(selected_ma_hang)
    rows = data["rows"]
    kpi_tong_tien_dh = data["kpi"]["kpi_tong_tien_dh"]
    kpi_tong_da_xuat_tien = data["kpi"]["kpi_tong_da_xuat_tien"]
    kpi_tong_con_lai_tien = data["kpi"]["kpi_tong_con_lai_tien"]
    kpi_tong_so_luong_dh = data["kpi"]["kpi_tong_so_luong_dh"]
    kpi_tong_da_xuat_sl = data["kpi"]["kpi_tong_da_xuat_sl"]
    kpi_tong_con_lai_sl = data["kpi"]["kpi_tong_con_lai_sl"]
    kpi_tong_da_thanh_toan = data["kpi"]["kpi_tong_da_thanh_toan"]
    kpi_tong_chua_thanh_toan = data["kpi"]["kpi_tong_chua_thanh_toan"]
    kpi_tien_do_tong = data["kpi"]["kpi_tien_do_tong"]
    payments_by_pc = data["payments_by_pc"]

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
        "kpi_tong_da_thanh_toan": kpi_tong_da_thanh_toan,
        "kpi_tong_chua_thanh_toan": kpi_tong_chua_thanh_toan,
        "kpi_tien_do_tong": kpi_tien_do_tong,
        "success_msg": success_msg,
        "error_msg": error_msg,
        "payments_by_pc": payments_by_pc,
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
            gia_cm = _parse_currency(request.POST.get("gia_cm"))
            if color_id:
                pc = get_object_or_404(ProductColor, id=color_id)
                price_obj, _ = ProductPrice.objects.get_or_create(product_color=pc)
                price_obj.don_gia = don_gia
                price_obj.gia_cm = gia_cm
                price_obj.updated_by = user
                price_obj.save()
                success_msg = f"Đã lưu bảng giá cho [{pc.product.name} - {pc.name}]: Đơn giá {don_gia:,} VNĐ | Giá CM {gia_cm:,} VNĐ"
        elif action == "update_bulk":
            updated_count = 0
            color_prices = {}
            color_cm_prices = {}
            for key, val in request.POST.items():
                if key.startswith("cm_price_") or key.startswith("m_cm_price_"):
                    try:
                        clean_key = key.replace("m_cm_price_", "").replace("cm_price_", "")
                        color_id = int(clean_key)
                        color_cm_prices[color_id] = _parse_currency(val)
                    except Exception:
                        pass
                elif key.startswith("price_") or key.startswith("m_price_"):
                    try:
                        clean_key = key.replace("m_price_", "").replace("price_", "")
                        color_id = int(clean_key)
                        color_prices[color_id] = _parse_currency(val)
                    except Exception:
                        pass

            all_ids = set(color_prices.keys()) | set(color_cm_prices.keys())
            for color_id in all_ids:
                try:
                    pc = ProductColor.objects.get(id=color_id)
                    price_obj, _ = ProductPrice.objects.get_or_create(product_color=pc)
                    new_don_gia = color_prices.get(color_id, price_obj.don_gia)
                    new_gia_cm = color_cm_prices.get(color_id, price_obj.gia_cm)

                    if price_obj.don_gia != new_don_gia or price_obj.gia_cm != new_gia_cm or not price_obj.id:
                        price_obj.don_gia = new_don_gia
                        price_obj.gia_cm = new_gia_cm
                        price_obj.updated_by = user
                        price_obj.save()
                        updated_count += 1
                except Exception:
                    pass

            if updated_count > 0:
                success_msg = f"Đã lưu thành công bảng giá cho {updated_count} mặt hàng."
            else:
                success_msg = "Dữ liệu bảng giá đã được cập nhật đồng bộ."

    # Lấy danh sách ProductColor kèm Product & ProductPrice
    colors = ProductColor.objects.select_related("product", "price").all().order_by("product__name", "name")
    
    price_items = []
    for pc in colors:
        don_gia = pc.price.don_gia if hasattr(pc, "price") else 0
        gia_cm = pc.price.gia_cm if hasattr(pc, "price") else 0
        tong_tien = pc.quantity * don_gia
        price_items.append({
            "id": pc.id,
            "ma_hang": pc.product.name,
            "mau": pc.name,
            "quantity": pc.quantity,
            "don_gia": don_gia,
            "gia_cm": gia_cm,
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
        "Còn lại (Cái)", "Tiền còn lại (VNĐ)",
        "Tiền đã thanh toán (VNĐ)", "Tiền chưa thanh toán (VNĐ)",
        "Tiến độ xuất (%)"
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

    # Lấy tổng tiền đã thanh toán nhóm theo product_color_id
    payment_agg = (
        PaymentReport.objects
        .values("product_color_id")
        .annotate(tong_da_thanh_toan=Sum("so_tien"))
    )
    payment_map = {item["product_color_id"]: (item["tong_da_thanh_toan"] or 0) for item in payment_agg}

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

        tien_da_thanh_toan = payment_map.get(pc.id, 0)
        tien_chua_thanh_toan = max(0, tien_da_xuat - tien_da_thanh_toan)

        ws1.append([
            idx, ma, mau, tong_sl, don_gia, tong_tien, da_xuat, tien_da_xuat, con_lai, tien_con_lai,
            tien_da_thanh_toan, tien_chua_thanh_toan, f"{ty_le}%"
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

    # Sheet 3: Danh Sách Các Đợt Thanh Toán Chi Tiết
    ws3 = wb.create_sheet(title="Lịch Sử Thanh Toán Chi Tiết")
    headers3 = [
        "STT", "Ngày thanh toán", "Mã hàng", "Màu sắc", "Số tiền thanh toán (VNĐ)",
        "Người ghi nhận", "Ghi chú / Chứng từ", "Thời gian ghi nhận"
    ]
    ws3.append(headers3)

    payments = PaymentReport.objects.select_related("product_color__product", "nguoi_nhap").all().order_by("-ngay_thanh_toan", "-created_at")
    for idx, p in enumerate(payments, 1):
        ws3.append([
            idx,
            p.ngay_thanh_toan.strftime("%d/%m/%Y"),
            p.product_color.product.name,
            p.product_color.name,
            p.so_tien,
            p.nguoi_nhap.name or p.nguoi_nhap.account if p.nguoi_nhap else "",
            p.ghi_chu,
            p.created_at.strftime("%d/%m/%Y %H:%M"),
        ])

    # Style cả 3 sheets
    header_fill = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
    header_font = Font(name="Arial", size=11, bold=True, color="FFFFFF")
    thin_border = Border(
        left=Side(style='thin', color='CBD5E1'),
        right=Side(style='thin', color='CBD5E1'),
        top=Side(style='thin', color='CBD5E1'),
        bottom=Side(style='thin', color='CBD5E1')
    )

    for ws in [ws1, ws2, ws3]:
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
    Sử dụng logic từ services.py để tính doanh thu tổ/xưởng.
    """
    data = get_team_revenue_data(request.GET)
    
    # 9. Phân trang cho Bảng Chi Tiết Theo Ngày & Tổ (5 hàng / trang)
    total_daily_groups_count = len(data["daily_team_groups"])
    paginator = Paginator(data["daily_team_groups"], 5)
    page_number = request.GET.get("page", 1)
    daily_page_obj = paginator.get_page(page_number)
    
    data["total_daily_groups_count"] = total_daily_groups_count
    data["daily_page_obj"] = daily_page_obj
    
    # Do _get_team_revenue_data expected all_products as objects not dict in views.py context
    data["all_products"] = Product.objects.all().order_by("name")

    return data





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
        "Số lượng ra chuyền (Cái)", "Giá CM (VNĐ)", "Thành tiền (VNĐ)", "Trạng thái giá CM"
    ]
    ws1.append(headers1)

    stt = 1
    for g in data["daily_team_groups"]:
        ngay_str = g["ngay_lam_viec"].strftime("%d/%m/%Y")
        xuong_label = f"Xưởng {g['xuong']}" if g['xuong'] else "Chưa phân xưởng"
        to_label = f"Tổ {g['to']}" if g['to'] else "Chưa phân tổ"

        for it in g["items"]:
            status_dg = "Đã có giá CM" if it["has_price"] else "CHƯA CÓ GIÁ CM"
            ws1.append([
                stt,
                ngay_str,
                xuong_label,
                to_label,
                it["ma_hang"],
                it["mau"],
                it["so_luong"],
                it["gia_cm"],
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

