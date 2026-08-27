from django.db.models import Sum
from Working.models import CutReport, ProcessReport, KcsReport, FinishingReport, ProductColor

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
