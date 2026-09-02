/**
 * UX Role Convenience Hook
 *
 * IMPORTANT:
 * React role checks are for UI and navigation convenience ONLY (e.g. hiding menu links).
 * Backend Django REST API permissions remain the authoritative security boundary.
 */

import { useAuth } from './useAuth';

export function useRoles() {
  const { user } = useAuth();
  const currentRole = user?.role || null;

  const hasRole = (role) => {
    if (!currentRole) return false;
    return currentRole === role;
  };

  const hasAnyRole = (roles = []) => {
    if (!currentRole) return false;
    return roles.includes(currentRole);
  };

  const isAdmin = currentRole === 'PREMIUM';
  const isManager = currentRole === 'QUAN_LY' || currentRole === 'PREMIUM';
  const isAccountant = currentRole === 'KE_TOAN';
  const isWarehouse = currentRole === 'KHO';

  return {
    role: currentRole,
    hasRole,
    hasAnyRole,
    isAdmin,
    isManager,
    isAccountant,
    isWarehouse,
  };
}

export default useRoles;
