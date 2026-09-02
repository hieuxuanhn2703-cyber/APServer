import React from 'react';
import { useAuth } from '../hooks/useAuth';

export function WorkingPlaceholder() {
  const { user } = useAuth();

  return (
    <div className="card" style={{ maxWidth: '900px', margin: '20px auto' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '16px' }}>
        <span style={{ fontSize: '2rem' }}>⚙️</span>
        <div>
          <h2 style={{ fontSize: '1.25rem', fontWeight: 700 }}>Quy Trình Sản Xuất & Chấm Công (Khung Nền Tảng)</h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
            Phân hệ theo dõi sản lượng Cắt, Sản Xuất (Chuyền may), KCS, và Hoàn Thiện.
          </p>
        </div>
      </div>

      <div className="alert alert-info" style={{ marginTop: '16px' }}>
        <strong>Phân Quyền Hiện Tại:</strong>
        <p style={{ marginTop: '4px' }}>
          Tài khoản: <strong>{user?.name}</strong> | Vai trò: <strong>{user?.role}</strong>
        </p>
        <p style={{ marginTop: '4px', fontSize: '0.85rem' }}>
          REST API đã sẵn sàng: <code>/api/v1/working/reports/</code>, <code>/api/v1/working/config/</code>
        </p>
      </div>
    </div>
  );
}

export default WorkingPlaceholder;
