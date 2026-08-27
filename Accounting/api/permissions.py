from rest_framework import permissions

class IsAccountingTeam(permissions.BasePermission):
    """
    Cho phép truy cập nếu user đã đăng nhập và có role là QUAN_LY hoặc KE_TOAN.
    """

    def has_permission(self, request, view):
        return bool(
            request.user and
            hasattr(request.user, 'role') and
            request.user.role in ['QUAN_LY', 'KE_TOAN', 'PREMIUM']
        )

class IsAppUser(permissions.BasePermission):
    """
    Xác thực AppUser.
    """
    def has_permission(self, request, view):
        return bool(request.user and hasattr(request.user, 'role'))
