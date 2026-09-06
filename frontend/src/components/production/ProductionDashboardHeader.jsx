import React from 'react';

export function ProductionDashboardHeader({
  title = 'Báo Cáo Sản Xuất',
  subtitle = 'Tiến độ chi tiết từng công đoạn theo Mã hàng & Màu sắc',
  onRefresh,
  isLoading,
  exportUrl,
}) {
  return (
    <div className="prod-header">
      <div className="prod-header-left">
        <div className="prod-header-title-box">
          <span className="prod-header-icon" aria-hidden="true">
            📊
          </span>
          <div>
            <h1 className="prod-header-title">{title}</h1>
            <p className="prod-header-subtitle">{subtitle}</p>
          </div>
        </div>
      </div>

      <div className="prod-header-actions">
        {onRefresh && (
          <button
            type="button"
            className="prod-btn prod-btn-secondary"
            onClick={onRefresh}
            disabled={isLoading}
            title="Làm mới dữ liệu"
          >
            <span className={`prod-refresh-icon ${isLoading ? 'spinning' : ''}`}>🔄</span>
            <span>{isLoading ? 'Đang tải...' : 'Làm mới'}</span>
          </button>
        )}

        {exportUrl && (
          <a
            href={exportUrl}
            className="prod-btn prod-btn-primary prod-btn-export"
            target="_blank"
            rel="noopener noreferrer"
            title="Xuất báo cáo Excel"
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
            >
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
              <polyline points="7 10 12 15 17 10"></polyline>
              <line x1="12" y1="15" x2="12" y2="3"></line>
            </svg>
            <span>Xuất Excel</span>
          </a>
        )}
      </div>
    </div>
  );
}

export default ProductionDashboardHeader;
