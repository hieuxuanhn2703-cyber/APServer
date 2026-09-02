import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useRoles } from '../hooks/useRoles';
import ProtectedRoute from './ProtectedRoute';
import AppLayout from '../layouts/AppLayout';

import LoginPage from '../pages/LoginPage';
import DashboardPlaceholder from '../pages/DashboardPlaceholder';
import WorkingPlaceholder from '../pages/WorkingPlaceholder';
import InventoryPlaceholder from '../pages/InventoryPlaceholder';
import AccountingPlaceholder from '../pages/AccountingPlaceholder';
import NotFoundPage from '../pages/NotFoundPage';

/**
 * Smart landing redirector based on user role
 */
function HomeRedirect() {
  const { hasAnyRole } = useRoles();

  if (hasAnyRole(['PREMIUM', 'QUAN_LY', 'KE_TOAN'])) {
    return <Navigate to="/dashboard" replace />;
  }

  if (hasAnyRole(['KHO'])) {
    return <Navigate to="/inventory" replace />;
  }

  if (hasAnyRole(['BASIC', 'NHA_CAT', 'KCS', 'HOAN_THIEN'])) {
    return <Navigate to="/working" replace />;
  }

  // Safe fallback for any unknown or unassigned role
  return <Navigate to="/dashboard" replace />;
}

export function AppRoutes() {
  return (
    <Routes>
      {/* Public Routes */}
      <Route path="/login" element={<LoginPage />} />

      {/* Protected Routes inside AppLayout */}
      <Route
        element={
          <ProtectedRoute>
            <AppLayout />
          </ProtectedRoute>
        }
      >
        <Route path="/" element={<HomeRedirect />} />
        <Route path="/dashboard" element={<DashboardPlaceholder />} />
        <Route path="/working" element={<WorkingPlaceholder />} />
        <Route path="/inventory" element={<InventoryPlaceholder />} />
        <Route path="/accounting" element={<AccountingPlaceholder />} />
      </Route>

      {/* 404 Route */}
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
}

export default AppRoutes;
