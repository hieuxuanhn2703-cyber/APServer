/**
 * Token Storage Abstraction
 * Handles storage of JWT access and refresh tokens.
 * Encapsulates localStorage access so storage strategy can be easily adapted.
 * NEVER logs tokens or credentials.
 */

const ACCESS_TOKEN_KEY = 'pm_access_token';
const REFRESH_TOKEN_KEY = 'pm_refresh_token';

export const tokenStorage = {
  getAccessToken: () => {
    try {
      return localStorage.getItem(ACCESS_TOKEN_KEY);
    } catch {
      return null;
    }
  },

  getRefreshToken: () => {
    try {
      return localStorage.getItem(REFRESH_TOKEN_KEY);
    } catch {
      return null;
    }
  },

  setTokens: ({ access, refresh }) => {
    try {
      if (access) {
        localStorage.setItem(ACCESS_TOKEN_KEY, access);
      }
      if (refresh) {
        localStorage.setItem(REFRESH_TOKEN_KEY, refresh);
      }
    } catch {
      // Storage errors handled silently without exposing token data
    }
  },

  setAccessToken: (access) => {
    try {
      if (access) {
        localStorage.setItem(ACCESS_TOKEN_KEY, access);
      }
    } catch {
      // Handled silently
    }
  },

  clearTokens: () => {
    try {
      localStorage.removeItem(ACCESS_TOKEN_KEY);
      localStorage.removeItem(REFRESH_TOKEN_KEY);
    } catch {
      // Handled silently
    }
  },

  hasAccessToken: () => {
    return Boolean(tokenStorage.getAccessToken());
  },

  hasRefreshToken: () => {
    return Boolean(tokenStorage.getRefreshToken());
  }
};

export default tokenStorage;
