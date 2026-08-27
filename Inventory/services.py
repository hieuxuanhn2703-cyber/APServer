from django.db.models import Sum
from .models import MaterialReceipt, MaterialIssue

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
