import React from 'react';

export function ProductionFilterBar({
  maHang,
  setMaHang,
  mau,
  setMau,
  startDate,
  setStartDate,
  endDate,
  setEndDate,
  productsList = [],
  showDateFilters = true,
  onResetFilters,
}) {
  // Cascading colors: if maHang selected, filter colors for that product
  const availableColors = React.useMemo(() => {
    if (!maHang) {
      const allColors = new Set();
      productsList.forEach((p) => {
        (p.colors || []).forEach((c) => {
          if (c.name) allColors.add(c.name);
        });
      });
      return Array.from(allColors).sort((a, b) => a.localeCompare(b, 'vi'));
    }
    const matched = productsList.find((p) => p.name === maHang);
    if (!matched) return [];
    return (matched.colors || [])
      .map((c) => c.name)
      .filter(Boolean)
      .sort((a, b) => a.localeCompare(b, 'vi'));
  }, [maHang, productsList]);

  const hasFilter = Boolean(maHang || mau || (showDateFilters && (startDate || endDate)));

  return (
    <div className="prod-filter-container">
      <div className={`prod-filter-grid ${showDateFilters ? 'grid-4' : 'grid-2'}`}>
        {/* Mã hàng */}
        <div className="prod-filter-item">
          <label htmlFor="filter-ma-hang" className="prod-filter-label">
            Mã hàng
          </label>
          <select
            id="filter-ma-hang"
            className="prod-filter-select"
            value={maHang}
            onChange={(e) => {
              setMaHang(e.target.value);
              // Reset color if current color is not in the new product's colors
              if (mau && e.target.value) {
                const p = productsList.find((item) => item.name === e.target.value);
                const colors = (p?.colors || []).map((c) => c.name);
                if (!colors.includes(mau)) {
                  setMau('');
                }
              }
            }}
          >
            <option value="">-- Tất cả Mã hàng --</option>
            {productsList.map((p) => (
              <option key={p.id || p.name} value={p.name}>
                {p.name}
              </option>
            ))}
          </select>
        </div>

        {/* Màu */}
        <div className="prod-filter-item">
          <label htmlFor="filter-mau" className="prod-filter-label">
            Màu sắc
          </label>
          <select
            id="filter-mau"
            className="prod-filter-select"
            value={mau}
            onChange={(e) => setMau(e.target.value)}
          >
            <option value="">-- Tất cả Màu --</option>
            {availableColors.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>
        </div>

        {/* Date filters for activity and stage tabs */}
        {showDateFilters && (
          <>
            <div className="prod-filter-item">
              <label htmlFor="filter-start-date" className="prod-filter-label">
                Từ ngày
              </label>
              <input
                type="date"
                id="filter-start-date"
                className="prod-filter-input"
                value={startDate || ''}
                onChange={(e) => setStartDate(e.target.value)}
              />
            </div>

            <div className="prod-filter-item">
              <label htmlFor="filter-end-date" className="prod-filter-label">
                Đến ngày
              </label>
              <input
                type="date"
                id="filter-end-date"
                className="prod-filter-input"
                value={endDate || ''}
                onChange={(e) => setEndDate(e.target.value)}
              />
            </div>
          </>
        )}
      </div>

      {hasFilter && (
        <div className="prod-filter-actions">
          <button
            type="button"
            className="prod-btn-clear"
            onClick={onResetFilters}
            title="Đặt lại toàn bộ bộ lọc"
          >
            <svg
              width="12"
              height="12"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
            <span>Xóa lọc</span>
          </button>
        </div>
      )}
    </div>
  );
}

export default ProductionFilterBar;
