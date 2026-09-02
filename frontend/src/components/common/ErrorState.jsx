import React from 'react';

export function ErrorState({ title = 'Đã có lỗi xảy ra', message, onRetry }) {
  return (
    <div className="alert alert-danger" role="alert" style={{ margin: '20px auto', maxWidth: '600px' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
        <strong>⚠️ {title}</strong>
      </div>
      {message && <p style={{ margin: '4px 0 12px 0' }}>{message}</p>}
      {onRetry && (
        <button
          type="button"
          className="btn btn-primary"
          onClick={onRetry}
          style={{ padding: '6px 12px', fontSize: '0.82rem', marginTop: '6px' }}
        >
          Thử lại
        </button>
      )}
    </div>
  );
}

export default ErrorState;
