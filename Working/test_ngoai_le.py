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

    def test_quan_ly_can_monitor_and_manage_ngoai_le(self):
        quan_ly = AppUser.objects.create(
            name="Trần Quản Lý",
            account="quanly1",
            password="123",
            role="QUAN_LY",
            is_approved=True
        )
        self._login(quan_ly)

        # 1. Quản lý có thể truy cập trang ngoại lệ và chỉ thấy danh sách theo dõi, không thấy form nhập, không có nút header và không có cột thao tác
        response = self.client.get(reverse("finishing_ngoai_le"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["user"].role, "QUAN_LY")
        content = response.content.decode("utf-8")
        self.assertNotIn("Lưu Phiếu Trả Hàng Lỗi", content)
        self.assertNotIn("Lưu Phiếu Lấy Mẫu", content)
        self.assertNotIn("btn-entry-list", content)
        self.assertNotIn("Về form chính", content)
        self.assertNotIn("<th>Thao Tác</th>", content)
        self.assertNotIn("btn-receive", content)
        self.assertIn("Hàng trả lỗi đang treo", content)

        # Tạo sẵn phiếu trả hàng lỗi từ role Hoàn thiện
        report = DefectReturnReport.objects.create(
            ngay_tra="2026-08-18",
            ma_hang="A1",
            mau="Đen",
            xuong=2,
            to=3,
            so_luong_tra=8,
            nguoi_nhap=self.user
        )

        # 2. Quản lý có thể nhận lại hàng
        response = self.client.post(reverse("defect_receive_back", args=[report.id]), {
            "so_luong_nhan_lai": 8,
            "ngay_nhan": "2026-08-18",
            "ghi_chu": "Quản lý nhận đủ 8 cái"
        })
        self.assertEqual(response.status_code, 302)
        report.refresh_from_db()
        self.assertEqual(report.so_luong_treo, 0)

        # 3. Quản lý xem toàn bộ lịch sử (show_all=1)
        response = self.client.get(reverse("finishing_ngoai_le") + "?show_all=1")
        self.assertEqual(response.status_code, 200)
        self.assertIn(report, response.context["defect_list"])
        self.assertTrue(response.context["show_all"])

    def test_premium_can_monitor_and_manage_ngoai_le(self):
        premium = AppUser.objects.create(
            name="Lê Admin",
            account="admin1",
            password="123",
            role="PREMIUM",
            is_approved=True
        )
        self._login(premium)

        # 1. Premium có thể truy cập trang ngoại lệ (chỉ thấy theo dõi, không thấy form nhập, nút header và cột thao tác)
        response = self.client.get(reverse("finishing_ngoai_le"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["user"].role, "PREMIUM")
        content = response.content.decode("utf-8")
        self.assertNotIn("Lưu Phiếu Trả Hàng Lỗi", content)
        self.assertNotIn("Lưu Phiếu Lấy Mẫu", content)
        self.assertNotIn("btn-entry-list", content)
        self.assertNotIn("Về form chính", content)
        self.assertNotIn("<th>Thao Tác</th>", content)
        self.assertNotIn("btn-receive", content)

        # Tạo sẵn phiếu lấy mẫu từ role Hoàn thiện
        sample = SampleTakeReport.objects.create(
            ngay_lay="2026-08-18",
            ma_hang="A1",
            mau="Đen",
            nguoi_lay="Lãnh đạo",
            so_luong_lay=3,
            nguoi_nhap=self.user
        )

        # 3. Premium nhận lại mẫu
        response = self.client.post(reverse("sample_receive_back", args=[sample.id]), {
            "so_luong_nhan_lai": 3,
            "ngay_nhan": "2026-08-18",
            "ghi_chu": "Khách trả đủ mẫu"
        })
        self.assertEqual(response.status_code, 302)
        sample.refresh_from_db()
        self.assertEqual(sample.so_luong_treo, 0)

        # 4. Dashboard finishing có context đếm số lượng đang treo
        response = self.client.get(reverse("dashboard_finishing"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("pending_defect_count", response.context)
        self.assertIn("pending_sample_count", response.context)
        self.assertIn("total_pending_ngoai_le", response.context)

    def test_active_tab_preservation_and_redirection(self):
        self._login(self.user)

        # 1. Truy cập trực tiếp tab 2 (Lấy hàng mẫu)
        response = self.client.get(reverse("finishing_ngoai_le") + "?tab=tab-lay-mau")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["active_tab"], "tab-lay-mau")

        # 2. Tạo phiếu lấy mẫu -> phải redirect kèm ?tab=tab-lay-mau
        response = self.client.post(reverse("finishing_ngoai_le"), {
            "action": "lay_mau",
            "active_tab": "tab-lay-mau",
            "ngay_lay": "2026-08-18",
            "ma_hang": "A1",
            "mau": "Đen",
            "nguoi_lay_choice": "KCS",
            "so_luong_lay": 4
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn("tab=tab-lay-mau", response.url)

        sample = SampleTakeReport.objects.first()

        # 3. Nhận lại hàng mẫu -> redirect kèm ?tab=tab-lay-mau
        response = self.client.post(reverse("sample_receive_back", args=[sample.id]), {
            "so_luong_nhan_lai": 4,
            "ngay_nhan": "2026-08-18",
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn("tab=tab-lay-mau", response.url)

        # 4. Nhận lại hàng lỗi -> redirect kèm ?tab=tab-tra-hang
        defect = DefectReturnReport.objects.create(
            ngay_tra="2026-08-18",
            ma_hang="A1",
            mau="Đen",
            xuong=1,
            to=1,
            so_luong_tra=5,
            nguoi_nhap=self.user
        )
        response = self.client.post(reverse("defect_receive_back", args=[defect.id]), {
            "so_luong_nhan_lai": 5,
            "ngay_nhan": "2026-08-18",
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn("tab=tab-tra-hang", response.url)

    def test_unauthorized_roles_cannot_access_ngoai_le(self):
        kcs_user = AppUser.objects.create(
            name="Nguyễn KCS",
            account="kcs_user",
            password="123",
            role="KCS",
            is_approved=True
        )
        self._login(kcs_user)

        response = self.client.get(reverse("finishing_ngoai_le"))
        self.assertEqual(response.status_code, 403)

        defect = DefectReturnReport.objects.create(
            ngay_tra="2026-08-18",
            ma_hang="A1",
            mau="Đen",
            xuong=1,
            to=1,
            so_luong_tra=5,
            nguoi_nhap=self.user
        )
        response = self.client.post(reverse("defect_receive_back", args=[defect.id]), {
            "so_luong_nhan_lai": 1
        })
        self.assertEqual(response.status_code, 403)

    def test_non_hoan_thien_cannot_create_reports_via_post(self):
        quan_ly = AppUser.objects.create(
            name="Quản Lý Thử",
            account="quanly_thu",
            password="123",
            role="QUAN_LY",
            is_approved=True
        )
        self._login(quan_ly)

        response = self.client.post(reverse("finishing_ngoai_le"), {
            "action": "tra_loi",
            "ngay_tra": "2026-08-18",
            "ma_hang": "A1",
            "mau": "Đen",
            "xuong": 1,
            "to": 1,
            "so_luong_tra": 5
        })
        self.assertEqual(response.status_code, 403)

    def test_safe_handling_of_invalid_receive_input(self):
        self._login(self.user)
        defect = DefectReturnReport.objects.create(
            ngay_tra="2026-08-18",
            ma_hang="A1",
            mau="Đen",
            xuong=1,
            to=1,
            so_luong_tra=5,
            nguoi_nhap=self.user
        )

        # Truyền giá trị không phải số vào so_luong_nhan_lai
        response = self.client.post(reverse("defect_receive_back", args=[defect.id]), {
            "so_luong_nhan_lai": "invalid_number_abc",
            "ngay_nhan": "invalid-date",
        })
        self.assertEqual(response.status_code, 302)
        defect.refresh_from_db()
        self.assertEqual(defect.so_luong_nhan_lai, 0)
        self.assertEqual(defect.receive_logs.count(), 0)
