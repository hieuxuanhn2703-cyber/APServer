import React from 'react';

export function AccountingProductFilter({
  products = [],
  selectedMaHang = '',
  onSelectMaHang,
}) {
  return (
    <div className="filter-bar">
      <div className="filter-group">
        <label htmlFor="id_ma_hang_filter" className="filter-label">
          Lọc Mã Hàng:
        </label>
        <select
          id="id_ma_hang_filter"
          className="select-filter"
          value={selectedMaHang}
          onChange={(e) => onSelectMaHang(e.target.value)}
        >
          <option value="">-- Tất cả mã hàng --</option>
          {products.map((p) => {
            const name = typeof p === 'string' ? p : p.name;
            const key = typeof p === 'object' && p.id ? p.id : name;
            return (
              <option key={key} value={name}>
                {name}
              </option>
            );
          })}
        </select>

        {selectedMaHang && (
          <button
            type="button"
            className="btn-act btn-act-gray"
            onClick={() => onSelectMaHang('')}
            title="Xóa bộ lọc mã hàng"
          >
            <svg
              width="15"
              height="15"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2.2"
              strokeLinecap="round"
              strokeLinejoin="round"
              aria-hidden="true"
            >
              <line x1="18" y1="6" x2="6" y2="18" />
              <line x1="6" y1="6" x2="18" y2="18" />
            </svg>
            Xóa lọc
          </button>
        )}
      </div>

      <div className="btn-action-group">
        {/* Legacy Django link to Team Revenue view */}
        <a
          href="/accounting/team-revenue/"
          className="btn-act btn-act-blue"
          title="Xem báo cáo doanh thu làm được của từng tổ/xưởng theo ngày"
        >
          <svg
            width="15"
            height="15"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            aria-hidden="true"
          >
            <line x1="18" y1="20" x2="18" y2="10" />
            <line x1="12" y1="20" x2="12" y2="4" />
            <line x1="6" y1="20" x2="6" y2="14" />
          </svg>
          Doanh Thu Tổ/Xưởng
        </a>

        {/* Legacy Django Excel Export view */}
        <a
          href="/accounting/export-excel/"
          className="btn-act btn-act-emerald"
          title="Tải bảng tính Excel tổng hợp doanh thu"
          download
        >
          <svg
            width="15"
            height="15"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            aria-hidden="true"
          >
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
            <polyline points="7 10 12 15 17 10" />
            <line x1="12" y1="15" x2="12" y2="3" />
          </svg>
          Xuất Excel
        </a>
      </div>
    </div>
  );
}

export default AccountingProductFilter;
