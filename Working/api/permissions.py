from rest_framework import permissions

class IsAppUser(permissions.BasePermission):
    """Xác thực AppUser cơ bản."""
    def has_permission(self, request, view):
        return bool(request.user and hasattr(request.user, 'role'))

class IsAdminOrManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and hasattr(request.user, 'role') and
            request.user.role in ['PREMIUM', 'QUAN_LY']
        )

class IsBasicWorker(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and hasattr(request.user, 'role') and
            request.user.role == 'BASIC'
        )

class IsFinishingWorker(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and hasattr(request.user, 'role') and
            request.user.role == 'HOAN_THIEN'
        )

class IsKcsWorker(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and hasattr(request.user, 'role') and
            request.user.role == 'KCS'
        )

class IsCutWorker(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and hasattr(request.user, 'role') and
            request.user.role == 'NHA_CAT'
        )

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Object-level permission để chỉ người nhập hoặc quản lý mới có quyền sửa/xóa.
    """
    def has_object_permission(self, request, view, obj):
        # Admin or Manager can modify anything
        if request.user.role in ['PREMIUM', 'QUAN_LY']:
            return True
        # Original creator can modify
        if hasattr(obj, 'nguoi_nhap') and obj.nguoi_nhap == request.user:
            return True
        return False
