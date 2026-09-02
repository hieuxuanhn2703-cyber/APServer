import React from 'react';
import { NavLink } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { useRoles } from '../../hooks/useRoles';

export function Sidebar({ isOpen, isCollapsed, onCloseSidebar }) {
  const { user, logout } = useAuth();
  const { hasAnyRole } = useRoles();

  // Role visibility checks (UX convenience only; Django DRF permissions remain authoritative)
  const canSeeDashboard = hasAnyRole(['PREMIUM', 'QUAN_LY', 'KE_TOAN']);
  const canSeeAccounting = hasAnyRole(['PREMIUM', 'QUAN_LY', 'KE_TOAN']);
  const canSeeWorking = hasAnyRole(['PREMIUM', 'QUAN_LY', 'NHA_CAT', 'BASIC', 'KCS', 'HOAN_THIEN']);
  const canSeeInventory = hasAnyRole(['PREMIUM', 'QUAN_LY', 'KE_TOAN', 'KHO']);

  // Keyboard accessibility: Close drawer on Escape when open
  React.useEffect(() => {
    if (!isOpen) return;
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') {
        onCloseSidebar();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onCloseSidebar]);

  const handleLogout = () => {
    if (onCloseSidebar) onCloseSidebar();
    logout();
  };

  const userInitial = user?.name ? user.name.charAt(0).toUpperCase() : 'U';

  return (
    <aside
      className={`app-sidebar ${isCollapsed ? 'collapsed' : ''} ${isOpen ? 'open' : ''}`}
      id="appSidebar"
      role="navigation"
      aria-label="Điều hướng chính"
    >
      {/* Brand Header */}
      <div className="sidebar-brand">
        <div className="brand-logo-wrap" aria-hidden="true">
          🏭
        </div>
        <div className="brand-text">
          <span className="brand-name">MAY AN PHÁT</span>
          <span className="brand-badge">Hệ Thống Sản Xuất</span>
        </div>
        <button
          type="button"
          className="sidebar-close-btn"
          onClick={onCloseSidebar}
          aria-label="Đóng menu"
        >
          ✕
        </button>
      </div>

      {/* Navigation Links */}
      <nav className="sidebar-nav">
        {/* Báo Cáo Tổng Hợp */}
        {canSeeDashboard && (
          <div className="nav-section">
            <span className="nav-section-title">Báo Cáo Tổng Hợp</span>
            <NavLink
              to="/dashboard"
              className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
              onClick={onCloseSidebar}
            >
              <span className="nav-icon">📊</span>
              <span className="nav-label">Báo Cáo Sản Xuất</span>
            </NavLink>
          </div>
        )}

        {/* Quy Trình Sản Xuất */}
        {canSeeWorking && (
          <div className="nav-section">
            <span className="nav-section-title">Quy Trình Sản Xuất</span>
            <NavLink
              to="/working"
              className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
              onClick={onCloseSidebar}
            >
              <span className="nav-icon">⚙️</span>
              <span className="nav-label">Nhật Ký Làm Việc</span>
            </NavLink>
          </div>
        )}

        {/* Kho Vật Tư */}
        {canSeeInventory && (
          <div className="nav-section">
            <span className="nav-section-title">Kho Vật Tư</span>
            <NavLink
              to="/inventory"
              className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
              onClick={onCloseSidebar}
            >
              <span className="nav-icon">📦</span>
              <span className="nav-label">Quản Lý Kho</span>
            </NavLink>
          </div>
        )}

        {/* Kế Toán & Tài Chính */}
        {canSeeAccounting && (
          <div className="nav-section">
            <span className="nav-section-title">Kế Toán & Tài Chính</span>
            <NavLink
              to="/accounting"
              className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
              onClick={onCloseSidebar}
            >
              <span className="nav-icon">💰</span>
              <span className="nav-label">Doanh Thu & Đơn Giá</span>
            </NavLink>
          </div>
        )}
      </nav>

      {/* Footer Profile & Logout */}
      <div className="sidebar-footer">
        <div className="user-card">
          <div className="user-avatar">{userInitial}</div>
          <div className="user-info">
            <span className="user-name" title={user?.name}>
              {user?.name || user?.account || 'Người dùng'}
            </span>
            <span className="user-role-badge">{user?.role || 'BASIC'}</span>
          </div>
        </div>

        <div className="user-quick-actions">
          <button
            type="button"
            className="quick-action-btn logout-btn"
            onClick={handleLogout}
            title="Đăng xuất khỏi hệ thống"
          >
            <span>Đăng xuất</span>
          </button>
        </div>
      </div>
    </aside>
  );
}

export default Sidebar;
