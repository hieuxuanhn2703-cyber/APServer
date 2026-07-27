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
        if not request.session.get(SESSION_KEY):
            return redirect("login")
        return view_func(request, *args, **kwargs)
    return wrapper