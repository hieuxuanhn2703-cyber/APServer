from rest_framework.permissions import BasePermission

class IsAuthenticatedAppUser(BasePermission):
    """
    Allows access only to authenticated AppUser users.
    """
    def has_permission(self, request, view):
        return bool(request.user and hasattr(request.user, 'is_approved') and request.user.is_approved)

def HasRole(allowed_roles):
    """
    Factory function to create a permission class that checks for specific roles.
    Example: HasRole(["PREMIUM", "QUAN_LY"])
    """
    class HasRolePermission(BasePermission):
        def has_permission(self, request, view):
            if not bool(request.user and hasattr(request.user, 'role')):
                return False
            return request.user.role in allowed_roles
            
    return HasRolePermission
