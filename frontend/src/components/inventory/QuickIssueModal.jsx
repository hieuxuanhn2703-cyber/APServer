import React, { useState, useEffect } from 'react';
import { createMaterialIssue } from '../../api/inventory';

function formatQty(val, donVi) {
  const num = parseFloat(val) || 0;
  if (donVi === 'chiếc') {
    return Math.round(num).toLocaleString('en-US');
  }
  return num.toLocaleString('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
}

export function QuickIssueModal({
  isOpen,
  item,
  onClose,
  onIssueSuccess,
}) {
  const [ngayXuat, setNgayXuat] = useState('');
  const [soLuongKien, setSoLuongKien] = useState(0);
  const [soLuong, setSoLuong] = useState('');
  const [nguoiNhan, setNguoiNhan] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  // Initialize form values whenever a new item is selected
  useEffect(() => {
    if (isOpen && item) {
      const today = new Date().toISOString().split('T')[0];
      setNgayXuat(today);
      setSoLuongKien(0);
      setSoLuong('');
      setNguoiNhan('');
      setErrorMessage('');
      setIsSubmitting(false);
    }
  }, [isOpen, item]);

  // Handle Escape key
  useEffect(() => {
    if (!isOpen) return;
    const handleKeyDown = (e) => {
      if (e.key === 'Escape' && !isSubmitting) {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, isSubmitting, onClose]);

  if (!isOpen || !item) return null;

  const donVi = item.don_vi || 'm';
  const isChiec = donVi === 'chiếc';
  const maxKien = Math.max(0, item.con_lai_kien || 0);
  const maxSoLuong = Math.max(0, item.con_lai_so_luong || 0);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (isSubmitting) return;

    setErrorMessage('');

    const kienNum = parseInt(soLuongKien, 10) || 0;
    const qtyNum = parseFloat(soLuong) || 0;
    const recipient = (nguoiNhan || '').trim();

    if (!recipient) {
      setErrorMessage('Vui lòng nhập tên người nhận hàng.');
      return;
    }

    if (kienNum < 0 || qtyNum < 0) {
      setErrorMessage('Số lượng xuất không được là số âm.');
      return;
    }

    if (kienNum <= 0 && qtyNum <= 0) {
      setErrorMessage('Vui lòng nhập số lượng kiện hoặc số lượng xuất lớn hơn 0.');
      return;
    }

    if (isChiec && !Number.isInteger(qtyNum)) {
      setErrorMessage("Số lượng xuất phải là số nguyên khi đơn vị là 'chiếc'.");
      return;
    }

    setIsSubmitting(true);
    try {
      await createMaterialIssue({
        ma_hang: item.ma_hang,
        mau: item.mau,
        ten_vat_tu: item.ten_vat_tu,
        don_vi: donVi,
        ngay_xuat: ngayXuat || new Date().toISOString().split('T')[0],
        so_luong_kien: kienNum,
        so_luong: qtyNum,
        nguoi_nhan: recipient,
      });

      if (onIssueSuccess) {
        onIssueSuccess();
      }
      onClose();
    } catch (err) {
      setErrorMessage(err.message || 'Không thể tạo phiếu xuất kho. Vui lòng thử lại.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div
      className="quick-issue-modal-backdrop"
      onClick={(e) => {
        if (e.target === e.currentTarget && !isSubmitting) {
          onClose();
        }
      }}
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal_issue_heading"
    >
      <div className="quick-issue-modal-card">
        {/* Modal Header */}
        <div className="quick-issue-modal-header">
          <div id="modal_issue_heading" className="quick-issue-modal-title">
            <svg
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2.5"
              strokeLinecap="round"
              strokeLinejoin="round"
              aria-hidden="true"
            >
              <line x1="5" y1="12" x2="19" y2="12" />
              <polyline points="12 5 19 12 12 19" />
            </svg>
            Xuất Nguyên Liệu
          </div>
          <button
            type="button"
            className="quick-issue-modal-close"
            onClick={onClose}
            disabled={isSubmitting}
            aria-label="Đóng cửa sổ"
          >
            &times;
          </button>
        </div>

        {/* Form Body */}
        <form onSubmit={handleSubmit} className="quick-issue-modal-form" noValidate>
          {/* Error Message */}
          {errorMessage && (
            <div className="quick-issue-error-alert" role="alert">
              <span>⚠️</span>
              <span>{errorMessage}</span>
            </div>
          )}

          {/* Info Card */}
          <div className="quick-issue-info-card">
            <div className="info-title">
              {item.ma_hang} - Màu: {item.mau}
            </div>
            <div className="info-material">
              Vật tư: {item.ten_vat_tu} (ĐVT: {donVi})
            </div>
            <div className="info-stock">
              Hiện còn tồn: <b>{item.con_lai_kien ?? 0}</b> kiện |{' '}
              <b>{formatQty(item.con_lai_so_luong, donVi)}</b> {donVi}
            </div>
          </div>

          {/* Ngày xuất */}
          <div className="form-group">
            <label htmlFor="id_modal_ngay_xuat" className="form-label">
              Ngày xuất (*)
            </label>
            <input
              type="date"
              id="id_modal_ngay_xuat"
              className="form-input"
              value={ngayXuat}
              onChange={(e) => setNgayXuat(e.target.value)}
              required
              disabled={isSubmitting}
            />
          </div>

          {/* SL kiện & SL xuất */}
          <div className="form-grid-2">
            <div className="form-group">
              <label htmlFor="id_modal_so_luong_kien" className="form-label">
                SL kiện xuất (*)
              </label>
              <input
                type="number"
                id="id_modal_so_luong_kien"
                className="form-input"
                min="0"
                max={maxKien > 0 ? maxKien : undefined}
                value={soLuongKien}
                onChange={(e) => setSoLuongKien(e.target.value)}
                required
                disabled={isSubmitting}
              />
            </div>
            <div className="form-group">
              <label htmlFor="id_modal_so_luong" className="form-label">
                SL xuất ({donVi}) (*)
              </label>
              <input
                type="number"
                id="id_modal_so_luong"
                className="form-input"
                min="0"
                step={isChiec ? '1' : '0.01'}
                max={maxSoLuong > 0 ? maxSoLuong : undefined}
                value={soLuong}
                onChange={(e) => setSoLuong(e.target.value)}
                placeholder={isChiec ? '0' : '0.00'}
                required
                disabled={isSubmitting}
              />
            </div>
          </div>

          {/* Người nhận */}
          <div className="form-group">
            <label htmlFor="id_modal_nguoi_nhan" className="form-label">
              Người nhận (*)
            </label>
            <input
              type="text"
              id="id_modal_nguoi_nhan"
              className="form-input"
              placeholder="Ví dụ: Tổ Cắt, Anh Nam, Chị Hoa..."
              value={nguoiNhan}
              onChange={(e) => setNguoiNhan(e.target.value)}
              required
              disabled={isSubmitting}
            />
          </div>

          {/* Form Actions */}
          <div className="modal-actions-row">
            <button
              type="button"
              className="btn-modal-cancel"
              onClick={onClose}
              disabled={isSubmitting}
            >
              Hủy
            </button>
            <button
              type="submit"
              className="btn-modal-submit"
              disabled={isSubmitting}
            >
              {isSubmitting ? 'Đang xử lý...' : 'Xác Nhận Xuất'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default QuickIssueModal;
