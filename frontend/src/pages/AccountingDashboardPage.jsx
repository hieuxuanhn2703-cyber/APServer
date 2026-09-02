import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { useSearchParams } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { useRoles } from '../hooks/useRoles';
import { getAccountingDashboard, getProductOptions } from '../api/accounting';
import AccountingKPICards from '../components/accounting/AccountingKPICards';
import AccountingProductFilter from '../components/accounting/AccountingProductFilter';
import AccountingSummaryTable from '../components/accounting/AccountingSummaryTable';
import PaymentModal from '../components/accounting/PaymentModal';
import './AccountingDashboard.css';

export function AccountingDashboardPage() {
  const { user } = useAuth();
  const { hasAnyRole } = useRoles();
  const [searchParams, setSearchParams] = useSearchParams();

  // URL state for product filter
  const selectedMaHang = searchParams.get('ma_hang') || '';

  // Data & UI states
  const [dashboardData, setDashboardData] = useState({
    rows: [],
    kpi: {},
    payments_by_pc: {},
  });
  const [products, setProducts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [permissionDenied, setPermissionDenied] = useState(false);

  // Active row for payment modal
  const [activePaymentRow, setActivePaymentRow] = useState(null);

  // Role check: Only PREMIUM, QUAN_LY, KE_TOAN are permitted
  const isPermitted = hasAnyRole(['PREMIUM', 'QUAN_LY', 'KE_TOAN']);

  // Fetch product list for the filter (once on mount)
  useEffect(() => {
    if (!isPermitted) return;
    let isMounted = true;

    async function loadProducts() {
      try {
        const prodList = await getProductOptions();
        if (isMounted && Array.isArray(prodList)) {
          setProducts(prodList);
        }
      } catch (err) {
        // Non-blocking fallback: products will be extracted from rows if this fails
        console.warn('Could not load products list for filter:', err);
      }
    }

    loadProducts();
    return () => {
      isMounted = false;
    };
  }, [isPermitted]);

  // Main dashboard fetch function
  const fetchDashboard = useCallback(
    async (showLoading = true) => {
      if (!isPermitted) return;

      try {
        if (showLoading) setIsLoading(true);
        setError(null);
        setPermissionDenied(false);

        const data = await getAccountingDashboard(selectedMaHang);
        setDashboardData(data || { rows: [], kpi: {}, payments_by_pc: {} });

        // If active modal is open, refresh the active row with latest data
        if (activePaymentRow && data?.rows) {
          const updatedRow = data.rows.find(
            (r) => r.product_color_id === activePaymentRow.product_color_id
          );
          if (updatedRow) {
            setActivePaymentRow(updatedRow);
          }
        }
      } catch (err) {
        if (err.status === 403) {
          setPermissionDenied(true);
        } else {
          setError(err.message || 'Không thể tải dữ liệu Dashboard Kế toán.');
        }
      } finally {
        if (showLoading) setIsLoading(false);
      }
    },
    [isPermitted, selectedMaHang, activePaymentRow]
  );

  // Fetch whenever selectedMaHang changes
  useEffect(() => {
    fetchDashboard(true);
  }, [selectedMaHang, isPermitted]);

  // Handle filter selection
  const handleSelectMaHang = (maHang) => {
    if (maHang) {
      setSearchParams({ ma_hang: maHang });
    } else {
      setSearchParams({});
    }
  };

  // Derive unique product list if product config API was empty
  const filterProductOptions = useMemo(() => {
    if (products.length > 0) return products;
    const set = new Set();
    dashboardData.rows.forEach((r) => {
      if (r.ma_hang) set.add(r.ma_hang);
    });
    return Array.from(set).map((name) => ({ id: name, name }));
  }, [products, dashboardData.rows]);

  // Payments list for active modal
  const activePaymentsList = useMemo(() => {
    if (!activePaymentRow) return [];
    const pcId = activePaymentRow.product_color_id;
    return (
      dashboardData.payments_by_pc?.[pcId] ||
      dashboardData.payments_by_pc?.[String(pcId)] ||
      activePaymentRow.payments_list ||
      []
    );
  }, [activePaymentRow, dashboardData.payments_by_pc]);

  // Render Permission Denied State (403 without logging out)
  if (!isPermitted || permissionDenied) {
    return (
      <div className="accounting-page-container">
        <div className="accounting-permission-denied" role="alert">
          <h2 style={{ fontSize: '1.25rem', fontWeight: 800, marginBottom: '8px' }}>
            🚫 Quyền Truy Cập Bị Từ Chối
          </h2>
          <p style={{ fontSize: '0.92rem', lineHeight: 1.5 }}>
            Tài khoản của bạn (<b>{user?.name || user?.account}</b>, vai trò:{' '}
            <b>{user?.role}</b>) không có quyền truy cập vào phân hệ <b>Kế Toán & Doanh Thu</b>.
          </p>
          <p style={{ fontSize: '0.84rem', marginTop: '8px', color: '#b45309' }}>
            Vui lòng liên hệ Quản trị viên nếu bạn cần phân quyền vai trò <b>KE_TOAN</b>,{' '}
            <b>QUAN_LY</b> hoặc <b>PREMIUM</b>.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="accounting-page-container">
      {/* Page Header */}
      <div style={{ marginBottom: '16px' }}>
        <h1 style={{ fontSize: '1.35rem', fontWeight: 800, color: '#0f172a' }}>
          💰 Doanh Thu & Tiến Độ Xuất Hàng
        </h1>
        <p style={{ color: '#64748b', fontSize: '0.86rem', marginTop: '2px' }}>
          Theo dõi doanh số đơn hàng, sản lượng xuất kho, và thanh toán công nợ theo thời gian thực.
        </p>
      </div>

      {/* Error Banner with Retry Action */}
      {error && (
        <div className="accounting-error-banner" role="alert">
          <div className="accounting-error-text">
            <span>⚠️</span>
            <span>{error}</span>
          </div>
          <button
            type="button"
            className="btn-retry"
            onClick={() => fetchDashboard(true)}
          >
            Thử lại
          </button>
        </div>
      )}

      {/* Loading Skeleton */}
      {isLoading ? (
        <div className="accounting-loading-container" aria-live="polite">
          <div className="loading-spinner" />
          <span style={{ fontSize: '0.9rem', color: '#64748b', fontWeight: 600 }}>
            Đang tải dữ liệu Kế toán...
          </span>
        </div>
      ) : (
        <>
          {/* KPI Cards & Delivery Progress */}
          <AccountingKPICards kpi={dashboardData.kpi} />

          {/* Product Filter Bar & Actions */}
          <AccountingProductFilter
            products={filterProductOptions}
            selectedMaHang={selectedMaHang}
            onSelectMaHang={handleSelectMaHang}
          />

          {/* Detailed Summary Table & Mobile Cards */}
          <AccountingSummaryTable
            rows={dashboardData.rows}
            onOpenPayment={(row) => setActivePaymentRow(row)}
          />
        </>
      )}

      {/* Payment Creation & History Modal */}
      <PaymentModal
        isOpen={Boolean(activePaymentRow)}
        row={activePaymentRow}
        paymentsList={activePaymentsList}
        onClose={() => setActivePaymentRow(null)}
        onPaymentSuccess={() => fetchDashboard(false)}
      />
    </div>
  );
}

export default AccountingDashboardPage;
