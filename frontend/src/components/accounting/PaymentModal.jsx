import React, { useState, useEffect } from 'react';
import { createPayment, deletePayment } from '../../api/accounting';

function formatNumber(num) {
  if (num === null || num === undefined || isNaN(num)) return '0';
  return Number(num).toLocaleString('en-US');
}

export function PaymentModal({
  isOpen,
  row,
  paymentsList = [],
  onClose,
  onPaymentSuccess,
}) {
  const [ngayThanhToan, setNgayThanhToan] = useState('');
  const [soTienStr, setSoTienStr] = useState('');
  const [ghiChu, setGhiChu] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isDeletingId, setIsDeletingId] = useState(null);
  const [errorMessage, setErrorMessage] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  // Reset form when opened for a specific row
  useEffect(() => {
    if (isOpen && row) {
      const today = new Date().toISOString().split('T')[0];
      setNgayThanhToan(today);
      const remaining = row.tien_chua_thanh_toan > 0 ? row.tien_chua_thanh_toan : 0;
      setSoTienStr(remaining > 0 ? formatNumber(remaining) : '');
      setGhiChu('');
      setErrorMessage('');
      setSuccessMessage('');
    }
  }, [isOpen, row]);

  // Handle escape key to close
  useEffect(() => {
    if (!isOpen) return;
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen || !row) return null;

  const currentRemainingDebt = row.tien_chua_thanh_toan > 0 ? row.tien_chua_thanh_toan : 0;

  const handleFillRemaining = () => {
    setSoTienStr(formatNumber(currentRemainingDebt));
  };

  const handleSoTienChange = (e) => {
    const raw = e.target.value.replace(/[^\d]/g, '');
    if (raw) {
      const num = parseInt(raw, 10);
      setSoTienStr(formatNumber(num));
    } else {
      setSoTienStr('');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage('');
    setSuccessMessage('');

    const numericAmount = parseInt(soTienStr.replace(/[^\d]/g, ''), 10);
    if (!numericAmount || numericAmount <= 0) {
      setErrorMessage('Vui lòng nhập số tiền thanh toán hợp lệ lớn hơn 0.');
      return;
    }

    if (!ngayThanhToan) {
      setErrorMessage('Vui lòng chọn ngày thanh toán.');
      return;
    }

    try {
      setIsSubmitting(true);
      await createPayment({
        ngay_thanh_toan: ngayThanhToan,
        product_color: row.product_color_id,
        so_tien: numericAmount,
        ghi_chu: ghiChu.trim(),
      });

      setSuccessMessage('Ghi nhận đợt thanh toán thành công!');
      // Refresh parent data
      await onPaymentSuccess();
      // Reset input fields
      setGhiChu('');
    } catch (err) {
      setErrorMessage(err.message || 'Có lỗi xảy ra khi lưu đợt thanh toán.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDelete = async (paymentId) => {
    if (!window.confirm('Bạn có chắc chắn muốn xóa đợt thanh toán này không?')) {
      return;
    }

    try {
      setIsDeletingId(paymentId);
      setErrorMessage('');
      await deletePayment(paymentId);
      setSuccessMessage('Đã xóa đợt thanh toán.');
      await onPaymentSuccess();
    } catch (err) {
      setErrorMessage(err.message || 'Không thể xóa đợt thanh toán.');
    } finally {
      setIsDeletingId(null);
    }
  };

  return (
    <div
      className="modal-backdrop active"
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
      role="dialog"
      aria-modal="true"
      aria-labelledby="modalPaymentTitle"
    >
      <div className="modal-dialog-box">
        {/* Modal Header */}
        <div className="modal-header">
          <h3 className="modal-title" id="modalPaymentTitle">
            💳 Ghi Nhận Thanh Toán:{' '}
            <span style={{ color: '#6d28d9' }}>
              {row.ma_hang} — {row.mau}
            </span>
          </h3>
          <button
            type="button"
            className="modal-close-btn"
            onClick={onClose}
            aria-label="Đóng cửa sổ"
          >
            &times;
          </button>
        </div>

        <div className="modal-body">
          {/* Banner tóm tắt công nợ mặt hàng */}
          <div className="modal-info-banner">
            <div className="modal-info-item">
              <span className="modal-info-lbl">Tiền Đã Xuất</span>
              <span className="modal-info-val" style={{ color: '#16a34a' }}>
                {formatNumber(row.tien_da_xuat)} đ
              </span>
            </div>
            <div className="modal-info-item">
              <span className="modal-info-lbl">Đã Thanh Toán</span>
              <span className="modal-info-val" style={{ color: '#6d28d9' }}>
                {formatNumber(row.tien_da_thanh_toan)} đ
              </span>
            </div>
            <div className="modal-info-item">
              <span className="modal-info-lbl">Chưa Thanh Toán</span>
              <span className="modal-info-val" style={{ color: '#dc2626' }}>
                {formatNumber(row.tien_chua_thanh_toan)} đ
              </span>
            </div>
          </div>

          {/* Feedback Messages */}
          {errorMessage && (
            <div className="modal-alert modal-alert-error" role="alert">
              ⚠️ {errorMessage}
            </div>
          )}
          {successMessage && (
            <div className="modal-alert modal-alert-success" role="alert">
              ✅ {successMessage}
            </div>
          )}

          {/* Form tạo đợt thanh toán mới */}
          <form onSubmit={handleSubmit} id="createPaymentForm">
            <div className="form-group-modal">
              <label className="form-label-modal" htmlFor="modal_ngay_thanh_toan">
                Ngày thanh toán (*)
              </label>
              <input
                type="date"
                id="modal_ngay_thanh_toan"
                className="form-input-modal"
                value={ngayThanhToan}
                onChange={(e) => setNgayThanhToan(e.target.value)}
                required
              />
            </div>

            <div className="form-group-modal">
              <label className="form-label-modal" htmlFor="modal_so_tien">
                Số tiền thanh toán (VNĐ) (*)
              </label>
              <input
                type="text"
                id="modal_so_tien"
                className="form-input-modal"
                placeholder="Nhập số tiền VNĐ..."
                value={soTienStr}
                onChange={handleSoTienChange}
                required
                autoComplete="off"
              />
              <button
                type="button"
                className="btn-fill-all"
                onClick={handleFillRemaining}
              >
                ⚡ Điền toàn bộ số tiền chưa thanh toán
              </button>
            </div>

            <div className="form-group-modal" style={{ marginBottom: '18px' }}>
              <label className="form-label-modal" htmlFor="modal_ghi_chu">
                Ghi chú / Chứng từ thanh toán
              </label>
              <input
                type="text"
                id="modal_ghi_chu"
                className="form-input-modal"
                placeholder="Số ủy nhiệm chi, ngân hàng, người nộp..."
                value={ghiChu}
                onChange={(e) => setGhiChu(e.target.value)}
              />
            </div>

            <button
              type="submit"
              className="btn-submit-modal"
              disabled={isSubmitting}
            >
              <svg
                width="18"
                height="18"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2.5"
                strokeLinecap="round"
                strokeLinejoin="round"
                aria-hidden="true"
              >
                <polyline points="20 6 9 17 4 12" />
              </svg>
              {isSubmitting ? 'Đang lưu...' : 'Lưu Đợt Thanh Toán'}
            </button>
          </form>

          {/* Lịch sử các lần thanh toán trước */}
          <div className="history-section-modal">
            <div className="history-title-modal">
              📜 Lịch sử các lần thanh toán trước:
            </div>
            <div className="history-list-scroll">
              {paymentsList && paymentsList.length > 0 ? (
                <table className="history-table-modal">
                  <thead>
                    <tr>
                      <th>Ngày</th>
                      <th>Số tiền</th>
                      <th>Ghi chú</th>
                      <th>Người ghi</th>
                      <th style={{ width: '40px', textAlign: 'center' }}></th>
                    </tr>
                  </thead>
                  <tbody>
                    {paymentsList.map((p) => (
                      <tr key={p.id}>
                        <td>{p.ngay_thanh_toan}</td>
                        <td style={{ fontWeight: 700, color: '#6d28d9' }}>
                          {formatNumber(p.so_tien)} đ
                        </td>
                        <td>{p.ghi_chu || '-'}</td>
                        <td style={{ color: '#64748b', fontSize: '0.78rem' }}>
                          {p.nguoi_nhap || '-'}
                        </td>
                        <td style={{ textAlign: 'center' }}>
                          <button
                            type="button"
                            className="btn-del-pay"
                            onClick={() => handleDelete(p.id)}
                            disabled={isDeletingId === p.id}
                            title="Xóa đợt thanh toán này"
                            aria-label={`Xóa đợt thanh toán ${p.id}`}
                          >
                            {isDeletingId === p.id ? '⏳' : '🗑️'}
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              ) : (
                <div className="history-empty-text">
                  Chưa có lịch sử thanh toán nào cho mặt hàng này.
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default PaymentModal;
