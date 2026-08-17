from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings
from Working.models import (
    AppUser, DefectReturnReport, SampleTakeReport, DefectReceiveLog, SampleReceiveLog, Product, ProductColor
)

class FinishingNgoaiLeTests(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Tạo Product và ProductColor cho load_config
        self.product = Product.objects.create(name="A1")
        self.color = ProductColor.objects.create(product=self.product, name="Đen", quantity=100)
        
        # Tạo user Hoàn thiện
        self.user = AppUser.objects.create(
            name="Nguyễn Văn A",
            account="hoanthien1",
            password="123",
            role="HOAN_THIEN",
            is_approved=True
        )
        
        # User không có quyền
        self.unauth_user = AppUser.objects.create(
            name="Nguyễn Văn B",
            account="chuyen1",
            password="123",
            role="TO_TRUONG",
            is_approved=True
        )

    def _login(self, user):
        session = self.client.session
        session["user_id"] = user.id
        session["display_name"] = user.name
        session.save()
        self.client.cookies[settings.SESSION_COOKIE_NAME] = session.session_key

    def test_permission_denied_for_unauthorized_role(self):
        self._login(self.unauth_user)
        response = self.client.get(reverse("finishing_ngoai_le"))
        self.assertEqual(response.status_code, 403)

    def test_create_defect_return_report_and_partial_receives(self):
        self._login(self.user)
        
        # 1. Tạo phiếu trả hàng lỗi
        response = self.client.post(reverse("finishing_ngoai_le"), {
            "action": "tra_loi",
            "ngay_tra": "2026-08-17",
            "ma_hang": "A1",
            "mau": "Đen",
            "xuong": 1,
            "to": 2,
            "so_luong_tra": 10
        })
        self.assertEqual(response.status_code, 302)
        
        report = DefectReturnReport.objects.first()
        self.assertIsNotNone(report)
        self.assertEqual(report.so_luong_tra, 10)
        self.assertEqual(report.so_luong_nhan_lai, 0)
        self.assertEqual(report.so_luong_treo, 10)
        
        # 2. Nhận lại đợt 1: 4 chiếc
        response = self.client.post(reverse("defect_receive_back", args=[report.id]), {
            "so_luong_nhan_lai": 4,
            "ngay_nhan": "2026-08-17",
            "ghi_chu": "Đợt 1 nhận 4 cái"
        })
        self.assertEqual(response.status_code, 302)
        
        report.refresh_from_db()
        self.assertEqual(report.so_luong_nhan_lai, 4)
        self.assertEqual(report.so_luong_treo, 6)
        self.assertEqual(report.receive_logs.count(), 1)
        
        log1 = report.receive_logs.first()
        self.assertEqual(log1.so_luong, 4)
        self.assertEqual(log1.ghi_chu, "Đợt 1 nhận 4 cái")
        
        # Kiểm tra phiếu vẫn xuất hiện trong danh sách treo
        response = self.client.get(reverse("finishing_ngoai_le"))
        self.assertIn(report, response.context["defect_list"])
        
        # 3. Nhận vượt quá số lượng còn lại (nhập 20 cái khi chỉ còn thiếu 6 cái)
        # Hệ thống phải tự động giới hạn ở mức 6 cái (không nhận lố)
        response = self.client.post(reverse("defect_receive_back", args=[report.id]), {
            "so_luong_nhan_lai": 20,
            "ngay_nhan": "2026-08-18",
            "ghi_chu": "Nhận hết phần còn lại"
        })
        self.assertEqual(response.status_code, 302)
        
        report.refresh_from_db()
        self.assertEqual(report.so_luong_nhan_lai, 10)
        self.assertEqual(report.so_luong_treo, 0)
        self.assertEqual(report.receive_logs.count(), 2)
        
        # Phiếu KHÔNG CÒN xuất hiện trong danh sách treo
        response = self.client.get(reverse("finishing_ngoai_le"))
        self.assertNotIn(report, response.context["defect_list"])

    def test_sample_take_report_standard_and_custom(self):
        self._login(self.user)
        
        # 1. Phiếu lấy mẫu với lựa chọn sẵn "KCS"
        response = self.client.post(reverse("finishing_ngoai_le"), {
            "action": "lay_mau",
            "ngay_lay": "2026-08-17",
            "ma_hang": "A1",
            "mau": "Đen",
            "nguoi_lay_choice": "KCS",
            "so_luong_lay": 5
        })
        self.assertEqual(response.status_code, 302)
        
        report_kcs = SampleTakeReport.objects.filter(nguoi_lay="KCS").first()
        self.assertIsNotNone(report_kcs)
        self.assertEqual(report_kcs.so_luong_lay, 5)
        
        # 2. Phiếu lấy mẫu với "Khác" -> "Phòng Giám định"
        response = self.client.post(reverse("finishing_ngoai_le"), {
            "action": "lay_mau",
            "ngay_lay": "2026-08-17",
            "ma_hang": "A1",
            "mau": "Đen",
            "nguoi_lay_choice": "Khác",
            "nguoi_lay_khac": "Phòng Giám định",
            "so_luong_lay": 2
        })
        self.assertEqual(response.status_code, 302)
        
        report_custom = SampleTakeReport.objects.filter(nguoi_lay="Phòng Giám định").first()
        self.assertIsNotNone(report_custom)
        self.assertEqual(report_custom.so_luong_lay, 2)
        
        # 3. Thử nghiệm form lỗi: Chọn "Khác" nhưng bỏ trống tên
        response = self.client.post(reverse("finishing_ngoai_le"), {
            "action": "lay_mau",
            "ngay_lay": "2026-08-17",
            "ma_hang": "A1",
            "mau": "Đen",
            "nguoi_lay_choice": "Khác",
            "nguoi_lay_khac": "",
            "so_luong_lay": 2
        })
        self.assertEqual(response.status_code, 200) # Form render lại với lỗi
        self.assertTrue(response.context["sample_form"].errors)
        self.assertIn("nguoi_lay_khac", response.context["sample_form"].errors)
