import React from 'react';

function formatNumber(val) {
  if (val === null || val === undefined) return '-';
  const num = Number(val);
  if (isNaN(num)) return '-';
  return num.toLocaleString('vi-VN');
}

export function OrderTrackingTable({ data = [], isLoading = false }) {
  if (isLoading) {
    return (
      <div className="prod-loading-state">
        <div className="prod-spinner"></div>
        <p>Đang tải dữ liệu tiến độ đơn hàng...</p>
      </div>
    );
  }

  if (!data || data.length === 0) {
    return (
      <div className="prod-empty-state">
        <span className="prod-empty-icon">📦</span>
        <h4>Không có dữ liệu tiến độ</h4>
        <p>Không tìm thấy đơn hàng nào phù hợp với bộ lọc hiện tại.</p>
      </div>
    );
  }

  // Calculate totals across all rows
  const totals = data.reduce(
    (acc, row) => {
      const getStage = (key, legacyLam, legacyCon) => ({
        lam: row[key]?.lam ?? row[legacyLam] ?? 0,
        con: row[key]?.con ?? row[legacyCon] ?? 0,
      });

      const sNhanBtp = getStage('nhan_btp', 'nhan_btp_nhap', 'nhan_btp_con');
      const sVaoChuyen = getStage('vao_chuyen', 'vao_chuyen_vao', 'vao_chuyen_con');
      const sGiuaChuyen = getStage('giua_chuyen', 'giua_chuyen_ra', 'giua_chuyen_con');
      const sRaChuyen = getStage('ra_chuyen', 'ra_chuyen_ra', 'ra_chuyen_con');
      const sThuHoa = getStage('thu_hoa', 'thu_hoa_thu', 'thu_hoa_con');
      const sLaTP = getStage('la_thanh_pham', 'la_thanh_pham_lam', 'la_thanh_pham_con');
      const sNhapHT = getStage('nhap_hoan_thien', 'nhap_hoan_thien_nhap', 'nhap_hoan_thien_con');

      acc.so_luong += Number(row.so_luong) || 0;
      acc.nhan_btp.lam += sNhanBtp.lam;
      acc.nhan_btp.con += sNhanBtp.con;
      acc.vao_chuyen.lam += sVaoChuyen.lam;
      acc.vao_chuyen.con += sVaoChuyen.con;
      acc.giua_chuyen.lam += sGiuaChuyen.lam;
      acc.giua_chuyen.con += sGiuaChuyen.con;
      acc.ra_chuyen.lam += sRaChuyen.lam;
      acc.ra_chuyen.con += sRaChuyen.con;
      acc.thu_hoa.lam += sThuHoa.lam;
      acc.thu_hoa.con += sThuHoa.con;
      acc.la_thanh_pham.lam += sLaTP.lam;
      acc.la_thanh_pham.con += sLaTP.con;
      acc.nhap_hoan_thien.lam += sNhapHT.lam;
      acc.nhap_hoan_thien.con += sNhapHT.con;
      return acc;
    },
    {
      so_luong: 0,
      nhan_btp: { lam: 0, con: 0 },
      vao_chuyen: { lam: 0, con: 0 },
      giua_chuyen: { lam: 0, con: 0 },
      ra_chuyen: { lam: 0, con: 0 },
      thu_hoa: { lam: 0, con: 0 },
      la_thanh_pham: { lam: 0, con: 0 },
      nhap_hoan_thien: { lam: 0, con: 0 },
    }
  );

  return (
    <div className="prod-table-wrapper">
      <table className="prod-table tracking-table">
        <thead>
          <tr>
            <th rowSpan="2" className="col-freeze col-ma-hang">
              Mã hàng
            </th>
            <th rowSpan="2" className="col-freeze col-mau">
              Màu
            </th>
            <th rowSpan="2" className="col-numeric col-so-luong">
              Số lượng ĐH
            </th>
            <th colSpan="2" className="stage-header">
              Nhận BTP
            </th>
            <th colSpan="2" className="stage-header">
              Vào Chuyền
            </th>
            <th colSpan="2" className="stage-header">
              Giữa chuyền
            </th>
            <th colSpan="2" className="stage-header">
              Ra Chuyền
            </th>
            <th colSpan="2" className="stage-header">
              Thu Hoá
            </th>
            <th colSpan="2" className="stage-header">
              Là thành phẩm
            </th>
            <th colSpan="2" className="stage-header">
              Nhập Hoàn Thiện
            </th>
          </tr>
          <tr>
            <th className="th-sub-head">Đã Nhập</th>
            <th className="th-sub-head">Còn lại</th>
            <th className="th-sub-head">Đã Vào</th>
            <th className="th-sub-head">Còn lại</th>
            <th className="th-sub-head">Đã Ra</th>
            <th className="th-sub-head">Còn Lại</th>
            <th className="th-sub-head">Đã Ra</th>
            <th className="th-sub-head">Còn Lại</th>
            <th className="th-sub-head">Đã Thu</th>
            <th className="th-sub-head">Còn lại</th>
            <th className="th-sub-head">Đã Làm</th>
            <th className="th-sub-head">Còn lại</th>
            <th className="th-sub-head">Đã Nhập</th>
            <th className="th-sub-head">Còn lại</th>
          </tr>
        </thead>
        <tbody>
          {data.map((row, idx) => {
            const nhanBtpLam = row.nhan_btp?.lam ?? row.nhan_btp_nhap ?? 0;
            const nhanBtpCon = row.nhan_btp?.con ?? row.nhan_btp_con ?? 0;

            const vaoChuyenLam = row.vao_chuyen?.lam ?? row.vao_chuyen_vao ?? 0;
            const vaoChuyenCon = row.vao_chuyen?.con ?? row.vao_chuyen_con ?? 0;

            const giuaChuyenLam = row.giua_chuyen?.lam ?? row.giua_chuyen_ra ?? 0;
            const giuaChuyenCon = row.giua_chuyen?.con ?? row.giua_chuyen_con ?? 0;

            const raChuyenLam = row.ra_chuyen?.lam ?? row.ra_chuyen_ra ?? 0;
            const raChuyenCon = row.ra_chuyen?.con ?? row.ra_chuyen_con ?? 0;

            const thuHoaLam = row.thu_hoa?.lam ?? row.thu_hoa_thu ?? 0;
            const thuHoaCon = row.thu_hoa?.con ?? row.thu_hoa_con ?? 0;

            const laTPLam = row.la_thanh_pham?.lam ?? row.la_thanh_pham_lam ?? 0;
            const laTPCon = row.la_thanh_pham?.con ?? row.la_thanh_pham_con ?? 0;

            const nhapHTLam = row.nhap_hoan_thien?.lam ?? row.nhap_hoan_thien_nhap ?? 0;
            const nhapHTCon = row.nhap_hoan_thien?.con ?? row.nhap_hoan_thien_con ?? 0;

            return (
              <tr key={`${row.ma_hang}-${row.mau}-${idx}`}>
                <td className="col-freeze col-ma-hang font-medium">{row.ma_hang}</td>
                <td className="col-freeze col-mau">{row.mau}</td>
                <td className="col-numeric col-so-luong font-semibold">{formatNumber(row.so_luong)}</td>

                {/* Nhận BTP */}
                <td className="col-numeric">{formatNumber(nhanBtpLam)}</td>
                <td className={`col-numeric ${nhanBtpCon < 0 ? 'con-lai-am' : ''}`}>
                  {formatNumber(nhanBtpCon)}
                </td>

                {/* Vào Chuyền */}
                <td className="col-numeric">{formatNumber(vaoChuyenLam)}</td>
                <td className={`col-numeric ${vaoChuyenCon < 0 ? 'con-lai-am' : ''}`}>
                  {formatNumber(vaoChuyenCon)}
                </td>

                {/* Giữa Chuyền */}
                <td className="col-numeric">{formatNumber(giuaChuyenLam)}</td>
                <td className={`col-numeric ${giuaChuyenCon < 0 ? 'con-lai-am' : ''}`}>
                  {formatNumber(giuaChuyenCon)}
                </td>

                {/* Ra Chuyền */}
                <td className="col-numeric">{formatNumber(raChuyenLam)}</td>
                <td className={`col-numeric ${raChuyenCon < 0 ? 'con-lai-am' : ''}`}>
                  {formatNumber(raChuyenCon)}
                </td>

                {/* Thu Hoá */}
                <td className="col-numeric">{formatNumber(thuHoaLam)}</td>
                <td className={`col-numeric ${thuHoaCon < 0 ? 'con-lai-am' : ''}`}>
                  {formatNumber(thuHoaCon)}
                </td>

                {/* Là thành phẩm */}
                <td className="col-numeric">{formatNumber(laTPLam)}</td>
                <td className={`col-numeric ${laTPCon < 0 ? 'con-lai-am' : ''}`}>
                  {formatNumber(laTPCon)}
                </td>

                {/* Nhập Hoàn Thiện */}
                <td className="col-numeric">{formatNumber(nhapHTLam)}</td>
                <td className={`col-numeric ${nhapHTCon < 0 ? 'con-lai-am' : ''}`}>
                  {formatNumber(nhapHTCon)}
                </td>
              </tr>
            );
          })}
        </tbody>
        <tfoot>
          <tr className="prod-total-row">
            <td colSpan="2" className="col-freeze font-bold">
              TỔNG CỘNG ({data.length} đơn hàng)
            </td>
            <td className="col-numeric font-bold">{formatNumber(totals.so_luong)}</td>

            <td className="col-numeric font-bold">{formatNumber(totals.nhan_btp.lam)}</td>
            <td className={`col-numeric font-bold ${totals.nhan_btp.con < 0 ? 'con-lai-am' : ''}`}>
              {formatNumber(totals.nhan_btp.con)}
            </td>

            <td className="col-numeric font-bold">{formatNumber(totals.vao_chuyen.lam)}</td>
            <td className={`col-numeric font-bold ${totals.vao_chuyen.con < 0 ? 'con-lai-am' : ''}`}>
              {formatNumber(totals.vao_chuyen.con)}
            </td>

            <td className="col-numeric font-bold">{formatNumber(totals.giua_chuyen.lam)}</td>
            <td className={`col-numeric font-bold ${totals.giua_chuyen.con < 0 ? 'con-lai-am' : ''}`}>
              {formatNumber(totals.giua_chuyen.con)}
            </td>

            <td className="col-numeric font-bold">{formatNumber(totals.ra_chuyen.lam)}</td>
            <td className={`col-numeric font-bold ${totals.ra_chuyen.con < 0 ? 'con-lai-am' : ''}`}>
              {formatNumber(totals.ra_chuyen.con)}
            </td>

            <td className="col-numeric font-bold">{formatNumber(totals.thu_hoa.lam)}</td>
            <td className={`col-numeric font-bold ${totals.thu_hoa.con < 0 ? 'con-lai-am' : ''}`}>
              {formatNumber(totals.thu_hoa.con)}
            </td>

            <td className="col-numeric font-bold">{formatNumber(totals.la_thanh_pham.lam)}</td>
            <td className={`col-numeric font-bold ${totals.la_thanh_pham.con < 0 ? 'con-lai-am' : ''}`}>
              {formatNumber(totals.la_thanh_pham.con)}
            </td>

            <td className="col-numeric font-bold">{formatNumber(totals.nhap_hoan_thien.lam)}</td>
            <td className={`col-numeric font-bold ${totals.nhap_hoan_thien.con < 0 ? 'con-lai-am' : ''}`}>
              {formatNumber(totals.nhap_hoan_thien.con)}
            </td>
          </tr>
        </tfoot>
      </table>
    </div>
  );
}

export default OrderTrackingTable;
