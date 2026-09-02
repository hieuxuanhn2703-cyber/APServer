/**
 * Authentication API Endpoints
 * Maps exactly to Django REST backend:
 * - POST /api/v1/auth/token/
 * - POST /api/v1/auth/token/refresh/
 * - GET  /api/v1/auth/me/
 */

import { apiClient } from './client';

export const authApi = {
  /**
   * Request JWT access & refresh tokens
   * @param {Object} credentials - { account, password }
   */
  login: async (credentials) => {
    return apiClient('/auth/token/', {
      method: 'POST',
      body: credentials,
      skipAuth: true,
    });
  },

  /**
   * Refresh expired access token
   * @param {string} refreshToken
   */
  refreshToken: async (refreshToken) => {
    return apiClient('/auth/token/refresh/', {
      method: 'POST',
      body: { refresh: refreshToken },
      skipAuth: true,
    });
  },

  /**
   * Retrieve current authenticated AppUser profile
   */
  getMe: async () => {
    return apiClient('/auth/me/', {
      method: 'GET',
    });
  },
};

export default authApi;
