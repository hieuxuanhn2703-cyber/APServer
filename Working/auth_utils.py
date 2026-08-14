from functools import wraps
from django.shortcuts import redirect
from .models import AppUser

SESSION_KEY = "user_id"


def verify_credentials(account: str, password: str):
    """Kiểm tra tài khoản/mật khẩu trong database, trả về AppUser nếu đúng, None nếu sai."""
    try:
        return AppUser.objects.get(account=account, password=password)
    except AppUser.DoesNotExist:
        return None


def get_current_user(request):
    """Lấy AppUser đang đăng nhập từ session, trả về None nếu chưa đăng nhập/không tồn tại."""
    if hasattr(request, 'app_user') and request.app_user:
        return request.app_user
    user_id = request.session.get(SESSION_KEY)
    if not user_id:
        return None
    try:
        return AppUser.objects.get(pk=user_id)
    except AppUser.DoesNotExist:
        return None


def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user_id = request.session.get(SESSION_KEY)
        if not user_id:
            return redirect("login")
        try:
            user = AppUser.objects.get(pk=user_id)
            if not user.is_approved:
                request.session.flush()
                return redirect("login")
        except AppUser.DoesNotExist:
            request.session.flush()
            return redirect("login")
        return view_func(request, *args, **kwargs)
    return wrapper