from django.shortcuts import redirect
from django.urls import reverse, NoReverseMatch
from .models import AppUser
from .auth_utils import SESSION_KEY

class LoginRequiredMiddleware:
    """
    Middleware đảm bảo tất cả các trang yêu cầu đăng nhập.
    Nếu người dùng chưa đăng nhập (hoặc tài khoản không hợp lệ / chưa duyệt),
    tự động chuyển hướng về trang login.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        
        # Danh sách các đường dẫn công khai không yêu cầu đăng nhập
        try:
            public_paths = [
                reverse("login"),
                reverse("register"),
                reverse("logout"),
            ]
        except NoReverseMatch:
            public_paths = ["/login/", "/register/", "/logout/"]
        
        # Cho phép các file tĩnh (static) và các đường dẫn công khai
        if path.startswith("/static/") or path in public_paths:
            return self.get_response(request)
            
        user_id = request.session.get(SESSION_KEY)
        if not user_id:
            return redirect("login")
            
        try:
            user = AppUser.objects.get(pk=user_id)
            if not user.is_approved:
                request.session.flush()
                return redirect("login")
            request.app_user = user
        except AppUser.DoesNotExist:
            request.session.flush()
            return redirect("login")

        return self.get_response(request)
