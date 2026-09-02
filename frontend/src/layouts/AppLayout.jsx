import React, { useState, useEffect } from 'react';
import { Outlet, useLocation } from 'react-router-dom';
import Sidebar from '../components/layout/Sidebar';
import Topbar from '../components/layout/Topbar';

const ROUTE_TITLES = {
  '/': 'Tổng Quan Hệ Thống',
  '/dashboard': 'Báo Cáo Tổng Hợp Sản Xuất',
  '/working': 'Quy Trình Sản Xuất & Chấm Công',
  '/inventory': 'Quản Lý Kho Vật Tư',
  '/accounting': 'Kế Toán & Doanh Thu',
};

export function AppLayout() {
  const [isMobileOpen, setIsMobileOpen] = useState(false);
  const [isCollapsed, setIsCollapsed] = useState(() => {
    try {
      return localStorage.getItem('pm_sidebar_collapsed') === 'true';
    } catch {
      return false;
    }
  });

  const location = useLocation();
  const currentTitle = ROUTE_TITLES[location.pathname] || 'May An Phát';

  // Toggle sidebar depending on screen size
  const handleToggleSidebar = () => {
    if (window.innerWidth <= 1024) {
      setIsMobileOpen((prev) => !prev);
    } else {
      setIsCollapsed((prev) => {
        const next = !prev;
        try {
          localStorage.setItem('pm_sidebar_collapsed', String(next));
        } catch {}
        return next;
      });
    }
  };

  const handleCloseSidebar = () => {
    setIsMobileOpen(false);
  };

  // Close mobile drawer on route change
  useEffect(() => {
    setIsMobileOpen(false);
  }, [location.pathname]);

  // Prevent body scrolling when mobile drawer is open
  useEffect(() => {
    if (isMobileOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
    return () => {
      document.body.style.overflow = '';
    };
  }, [isMobileOpen]);

  const isSidebarOpen = isMobileOpen || !isCollapsed;

  return (
    <div className="app-wrapper">
      {/* Mobile Drawer Backdrop */}
      <div
        className={`sidebar-backdrop ${isMobileOpen ? 'active' : ''}`}
        onClick={handleCloseSidebar}
        aria-hidden="true"
      />

      {/* Sidebar Navigation */}
      <Sidebar
        isOpen={isMobileOpen}
        isCollapsed={isCollapsed}
        onCloseSidebar={handleCloseSidebar}
      />

      {/* Main Content Area */}
      <div className="main-wrapper">
        <Topbar
          onToggleSidebar={handleToggleSidebar}
          isSidebarOpen={isSidebarOpen}
          title={currentTitle}
        />
        <main className="main-content" id="mainContent">
          <Outlet />
        </main>
      </div>
    </div>
  );
}

export default AppLayout;
