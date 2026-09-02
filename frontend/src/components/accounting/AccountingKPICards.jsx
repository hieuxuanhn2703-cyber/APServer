import React from 'react';

/**
 * Format number with comma separators
 */
function formatNumber(num) {
  if (num === null || num === undefined || isNaN(num)) return '0';
  return Number(num).toLocaleString('en-US');
}

export function AccountingKPICards({ kpi = {} }) {
  const tongTienDh = kpi.kpi_tong_tien_dh || 0;
  const daXuatTien = kpi.kpi_tong_da_xuat_tien || 0;
  const daThanhToan = kpi.kpi_tong_da_thanh_toan || 0;
  const chuaThanhToan = kpi.kpi_tong_chua_thanh_toan || 0;

  const tongSlDh = kpi.kpi_tong_so_luong_dh || 0;
  const daXuatSl = kpi.kpi_tong_da_xuat_sl || 0;
  const tienDoTong = kpi.kpi_tien_do_tong || 0;

  // Recovery percentage calculation for display
  const tyLeThuHoi = daXuatTien > 0 ? ((daThanhToan / daXuatTien) * 100).toFixed(1) : '0.0';

  return (
    <div className="accounting-kpi-section">
      {/* 4 Main KPI Cards */}
      <div className="kpi-grid">
        {/* Card 1: Tổng Giá Trị Đơn Hàng */}
        <div className="kpi-card blue">
          <div className="kpi-title">Tổng Giá Trị Đơn Hàng</div>
          <div className="kpi-value">
            {formatNumber(tongTienDh)} <small style={{ fontSize: '0.85rem' }}>VNĐ</small>
          </div>
          <div className="kpi-sub">
            <span>Tổng số lượng:</span>
            <strong>{formatNumber(tongSlDh)} cái</strong>
          </div>
        </div>

        {/* Card 2: Tổng Tiền Đã Xuất */}
        <div className="kpi-card emerald">
          <div className="kpi-title">Tổng Tiền Đã Xuất</div>
          <div className="kpi-value">
            {formatNumber(daXuatTien)} <small style={{ fontSize: '0.85rem' }}>VNĐ</small>
          </div>
          <div className="kpi-sub">
            <span>Sản lượng đã xuất:</span>
            <strong>{formatNumber(daXuatSl)} cái</strong>
          </div>
        </div>

        {/* Card 3: Tiền Đã Thanh Toán */}
        <div className="kpi-card purple">
          <div className="kpi-title">Tiền Đã Thanh Toán</div>
          <div className="kpi-value">
            {formatNumber(daThanhToan)} <small style={{ fontSize: '0.85rem' }}>VNĐ</small>
          </div>
          <div className="kpi-sub">
            <span>Thu hồi tiền xuất:</span>
            <strong style={{ color: '#6d28d9' }}>{tyLeThuHoi}%</strong>
          </div>
        </div>

        {/* Card 4: Tiền Chưa Thanh Toán */}
        <div className="kpi-card amber">
          <div className="kpi-title">Tiền Chưa Thanh Toán</div>
          <div
            className="kpi-value"
            style={{ color: chuaThanhToan > 0 ? '#dc2626' : '#15803d' }}
          >
            {formatNumber(chuaThanhToan)} <small style={{ fontSize: '0.85rem' }}>VNĐ</small>
          </div>
          <div className="kpi-sub">
            <span>Công nợ hàng xuất:</span>
            <strong style={{ color: '#ea580c' }}>{formatNumber(chuaThanhToan)} đ</strong>
          </div>
        </div>
      </div>

      {/* Progress Bar Section */}
      <div className="progress-section-card">
        <div className="progress-header">
          <span className="progress-title">Tiến độ xuất hàng tổng thể:</span>
          <span className="progress-stats">
            Đã xuất <b>{formatNumber(daXuatSl)}</b> / {formatNumber(tongSlDh)} cái (
            <b>{tienDoTong}%</b>)
          </span>
        </div>
        <div className="progress-bar-wrap" role="progressbar" aria-valuenow={tienDoTong} aria-valuemin="0" aria-valuemax="100">
          <div
            className="progress-bar-fill"
            style={{ width: `${Math.min(100, Math.max(0, tienDoTong))}%` }}
          />
        </div>
      </div>
    </div>
  );
}

export default AccountingKPICards;
