import React from 'react';
import { useAuth } from '../hooks/useAuth';

export function DashboardPlaceholder() {
  const { user } = useAuth();

  return (
    <div className="card" style={{ maxWidth: '900px', margin: '20px auto' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '16px' }}>
        <span style={{ fontSize: '2rem' }}>📊</span>
        <div>
          <h2 style={{ fontSize: '1.25rem', fontWeight: 700 }}>Báo Cáo Tổng Hợp Sản Xuất (Khung Nền Tảng)</h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
            Khu vực này đã được tích hợp kiến trúc định tuyến và xác thực JWT sẵn sàng cho việc di chuyển giao diện.
          </p>
        </div>
      </div>

      <div className="alert alert-info" style={{ marginTop: '16px' }}>
        <strong>Thông tin phiên làm việc:</strong>
        <ul style={{ marginTop: '8px', paddingLeft: '20px', lineHeight: '1.8' }}>
          <li>Người dùng: <strong>{user?.name}</strong> ({user?.account})</li>
          <li>Vai trò hệ thống: <strong>{user?.role}</strong></li>
          <li>Trạng thái phê duyệt: <strong>{user?.is_approved ? 'Đã duyệt' : 'Chưa duyệt'}</strong></li>
          <li>API Backend: <code>/api/v1/working/dashboards/</code> (Hoạt động tốt)</li>
        </ul>
      </div>

      <div style={{ marginTop: '20px', fontSize: '0.88rem', color: 'var(--text-muted)' }}>
        <em>Lưu ý: Theo đúng quy định Phase 4A, màn hình giao diện chi tiết sẽ được chuyển đổi theo từng phân hệ trong các phase tiếp theo.</em>
      </div>
    </div>
  );
}

export default DashboardPlaceholder;
