import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

export function LoginPage() {
  const [account, setAccount] = useState('');
  const [password, setPassword] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [formError, setFormError] = useState('');

  const { login, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  // Redirect if already authenticated
  const from = location.state?.from?.pathname || '/';

  React.useEffect(() => {
    if (isAuthenticated) {
      navigate(from, { replace: true });
    }
  }, [isAuthenticated, navigate, from]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setFormError('');

    if (!account.trim()) {
      setFormError('Vui lòng nhập tên tài khoản.');
      return;
    }

    if (!password) {
      setFormError('Vui lòng nhập mật khẩu.');
      return;
    }

    setIsSubmitting(true);
    try {
      await login(account.trim(), password);
      navigate(from, { replace: true });
    } catch (err) {
      setFormError(err.message || 'Tài khoản hoặc mật khẩu không chính xác.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="login-page-container">
      <div className="login-card">
        <div className="login-header">
          <div style={{ fontSize: '2.5rem', marginBottom: '8px' }}>🏭</div>
          <h1 className="login-title">MAY AN PHÁT</h1>
          <p className="login-subtitle">Hệ Thống Quản Lý Sản Xuất & Chấm Công</p>
        </div>

        {formError && (
          <div className="alert alert-danger" role="alert">
            {formError}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="account">Tên tài khoản</label>
            <input
              id="account"
              type="text"
              className="form-input"
              value={account}
              onChange={(e) => setAccount(e.target.value)}
              placeholder="Nhập tên tài khoản..."
              autoComplete="username"
              disabled={isSubmitting}
              autoFocus
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Mật khẩu</label>
            <input
              id="password"
              type="password"
              className="form-input"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Nhập mật khẩu..."
              autoComplete="current-password"
              disabled={isSubmitting}
            />
          </div>

          <button
            type="submit"
            className="btn-submit-login"
            disabled={isSubmitting}
          >
            {isSubmitting ? 'Đang xác thực...' : 'Đăng Nhập'}
          </button>
        </form>
      </div>
    </div>
  );
}

export default LoginPage;
