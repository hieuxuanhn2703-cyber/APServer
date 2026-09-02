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

    const trimmedAccount = account.trim();

    if (!trimmedAccount && !password) {
      setFormError('Vui lòng nhập tên tài khoản và mật khẩu.');
      return;
    }

    if (!trimmedAccount) {
      setFormError('Vui lòng nhập tên tài khoản.');
      return;
    }

    if (!password) {
      setFormError('Vui lòng nhập mật khẩu.');
      return;
    }

    setIsSubmitting(true);
    try {
      await login(trimmedAccount, password);
      navigate(from, { replace: true });
    } catch (err) {
      const rawMsg = err.message || '';
      if (rawMsg.includes('chưa được duyệt') || rawMsg.includes('inactive')) {
        setFormError('Tài khoản chưa được duyệt bởi quản trị viên.');
      } else if (rawMsg.includes('không đúng') || rawMsg.includes('không chính xác') || err.status === 401) {
        setFormError('Tài khoản hoặc mật khẩu không chính xác.');
      } else if (rawMsg.includes('kết nối') || err.status === 0) {
        setFormError('Không thể kết nối đến máy chủ. Vui lòng kiểm tra đường truyền mạng.');
      } else {
        setFormError(rawMsg || 'Đăng nhập thất bại. Vui lòng thử lại sau.');
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="login-page-container">
      <div className="login-card">
        <div className="login-header">
          <div style={{ fontSize: '2.5rem', marginBottom: '8px' }} aria-hidden="true">🏭</div>
          <h1 className="login-title">MAY AN PHÁT</h1>
          <p className="login-subtitle">Hệ Thống Quản Lý Sản Xuất & Chấm Công</p>
        </div>

        {formError && (
          <div
            id="login-error-msg"
            className="alert alert-danger"
            role="alert"
            aria-live="polite"
          >
            {formError}
          </div>
        )}

        <form onSubmit={handleSubmit} noValidate>
          <div className="form-group">
            <label htmlFor="account">Tên tài khoản</label>
            <input
              id="account"
              type="text"
              className="form-input"
              value={account}
              onChange={(e) => {
                setAccount(e.target.value);
                if (formError) setFormError('');
              }}
              placeholder="Nhập tên tài khoản..."
              autoComplete="username"
              disabled={isSubmitting}
              autoFocus
              aria-invalid={Boolean(formError)}
              aria-describedby={formError ? 'login-error-msg' : undefined}
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Mật khẩu</label>
            <input
              id="password"
              type="password"
              className="form-input"
              value={password}
              onChange={(e) => {
                setPassword(e.target.value);
                if (formError) setFormError('');
              }}
              placeholder="Nhập mật khẩu..."
              autoComplete="current-password"
              disabled={isSubmitting}
              aria-invalid={Boolean(formError)}
              aria-describedby={formError ? 'login-error-msg' : undefined}
            />
          </div>

          <button
            type="submit"
            className="btn-submit-login"
            disabled={isSubmitting}
            aria-busy={isSubmitting}
          >
            {isSubmitting ? (
              <span style={{ display: 'inline-flex', alignItems: 'center', gap: '8px' }}>
                <span className="spinner" style={{ width: '16px', height: '16px', borderWidth: '2px' }} aria-hidden="true" />
                Đang xác thực...
              </span>
            ) : (
              'Đăng Nhập'
            )}
          </button>
        </form>
      </div>
    </div>
  );
}

export default LoginPage;
