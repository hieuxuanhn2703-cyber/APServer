import React from 'react';
import { Navigate, useLocation, Outlet } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { useRoles } from '../hooks/useRoles';
import LoadingSpinner from '../components/common/LoadingSpinner';
import Unauthorized from '../components/common/Unauthorized';

/**
 * Route Guard Component
 * Blocks unauthenticated users and redirects to /login.
 * Optionally supports role-based protection (as UX safeguard; backend remains authoritative).
 */
export function ProtectedRoute({ allowedRoles = null, children }) {
  const { isAuthenticated, isLoading } = useAuth();
  const { hasAnyRole } = useRoles();
  const location = useLocation();

  if (isLoading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh' }}>
        <LoadingSpinner message="Đang kiểm tra phiên đăng nhập..." />
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  if (allowedRoles && !hasAnyRole(allowedRoles)) {
    return <Unauthorized />;
  }

  return children ? children : <Outlet />;
}

export default ProtectedRoute;
