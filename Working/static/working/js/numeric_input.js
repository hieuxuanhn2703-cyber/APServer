/**
 * Tự động xoá giá trị "0" mặc định khi người dùng bấm/chạm vào ô nhập số,
 * giúp gõ số mới ngay mà không cần xoá thủ công.
 * Nếu người dùng rời khỏi ô mà không nhập gì, tự động trả lại giá trị 0.
 */
(function () {
    function initNumericInputs() {
        const numericInputs = document.querySelectorAll('.numeric-input');

        numericInputs.forEach(input => {
            // Khi focus vào ô: nếu đang là 0 thì xoá trắng
            input.addEventListener('focus', function () {
                if (this.value === '0') {
                    this.value = '';
                }
            });

            // Khi rời khỏi ô: nếu để trống thì trả lại về 0
            input.addEventListener('blur', function () {
                if (this.value === '') {
                    this.value = '0';
                }
            });

            // Hỗ trợ thêm cho thiết bị cảm ứng: chọn toàn bộ nội dung khi tap
            // (một số trình duyệt mobile không trigger đúng focus khi tap lần đầu)
            input.addEventListener('touchstart', function () {
                if (this.value === '0') {
                    this.value = '';
                }
            });
        });
    }

    document.addEventListener('DOMContentLoaded', initNumericInputs);
})();