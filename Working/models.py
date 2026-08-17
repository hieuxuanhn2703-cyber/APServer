from django.db import models
import datetime


class ProcessReport(models.Model):
    # Thông tin sản phẩm
    ngay_lam_viec = models.DateField("Ngày làm việc", default=datetime.date.today)
    xuong = models.PositiveIntegerField("Xưởng", default=0)
    to = models.PositiveIntegerField("Tổ", default=0)
    so_luong_ld = models.PositiveIntegerField("Số lượng LĐ", default=0)
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
    ROLE_CHOICES = (
        ("BASIC", "Sản xuất"),
        ("HOAN_THIEN", "Hoàn thiện"),
        ("KCS", "KCS"),
        ("NHA_CAT", "Nhà cắt"),
        ("QUAN_LY", "Quản lý"),
        ("PREMIUM", "Cao cấp (Admin)"),
    )

    name = models.CharField("Họ tên", max_length=255)
    account = models.CharField("Tài khoản", max_length=150, unique=True)
    password = models.CharField("Mật khẩu", max_length=255)  # nên lưu dạng hash, xem lưu ý bên dưới
    role = models.CharField("Quyền hạn", max_length=20, choices=ROLE_CHOICES, default="BASIC")
    is_approved = models.BooleanField("Đã duyệt", default=False)

    class Meta:
        verbose_name = "Tài khoản người dùng"
        verbose_name_plural = "Tài khoản người dùng"

    @property
    def username(self):
        return self.account

    def __str__(self):
        return f"{self.name} ({self.account})"


class FinishingReport(models.Model):
    # Thông tin sản phẩm
    ngay_lam_viec = models.DateField("Ngày làm việc", default=datetime.date.today)
    ma_hang = models.CharField("Mã hàng", max_length=255, null=False)
    mau = models.CharField("Màu", max_length=255, null=False)
    size = models.CharField("Cỡ", max_length=50, default="N/A")

    # Các công đoạn hoàn thiện — mặc định 0, không cho âm
    the_bai = models.PositiveIntegerField("Thẻ bài", default=0)
    gap_hang = models.PositiveIntegerField("Gấp hàng", default=0)
    treo_dong_thung = models.PositiveIntegerField("Treo/Đóng thùng", default=0)

    # Người ghi nhận dữ liệu
    nguoi_nhap = models.ForeignKey(
        "AppUser",
        on_delete=models.PROTECT,
        related_name="finishing_reports",
        verbose_name="Người nhập",
    )

    created_at = models.DateTimeField("Thời gian nhập", auto_now_add=True)
    updated_at = models.DateTimeField("Cập nhật lần cuối", auto_now=True)

    class Meta:
        verbose_name = "Báo cáo hoàn thiện"
        verbose_name_plural = "Báo cáo hoàn thiện"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.ma_hang} - {self.mau} ({self.nguoi_nhap})"


class KcsReport(models.Model):
    # Thông tin sản phẩm
    ngay_lam_viec = models.DateField("Ngày làm việc", default=datetime.date.today)
    xuong = models.PositiveIntegerField("Xưởng", default=0)
    to = models.PositiveIntegerField("Tổ", default=0)
    ma_hang = models.CharField("Mã hàng", max_length=255, null=False)
    mau = models.CharField("Màu", max_length=255, null=False)
    size = models.CharField("Cỡ", max_length=50, default="N/A")

    # Các công đoạn KCS
    qua_tay = models.PositiveIntegerField("Qua tay", default=0)
    dat = models.PositiveIntegerField("Đạt", default=0)
    loi = models.PositiveIntegerField("Lỗi", default=0)
    tong_dat = models.PositiveIntegerField("Tổng đạt", default=0)

    # Người ghi nhận dữ liệu
    nguoi_nhap = models.ForeignKey(
        "AppUser",
        on_delete=models.PROTECT,
        related_name="kcs_reports",
        verbose_name="Người nhập",
    )

    created_at = models.DateTimeField("Thời gian nhập", auto_now_add=True)
    updated_at = models.DateTimeField("Cập nhật lần cuối", auto_now=True)

    class Meta:
        verbose_name = "Báo cáo KCS"
        verbose_name_plural = "Báo cáo KCS"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.ma_hang} - {self.mau} ({self.nguoi_nhap})"


class Product(models.Model):
    name = models.CharField("Mã hàng", max_length=255, unique=True)

    class Meta:
        verbose_name = "Mã hàng"
        verbose_name_plural = "Mã hàng"
        ordering = ['name']

    def __str__(self):
        return self.name


class ProductColor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='colors', verbose_name="Mã hàng")
    name = models.CharField("Màu sắc", max_length=255)
    quantity = models.PositiveIntegerField("Tổng số lượng", default=0)

    class Meta:
        verbose_name = "Màu sắc"
        verbose_name_plural = "Màu sắc"
        unique_together = ('product', 'name')
        ordering = ['name']

    def __str__(self):
        return f"{self.product.name} - {self.name}"


class ProductSize(models.Model):
    color = models.ForeignKey(ProductColor, on_delete=models.CASCADE, related_name='sizes', verbose_name="Màu sắc")
    name = models.CharField("Cỡ", max_length=50)

    class Meta:
        verbose_name = "Cỡ"
        verbose_name_plural = "Cỡ"
        unique_together = ('color', 'name')
        ordering = ['name']

    def __str__(self):
        return f"{self.color.product.name} - {self.color.name} - {self.name}"


class CutReport(models.Model):
    # Thông tin sản phẩm
    ngay_lam_viec = models.DateField("Ngày làm việc", default=datetime.date.today)
    ma_hang = models.CharField("Mã hàng", max_length=255, null=False)
    mau = models.CharField("Màu", max_length=255, null=False)
    size = models.CharField("Cỡ", max_length=50, default="N/A")

    # Các công đoạn cắt
    cat_chinh = models.PositiveIntegerField("Cắt chính", default=0)
    cat_lot = models.PositiveIntegerField("Cắt lót", default=0)
    cat_mex = models.PositiveIntegerField("Cắt Mex", default=0)
    cat_bong = models.PositiveIntegerField("Cắt bông", default=0)

    # Người ghi nhận dữ liệu
    nguoi_nhap = models.ForeignKey(
        "AppUser",
        on_delete=models.PROTECT,
        related_name="cut_reports",
        verbose_name="Người nhập",
    )

    created_at = models.DateTimeField("Thời gian nhập", auto_now_add=True)
    updated_at = models.DateTimeField("Cập nhật lần cuối", auto_now=True)

    class Meta:
        verbose_name = "Báo cáo Tổ Cắt"
        verbose_name_plural = "Báo cáo Tổ Cắt"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.ma_hang} - {self.mau} ({self.nguoi_nhap})"


class DefectReturnReport(models.Model):
    # Trả hàng lỗi
    ngay_tra = models.DateField("Ngày trả", default=datetime.date.today)
    ma_hang = models.CharField("Mã hàng", max_length=255, null=False)
    mau = models.CharField("Màu", max_length=255, null=False)
    xuong = models.PositiveIntegerField("Xưởng", default=0)
    to = models.PositiveIntegerField("Tổ", default=0)
    
    so_luong_tra = models.PositiveIntegerField("Số lượng trả", default=0)
    so_luong_nhan_lai = models.PositiveIntegerField("Số lượng nhận lại", default=0)

    # Người ghi nhận dữ liệu
    nguoi_nhap = models.ForeignKey(
        "AppUser",
        on_delete=models.PROTECT,
        related_name="defect_return_reports",
        verbose_name="Người nhập",
    )

    created_at = models.DateTimeField("Thời gian nhập", auto_now_add=True)
    updated_at = models.DateTimeField("Cập nhật lần cuối", auto_now=True)

    class Meta:
        verbose_name = "Báo cáo trả hàng lỗi"
        verbose_name_plural = "Báo cáo trả hàng lỗi"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.ma_hang} - {self.mau} ({self.so_luong_tra} lỗi)"

    @property
    def so_luong_treo(self):
        return max(0, self.so_luong_tra - self.so_luong_nhan_lai)


class SampleTakeReport(models.Model):
    # Lấy hàng mẫu
    ngay_lay = models.DateField("Ngày lấy", default=datetime.date.today)
    ma_hang = models.CharField("Mã hàng", max_length=255, null=False)
    mau = models.CharField("Màu", max_length=255, null=False)
    
    # Nguoi lay co the go them, nen de la CharField (tu do nhap)
    nguoi_lay = models.CharField("Người lấy", max_length=255, default="")
    
    so_luong_lay = models.PositiveIntegerField("Số lượng lấy", default=0)
    so_luong_nhan_lai = models.PositiveIntegerField("Số lượng nhận lại", default=0)

    # Người ghi nhận dữ liệu
    nguoi_nhap = models.ForeignKey(
        "AppUser",
        on_delete=models.PROTECT,
        related_name="sample_take_reports",
        verbose_name="Người nhập",
    )

    created_at = models.DateTimeField("Thời gian nhập", auto_now_add=True)
    updated_at = models.DateTimeField("Cập nhật lần cuối", auto_now=True)

    class Meta:
        verbose_name = "Báo cáo lấy mẫu"
        verbose_name_plural = "Báo cáo lấy mẫu"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.ma_hang} - {self.mau} ({self.so_luong_lay} mẫu)"

    @property
    def so_luong_treo(self):
        return max(0, self.so_luong_lay - self.so_luong_nhan_lai)


class DefectReceiveLog(models.Model):
    # Lịch sử từng lần nhận lại hàng lỗi
    report = models.ForeignKey(
        DefectReturnReport,
        on_delete=models.CASCADE,
        related_name="receive_logs",
        verbose_name="Phiếu trả lỗi",
    )
    ngay_nhan = models.DateField("Ngày nhận lại", default=datetime.date.today)
    so_luong = models.PositiveIntegerField("Số lượng nhận lại", default=0)
    nguoi_nhap = models.ForeignKey(
        "AppUser",
        on_delete=models.PROTECT,
        related_name="defect_receive_logs",
        verbose_name="Người ghi nhận",
    )
    ghi_chu = models.CharField("Ghi chú", max_length=255, blank=True, default="")
    created_at = models.DateTimeField("Thời gian ghi nhận", auto_now_add=True)

    class Meta:
        verbose_name = "Lịch sử nhận lại hàng lỗi"
        verbose_name_plural = "Lịch sử nhận lại hàng lỗi"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Nhận {self.so_luong} chiếc ({self.report.ma_hang} - {self.report.mau}) ngày {self.ngay_nhan}"


class SampleReceiveLog(models.Model):
    # Lịch sử từng lần nhận lại hàng mẫu
    report = models.ForeignKey(
        SampleTakeReport,
        on_delete=models.CASCADE,
        related_name="receive_logs",
        verbose_name="Phiếu lấy mẫu",
    )
    ngay_nhan = models.DateField("Ngày nhận lại", default=datetime.date.today)
    so_luong = models.PositiveIntegerField("Số lượng nhận lại", default=0)
    nguoi_nhap = models.ForeignKey(
        "AppUser",
        on_delete=models.PROTECT,
        related_name="sample_receive_logs",
        verbose_name="Người ghi nhận",
    )
    ghi_chu = models.CharField("Ghi chú", max_length=255, blank=True, default="")
    created_at = models.DateTimeField("Thời gian ghi nhận", auto_now_add=True)

    class Meta:
        verbose_name = "Lịch sử nhận lại hàng mẫu"
        verbose_name_plural = "Lịch sử nhận lại hàng mẫu"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Nhận {self.so_luong} mẫu ({self.report.ma_hang} - {self.report.mau}) ngày {self.ngay_nhan}"
