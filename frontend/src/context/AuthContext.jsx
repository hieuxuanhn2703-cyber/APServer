import React, { createContext, useState, useEffect, useCallback } from 'react';
import tokenStorage from '../utils/tokenStorage';
import authApi from '../api/auth';

export const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  /**
   * Fetch current user profile using stored JWT
   */
  const refreshUser = useCallback(async () => {
    if (!tokenStorage.hasAccessToken() && !tokenStorage.hasRefreshToken()) {
      setUser(null);
      setIsLoading(false);
      return null;
    }

    try {
      const userData = await authApi.getMe();
      setUser(userData);
      setError(null);
      return userData;
    } catch (err) {
      setUser(null);
      tokenStorage.clearTokens();
      setError(err.message || 'Không thể xác thực phiên đăng nhập');
      return null;
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Initialize auth state on mount
  useEffect(() => {
    refreshUser();

    // Listen for session expiration events dispatched by apiClient
    const handleSessionExpired = () => {
      setUser(null);
      setError('Phiên làm việc đã hết hạn. Vui lòng đăng nhập lại.');
    };

    window.addEventListener('auth:session-expired', handleSessionExpired);
    return () => {
      window.removeEventListener('auth:session-expired', handleSessionExpired);
    };
  }, [refreshUser]);

  /**
   * Log in with account and password
   * NEVER stores or logs credentials
   */
  const login = async (account, password) => {
    setIsLoading(true);
    setError(null);

    try {
      const tokens = await authApi.login({ account, password });
      tokenStorage.setTokens({
        access: tokens.access,
        refresh: tokens.refresh,
      });

      const profile = await authApi.getMe();
      setUser(profile);
      return profile;
    } catch (err) {
      setError(err.message || 'Đăng nhập thất bại. Vui lòng kiểm tra lại tài khoản và mật khẩu.');
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Log out and clear state
   */
  const logout = useCallback(() => {
    tokenStorage.clearTokens();
    setUser(null);
    setError(null);
  }, []);

  const value = {
    user,
    isAuthenticated: Boolean(user),
    isLoading,
    error,
    login,
    logout,
    refreshUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export default AuthContext;
