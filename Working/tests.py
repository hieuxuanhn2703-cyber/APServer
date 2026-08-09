from django.test import TestCase, Client
from django.urls import reverse
from .models import AppUser, Product, ProductColor, ProductSize, ProcessReport

class SystemVerificationTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Tạo sẵn các tài khoản
        self.premium_user = AppUser.objects.create(account="admin_vip", password="123", name="Admin", role="PREMIUM", is_approved=True)
        self.basic_user = AppUser.objects.create(account="staff", password="123", name="Staff", role="BASIC", is_approved=True)
        self.unapproved_user = AppUser.objects.create(account="newbie", password="123", name="Newbie", role="BASIC", is_approved=False)
        
    def test_registration_success(self):
        # Đăng ký thành công
        response = self.client.post(reverse('register'), {
            'account': 'new_user',
            'name': 'New User',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        self.assertTrue(AppUser.objects.filter(account='new_user').exists())
        self.assertFalse(AppUser.objects.get(account='new_user').is_approved) # Phải là chờ duyệt

    def test_registration_password_mismatch(self):
        # 2 mật khẩu không khớp
        response = self.client.post(reverse('register'), {
            'account': 'bad_user',
            'name': 'Bad User',
            'password': 'password123',
            'confirm_password': 'password456'
        })
        self.assertFalse(AppUser.objects.filter(account='bad_user').exists())
        self.assertContains(response, "Mật khẩu nhập lại không khớp")

    def test_registration_duplicate_username(self):
        # Username trùng
        response = self.client.post(reverse('register'), {
            'account': 'staff', # Đã tồn tại
            'name': 'Fake Staff',
            'password': '123',
            'confirm_password': '123'
        })
        self.assertEqual(AppUser.objects.filter(account='staff').count(), 1)
        self.assertContains(response, "Tài khoản này đã tồn tại, vui lòng chọn tên khác.")

    def test_login_success(self):
        # Login chuẩn
        response = self.client.post(reverse('login'), {'account': 'staff', 'password': '123'})
        self.assertRedirects(response, reverse('web')) # Trả về trang nhập liệu

    def test_login_unapproved(self):
        # Login khi is_approved = False
        response = self.client.post(reverse('login'), {'account': 'newbie', 'password': '123'})
        self.assertContains(response, "Tài khoản của bạn đang chờ quản trị viên phê duyệt.")

    def test_login_wrong_password(self):
        # Sai mật khẩu
        response = self.client.post(reverse('login'), {'account': 'staff', 'password': 'wrong'})
        self.assertContains(response, "Tài khoản hoặc mật khẩu không đúng")

    def test_authorization_basic_vs_premium(self):
        # Staff (BASIC) đăng nhập
        session = self.client.session
        session['user_id'] = self.basic_user.id
        session.save()
        
        # Thử vào manage_accounts
        response = self.client.get(reverse('manage_accounts'))
        self.assertEqual(response.status_code, 403) # Bị chặn
        
        # Thử vào config_list
        response = self.client.get(reverse('config_list'))
        self.assertEqual(response.status_code, 403)
        
        # Thử xuất Excel
        response = self.client.get(reverse('export_excel'))
        self.assertEqual(response.status_code, 403)

    def test_authorization_unauthenticated(self):
        # Chưa đăng nhập
        response = self.client.get(reverse('web'))
        self.assertRedirects(response, reverse('login'))

    def test_config_add_product(self):
        session = self.client.session
        session['user_id'] = self.premium_user.id
        session.save()
        
        # Gửi form tạo Product + Colors + Sizes
        response = self.client.post(reverse('config_add_product'), {
            'name': 'AT100',
            'colors': 'Đỏ, Xanh',
            'sizes': ['M', 'L']
        })
        self.assertRedirects(response, reverse('config_list'))
        
        product = Product.objects.get(name='AT100')
        self.assertEqual(product.colors.count(), 2)
        
        color_do = product.colors.get(name='Đỏ')
        self.assertEqual(color_do.sizes.count(), 2)
        self.assertTrue(color_do.sizes.filter(name='M').exists())

    def test_config_empty_name(self):
        session = self.client.session
        session['user_id'] = self.premium_user.id
        session.save()
        
        # Cố ý gửi chuỗi rỗng
        response = self.client.post(reverse('config_add_product'), {
            'name': '   ',
            'colors': '',
        })
        # Server không được crash, redirect về list an toàn
        self.assertEqual(Product.objects.filter(name='').count(), 0)

    def test_config_cascade_delete(self):
        session = self.client.session
        session['user_id'] = self.premium_user.id
        session.save()
        
        product = Product.objects.create(name='DelMe')
        color = ProductColor.objects.create(product=product, name='Màu')
        size = ProductSize.objects.create(color=color, name='Cỡ')
        
        # Test xoá Product
        self.client.post(reverse('config_delete_product', args=[product.id]))
        
        self.assertEqual(Product.objects.count(), 0)
        self.assertEqual(ProductColor.objects.count(), 0) # Cascade xoá Màu
        self.assertEqual(ProductSize.objects.count(), 0) # Cascade xoá Cỡ
        
    def test_export_excel(self):
        session = self.client.session
        session['user_id'] = self.premium_user.id
        session.save()
        
        # Export excel request
        response = self.client.get(reverse('export_excel'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
