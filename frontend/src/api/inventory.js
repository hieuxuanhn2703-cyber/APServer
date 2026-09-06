/**
 * Inventory API Service
 * Handles communication with Inventory REST endpoints:
 * - GET /api/v1/inventory/summary/?ma_hang=...&mau=...&ten_vat_tu=...&don_vi=...
 * - POST /api/v1/inventory/issues/
 * - GET /api/v1/inventory/receipts/
 */

import apiClient from './client';

/**
 * Fetch computed inventory stock summary
 * @param {Object} [filters={}] - Optional filters (ma_hang, mau, ten_vat_tu, don_vi)
 * @returns {Promise<Array<Object>>}
 */
export async function getInventorySummary(filters = {}) {
  const queryParams = new URLSearchParams();

  if (filters.ma_hang) {
    if (Array.isArray(filters.ma_hang)) {
      filters.ma_hang.forEach((v) => queryParams.append('ma_hang', v));
    } else {
      queryParams.append('ma_hang', filters.ma_hang);
    }
  }

  if (filters.mau) {
    if (Array.isArray(filters.mau)) {
      filters.mau.forEach((v) => queryParams.append('mau', v));
    } else {
      queryParams.append('mau', filters.mau);
    }
  }

  if (filters.ten_vat_tu) {
    if (Array.isArray(filters.ten_vat_tu)) {
      filters.ten_vat_tu.forEach((v) => queryParams.append('ten_vat_tu', v));
    } else {
      queryParams.append('ten_vat_tu', filters.ten_vat_tu);
    }
  }

  if (filters.don_vi) {
    if (Array.isArray(filters.don_vi)) {
      filters.don_vi.forEach((v) => queryParams.append('don_vi', v));
    } else {
      queryParams.append('don_vi', filters.don_vi);
    }
  }

  const queryStr = queryParams.toString();
  const endpoint = queryStr ? `/inventory/summary/?${queryStr}` : '/inventory/summary/';
  return apiClient(endpoint);
}

/**
 * Create a new material issue record (quick issue)
 * @param {Object} payload
 * @param {string} payload.ma_hang
 * @param {string} payload.mau
 * @param {string} payload.ten_vat_tu
 * @param {string} [payload.don_vi='m']
 * @param {string} payload.ngay_xuat - YYYY-MM-DD
 * @param {number} payload.so_luong_kien
 * @param {number} payload.so_luong
 * @param {string} payload.nguoi_nhan
 * @param {number} [payload.receipt] - Optional receipt ID
 * @returns {Promise<Object>} Created MaterialIssue record
 */
export async function createMaterialIssue(payload) {
  return apiClient('/inventory/issues/', {
    method: 'POST',
    body: {
      ma_hang: payload.ma_hang,
      mau: payload.mau,
      ten_vat_tu: payload.ten_vat_tu,
      don_vi: payload.don_vi || 'm',
      ngay_xuat: payload.ngay_xuat,
      so_luong_kien: payload.so_luong_kien,
      so_luong: payload.so_luong,
      nguoi_nhan: payload.nguoi_nhan,
      receipt: payload.receipt || null,
    },
  });
}

export const inventoryApi = {
  getSummary: getInventorySummary,
  createIssue: createMaterialIssue,
};

export default inventoryApi;
