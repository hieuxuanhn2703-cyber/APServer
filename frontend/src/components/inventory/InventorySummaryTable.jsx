import React from 'react';

function formatQty(val, donVi) {
  if (val === null || val === undefined) return '0';
  const num = parseFloat(val);
  if (isNaN(num)) return '0';
  if (donVi === 'chiếc') {
    return Math.round(num).toLocaleString('en-US');
  }
  return num.toLocaleString('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
}

export function InventorySummaryTable({
  rows = [],
  onOpenIssue,
}) {
  return (
    <div className="inventory-table-section">
      {/* Mobile scroll hint for medium/small screens */}
      <div className="mobile-scroll-hint">
        <svg
          width="16"
          height="16"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          aria-hidden="true"
        >
          <path d="M17 8l4 4m0 0l-4 4m4-4H3" />
        </svg>
        <span>Vuốt ngang bảng để xem đủ Thực nhận / Thực xuất / Còn lại và Xuất kho</span>
      </div>

      {/* Desktop & Tablet Table */}
      <div className="table-wrapper">
        <table className="inventory-summary-table" data-table-type="summary">
          <thead>
            <tr>
              <th rowSpan="2" className="th-base th-header-sticky-1">Mã hàng</th>
              <th rowSpan="2" className="th-base th-header-sticky-1">Màu</th>
              <th rowSpan="2" className="th-base th-header-sticky-1">Tên vật tư</th>
              <th rowSpan="2" className="th-base th-header-sticky-1">Đơn vị</th>
              <th colSpan="2" className="th-receive th-header-sticky-1">Thực nhận</th>
              <th colSpan="2" className="th-issue th-header-sticky-1">Thực xuất</th>
              <th colSpan="2" className="th-stock th-header-sticky-1">Còn lại</th>
              <th rowSpan="2" className="th-base th-header-sticky-1 th-action">Thao tác</th>
            </tr>
            <tr>
              <th className="th-receive-sub th-header-sticky-2">SL kiện/cây</th>
              <th className="th-receive-sub th-header-sticky-2">Số lượng</th>
              <th className="th-issue-sub th-header-sticky-2">SL kiện/cây</th>
              <th className="th-issue-sub th-header-sticky-2">Số lượng</th>
              <th className="th-stock-sub th-header-sticky-2">SL kiện/cây</th>
              <th className="th-stock-sub th-header-sticky-2">Số lượng</th>
            </tr>
          </thead>
          <tbody>
            {rows.length === 0 ? (
              <tr>
                <td colSpan="11" className="td-empty">
                  Chưa có dữ liệu kho. Vui lòng nhập nguyên liệu trước.
                </td>
              </tr>
            ) : (
              rows.map((row, idx) => {
                const isOutOfStock = !row.has_stock;
                const conLaiKien = row.con_lai_kien ?? 0;
                const conLaiSoLuong = row.con_lai_so_luong ?? 0;

                const rowKey = `${row.ma_hang}-${row.mau}-${row.ten_vat_tu}-${row.don_vi}-${idx}`;

                return (
                  <tr key={rowKey} className="inventory-row">
                    <td className="td-center font-bold">{row.ma_hang}</td>
                    <td className="td-center">{row.mau}</td>
                    <td className="td-center font-medium">{row.ten_vat_tu}</td>
                    <td className="td-center td-unit">{row.don_vi}</td>

                    {/* Thực nhận */}
                    <td className="td-center td-receive-bold">
                      {row.nhap_kien ?? 0}
                    </td>
                    <td className="td-center td-receive">
                      {formatQty(row.nhap_so_luong, row.don_vi)}
                    </td>

                    {/* Thực xuất */}
                    <td className="td-center td-issue-bold">
                      {row.xuat_kien ?? 0}
                    </td>
                    <td className="td-center td-issue">
                      {formatQty(row.xuat_so_luong, row.don_vi)}
                    </td>

                    {/* Còn lại */}
                    <td
                      className={`td-center font-bold ${
                        conLaiKien <= 0 ? 'text-danger' : 'text-success'
                      }`}
                    >
                      {conLaiKien}
                    </td>
                    <td
                      className={`td-center font-bold ${
                        conLaiSoLuong <= 0 ? 'text-danger' : 'text-success'
                      }`}
                    >
                      {formatQty(conLaiSoLuong, row.don_vi)}
                    </td>

                    {/* Thao tác */}
                    <td className="td-center">
                      {!isOutOfStock ? (
                        <button
                          type="button"
                          className="btn-trigger-quick-issue"
                          onClick={() => onOpenIssue(row)}
                          title={`Xuất ${row.ten_vat_tu} (${row.ma_hang} - ${row.mau})`}
                        >
                          <svg
                            width="13"
                            height="13"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth="2.5"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            aria-hidden="true"
                          >
                            <line x1="5" y1="12" x2="19" y2="12" />
                            <polyline points="12 5 19 12 12 19" />
                          </svg>
                          Xuất
                        </button>
                      ) : (
                        <span className="badge-out-of-stock">Hết hàng</span>
                      )}
                    </td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>

      {/* Mobile Card View (< 768px) */}
      <div className="card-list">
        {rows.length === 0 ? (
          <div className="card-empty">
            Chưa có dữ liệu kho. Vui lòng nhập nguyên liệu trước.
          </div>
        ) : (
          rows.map((row, idx) => {
            const isOutOfStock = !row.has_stock;
            const conLaiKien = row.con_lai_kien ?? 0;
            const conLaiSoLuong = row.con_lai_so_luong ?? 0;
            const cardKey = `card-${row.ma_hang}-${row.mau}-${row.ten_vat_tu}-${row.don_vi}-${idx}`;

            return (
              <div key={cardKey} className="data-card">
                <div className="card-top-header">
                  <div>
                    <div className="card-badges-wrap">
                      <span className="card-badge-code">{row.ma_hang}</span>
                      <span className="card-badge-color">{row.mau}</span>
                      <span className="card-badge-unit">{row.don_vi}</span>
                    </div>
                    <div className="card-material-name">{row.ten_vat_tu}</div>
                  </div>
                  <div>
                    {!isOutOfStock ? (
                      <button
                        type="button"
                        className="btn-trigger-quick-issue btn-mobile-issue"
                        onClick={() => onOpenIssue(row)}
                      >
                        <svg
                          width="14"
                          height="14"
                          viewBox="0 0 24 24"
                          fill="none"
                          stroke="currentColor"
                          strokeWidth="2.5"
                          aria-hidden="true"
                        >
                          <line x1="5" y1="12" x2="19" y2="12" />
                          <polyline points="12 5 19 12 12 19" />
                        </svg>
                        Xuất
                      </button>
                    ) : (
                      <span className="badge-out-of-stock">Hết hàng</span>
                    )}
                  </div>
                </div>

                <div className="card-metrics-grid">
                  {/* Thực nhận */}
                  <div className="metric-col metric-col-receive">
                    <div className="metric-label">Thực nhận</div>
                    <div className="metric-val-main">
                      {row.nhap_kien ?? 0}{' '}
                      <span className="metric-sub-unit">k</span>
                    </div>
                    <div className="metric-val-sub">
                      {formatQty(row.nhap_so_luong, row.don_vi)}{' '}
                      <span className="metric-sub-unit">{row.don_vi}</span>
                    </div>
                  </div>

                  {/* Thực xuất */}
                  <div className="metric-col metric-col-issue">
                    <div className="metric-label">Thực xuất</div>
                    <div className="metric-val-main">
                      {row.xuat_kien ?? 0}{' '}
                      <span className="metric-sub-unit">k</span>
                    </div>
                    <div className="metric-val-sub">
                      {formatQty(row.xuat_so_luong, row.don_vi)}{' '}
                      <span className="metric-sub-unit">{row.don_vi}</span>
                    </div>
                  </div>

                  {/* Còn lại */}
                  <div className="metric-col metric-col-stock">
                    <div
                      className={`metric-label ${
                        conLaiKien <= 0 ? 'text-danger' : 'text-success'
                      }`}
                    >
                      Còn lại
                    </div>
                    <div
                      className={`metric-val-main ${
                        conLaiKien <= 0 ? 'text-danger' : 'text-success'
                      }`}
                    >
                      {conLaiKien}{' '}
                      <span className="metric-sub-unit">k</span>
                    </div>
                    <div
                      className={`metric-val-sub ${
                        conLaiSoLuong <= 0 ? 'text-danger' : 'text-success'
                      }`}
                    >
                      {formatQty(conLaiSoLuong, row.don_vi)}{' '}
                      <span className="metric-sub-unit">{row.don_vi}</span>
                    </div>
                  </div>
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}

export default InventorySummaryTable;
