/**
 * Working & Production Dashboard API Service
 * Handles communication with Working / Production REST endpoints:
 * - Dashboards:
 *   - GET /api/v1/working/dashboards/tracking/
 *   - GET /api/v1/working/dashboards/cut/
 *   - GET /api/v1/working/dashboards/process/
 *   - GET /api/v1/working/dashboards/kcs/
 *   - GET /api/v1/working/dashboards/finishing/
 * - Activity Reports (with ?with_totals=true):
 *   - GET /api/v1/working/reports/cut/
 *   - GET /api/v1/working/reports/process/
 *   - GET /api/v1/working/reports/kcs/
 *   - GET /api/v1/working/reports/finishing/
 * - Config:
 *   - GET /api/v1/working/config/products/
 */

import apiClient from './client';

/**
 * Helper to build a URLSearchParams string from an object
 */
function buildQueryString(params = {}) {
  const query = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '') {
      if (Array.isArray(value)) {
        value.forEach((v) => query.append(key, v));
      } else {
        query.append(key, value);
      }
    }
  });
  const str = query.toString();
  return str ? `?${str}` : '';
}

/**
 * Fetch Order Tracking Matrix data
 * @param {Object} [filters={}] - Optional filters: ma_hang, mau
 * @returns {Promise<Array<Object>>}
 */
export async function getTrackingDashboard(filters = {}) {
  const qs = buildQueryString({
    ma_hang: filters.ma_hang,
    mau: filters.mau,
  });
  return apiClient(`/working/dashboards/tracking/${qs}`);
}

/**
 * Fetch Cut Dashboard Summary
 * @param {Object} [filters={}] - Optional filters: start_date, end_date, ma_hang, mau
 * @returns {Promise<Array<Object>>}
 */
export async function getCutDashboard(filters = {}) {
  const qs = buildQueryString(filters);
  return apiClient(`/working/dashboards/cut/${qs}`);
}

/**
 * Fetch Process (Sewing) Dashboard Summary
 * @param {Object} [filters={}] - Optional filters: start_date, end_date, ma_hang, mau
 * @returns {Promise<Array<Object>>}
 */
export async function getProcessDashboard(filters = {}) {
  const qs = buildQueryString(filters);
  return apiClient(`/working/dashboards/process/${qs}`);
}

/**
 * Fetch KCS Dashboard Summary
 * @param {Object} [filters={}] - Optional filters: start_date, end_date, ma_hang, mau
 * @returns {Promise<Array<Object>>}
 */
export async function getKcsDashboard(filters = {}) {
  const qs = buildQueryString(filters);
  return apiClient(`/working/dashboards/kcs/${qs}`);
}

/**
 * Fetch Finishing Dashboard Summary
 * @param {Object} [filters={}] - Optional filters: start_date, end_date, ma_hang, mau
 * @returns {Promise<Array<Object>>}
 */
export async function getFinishingDashboard(filters = {}) {
  const qs = buildQueryString(filters);
  return apiClient(`/working/dashboards/finishing/${qs}`);
}

/**
 * Fetch Cut activity reports (paginated, with cumulative totals)
 * @param {Object} [params={}]
 * @returns {Promise<{ count: number, next: string|null, previous: string|null, results: Array<Object> }>}
 */
export async function getCutReports(params = {}) {
  const qs = buildQueryString({ with_totals: true, ...params });
  return apiClient(`/working/reports/cut/${qs}`);
}

/**
 * Fetch Process activity reports (paginated, with cumulative totals)
 * @param {Object} [params={}]
 * @returns {Promise<{ count: number, next: string|null, previous: string|null, results: Array<Object> }>}
 */
export async function getProcessReports(params = {}) {
  const qs = buildQueryString({ with_totals: true, ...params });
  return apiClient(`/working/reports/process/${qs}`);
}

/**
 * Fetch KCS activity reports (paginated, with cumulative totals)
 * @param {Object} [params={}]
 * @returns {Promise<{ count: number, next: string|null, previous: string|null, results: Array<Object> }>}
 */
export async function getKcsReports(params = {}) {
  const qs = buildQueryString({ with_totals: true, ...params });
  return apiClient(`/working/reports/kcs/${qs}`);
}

/**
 * Fetch Finishing activity reports (paginated, with cumulative totals)
 * @param {Object} [params={}]
 * @returns {Promise<{ count: number, next: string|null, previous: string|null, results: Array<Object> }>}
 */
export async function getFinishingReports(params = {}) {
  const qs = buildQueryString({ with_totals: true, ...params });
  return apiClient(`/working/reports/finishing/${qs}`);
}

/**
 * Fetch Product catalog with colors and sizes for cascading filters
 * @returns {Promise<Array<Object>>}
 */
export async function getProductsConfig() {
  const res = await apiClient('/working/config/products/?page_size=1000');
  return Array.isArray(res) ? res : (res?.results || []);
}

export default {
  getTrackingDashboard,
  getCutDashboard,
  getProcessDashboard,
  getKcsDashboard,
  getFinishingDashboard,
  getCutReports,
  getProcessReports,
  getKcsReports,
  getFinishingReports,
  getProductsConfig,
};
