/**
 * Cascading dropdown: Mã hàng -> Màu -> Cỡ
 * Yêu cầu: trang phải có sẵn:
 *   - Thẻ <script id="config-data" type="application/json">...</script> (render bằng {{ config|json_script:"config-data" }})
 *   - 3 thẻ <select id="id_ma_hang">, <select id="id_mau">, <select id="id_co">
 *     mỗi thẻ có data-initial="<giá trị cũ nếu có>"
 */
(function () {
    function initCascadeSelect() {
        const configDataEl = document.getElementById('config-data');
        const maHangSelect = document.getElementById('id_ma_hang');
        const mauSelect = document.getElementById('id_mau');
        const coSelect = document.getElementById('id_co');

        if (!configDataEl || !maHangSelect || !mauSelect || !coSelect) {
            return; // Trang không có đủ phần tử cần thiết thì bỏ qua
        }

        const configData = JSON.parse(configDataEl.textContent);

        function populateMaHang(selected) {
            maHangSelect.innerHTML = '<option value="">-- Chọn mã hàng --</option>';
            Object.keys(configData).forEach(ma => {
                const opt = document.createElement('option');
                opt.value = ma;
                opt.textContent = ma;
                if (ma === selected) opt.selected = true;
                maHangSelect.appendChild(opt);
            });
        }

        function populateMau(maHang, selected) {
            mauSelect.innerHTML = '<option value="">-- Chọn màu --</option>';
            if (!maHang || !configData[maHang]) return;
            Object.keys(configData[maHang].colors).forEach(mau => {
                const opt = document.createElement('option');
                opt.value = mau;
                opt.textContent = mau;
                if (mau === selected) opt.selected = true;
                mauSelect.appendChild(opt);
            });
        }

        function populateCo(maHang, mau, selected) {
            coSelect.innerHTML = '<option value="">-- Chọn cỡ --</option>';
            if (!maHang || !mau || !configData[maHang] || !configData[maHang].colors[mau]) return;
            configData[maHang].colors[mau].forEach(co => {
                const opt = document.createElement('option');
                opt.value = co;
                opt.textContent = co;
                if (co === selected) opt.selected = true;
                coSelect.appendChild(opt);
            });
        }

        const initMaHang = maHangSelect.dataset.initial || "";
        const initMau = mauSelect.dataset.initial || "";
        const initCo = coSelect.dataset.initial || "";

        populateMaHang(initMaHang);
        populateMau(initMaHang, initMau);
        populateCo(initMaHang, initMau, initCo);

        maHangSelect.addEventListener('change', () => {
            populateMau(maHangSelect.value, "");
            coSelect.innerHTML = '<option value="">-- Chọn cỡ --</option>';
        });

        mauSelect.addEventListener('change', () => {
            populateCo(maHangSelect.value, mauSelect.value, "");
        });
    }

    document.addEventListener('DOMContentLoaded', initCascadeSelect);
})();