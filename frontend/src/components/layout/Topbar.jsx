import React from 'react';
import { useAuth } from '../../hooks/useAuth';

export function Topbar({ onToggleSidebar, isSidebarOpen = true, title = 'Tổng Quan Hệ Thống' }) {
  const { user } = useAuth();

  return (
    <header className="top-bar">
      <div className="topbar-left">
        <button
          type="button"
          className="sidebar-toggle-btn"
          onClick={onToggleSidebar}
          aria-label="Thu gọn hoặc mở rộng thanh điều hướng"
          aria-controls="appSidebar"
          aria-expanded={isSidebarOpen}
          title="Thu gọn/Mở rộng menu"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="3" y1="12" x2="21" y2="12"></line>
            <line x1="3" y1="6" x2="21" y2="6"></line>
            <line x1="3" y1="18" x2="21" y2="18"></line>
          </svg>
        </button>
        <h1 className="page-title">{title}</h1>
      </div>

      <div className="topbar-right">
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.85rem' }}>
          <span style={{ color: 'var(--text-muted)' }}>Xin chào,</span>
          <strong>{user?.name || user?.account}</strong>
          <span className="user-role-badge" style={{ margin: 0 }}>
            {user?.role}
          </span>
        </div>
      </div>
    </header>
  );
}

export default Topbar;
