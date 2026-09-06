from collections import defaultdict
from django.db.models import Sum
from Working.models import CutReport, ProcessReport, KcsReport, FinishingReport, Product, ProductColor

def get_cut_dashboard_data(start_date=None, end_date=None, nguoi_nhap_ids=None, ma_hangs=None, maus=None):
    qs = CutReport.objects.all()
    if start_date:
        qs = qs.filter(created_at__gte=start_date)
    if end_date:
        qs = qs.filter(created_at__lte=end_date)
    if nguoi_nhap_ids:
        qs = qs.filter(nguoi_nhap_id__in=nguoi_nhap_ids)
    if ma_hangs:
        qs = qs.filter(ma_hang__in=ma_hangs)
    if maus:
        qs = qs.filter(mau__in=maus)

    data = qs.values('ma_hang', 'mau').annotate(
        total_cat_chinh=Sum('cat_chinh'),
        total_cat_lot=Sum('cat_lot'),
        total_cat_mex=Sum('cat_mex'),
        total_cat_bong=Sum('cat_bong'),
    ).order_by('ma_hang', 'mau')

    # Join with ProductColor to get tong_don_hang (quantity)
    color_map = { (c.product.name, c.name): c.quantity for c in ProductColor.objects.select_related('product').all() }
    
    results = []
    for row in data:
        key = (row['ma_hang'], row['mau'])
        row['tong_don_hang'] = color_map.get(key, 0)
        results.append(row)
        
    return results

def get_process_dashboard_data(start_date=None, end_date=None, nguoi_nhap_ids=None, ma_hangs=None, maus=None):
    qs = ProcessReport.objects.all()
    if start_date:
        qs = qs.filter(created_at__gte=start_date)
    if end_date:
        qs = qs.filter(created_at__lte=end_date)
    if nguoi_nhap_ids:
        qs = qs.filter(nguoi_nhap_id__in=nguoi_nhap_ids)
    if ma_hangs:
        qs = qs.filter(ma_hang__in=ma_hangs)
    if maus:
        qs = qs.filter(mau__in=maus)

    data = qs.values('ma_hang', 'mau').annotate(
        total_nhan_btp=Sum('nhan_btp'),
        total_vao_chuyen=Sum('vao_chuyen'),
        total_giua_chuyen=Sum('giua_chuyen'),
        total_ra_chuyen=Sum('ra_chuyen'),
        total_thu_hoa=Sum('thu_hoa'),
        total_la_thanh_pham=Sum('la_thanh_pham'),
        total_nhap_hoan_thien=Sum('nhap_hoan_thien'),
    ).order_by('ma_hang', 'mau')
    
    color_map = { (c.product.name, c.name): c.quantity for c in ProductColor.objects.select_related('product').all() }
    
    results = []
    for row in data:
        key = (row['ma_hang'], row['mau'])
        row['tong_don_hang'] = color_map.get(key, 0)
        results.append(row)
        
    return results

def get_kcs_dashboard_data(start_date=None, end_date=None, nguoi_nhap_ids=None, ma_hangs=None, maus=None):
    qs = KcsReport.objects.all()
    if start_date:
        qs = qs.filter(created_at__gte=start_date)
    if end_date:
        qs = qs.filter(created_at__lte=end_date)
    if nguoi_nhap_ids:
        qs = qs.filter(nguoi_nhap_id__in=nguoi_nhap_ids)
    if ma_hangs:
        qs = qs.filter(ma_hang__in=ma_hangs)
    if maus:
        qs = qs.filter(mau__in=maus)

    data = qs.values('ma_hang', 'mau').annotate(
        total_qua_tay=Sum('qua_tay'),
        total_dat=Sum('dat'),
        total_loi=Sum('loi'),
        total_tong_dat=Sum('tong_dat'),
    ).order_by('ma_hang', 'mau')
    
    color_map = { (c.product.name, c.name): c.quantity for c in ProductColor.objects.select_related('product').all() }
    
    results = []
    for row in data:
        key = (row['ma_hang'], row['mau'])
        row['tong_don_hang'] = color_map.get(key, 0)
        results.append(row)
        
    return results

def get_finishing_dashboard_data(start_date=None, end_date=None, nguoi_nhap_ids=None, ma_hangs=None, maus=None):
    qs = FinishingReport.objects.all()
    if start_date:
        qs = qs.filter(created_at__gte=start_date)
    if end_date:
        qs = qs.filter(created_at__lte=end_date)
    if nguoi_nhap_ids:
        qs = qs.filter(nguoi_nhap_id__in=nguoi_nhap_ids)
    if ma_hangs:
        qs = qs.filter(ma_hang__in=ma_hangs)
    if maus:
        qs = qs.filter(mau__in=maus)

    data = qs.values('ma_hang', 'mau').annotate(
        total_the_bai=Sum('the_bai'),
        total_gap_hang=Sum('gap_hang'),
        total_treo_dong_thung=Sum('treo_dong_thung'),
    ).order_by('ma_hang', 'mau')
    
    color_map = { (c.product.name, c.name): c.quantity for c in ProductColor.objects.select_related('product').all() }
    
    results = []
    for row in data:
        key = (row['ma_hang'], row['mau'])
        row['tong_don_hang'] = color_map.get(key, 0)
        results.append(row)
        
    return results
        

def get_tracking_dashboard_data(filter_ma_hang=None, filter_mau=None):
    """
    Lấy và tính toán dữ liệu tiến độ đơn hàng (Order Tracking Matrix)
    so sánh số lượng đơn hàng (ProductColor.quantity) với 7 công đoạn sản xuất (ProcessReport).
    """
    products = Product.objects.prefetch_related('colors').all()
    if filter_ma_hang:
        if isinstance(filter_ma_hang, str):
            filter_ma_hang = [filter_ma_hang]
        products = products.filter(name__in=filter_ma_hang)

    if filter_mau and isinstance(filter_mau, str):
        filter_mau = [filter_mau]

    report_sums = ProcessReport.objects.values('ma_hang', 'mau').annotate(
        t_nhan_btp=Sum('nhan_btp'),
        t_vao_chuyen=Sum('vao_chuyen'),
        t_giua_chuyen=Sum('giua_chuyen'),
        t_ra_chuyen=Sum('ra_chuyen'),
        t_thu_hoa=Sum('thu_hoa'),
        t_la_thanh_pham=Sum('la_thanh_pham'),
        t_nhap_hoan_thien=Sum('nhap_hoan_thien')
    )

    sum_map = {(r['ma_hang'], r['mau']): r for r in report_sums}
    tracking_data = []

    for product in products:
        for color in product.colors.all():
            if filter_mau and color.name not in filter_mau:
                continue
            key = (product.name, color.name)
            stats = sum_map.get(key, {})
            qty = color.quantity or 0

            def get_val(field_name):
                return stats.get(field_name) or 0

            t_nhan_btp = get_val('t_nhan_btp')
            t_vao_chuyen = get_val('t_vao_chuyen')
            t_giua_chuyen = get_val('t_giua_chuyen')
            t_ra_chuyen = get_val('t_ra_chuyen')
            t_thu_hoa = get_val('t_thu_hoa')
            t_la_thanh_pham = get_val('t_la_thanh_pham')
            t_nhap_hoan_thien = get_val('t_nhap_hoan_thien')

            tracking_data.append({
                'ma_hang': product.name,
                'mau': color.name,
                'so_luong': qty,
                # Structured stages matching Phase 4C-3A Section 7
                'nhan_btp': {'lam': t_nhan_btp, 'con': qty - t_nhan_btp},
                'vao_chuyen': {'lam': t_vao_chuyen, 'con': qty - t_vao_chuyen},
                'giua_chuyen': {'lam': t_giua_chuyen, 'con': qty - t_giua_chuyen},
                'ra_chuyen': {'lam': t_ra_chuyen, 'con': qty - t_ra_chuyen},
                'thu_hoa': {'lam': t_thu_hoa, 'con': qty - t_thu_hoa},
                'la_thanh_pham': {'lam': t_la_thanh_pham, 'con': qty - t_la_thanh_pham},
                'nhap_hoan_thien': {'lam': t_nhap_hoan_thien, 'con': qty - t_nhap_hoan_thien},
                # Flat legacy fields for 100% backward compatibility with tracking_view / tracking.html
                'nhan_btp_nhap': t_nhan_btp,
                'nhan_btp_con': qty - t_nhan_btp,
                'vao_chuyen_vao': t_vao_chuyen,
                'vao_chuyen_con': qty - t_vao_chuyen,
                'giua_chuyen_ra': t_giua_chuyen,
                'giua_chuyen_con': qty - t_giua_chuyen,
                'ra_chuyen_ra': t_ra_chuyen,
                'ra_chuyen_con': qty - t_ra_chuyen,
                'thu_hoa_thu': t_thu_hoa,
                'thu_hoa_con': qty - t_thu_hoa,
                'la_thanh_pham_lam': t_la_thanh_pham,
                'la_thanh_pham_con': qty - t_la_thanh_pham,
                'nhap_hoan_thien_nhap': t_nhap_hoan_thien,
                'nhap_hoan_thien_con': qty - t_nhap_hoan_thien,
            })

    return tracking_data


def calculate_cumulative_totals_cut():
    """
    Tính tổng lũy kế cho từng báo cáo Cắt theo thứ tự thời gian nhập (created_at, id).
    Trả về dict: report.id -> {'total_cat_chinh': int, ..., 'cat_chinh': int, ...}
    """
    running = defaultdict(lambda: {'cat_chinh': 0, 'cat_lot': 0, 'cat_mex': 0, 'cat_bong': 0})
    cumulative_map = {}
    for r in CutReport.objects.select_related('nguoi_nhap').order_by('created_at', 'id'):
        key = (r.ma_hang, r.mau)
        running[key]['cat_chinh'] += (r.cat_chinh or 0)
        running[key]['cat_lot'] += (r.cat_lot or 0)
        running[key]['cat_mex'] += (r.cat_mex or 0)
        running[key]['cat_bong'] += (r.cat_bong or 0)
        cumulative_map[r.id] = {
            'total_cat_chinh': running[key]['cat_chinh'],
            'total_cat_lot': running[key]['cat_lot'],
            'total_cat_mex': running[key]['cat_mex'],
            'total_cat_bong': running[key]['cat_bong'],
            'cat_chinh': running[key]['cat_chinh'],
            'cat_lot': running[key]['cat_lot'],
            'cat_mex': running[key]['cat_mex'],
            'cat_bong': running[key]['cat_bong'],
        }
    return cumulative_map


def calculate_cumulative_totals_prod():
    """
    Tính tổng lũy kế cho từng báo cáo Sản xuất theo thứ tự thời gian nhập (created_at, id).
    Tổng lũy kế được gom nhóm theo (mã hàng, màu, xưởng, tổ).
    Trả về dict: report.id -> {'total_nhan_btp': int, ..., 'nhan_btp': int, ...}
    """
    running = defaultdict(lambda: {
        'nhan_btp': 0,
        'vao_chuyen': 0,
        'giua_chuyen': 0,
        'ra_chuyen': 0,
        'thu_hoa': 0,
        'la_thanh_pham': 0,
        'nhap_hoan_thien': 0,
    })
    cumulative_map = {}
    for r in ProcessReport.objects.select_related('nguoi_nhap').order_by('created_at', 'id'):
        key = (r.ma_hang, r.mau, r.xuong, r.to)
        running[key]['nhan_btp'] += (r.nhan_btp or 0)
        running[key]['vao_chuyen'] += (r.vao_chuyen or 0)
        running[key]['giua_chuyen'] += (r.giua_chuyen or 0)
        running[key]['ra_chuyen'] += (r.ra_chuyen or 0)
        running[key]['thu_hoa'] += (r.thu_hoa or 0)
        running[key]['la_thanh_pham'] += (r.la_thanh_pham or 0)
        running[key]['nhap_hoan_thien'] += (r.nhap_hoan_thien or 0)
        cumulative_map[r.id] = {
            'total_nhan_btp': running[key]['nhan_btp'],
            'total_vao_chuyen': running[key]['vao_chuyen'],
            'total_giua_chuyen': running[key]['giua_chuyen'],
            'total_ra_chuyen': running[key]['ra_chuyen'],
            'total_thu_hoa': running[key]['thu_hoa'],
            'total_la_thanh_pham': running[key]['la_thanh_pham'],
            'total_nhap_hoan_thien': running[key]['nhap_hoan_thien'],
            'nhan_btp': running[key]['nhan_btp'],
            'vao_chuyen': running[key]['vao_chuyen'],
            'giua_chuyen': running[key]['giua_chuyen'],
            'ra_chuyen': running[key]['ra_chuyen'],
            'thu_hoa': running[key]['thu_hoa'],
            'la_thanh_pham': running[key]['la_thanh_pham'],
            'nhap_hoan_thien': running[key]['nhap_hoan_thien'],
        }
    return cumulative_map


def calculate_cumulative_totals_kcs():
    """
    Tính tổng lũy kế cho từng báo cáo KCS theo thứ tự thời gian nhập (created_at, id).
    Trả về dict: report.id -> {'total_qua_tay': int, ..., 'qua_tay': int, ...}
    """
    running = defaultdict(lambda: {'qua_tay': 0, 'dat': 0, 'loi': 0, 'tong_dat': 0})
    cumulative_map = {}
    for r in KcsReport.objects.select_related('nguoi_nhap').order_by('created_at', 'id'):
        key = (r.ma_hang, r.mau)
        running[key]['qua_tay'] += (r.qua_tay or 0)
        running[key]['dat'] += (r.dat or 0)
        running[key]['loi'] += (r.loi or 0)
        running[key]['tong_dat'] += (r.tong_dat or 0)
        cumulative_map[r.id] = {
            'total_qua_tay': running[key]['qua_tay'],
            'total_dat': running[key]['dat'],
            'total_loi': running[key]['loi'],
            'total_tong_dat': running[key]['tong_dat'],
            'qua_tay': running[key]['qua_tay'],
            'dat': running[key]['dat'],
            'loi': running[key]['loi'],
            'tong_dat': running[key]['tong_dat'],
        }
    return cumulative_map


def calculate_cumulative_totals_finishing():
    """
    Tính tổng lũy kế cho từng báo cáo Hoàn thiện theo thứ tự thời gian nhập (created_at, id).
    Trả về dict: report.id -> {'total_the_bai': int, ..., 'the_bai': int, ...}
    """
    running = defaultdict(lambda: {'the_bai': 0, 'gap_hang': 0, 'treo_dong_thung': 0})
    cumulative_map = {}
    for r in FinishingReport.objects.select_related('nguoi_nhap').order_by('created_at', 'id'):
        key = (r.ma_hang, r.mau)
        running[key]['the_bai'] += (r.the_bai or 0)
        running[key]['gap_hang'] += (r.gap_hang or 0)
        running[key]['treo_dong_thung'] += (r.treo_dong_thung or 0)
        cumulative_map[r.id] = {
            'total_the_bai': running[key]['the_bai'],
            'total_gap_hang': running[key]['gap_hang'],
            'total_treo_dong_thung': running[key]['treo_dong_thung'],
            'the_bai': running[key]['the_bai'],
            'gap_hang': running[key]['gap_hang'],
            'treo_dong_thung': running[key]['treo_dong_thung'],
        }
    return cumulative_map
