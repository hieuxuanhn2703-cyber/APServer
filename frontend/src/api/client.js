/**
 * Centralized API Client
 * Wraps native fetch with JWT authorization header injection,
 * automatic token refreshing upon 401, JSON serialization, and normalized error handling.
 */

import tokenStorage from '../utils/tokenStorage';

const BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1';

// Custom API Error class for rich error inspection
export class ApiError extends Error {
  constructor(message, status, data = null) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.data = data;
  }
}

// Track ongoing refresh promise to prevent race conditions during parallel 401s
let refreshTokenPromise = null;

async function refreshAccessToken() {
  const refreshToken = tokenStorage.getRefreshToken();
  if (!refreshToken) {
    tokenStorage.clearTokens();
    window.dispatchEvent(new CustomEvent('auth:session-expired'));
    throw new ApiError('No refresh token available', 401);
  }

  try {
    const response = await fetch(`${BASE_URL}/auth/token/refresh/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify({ refresh: refreshToken }),
    });

    if (!response.ok) {
      tokenStorage.clearTokens();
      window.dispatchEvent(new CustomEvent('auth:session-expired'));
      throw new ApiError('Refresh token expired or invalid', response.status);
    }

    const data = await response.json();
    if (data.access) {
      tokenStorage.setAccessToken(data.access);
      return data.access;
    }

    throw new ApiError('Invalid refresh response', 401);
  } catch (err) {
    tokenStorage.clearTokens();
    window.dispatchEvent(new CustomEvent('auth:session-expired'));
    throw err;
  } finally {
    refreshTokenPromise = null;
  }
}

export async function apiClient(endpoint, options = {}) {
  const {
    method = 'GET',
    headers = {},
    body = null,
    skipAuth = false,
    ...restOptions
  } = options;

  // Build complete URL
  const normalizedEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
  const url = `${BASE_URL}${normalizedEndpoint}`;

  // Build headers
  const requestHeaders = {
    'Accept': 'application/json',
    ...headers,
  };

  if (body && !(body instanceof FormData) && !requestHeaders['Content-Type']) {
    requestHeaders['Content-Type'] = 'application/json';
  }

  // Inject Authorization header unless skipAuth is true
  if (!skipAuth) {
    let token = tokenStorage.getAccessToken();
    if (!token && tokenStorage.hasRefreshToken() && !endpoint.includes('/auth/token/')) {
      try {
        if (!refreshTokenPromise) {
          refreshTokenPromise = refreshAccessToken();
        }
        token = await refreshTokenPromise;
      } catch {
        // Handled by refreshAccessToken
      }
    }
    if (token) {
      requestHeaders['Authorization'] = `Bearer ${token}`;
    }
  }

  const fetchOptions = {
    method,
    headers: requestHeaders,
    body: body && !(body instanceof FormData) && typeof body === 'object' ? JSON.stringify(body) : body,
    ...restOptions,
  };

  let response;
  try {
    response = await fetch(url, fetchOptions);
  } catch (networkError) {
    throw new ApiError('Không thể kết nối đến máy chủ. Vui lòng kiểm tra mạng.', 0, networkError);
  }

  // Handle 401 Unauthorized - Attempt token refresh if not already an auth endpoint
  if (response.status === 401 && !skipAuth && !endpoint.includes('/auth/token/')) {
    try {
      if (!refreshTokenPromise) {
        refreshTokenPromise = refreshAccessToken();
      }
      const newAccessToken = await refreshTokenPromise;

      // Retry original request with new token
      requestHeaders['Authorization'] = `Bearer ${newAccessToken}`;
      response = await fetch(url, {
        ...fetchOptions,
        headers: requestHeaders,
      });
    } catch {
      throw new ApiError('Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại.', 401);
    }
  }

  // Parse response
  const contentType = response.headers.get('content-type');
  let data = null;
  if (contentType && contentType.includes('application/json')) {
    data = await response.json();
  } else {
    data = await response.text();
  }

  if (!response.ok) {
    let errorMessage = `Yêu cầu thất bại (${response.status})`;
    if (typeof data === 'object' && data !== null) {
      if (data.error) {
        errorMessage = data.error;
      } else if (data.detail) {
        errorMessage = data.detail;
      } else if (data.message) {
        errorMessage = data.message;
      } else if (data.non_field_errors) {
        errorMessage = Array.isArray(data.non_field_errors) ? data.non_field_errors.join(', ') : data.non_field_errors;
      } else {
        const fieldErrors = Object.entries(data)
          .map(([key, val]) => `${key}: ${Array.isArray(val) ? val.join(', ') : val}`)
          .join('; ');
        if (fieldErrors) {
          errorMessage = fieldErrors;
        }
      }
    }
    throw new ApiError(errorMessage, response.status, data);
  }

  return data;
}

export default apiClient;
