import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { useSearchParams } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { useRoles } from '../hooks/useRoles';
import { getInventorySummary } from '../api/inventory';
import InventoryFilterBar from '../components/inventory/InventoryFilterBar';
import InventorySummaryTable from '../components/inventory/InventorySummaryTable';
import QuickIssueModal from '../components/inventory/QuickIssueModal';
import './InventoryDashboard.css';

export function InventoryDashboardPage() {
  const { user } = useAuth();
  const { hasAnyRole } = useRoles();
  const [searchParams, setSearchParams] = useSearchParams();

  // URL State for filters
  const selectedMaHang = searchParams.get('ma_hang') || '';
  const selectedMau = searchParams.get('mau') || '';
  const selectedTenVatTu = searchParams.get('ten_vat_tu') || '';
  const selectedDonVi = searchParams.get('don_vi') || '';

  // Local state
  const [rows, setRows] = useState([]);
  const [allOptions, setAllOptions] = useState({
    maHangList: [],
    mauList: [],
    tenVatTuList: [],
    donViList: [],
  });
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [permissionDenied, setPermissionDenied] = useState(false);

  // Quick Issue modal active item
  const [activeIssueItem, setActiveIssueItem] = useState(null);

  // Authorization check: KHO, PREMIUM, QUAN_LY, KE_TOAN
  const isAuthorized = hasAnyRole(['KHO', 'PREMIUM', 'QUAN_LY', 'KE_TOAN']);
  const canCreateReceipt = hasAnyRole(['KHO', 'QUAN_LY']);

  // Helper to extract unique sorted options from a dataset
  const extractOptions = (data) => {
    const maSet = new Set();
    const mauSet = new Set();
    const vtSet = new Set();
    const dvSet = new Set();

    data.forEach((r) => {
      if (r.ma_hang) maSet.add(r.ma_hang.trim());
      if (r.mau) mauSet.add(r.mau.trim());
      if (r.ten_vat_tu) vtSet.add(r.ten_vat_tu.trim());
      if (r.don_vi) dvSet.add(r.don_vi.trim());
    });

    const sortFn = (a, b) => a.localeCompare(b, 'vi', { numeric: true });

    return {
      maHangList: Array.from(maSet).sort(sortFn),
      mauList: Array.from(mauSet).sort(sortFn),
      tenVatTuList: Array.from(vtSet).sort(sortFn),
      donViList: Array.from(dvSet).sort(sortFn),
    };
  };

  // Dedicated effect to load full filter options on mount
  useEffect(() => {
    if (!isAuthorized) return;
    let isMounted = true;

    async function loadInitialOptions() {
      try {
        const fullData = await getInventorySummary({});
        if (isMounted && Array.isArray(fullData)) {
          setAllOptions(extractOptions(fullData));
        }
      } catch {
        // Fallback: options will be derived from active rows if this fails
      }
    }

    loadInitialOptions();
    return () => {
      isMounted = false;
    };
  }, [isAuthorized]);

  // Main data fetcher
  const fetchSummary = useCallback(
    async (showLoading = true) => {
      if (!isAuthorized) return;

      try {
        if (showLoading) setIsLoading(true);
        setError(null);
        setPermissionDenied(false);

        const filterPayload = {};
        if (selectedMaHang) filterPayload.ma_hang = selectedMaHang;
        if (selectedMau) filterPayload.mau = selectedMau;
        if (selectedTenVatTu) filterPayload.ten_vat_tu = selectedTenVatTu;
        if (selectedDonVi) filterPayload.don_vi = selectedDonVi;

        const data = await getInventorySummary(filterPayload);
        const safeRows = Array.isArray(data) ? data : [];
        setRows(safeRows);

        // Fallback: if options are still empty, populate from current rows
        setAllOptions((prev) => {
          if (prev.maHangList.length === 0 && safeRows.length > 0) {
            return extractOptions(safeRows);
          }
          return prev;
        });

        // If an item was open in the modal, refresh its stock data safely
        setActiveIssueItem((prev) => {
          if (!prev) return null;
          const matched = safeRows.find(
            (r) =>
              r.ma_hang === prev.ma_hang &&
              r.mau === prev.mau &&
              r.ten_vat_tu === prev.ten_vat_tu &&
              r.don_vi === prev.don_vi
          );
          return matched || prev;
        });
      } catch (err) {
        if (err.status === 403) {
          setPermissionDenied(true);
        } else {
          setError(err.message || 'Không thể tải dữ liệu tồn kho. Vui lòng kiểm tra kết nối.');
        }
      } finally {
        if (showLoading) setIsLoading(false);
      }
    },
    [isAuthorized, selectedMaHang, selectedMau, selectedTenVatTu, selectedDonVi]
  );

  // Fetch whenever filters change
  useEffect(() => {
    fetchSummary(true);
  }, [fetchSummary]);

  // Filter change handler
  const handleFilterChange = (key, value) => {
    const newParams = new URLSearchParams(searchParams);
    if (value) {
      newParams.set(key, value);
    } else {
      newParams.delete(key);
    }
    setSearchParams(newParams);
  };

  // Clear all filters handler
  const handleClearFilters = () => {
    setSearchParams({});
  };

  // 403 Forbidden State (without logging out)
  if (!isAuthorized || permissionDenied) {
    return (
      <div className="inventory-page-container">
        <div className="inventory-permission-denied" role="alert">
          <h2 style={{ fontSize: '1.25rem', fontWeight: 800, marginBottom: '8px' }}>
            🚫 Quyền Truy Cập Bị Từ Chối
          </h2>
          <p style={{ fontSize: '0.92rem', lineHeight: 1.5 }}>
            Tài khoản của bạn (<b>{user?.name || user?.account}</b>, vai trò:{' '}
            <b>{user?.role}</b>) không có quyền truy cập vào phân hệ <b>Quản Lý Kho Vật Tư</b>.
          </p>
          <p style={{ fontSize: '0.84rem', marginTop: '8px', color: '#b45309' }}>
            Vui lòng liên hệ Quản trị viên nếu bạn cần phân quyền vai trò <b>KHO</b>,{' '}
            <b>QUAN_LY</b>, <b>PREMIUM</b> hoặc <b>KE_TOAN</b>.
          </p>
        </div>
      </div>
    );
  }

  const currentFilters = {
    ma_hang: selectedMaHang,
    mau: selectedMau,
    ten_vat_tu: selectedTenVatTu,
    don_vi: selectedDonVi,
  };

  return (
    <div className="inventory-page-container">
      {/* Page Header */}
      <div className="inventory-header">
        <div className="inventory-header-title-box">
          <span className="inventory-header-icon" aria-hidden="true">
            📦
          </span>
          <div>
            <h1 className="inventory-header-title">Tổng Hợp Tồn Kho Nguyên Vật Liệu</h1>
            <p className="inventory-header-subtitle">
              Theo dõi cân đối thực nhận - thực xuất - tồn kho và thao tác xuất kho
            </p>
          </div>
        </div>
      </div>

      {/* Error Alert with Retry */}
      {error && (
        <div className="inventory-error-banner" role="alert">
          <div className="inventory-error-text">
            <span>⚠️</span>
            <span>{error}</span>
          </div>
          <button
            type="button"
            className="btn-retry"
            onClick={() => fetchSummary(true)}
          >
            Thử lại
          </button>
        </div>
      )}

      {/* Main Content Card */}
      <div className="inventory-card">
        <div className="inventory-card-header">
          <h3 className="inventory-card-title">
            <svg
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="#3b82f6"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              aria-hidden="true"
            >
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
              <polyline points="14 2 14 8 20 8" />
              <line x1="16" y1="13" x2="8" y2="13" />
              <line x1="16" y1="17" x2="8" y2="17" />
            </svg>
            Bảng Tổng Hợp Tất Cả Nguyên Vật Liệu Trong Kho
          </h3>
        </div>

        {/* Filter Toolbar */}
        <InventoryFilterBar
          options={allOptions}
          filters={currentFilters}
          onFilterChange={handleFilterChange}
          onClearFilters={handleClearFilters}
          canCreateReceipt={canCreateReceipt}
        />

        {/* Loading Spinner or Data Table */}
        {isLoading ? (
          <div className="inventory-loading-container" aria-live="polite">
            <div className="loading-spinner" />
            <span style={{ fontSize: '0.9rem', color: '#64748b', fontWeight: 600 }}>
              Đang tải dữ liệu tồn kho...
            </span>
          </div>
        ) : (
          <InventorySummaryTable
            rows={rows}
            onOpenIssue={(item) => setActiveIssueItem(item)}
          />
        )}
      </div>

      {/* Quick Issue Modal */}
      <QuickIssueModal
        isOpen={Boolean(activeIssueItem)}
        item={activeIssueItem}
        onClose={() => setActiveIssueItem(null)}
        onIssueSuccess={() => fetchSummary(false)}
      />
    </div>
  );
}

export default InventoryDashboardPage;
