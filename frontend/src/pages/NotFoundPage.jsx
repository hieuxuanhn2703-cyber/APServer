import React from 'react';
import { Link } from 'react-router-dom';

export function NotFoundPage() {
  return (
    <div className="card" style={{ maxWidth: '500px', margin: '40px auto', textAlign: 'center' }}>
      <div style={{ fontSize: '3rem', marginBottom: '12px' }}>🔍</div>
      <h2 style={{ marginBottom: '8px' }}>404 - Không Tìm Thấy Trang</h2>
      <p style={{ color: 'var(--text-muted)', marginBottom: '20px' }}>
        Đường dẫn bạn yêu cầu không tồn tại hoặc đã được di chuyển.
      </p>
      <Link to="/" className="btn btn-primary">
        Về Trang Chủ
      </Link>
    </div>
  );
}

export default NotFoundPage;
