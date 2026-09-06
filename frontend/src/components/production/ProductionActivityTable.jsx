import React from 'react';

function formatNumber(val) {
  if (val === null || val === undefined) return '-';
  const num = Number(val);
  if (isNaN(num)) return '-';
  return num.toLocaleString('vi-VN');
}

function formatDate(dateStr) {
  if (!dateStr) return '-';
  try {
    const d = new Date(dateStr);
    if (isNaN(d.getTime())) return dateStr;
    const day = String(d.getDate()).padStart(2, '0');
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const year = d.getFullYear();
    return `${day}/${month}/${year}`;
  } catch {
    return dateStr;
  }
}

function formatDateTime(dtStr) {
  if (!dtStr) return '-';
  try {
    const d = new Date(dtStr);
    if (isNaN(d.getTime())) return dtStr;
    const day = String(d.getDate()).padStart(2, '0');
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const year = d.getFullYear();
    const hours = String(d.getHours()).padStart(2, '0');
    const mins = String(d.getMinutes()).padStart(2, '0');
    return `${day}/${month}/${year} ${hours}:${mins}`;
  } catch {
    return dtStr;
  }
}

export function ProductionActivityTable({
  stage,
  reports = [],
  totalCount = 0,
  currentPage = 1,
  pageSize = 20,
  onPageChange,
  isLoading = false,
}) {
  if (isLoading) {
    return (
      <div className="prod-loading-state">
        <div className="prod-spinner"></div>
        <p>Đang tải nhật ký sản xuất...</p>
      </div>
    );
  }

  if (!reports || reports.length === 0) {
    return (
      <div className="prod-empty-state">
        <span className="prod-empty-icon">📝</span>
        <h4>Không có nhật ký sản xuất</h4>
        <p>Chưa có dữ liệu báo cáo nào cho giai đoạn và bộ lọc hiện tại.</p>
      </div>
    );
  }

  const totalPages = Math.max(1, Math.ceil(totalCount / pageSize));

  return (
    <div className="prod-activity-container">
      <div className="prod-activity-header">
        <h4 className="prod-activity-title">
          Nhật ký báo cáo chi tiết ({totalCount.toLocaleString('vi-VN')} bản ghi)
        </h4>
        <span className="prod-activity-badge">Đã gắn lũy kế tự động</span>
      </div>

      <div className="prod-table-wrapper">
        <table className="prod-table activity-table">
          <thead>
            {/* Cut Stage Headers */}
            {stage === 'cut' && (
              <>
                <tr>
                  <th rowSpan="2" className="col-freeze col-nguoi-nhap">Người nhập</th>
                  <th rowSpan="2">Ngày làm việc</th>
                  <th rowSpan="2">Ngày nhập</th>
                  <th rowSpan="2" className="col-ma-hang">Mã hàng</th>
                  <th rowSpan="2" className="col-mau">Màu</th>
                  <th rowSpan="2">Cỡ</th>
                  <th rowSpan="2" className="col-numeric">Tổng ĐH</th>
                  <th colSpan="2" className="stage-header">Cắt chính</th>
                  <th colSpan="2" className="stage-header">Cắt lót</th>
                  <th colSpan="2" className="stage-header">Cắt Mex</th>
                  <th colSpan="2" className="stage-header">Cắt bông</th>
                </tr>
                <tr>
                  <th className="th-sub-head">Ngày</th>
                  <th className="th-sub-head">Tổng</th>
                  <th className="th-sub-head">Ngày</th>
                  <th className="th-sub-head">Tổng</th>
                  <th className="th-sub-head">Ngày</th>
                  <th className="th-sub-head">Tổng</th>
                  <th className="th-sub-head">Ngày</th>
                  <th className="th-sub-head">Tổng</th>
                </tr>
              </>
            )}

            {/* Process Stage Headers */}
            {stage === 'process' && (
              <>
                <tr>
                  <th rowSpan="2" className="col-freeze col-nguoi-nhap">Người nhập</th>
                  <th rowSpan="2">Ngày làm việc</th>
                  <th rowSpan="2">Ngày nhập</th>
                  <th rowSpan="2" className="col-ma-hang">Mã hàng</th>
                  <th rowSpan="2" className="col-mau">Màu</th>
                  <th rowSpan="2">Cỡ</th>
                  <th rowSpan="2">Xưởng</th>
                  <th rowSpan="2">Tổ</th>
                  <th rowSpan="2" className="col-numeric">Số LĐ</th>
                  <th rowSpan="2" className="col-numeric">Tổng ĐH</th>
                  <th colSpan="2" className="stage-header">Nhận BTP</th>
                  <th colSpan="2" className="stage-header">Vào chuyền</th>
                  <th colSpan="2" className="stage-header">Giữa chuyền</th>
                  <th colSpan="2" className="stage-header">Ra chuyền</th>
                  <th colSpan="2" className="stage-header">Thu hóa</th>
                  <th colSpan="2" className="stage-header">Là TP</th>
                  <th colSpan="2" className="stage-header">Nhập HT</th>
                </tr>
                <tr>
                  <th className="th-sub-head">Ngày</th><th className="th-sub-head">Tổng</th>
                  <th className="th-sub-head">Ngày</th><th className="th-sub-head">Tổng</th>
                  <th className="th-sub-head">Ngày</th><th className="th-sub-head">Tổng</th>
                  <th className="th-sub-head">Ngày</th><th className="th-sub-head">Tổng</th>
                  <th className="th-sub-head">Ngày</th><th className="th-sub-head">Tổng</th>
                  <th className="th-sub-head">Ngày</th><th className="th-sub-head">Tổng</th>
                  <th className="th-sub-head">Ngày</th><th className="th-sub-head">Tổng</th>
                </tr>
              </>
            )}

            {/* KCS Stage Headers */}
            {stage === 'kcs' && (
              <>
                <tr>
                  <th rowSpan="2" className="col-freeze col-nguoi-nhap">Người nhập</th>
                  <th rowSpan="2">Ngày làm việc</th>
                  <th rowSpan="2">Ngày nhập</th>
                  <th rowSpan="2" className="col-ma-hang">Mã hàng</th>
                  <th rowSpan="2" className="col-mau">Màu</th>
                  <th rowSpan="2">Cỡ</th>
                  <th rowSpan="2" className="col-numeric">Tổng ĐH</th>
                  <th colSpan="2" className="stage-header">Qua tay</th>
                  <th colSpan="2" className="stage-header">Đạt</th>
                  <th colSpan="2" className="stage-header">Lỗi</th>
                  <th colSpan="2" className="stage-header">Tổng đạt</th>
                </tr>
                <tr>
                  <th className="th-sub-head">Ngày</th><th className="th-sub-head">Tổng</th>
                  <th className="th-sub-head">Ngày</th><th className="th-sub-head">Tổng</th>
                  <th className="th-sub-head">Ngày</th><th className="th-sub-head">Tổng</th>
                  <th className="th-sub-head">Ngày</th><th className="th-sub-head">Tổng</th>
                </tr>
              </>
            )}

            {/* Finishing Stage Headers */}
            {stage === 'finishing' && (
              <>
                <tr>
                  <th rowSpan="2" className="col-freeze col-nguoi-nhap">Người nhập</th>
                  <th rowSpan="2">Ngày làm việc</th>
                  <th rowSpan="2">Ngày nhập</th>
                  <th rowSpan="2" className="col-ma-hang">Mã hàng</th>
                  <th rowSpan="2" className="col-mau">Màu</th>
                  <th rowSpan="2">Cỡ</th>
                  <th rowSpan="2" className="col-numeric">Tổng ĐH</th>
                  <th rowSpan="2" className="col-numeric">Tổng nhập HT</th>
                  <th colSpan="2" className="stage-header">Thẻ bài</th>
                  <th colSpan="2" className="stage-header">Gấp hàng</th>
                  <th colSpan="2" className="stage-header">Treo / Đóng thùng</th>
                </tr>
                <tr>
                  <th className="th-sub-head">Ngày</th><th className="th-sub-head">Tổng</th>
                  <th className="th-sub-head">Ngày</th><th className="th-sub-head">Tổng</th>
                  <th className="th-sub-head">Ngày</th><th className="th-sub-head">Tổng</th>
                </tr>
              </>
            )}
          </thead>

          <tbody>
            {reports.map((r, idx) => {
              const cumul = r.cumulative || {};

              return (
                <tr key={r.id || idx}>
                  <td className="col-freeze col-nguoi-nhap font-medium">
                    {r.nguoi_nhap_name || r.nguoi_nhap || '-'}
                  </td>
                  <td>{formatDate(r.ngay_lam_viec)}</td>
                  <td>{formatDateTime(r.created_at)}</td>
                  <td className="col-ma-hang font-medium">{r.ma_hang}</td>
                  <td className="col-mau">{r.mau}</td>
                  <td>{r.size || '-'}</td>

                  {/* Cut Row */}
                  {stage === 'cut' && (
                    <>
                      <td className="col-numeric font-semibold">{formatNumber(r.tong_don_hang)}</td>
                      <td className="col-numeric">{formatNumber(r.cat_chinh)}</td>
                      <td className="col-numeric font-semibold">{formatNumber(cumul.cat_chinh)}</td>

                      <td className="col-numeric">{formatNumber(r.cat_lot)}</td>
                      <td className="col-numeric font-semibold">{formatNumber(cumul.cat_lot)}</td>

                      <td className="col-numeric">{formatNumber(r.cat_mex)}</td>
                      <td className="col-numeric font-semibold">{formatNumber(cumul.cat_mex)}</td>

                      <td className="col-numeric">{formatNumber(r.cat_bong)}</td>
                      <td className="col-numeric font-semibold">{formatNumber(cumul.cat_bong)}</td>
                    </>
                  )}

                  {/* Process Row */}
                  {stage === 'process' && (
                    <>
                      <td>{r.xuong ?? '-'}</td>
                      <td>{r.to ?? '-'}</td>
                      <td className="col-numeric">{formatNumber(r.so_luong_ld)}</td>
                      <td className="col-numeric font-semibold">{formatNumber(r.tong_don_hang)}</td>

                      <td className="col-numeric">{formatNumber(r.nhan_btp)}</td>
                      <td className="col-numeric font-semibold">{formatNumber(cumul.nhan_btp)}</td>

                      <td className="col-numeric">{formatNumber(r.vao_chuyen)}</td>
                      <td className="col-numeric font-semibold">{formatNumber(cumul.vao_chuyen)}</td>

                      <td className="col-numeric">{formatNumber(r.giua_chuyen)}</td>
                      <td className="col-numeric font-semibold">{formatNumber(cumul.giua_chuyen)}</td>

                      <td className="col-numeric">{formatNumber(r.ra_chuyen)}</td>
                      <td className="col-numeric font-semibold">{formatNumber(cumul.ra_chuyen)}</td>

                      <td className="col-numeric">{formatNumber(r.thu_hoa)}</td>
                      <td className="col-numeric font-semibold">{formatNumber(cumul.thu_hoa)}</td>

                      <td className="col-numeric">{formatNumber(r.la_thanh_pham)}</td>
                      <td className="col-numeric font-semibold">{formatNumber(cumul.la_thanh_pham)}</td>

                      <td className="col-numeric">{formatNumber(r.nhap_hoan_thien)}</td>
                      <td className="col-numeric font-semibold">{formatNumber(cumul.nhap_hoan_thien)}</td>
                    </>
                  )}

                  {/* KCS Row */}
                  {stage === 'kcs' && (
                    <>
                      <td className="col-numeric font-semibold">{formatNumber(r.tong_don_hang)}</td>

                      <td className="col-numeric">{formatNumber(r.qua_tay)}</td>
                      <td className="col-numeric font-semibold">{formatNumber(cumul.qua_tay)}</td>

                      <td className="col-numeric">{formatNumber(r.dat)}</td>
                      <td className="col-numeric font-semibold">{formatNumber(cumul.dat)}</td>

                      <td className="col-numeric text-danger">{formatNumber(r.loi)}</td>
                      <td className="col-numeric font-semibold text-danger">{formatNumber(cumul.loi)}</td>

                      <td className="col-numeric">{formatNumber(r.tong_dat)}</td>
                      <td className="col-numeric font-semibold">{formatNumber(cumul.tong_dat)}</td>
                    </>
                  )}

                  {/* Finishing Row */}
                  {stage === 'finishing' && (
                    <>
                      <td className="col-numeric font-semibold">{formatNumber(r.tong_don_hang)}</td>
                      <td className="col-numeric font-semibold">{formatNumber(r.tong_nhap_hoan_thien)}</td>

                      <td className="col-numeric">{formatNumber(r.the_bai)}</td>
                      <td className="col-numeric font-semibold">{formatNumber(cumul.the_bai)}</td>

                      <td className="col-numeric">{formatNumber(r.gap_hang)}</td>
                      <td className="col-numeric font-semibold">{formatNumber(cumul.gap_hang)}</td>

                      <td className="col-numeric">{formatNumber(r.treo_dong_thung)}</td>
                      <td className="col-numeric font-semibold">{formatNumber(cumul.treo_dong_thung)}</td>
                    </>
                  )}
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* Pagination Controls */}
      {totalPages > 1 && (
        <div className="prod-pagination">
          <div className="prod-pagination-info">
            Trang {currentPage} / {totalPages} (tổng {totalCount.toLocaleString('vi-VN')} bản ghi)
          </div>
          <div className="prod-pagination-buttons">
            <button
              type="button"
              className="prod-btn prod-btn-secondary btn-sm"
              onClick={() => onPageChange(currentPage - 1)}
              disabled={currentPage <= 1 || isLoading}
            >
              ← Trang trước
            </button>
            <span className="prod-page-current">{currentPage}</span>
            <button
              type="button"
              className="prod-btn prod-btn-secondary btn-sm"
              onClick={() => onPageChange(currentPage + 1)}
              disabled={currentPage >= totalPages || isLoading}
            >
              Trang sau →
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default ProductionActivityTable;
