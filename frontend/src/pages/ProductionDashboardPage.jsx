import React, { useState, useEffect, useCallback } from 'react';
import { useSearchParams } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { useRoles } from '../hooks/useRoles';
import Unauthorized from '../components/common/Unauthorized';

import {
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
} from '../api/working';

import ProductionDashboardHeader from '../components/production/ProductionDashboardHeader';
import ProductionDashboardNav, { PRODUCTION_TABS } from '../components/production/ProductionDashboardNav';
import ProductionFilterBar from '../components/production/ProductionFilterBar';
import OrderTrackingTable from '../components/production/OrderTrackingTable';
import StageSummaryCards from '../components/production/StageSummaryCards';
import ProductionActivityTable from '../components/production/ProductionActivityTable';

import './ProductionDashboard.css';

export function ProductionDashboardPage() {
  const { user } = useAuth();
  const { hasAnyRole } = useRoles();
  const [searchParams, setSearchParams] = useSearchParams();

  // Role authorization check: PREMIUM, QUAN_LY, KE_TOAN
  const isAuthorized = hasAnyRole(['PREMIUM', 'QUAN_LY', 'KE_TOAN']);

  // URL state
  const activeTab = searchParams.get('tab') || 'tracking';
  const selectedMaHang = searchParams.get('ma_hang') || '';
  const selectedMau = searchParams.get('mau') || '';
  const startDate = searchParams.get('start_date') || '';
  const endDate = searchParams.get('end_date') || '';
  const currentPage = parseInt(searchParams.get('page') || '1', 10);

  // Component State
  const [productsList, setProductsList] = useState([]);
  const [trackingData, setTrackingData] = useState([]);
  const [summaryData, setSummaryData] = useState([]);
  const [activityData, setActivityData] = useState([]);
  const [activityTotalCount, setActivityTotalCount] = useState(0);

  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  // Sync state helpers
  const updateQueryParam = useCallback(
    (key, value) => {
      setSearchParams((prev) => {
        const next = new URLSearchParams(prev);
        if (value) {
          next.set(key, value);
        } else {
          next.delete(key);
        }
        if (key !== 'page') {
          next.delete('page'); // Reset page when filters change
        }
        return next;
      });
    },
    [setSearchParams]
  );

  const handleTabChange = (newTab) => {
    setSearchParams((prev) => {
      const next = new URLSearchParams(prev);
      next.set('tab', newTab);
      next.delete('page');
      return next;
    });
  };

  const handleResetFilters = () => {
    setSearchParams((prev) => {
      const next = new URLSearchParams();
      const currentTab = prev.get('tab');
      if (currentTab) next.set('tab', currentTab);
      return next;
    });
  };

  // Load product catalog for filters
  useEffect(() => {
    if (!isAuthorized) return;
    let isMounted = true;

    async function loadCatalog() {
      try {
        const products = await getProductsConfig();
        if (isMounted && Array.isArray(products)) {
          setProductsList(products);
        }
      } catch {
        // Fallback: options will still work from manual inputs
      }
    }

    loadCatalog();
    return () => {
      isMounted = false;
    };
  }, [isAuthorized]);

  // Main Data Fetcher
  const fetchData = useCallback(
    async (showLoading = true) => {
      if (!isAuthorized) return;

      if (showLoading) setIsLoading(true);
      setError(null);

      try {
        const filterPayload = {};
        if (selectedMaHang) filterPayload.ma_hang = selectedMaHang;
        if (selectedMau) filterPayload.mau = selectedMau;
        if (startDate) filterPayload.start_date = startDate;
        if (endDate) filterPayload.end_date = endDate;

        if (activeTab === 'tracking') {
          // Fetch Order Tracking Matrix
          const data = await getTrackingDashboard({
            ma_hang: selectedMaHang,
            mau: selectedMau,
          });
          setTrackingData(Array.isArray(data) ? data : []);
        } else {
          // Stage tabs: Cut, Process, KCS, Finishing
          let summaryPromise;
          let activityPromise;

          const reportParams = {
            ...filterPayload,
            page: currentPage,
          };

          if (activeTab === 'cut') {
            summaryPromise = getCutDashboard(filterPayload);
            activityPromise = getCutReports(reportParams);
          } else if (activeTab === 'process') {
            summaryPromise = getProcessDashboard(filterPayload);
            activityPromise = getProcessReports(reportParams);
          } else if (activeTab === 'kcs') {
            summaryPromise = getKcsDashboard(filterPayload);
            activityPromise = getKcsReports(reportParams);
          } else if (activeTab === 'finishing') {
            summaryPromise = getFinishingDashboard(filterPayload);
            activityPromise = getFinishingReports(reportParams);
          }

          const [summaryRes, activityRes] = await Promise.all([
            summaryPromise,
            activityPromise,
          ]);

          setSummaryData(Array.isArray(summaryRes) ? summaryRes : []);

          if (activityRes && activityRes.results) {
            setActivityData(activityRes.results);
            setActivityTotalCount(activityRes.count || 0);
          } else if (Array.isArray(activityRes)) {
            setActivityData(activityRes);
            setActivityTotalCount(activityRes.length);
          } else {
            setActivityData([]);
            setActivityTotalCount(0);
          }
        }
      } catch (err) {
        setError(err.message || 'Không thể tải dữ liệu báo cáo sản xuất.');
      } finally {
        setIsLoading(false);
      }
    },
    [isAuthorized, activeTab, selectedMaHang, selectedMau, startDate, endDate, currentPage]
  );

  useEffect(() => {
    fetchData(true);
  }, [fetchData]);

  // Determine export URL based on active tab and filters
  const exportUrl = React.useMemo(() => {
    const params = new URLSearchParams();
    if (selectedMaHang) {
      if (activeTab === 'tracking') params.append('tracking_filter_ma_hang', selectedMaHang);
      else params.append('ma_hang', selectedMaHang);
    }
    if (selectedMau) {
      if (activeTab === 'tracking') params.append('tracking_filter_mau', selectedMau);
      else params.append('mau', selectedMau);
    }
    if (startDate) params.append('start_date', startDate);
    if (endDate) params.append('end_date', endDate);

    const queryStr = params.toString() ? `?${params.toString()}` : '';

    if (activeTab === 'tracking') return `/tracking/export/${queryStr}`;
    if (activeTab === 'cut') return `/cut/export-excel/${queryStr}`;
    if (activeTab === 'process') return `/export-excel/${queryStr}`;
    if (activeTab === 'kcs') return `/kcs/export-excel/${queryStr}`;
    if (activeTab === 'finishing') return `/finishing/export-excel/${queryStr}`;
    return null;
  }, [activeTab, selectedMaHang, selectedMau, startDate, endDate]);

  // If role is unauthorized, render Unauthorized component
  if (!isAuthorized) {
    return <Unauthorized />;
  }

  const currentTabObj = PRODUCTION_TABS.find((t) => t.id === activeTab) || PRODUCTION_TABS[0];

  return (
    <div className="prod-page-container">
      {/* Header */}
      <ProductionDashboardHeader
        title={activeTab === 'tracking' ? 'Báo Cáo Sản Xuất — Theo Dõi Đơn Hàng' : `Báo Cáo Sản Xuất — ${currentTabObj.label}`}
        subtitle="Tiến độ chi tiết từng công đoạn theo Mã hàng & Màu sắc (Backend Authoritative)"
        onRefresh={() => fetchData(true)}
        isLoading={isLoading}
        exportUrl={exportUrl}
      />

      {/* Main Card with Navigation & Filters */}
      <div className="prod-card">
        {/* Navigation Tabs */}
        <ProductionDashboardNav
          activeTab={activeTab}
          onTabChange={handleTabChange}
        />

        {/* Filters */}
        <ProductionFilterBar
          maHang={selectedMaHang}
          setMaHang={(val) => updateQueryParam('ma_hang', val)}
          mau={selectedMau}
          setMau={(val) => updateQueryParam('mau', val)}
          startDate={startDate}
          setStartDate={(val) => updateQueryParam('start_date', val)}
          endDate={endDate}
          setEndDate={(val) => updateQueryParam('end_date', val)}
          productsList={productsList}
          showDateFilters={activeTab !== 'tracking'}
          onResetFilters={handleResetFilters}
        />

        {/* Error State */}
        {error && (
          <div className="prod-error-state">
            <span className="prod-error-icon">⚠️</span>
            <h4>Đã xảy ra lỗi khi tải dữ liệu</h4>
            <p>{error}</p>
            <button
              type="button"
              className="prod-btn prod-btn-primary"
              onClick={() => fetchData(true)}
            >
              Thử lại
            </button>
          </div>
        )}

        {/* Tab 1: Order Tracking Matrix */}
        {!error && activeTab === 'tracking' && (
          <OrderTrackingTable
            data={trackingData}
            isLoading={isLoading}
          />
        )}

        {/* Tabs 2-5: Stage Dashboards with Summary & Cumulative Activity */}
        {!error && activeTab !== 'tracking' && (
          <>
            {/* KPI Summary Cards */}
            <StageSummaryCards
              stage={activeTab}
              summaryData={summaryData}
            />

            {/* Detailed Activity Table with Running Totals */}
            <ProductionActivityTable
              stage={activeTab}
              reports={activityData}
              totalCount={activityTotalCount}
              currentPage={currentPage}
              pageSize={20}
              onPageChange={(page) => updateQueryParam('page', page)}
              isLoading={isLoading}
            />
          </>
        )}
      </div>
    </div>
  );
}

export default ProductionDashboardPage;
