/**
 * Accounting API Service
 * Handles communication with Accounting REST endpoints:
 * - GET /api/v1/accounting/dashboard/?ma_hang=...
 * - POST /api/v1/accounting/payments/
 * - DELETE /api/v1/accounting/payments/{id}/
 * - GET /api/v1/working/config/products/
 */

import apiClient from './client';

/**
 * Fetch Accounting Dashboard data (rows, kpi, payments_by_pc)
 * @param {string} maHang - Optional product name filter
 * @returns {Promise<{ rows: Array, kpi: Object, payments_by_pc: Object }>}
 */
export async function getAccountingDashboard(maHang = '') {
  const query = maHang ? `?ma_hang=${encodeURIComponent(maHang)}` : '';
  return apiClient(`/accounting/dashboard/${query}`);
}

/**
 * Create a new payment record
 * @param {Object} payload
 * @param {string} payload.ngay_thanh_toan - Date string YYYY-MM-DD
 * @param {number} payload.product_color - ProductColor ID
 * @param {number} payload.so_tien - Amount in VNĐ
 * @param {string} [payload.ghi_chu] - Optional note
 * @returns {Promise<Object>} Created PaymentReport record
 */
export async function createPayment({ ngay_thanh_toan, product_color, so_tien, ghi_chu = '' }) {
  return apiClient('/accounting/payments/', {
    method: 'POST',
    body: {
      ngay_thanh_toan,
      product_color,
      so_tien,
      ghi_chu,
    },
  });
}

/**
 * Delete a payment record by ID
 * @param {number} paymentId
 * @returns {Promise<void>}
 */
export async function deletePayment(paymentId) {
  return apiClient(`/accounting/payments/${paymentId}/`, {
    method: 'DELETE',
  });
}

/**
 * Fetch list of all products for the filter dropdown
 * @returns {Promise<Array<{ id: number, name: string }>>}
 */
export async function getProductOptions() {
  return apiClient('/working/config/products/');
}
