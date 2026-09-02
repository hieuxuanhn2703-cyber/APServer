import React from 'react';

export function LoadingSpinner({ message = 'Đang tải dữ liệu...' }) {
  return (
    <div className="spinner-wrap" role="status" aria-live="polite">
      <div className="spinner"></div>
      <p>{message}</p>
    </div>
  );
}

export default LoadingSpinner;
