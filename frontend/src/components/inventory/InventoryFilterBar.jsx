import React from 'react';

export function InventoryFilterBar({
  options = { maHangList: [], mauList: [], tenVatTuList: [], donViList: [] },
  filters = { ma_hang: '', mau: '', ten_vat_tu: '', don_vi: '' },
  onFilterChange,
  onClearFilters,
  canCreateReceipt = true,
}) {
  const hasActiveFilter = Boolean(
    filters.ma_hang || filters.mau || filters.ten_vat_tu || filters.don_vi
  );

  return (
    <div className="inventory-filter-container">
      <div className="inventory-filter-grid">
        {/* Lọc Mã hàng */}
        <div className="inventory-filter-item">
          <label htmlFor="filter_ma_hang" className="inventory-filter-label">
            Mã hàng:
          </label>
          <select
            id="filter_ma_hang"
            className="inventory-filter-select"
            value={filters.ma_hang || ''}
            onChange={(e) => onFilterChange('ma_hang', e.target.value)}
          >
            <option value="">-- Tất cả mã hàng --</option>
            {options.maHangList.map((item) => (
              <option key={item} value={item}>
                {item}
              </option>
            ))}
          </select>
        </div>

        {/* Lọc Màu */}
        <div className="inventory-filter-item">
          <label htmlFor="filter_mau" className="inventory-filter-label">
            Màu:
          </label>
          <select
            id="filter_mau"
            className="inventory-filter-select"
            value={filters.mau || ''}
            onChange={(e) => onFilterChange('mau', e.target.value)}
          >
            <option value="">-- Tất cả màu --</option>
            {options.mauList.map((item) => (
              <option key={item} value={item}>
                {item}
              </option>
            ))}
          </select>
        </div>

        {/* Lọc Tên vật tư */}
        <div className="inventory-filter-item">
          <label htmlFor="filter_ten_vat_tu" className="inventory-filter-label">
            Tên vật tư:
          </label>
          <select
            id="filter_ten_vat_tu"
            className="inventory-filter-select"
            value={filters.ten_vat_tu || ''}
            onChange={(e) => onFilterChange('ten_vat_tu', e.target.value)}
          >
            <option value="">-- Tất cả vật tư --</option>
            {options.tenVatTuList.map((item) => (
              <option key={item} value={item}>
                {item}
              </option>
            ))}
          </select>
        </div>

        {/* Lọc Đơn vị */}
        <div className="inventory-filter-item">
          <label htmlFor="filter_don_vi" className="inventory-filter-label">
            Đơn vị:
          </label>
          <select
            id="filter_don_vi"
            className="inventory-filter-select"
            value={filters.don_vi || ''}
            onChange={(e) => onFilterChange('don_vi', e.target.value)}
          >
            <option value="">-- Tất cả đơn vị --</option>
            {options.donViList.map((item) => (
              <option key={item} value={item}>
                {item}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="inventory-actions-row">
        {/* Xóa lọc */}
        {hasActiveFilter && (
          <button
            type="button"
            className="btn-dash-clear"
            onClick={onClearFilters}
            title="Xóa toàn bộ các bộ lọc đang áp dụng"
          >
            <svg
              width="14"
              height="14"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2.5"
              strokeLinecap="round"
              strokeLinejoin="round"
              aria-hidden="true"
            >
              <line x1="18" y1="6" x2="6" y2="18" />
              <line x1="6" y1="6" x2="18" y2="18" />
            </svg>
            Xóa tất cả lọc
          </button>
        )}

        {/* Quick action links to legacy views */}
        <div className="inventory-legacy-links">
          {canCreateReceipt && (
            <a
              href="/kho/nhap/"
              className="btn-inv-link btn-inv-green"
              title="Mở biểu mẫu ghi nhận nhập kho"
            >
              <svg
                width="14"
                height="14"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2.5"
                strokeLinecap="round"
                strokeLinejoin="round"
                aria-hidden="true"
              >
                <line x1="12" y1="5" x2="12" y2="19" />
                <line x1="5" y1="12" x2="19" y2="12" />
              </svg>
              Ghi Nhận Nhập Kho
            </a>
          )}

          <a
            href="/kho/lich-su-nhap/"
            className="btn-inv-link btn-inv-emerald"
            title="Xem danh sách lịch sử các phiếu nhập kho"
          >
            <svg
              width="14"
              height="14"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              aria-hidden="true"
            >
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
              <polyline points="14 2 14 8 20 8" />
            </svg>
            Lịch Sử Nhập
          </a>

          <a
            href="/kho/lich-su-xuat/"
            className="btn-inv-link btn-inv-purple"
            title="Xem danh sách lịch sử các phiếu xuất kho"
          >
            <svg
              width="14"
              height="14"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              aria-hidden="true"
            >
              <circle cx="12" cy="12" r="10" />
              <polyline points="12 6 12 12 16 14" />
            </svg>
            Lịch Sử Xuất
          </a>
        </div>
      </div>
    </div>
  );
}

export default InventoryFilterBar;
