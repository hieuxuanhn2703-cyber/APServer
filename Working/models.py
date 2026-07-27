from django.db import models


class ProcessReport(models.Model):
    # Thông tin sản phẩm
    ma_hang = models.CharField("Mã hàng", max_length=255, null=False)
    mau = models.CharField("Màu", max_length=255, null=False)
    size = models.CharField("Cỡ", max_length=50, null=False)

    # Các công đoạn sản xuất — mặc định 0, không cho âm
    nhan_btp = models.PositiveIntegerField("Nhận BTP", default=0)
    vao_chuyen = models.PositiveIntegerField("Vào chuyền", default=0)
    giua_chuyen = models.PositiveIntegerField("Giữa chuyền", default=0)
    ra_chuyen = models.PositiveIntegerField("Ra chuyền", default=0)
    thu_hoa = models.PositiveIntegerField("Thu hóa", default=0)
    la_thanh_pham = models.PositiveIntegerField("Là thành phẩm", default=0)
    kcs = models.PositiveIntegerField("KCS", default=0)
    nhap_hoan_thien = models.PositiveIntegerField("Nhập hoàn thiện", default=0)

    # Người ghi nhận dữ liệu — liên kết tới bảng User thay vì lưu CharField tự do,
    # giúp truy vấn/lọc theo đúng người dùng chính xác và nhanh hơn nhiều so với CSV
    nguoi_nhap = models.ForeignKey(
        "AppUser",
        on_delete=models.PROTECT,   # không cho xoá user nếu vẫn còn dữ liệu do họ ghi
        related_name="process_reports",
        verbose_name="Người nhập",
    )

    # Thời gian tạo/sửa — tự động, không cần set tay như khi ghi CSV
    created_at = models.DateTimeField("Thời gian nhập", auto_now_add=True)
    updated_at = models.DateTimeField("Cập nhật lần cuối", auto_now=True)

    class Meta:
        verbose_name = "Báo cáo quy trình"
        verbose_name_plural = "Báo cáo quy trình"
        ordering = ["-created_at"]  # dòng mới nhất lên đầu, giống list_view cũ

    def __str__(self):
        return f"{self.ma_hang} - {self.mau} - {self.size} ({self.nguoi_nhap})"


class AppUser(models.Model):
    """
    Thay thế cho user.csv. Tách riêng khỏi django.contrib.auth.User
    để giữ nguyên logic đăng nhập tự viết (account/password) bạn đã có,
    chỉ đổi nơi lưu trữ từ CSV sang MySQL.
    """
    name = models.CharField("Họ tên", max_length=255)
    account = models.CharField("Tài khoản", max_length=150, unique=True)
    password = models.CharField("Mật khẩu", max_length=255)  # nên lưu dạng hash, xem lưu ý bên dưới

    class Meta:
        verbose_name = "Tài khoản người dùng"
        verbose_name_plural = "Tài khoản người dùng"

    def __str__(self):
        return f"{self.name} ({self.account})"