import React from 'react';

function formatNumber(num) {
  if (num === null || num === undefined || isNaN(num)) return '0';
  return Number(num).toLocaleString('en-US');
}

export function AccountingSummaryTable({ rows = [], onOpenPayment }) {
  return (
    <div className="dashboard-table-card">
      <div className="table-card-header">
        <h2 className="table-card-title">Chi Tiết Tiến Độ Xuất Hàng & Tồn Đọng</h2>
        <span className="table-card-count">
          Tổng cộng: <b>{rows.length}</b> mặt hàng (Đơn vị tiền: VNĐ)
        </span>
      </div>

      {/* DESKTOP TABLE VIEW */}
      <div className="desktop-table-container">
        <div className="table-dash-wrap">
          <table className="accounting-table">
            <thead>
              <tr>
                <th rowSpan="2" className="th-main th-col-ma-hang">Mã hàng</th>
                <th rowSpan="2" className="th-main th-col-mau">Màu</th>
                <th colSpan="3" className="th-group-dh">THÔNG TIN ĐƠN HÀNG</th>
                <th colSpan="2" className="th-group-xuat">ĐÃ XUẤT HÀNG</th>
                <th colSpan="2" className="th-group-ton">CÒN LẠI</th>
                <th colSpan="2" className="th-group-pay">THANH TOÁN TIỀN HÀNG ĐÃ XUẤT</th>
                <th rowSpan="2" className="th-main th-col-pct">Tiến độ</th>
                <th rowSpan="2" className="th-main th-col-act">Thao tác</th>
              </tr>
              <tr>
                <th className="th-group-dh number-col">Số lượng</th>
                <th className="th-group-dh number-col">Đơn giá</th>
                <th className="th-group-dh number-col">Thành tiền</th>
                <th className="th-group-xuat number-col">SL xuất</th>
                <th className="th-group-xuat number-col">Tiền đã xuất</th>
                <th className="th-group-ton number-col">SL còn</th>
                <th className="th-group-ton number-col">Tiền còn lại</th>
                <th className="th-group-pay number-col">Tiền đã thanh toán</th>
                <th className="th-group-pay number-col">Tiền chưa thanh toán</th>
              </tr>
            </thead>
            <tbody>
              {rows.length > 0 ? (
                rows.map((r, idx) => {
                  const key = r.product_color_id || `${r.ma_hang}-${r.mau}-${idx}`;
                  const conLaiColor = r.con_lai > 0 ? '#dc2626' : '#16a34a';
                  const chuaThanhToanColor = r.tien_chua_thanh_toan > 0 ? '#dc2626' : '#16a34a';

                  let badgeClass = 'red';
                  if (r.ty_le_xuat >= 100) {
                    badgeClass = 'green';
                  } else if (r.ty_le_xuat > 0) {
                    badgeClass = 'yellow';
                  }

                  return (
                    <tr key={key}>
                      <td className="col-ma-hang">
                        <strong style={{ color: '#0f172a', fontWeight: 700 }}>
                          {r.ma_hang}
                        </strong>
                      </td>
                      <td className="col-mau">
                        <span style={{ color: '#334155', fontWeight: 600 }}>
                          {r.mau}
                        </span>
                      </td>
                      <td className="number-col" style={{ fontWeight: 600, color: '#1e293b' }}>
                        {formatNumber(r.tong_so_luong)}
                      </td>
                      <td className="number-col" style={{ color: '#475569' }}>
                        {r.don_gia > 0 ? (
                          formatNumber(r.don_gia)
                        ) : (
                          <span style={{ color: '#ef4444', fontSize: '0.8rem', fontWeight: 600 }}>
                            Chưa giá
                          </span>
                        )}
                      </td>
                      <td className="number-col money-val">{formatNumber(r.tong_tien)}</td>
                      <td className="number-col" style={{ fontWeight: 700, color: '#16a34a' }}>
                        {formatNumber(r.da_xuat)}
                      </td>
                      <td className="number-col money-shipped">{formatNumber(r.tien_da_xuat)}</td>
                      <td className="number-col" style={{ fontWeight: 700, color: conLaiColor }}>
                        {formatNumber(r.con_lai)}
                      </td>
                      <td className="number-col money-pending">{formatNumber(r.tien_con_lai)}</td>
                      <td className="number-col money-paid">{formatNumber(r.tien_da_thanh_toan)}</td>
                      <td className="number-col" style={{ fontWeight: 800, color: chuaThanhToanColor }}>
                        {formatNumber(r.tien_chua_thanh_toan)}
                      </td>
                      <td style={{ textAlign: 'center' }}>
                        <span className={`badge-pct ${badgeClass}`}>
                          {r.ty_le_xuat}%
                        </span>
                      </td>
                      <td style={{ textAlign: 'center' }}>
                        <button
                          type="button"
                          className="btn-pay-action"
                          onClick={() => onOpenPayment(r)}
                          title="Ghi nhận hoặc xem thanh toán cho mã này"
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
                            <rect x="1" y="4" width="22" height="16" rx="2" ry="2" />
                            <line x1="1" y1="10" x2="23" y2="10" />
                          </svg>
                          Thanh toán
                        </button>
                      </td>
                    </tr>
                  );
                })
              ) : (
                <tr>
                  <td colSpan="13" className="table-empty-row">
                    Chưa có dữ liệu mã hàng.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* MOBILE CARDS VIEW */}
      <div className="mobile-cards-container">
        {rows.length > 0 ? (
          rows.map((r, idx) => {
            const key = r.product_color_id || `${r.ma_hang}-${r.mau}-${idx}`;
            let badgeClass = 'red';
            if (r.ty_le_xuat >= 100) {
              badgeClass = 'green';
            } else if (r.ty_le_xuat > 0) {
              badgeClass = 'yellow';
            }

            return (
              <div key={key} className="acc-card">
                <div className="acc-card-head">
                  <div>
                    <div style={{ fontSize: '1.05rem', fontWeight: 800, color: '#0f172a' }}>
                      {r.ma_hang} — {r.mau}
                    </div>
                    <div style={{ fontSize: '0.82rem', color: '#64748b', marginTop: '2px' }}>
                      Đơn giá:{' '}
                      <b style={{ color: '#2563eb' }}>
                        {r.don_gia > 0 ? `${formatNumber(r.don_gia)} VNĐ` : 'Chưa giá'}
                      </b>
                    </div>
                  </div>
                  <span className={`badge-pct ${badgeClass}`}>{r.ty_le_xuat}%</span>
                </div>

                <div className="acc-card-grid">
                  <div>
                    <div className="acc-card-lbl">Tổng ĐH</div>
                    <div className="acc-card-val">{formatNumber(r.tong_so_luong)} cái</div>
                  </div>
                  <div>
                    <div className="acc-card-lbl">Tổng Tiền ĐH</div>
                    <div className="acc-card-val" style={{ color: '#1e40af' }}>
                      {formatNumber(r.tong_tien)} đ
                    </div>
                  </div>
                  <div>
                    <div className="acc-card-lbl">Đã xuất</div>
                    <div className="acc-card-val" style={{ color: '#16a34a' }}>
                      {formatNumber(r.da_xuat)} cái
                    </div>
                  </div>
                  <div>
                    <div className="acc-card-lbl">Tiền đã xuất</div>
                    <div className="acc-card-val" style={{ color: '#16a34a' }}>
                      {formatNumber(r.tien_da_xuat)} đ
                    </div>
                  </div>
                  <div>
                    <div className="acc-card-lbl">Đã thanh toán</div>
                    <div className="acc-card-val" style={{ color: '#6d28d9' }}>
                      {formatNumber(r.tien_da_thanh_toan)} đ
                    </div>
                  </div>
                  <div>
                    <div className="acc-card-lbl">Chưa thanh toán</div>
                    <div
                      className="acc-card-val"
                      style={{ color: r.tien_chua_thanh_toan > 0 ? '#dc2626' : '#16a34a' }}
                    >
                      {formatNumber(r.tien_chua_thanh_toan)} đ
                    </div>
                  </div>
                </div>

                <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '6px' }}>
                  <button
                    type="button"
                    className="btn-pay-action"
                    style={{ padding: '6px 12px', fontSize: '0.85rem' }}
                    onClick={() => onOpenPayment(r)}
                  >
                    💳 Ghi nhận thanh toán
                  </button>
                </div>
              </div>
            );
          })
        ) : (
          <div className="mobile-empty-card">Chưa có dữ liệu mã hàng.</div>
        )}
      </div>
    </div>
  );
}

export default AccountingSummaryTable;
