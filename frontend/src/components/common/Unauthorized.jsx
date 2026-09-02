import React from 'react';
import { Link } from 'react-router-dom';

export function Unauthorized() {
  return (
    <div className="card" style={{ maxWidth: '500px', margin: '40px auto', textAlign: 'center' }}>
      <div style={{ fontSize: '3rem', marginBottom: '12px' }}>🔒</div>
      <h2 style={{ marginBottom: '8px' }}>Không Có Quyền Truy Cập</h2>
      <p style={{ color: 'var(--text-muted)', marginBottom: '20px' }}>
        Tài khoản của bạn không được phân quyền để truy cập khu vực này.
      </p>
      <Link to="/" className="btn btn-primary">
        Về Trang Chủ
      </Link>
    </div>
  );
}

export default Unauthorized;
