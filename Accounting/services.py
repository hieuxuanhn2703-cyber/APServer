import calendar
import datetime
from django.db.models import Sum
from Working.models import Product, ProductColor, ProcessReport
from Accounting.models import ExportReport, PaymentReport

def get_dashboard_data(selected_ma_hang=""):
    """
    Trích xuất logic tổng hợp dữ liệu cho Dashboard Kế toán.
    Trả về dictionary chứa list các rows và các KPIs.
    """
    colors_qs = ProductColor.objects.select_related("product", "price").all()
    if selected_ma_hang:
        colors_qs = colors_qs.filter(product__name=selected_ma_hang)
    
    colors_qs = colors_qs.order_by("product__name", "name")

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

    payment_agg = (
        PaymentReport.objects
        .values("product_color_id")
        .annotate(tong_da_thanh_toan=Sum("so_tien"))
    )
    payment_map = {item["product_color_id"]: (item["tong_da_thanh_toan"] or 0) for item in payment_agg}

    payments_by_pc = {}
    for pay in PaymentReport.objects.select_related("nguoi_nhap").order_by("-ngay_thanh_toan", "-created_at"):
        if pay.product_color_id not in payments_by_pc:
            payments_by_pc[pay.product_color_id] = []
        payments_by_pc[pay.product_color_id].append({
            "id": pay.id,
            "ngay_thanh_toan": pay.ngay_thanh_toan.strftime("%d/%m/%Y") if isinstance(pay.ngay_thanh_toan, datetime.date) else pay.ngay_thanh_toan,
            "so_tien": pay.so_tien,
            "ghi_chu": pay.ghi_chu,
            "nguoi_nhap": pay.nguoi_nhap.name or pay.nguoi_nhap.account if pay.nguoi_nhap else "",
            "created_at": pay.created_at.strftime("%d/%m/%Y %H:%M") if hasattr(pay.created_at, 'strftime') else str(pay.created_at),
            "nguoi_nhap_id": pay.nguoi_nhap_id
        })

    rows = []
    kpi_tong_tien_dh = 0
    kpi_tong_da_xuat_tien = 0
    kpi_tong_con_lai_tien = 0
    kpi_tong_so_luong_dh = 0
    kpi_tong_da_xuat_sl = 0
    kpi_tong_con_lai_sl = 0
    kpi_tong_da_thanh_toan = 0
    kpi_tong_chua_thanh_toan = 0

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

        tien_da_thanh_toan = payment_map.get(pc.id, 0)
        tien_chua_thanh_toan = max(0, tien_da_xuat - tien_da_thanh_toan)

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
            "tien_da_thanh_toan": tien_da_thanh_toan,
            "tien_chua_thanh_toan": tien_chua_thanh_toan,
            "payments_list": payments_by_pc.get(pc.id, []),
        })

        kpi_tong_so_luong_dh += tong_sl
        kpi_tong_tien_dh += tong_tien
        kpi_tong_da_xuat_sl += da_xuat
        kpi_tong_da_xuat_tien += tien_da_xuat
        kpi_tong_con_lai_sl += con_lai
        kpi_tong_con_lai_tien += tien_con_lai
        kpi_tong_da_thanh_toan += tien_da_thanh_toan
        kpi_tong_chua_thanh_toan += tien_chua_thanh_toan

    kpi_tien_do_tong = round((kpi_tong_da_xuat_sl / kpi_tong_so_luong_dh * 100), 1) if kpi_tong_so_luong_dh > 0 else 0

    return {
        "rows": rows,
        "kpi": {
            "kpi_tong_tien_dh": kpi_tong_tien_dh,
            "kpi_tong_da_xuat_tien": kpi_tong_da_xuat_tien,
            "kpi_tong_con_lai_tien": kpi_tong_con_lai_tien,
            "kpi_tong_so_luong_dh": kpi_tong_so_luong_dh,
            "kpi_tong_da_xuat_sl": kpi_tong_da_xuat_sl,
            "kpi_tong_con_lai_sl": kpi_tong_con_lai_sl,
            "kpi_tong_da_thanh_toan": kpi_tong_da_thanh_toan,
            "kpi_tong_chua_thanh_toan": kpi_tong_chua_thanh_toan,
            "kpi_tien_do_tong": kpi_tien_do_tong,
        },
        "payments_by_pc": payments_by_pc,
    }


def get_team_revenue_data(query_params):
    """
    Trích xuất logic từ Accounting/views.py _get_team_revenue_data.
    """
    has_filter_params = any(k in query_params for k in ["tu_ngay", "den_ngay", "xuong", "to", "ma_hang", "thang"])
    today = datetime.date.today()

    thang_param = query_params.get("thang", "").strip()
    tu_ngay_str = query_params.get("tu_ngay", "").strip()
    den_ngay_str = query_params.get("den_ngay", "").strip()

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

    selected_xuong = query_params.get("xuong", "").strip()
    selected_to = query_params.get("to", "").strip()
    selected_ma_hang = query_params.get("ma_hang", "").strip()

    cm_price_map = {}
    product_cm_price_fallback = {}
    for pc in ProductColor.objects.select_related("product", "price").all():
        p_val = pc.price.gia_cm if hasattr(pc, "price") else 0
        cm_price_map[(pc.product.name, pc.name)] = p_val
        if p_val > 0 and pc.product.name not in product_cm_price_fallback:
            product_cm_price_fallback[pc.product.name] = p_val

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
            gia_cm = cm_price_map.get(item_key, product_cm_price_fallback.get(r.ma_hang, 0))
            group["items_map"][item_key] = {
                "ma_hang": r.ma_hang,
                "mau": r.mau,
                "gia_cm": gia_cm,
                "don_gia": gia_cm,
                "so_luong": 0,
                "thanh_tien": 0,
                "has_price": (gia_cm > 0),
            }

        item = group["items_map"][item_key]
        item["so_luong"] += r.ra_chuyen
        item["thanh_tien"] += r.ra_chuyen * item["gia_cm"]

        group["tong_ra_chuyen"] += r.ra_chuyen
        group["tong_tien"] += r.ra_chuyen * item["gia_cm"]
        if item["gia_cm"] == 0:
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
        # Avoid serialization issue with dict keys if this hits DRF
        del group["items_map"]

        daily_team_groups.append(group)
        kpi_tong_tien += group["tong_tien"]
        kpi_tong_ra_chuyen += group["tong_ra_chuyen"]
        active_teams_set.add((group["xuong"], group["to"]))
        active_dates_set.add(group["ngay_lam_viec"])

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
        del ts["dates"]
        del ts["ma_hang_set"]
        team_summary_list.append(ts)
    team_summary_list.sort(key=lambda x: (x["xuong"], x["to"]))

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
        del ds["teams_set"]
        date_summary_list.append(ds)
    date_summary_list.sort(key=lambda x: x["ngay_lam_viec"], reverse=True)

    so_ngay_sx = len(active_dates_set)
    kpi_tien_bq_ngay = round(kpi_tong_tien / so_ngay_sx) if so_ngay_sx > 0 else 0
    kpi_so_to = len(active_teams_set)

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

    all_xuong_raw = ProcessReport.objects.order_by().values_list("xuong", flat=True).distinct()
    all_xuong = sorted(list(set(int(x) for x in all_xuong_raw if x is not None and int(x) > 0)))

    all_to_raw = ProcessReport.objects.order_by().values_list("to", flat=True).distinct()
    all_to = sorted(list(set(int(t) for t in all_to_raw if t is not None and int(t) > 0)))

    all_products = list(Product.objects.all().order_by("name").values("id", "name"))

    return {
        "tu_ngay": tu_ngay_str,
        "den_ngay": den_ngay_str,
        "selected_xuong": selected_xuong,
        "selected_to": selected_to,
        "selected_ma_hang": selected_ma_hang,
        "daily_team_groups": daily_team_groups,
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
