import React from 'react';

function formatNumber(val) {
  if (val === null || val === undefined) return '0';
  const num = Number(val);
  if (isNaN(num)) return '0';
  return num.toLocaleString('vi-VN');
}

export function StageSummaryCards({ stage, summaryData = [] }) {
  if (!summaryData || summaryData.length === 0) {
    return null;
  }

  // Derive metrics strictly from backend-provided summary totals
  const aggregated = summaryData.reduce((acc, row) => {
    Object.entries(row).forEach(([k, v]) => {
      if (typeof v === 'number' && k !== 'id') {
        acc[k] = (acc[k] || 0) + v;
      }
    });
    return acc;
  }, {});

  let cards = [];

  if (stage === 'cut') {
    cards = [
      { label: 'Tổng đơn hàng', value: aggregated.tong_don_hang || 0, icon: '📋', color: 'blue' },
      { label: 'Tổng Cắt chính', value: aggregated.total_cat_chinh || 0, icon: '✂️', color: 'indigo' },
      { label: 'Tổng Cắt lót', value: aggregated.total_cat_lot || 0, icon: '🧵', color: 'teal' },
      { label: 'Tổng Cắt Mex', value: aggregated.total_cat_mex || 0, icon: '📐', color: 'amber' },
      { label: 'Tổng Cắt bông', value: aggregated.total_cat_bong || 0, icon: '☁️', color: 'purple' },
    ];
  } else if (stage === 'process') {
    cards = [
      { label: 'Tổng đơn hàng', value: aggregated.tong_don_hang || 0, icon: '📋', color: 'blue' },
      { label: 'Nhận BTP', value: aggregated.total_nhan_btp || 0, icon: '📥', color: 'cyan' },
      { label: 'Vào chuyền', value: aggregated.total_vao_chuyen || 0, icon: '⚙️', color: 'indigo' },
      { label: 'Giữa chuyền', value: aggregated.total_giua_chuyen || 0, icon: '🔄', color: 'amber' },
      { label: 'Ra chuyền', value: aggregated.total_ra_chuyen || 0, icon: '📦', color: 'purple' },
      { label: 'Thu hóa', value: aggregated.total_thu_hoa || 0, icon: '🔍', color: 'orange' },
      { label: 'Là TP', value: aggregated.total_la_thanh_pham || 0, icon: '✨', color: 'emerald' },
      { label: 'Nhập HT', value: aggregated.total_nhap_hoan_thien || 0, icon: '🏷️', color: 'teal' },
    ];
  } else if (stage === 'kcs') {
    const loiRate = aggregated.total_qua_tay > 0
      ? ((aggregated.total_loi / aggregated.total_qua_tay) * 100).toFixed(1) + '%'
      : '0%';
    cards = [
      { label: 'Tổng đơn hàng', value: aggregated.tong_don_hang || 0, icon: '📋', color: 'blue' },
      { label: 'Tổng Qua tay', value: aggregated.total_qua_tay || 0, icon: '👀', color: 'indigo' },
      { label: 'Tổng Đạt', value: aggregated.total_dat || 0, icon: '✅', color: 'emerald' },
      { label: 'Tổng Lỗi', value: aggregated.total_loi || 0, icon: '⚠️', color: 'rose' },
      { label: 'Tỉ lệ Lỗi', valueText: loiRate, icon: '📊', color: 'amber' },
      { label: 'Tổng Đạt (chuẩn)', value: aggregated.total_tong_dat || 0, icon: '🏅', color: 'teal' },
    ];
  } else if (stage === 'finishing') {
    cards = [
      { label: 'Tổng đơn hàng', value: aggregated.tong_don_hang || 0, icon: '📋', color: 'blue' },
      { label: 'Tổng Thẻ bài', value: aggregated.total_the_bai || 0, icon: '🏷️', color: 'indigo' },
      { label: 'Tổng Gấp hàng', value: aggregated.total_gap_hang || 0, icon: '👔', color: 'teal' },
      { label: 'Treo / Đóng thùng', value: aggregated.total_treo_dong_thung || 0, icon: '📦', color: 'purple' },
    ];
  }

  if (cards.length === 0) return null;

  return (
    <div className="prod-summary-cards-grid">
      {cards.map((card, idx) => (
        <div key={idx} className={`prod-summary-card card-${card.color}`}>
          <div className="summary-card-icon">{card.icon}</div>
          <div className="summary-card-info">
            <span className="summary-card-label">{card.label}</span>
            <span className="summary-card-value">
              {card.valueText !== undefined ? card.valueText : formatNumber(card.value)}
            </span>
          </div>
        </div>
      ))}
    </div>
  );
}

export default StageSummaryCards;
