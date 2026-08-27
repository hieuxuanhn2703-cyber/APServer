from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsInventoryViewer(BasePermission):
    """
    Allows reading if the user is KHO, PREMIUM, QUAN_LY, or KE_TOAN.
    Allows creation (POST) for these roles as well.
    """
    def has_permission(self, request, view):
        if not bool(request.user and hasattr(request.user, 'role')):
            return False
        return request.user.role in ["KHO", "PREMIUM", "QUAN_LY", "KE_TOAN"]

class IsInventoryManager(BasePermission):
    """
    Allows update/delete only if the user is PREMIUM or QUAN_LY.
    """
    def has_permission(self, request, view):
        if not bool(request.user and hasattr(request.user, 'role')):
            return False
        return request.user.role in ["PREMIUM", "QUAN_LY"]

class InventoryAccessPolicy(BasePermission):
    """
    Combines Viewer and Manager rules for ViewSets:
    - GET, POST: requires IsInventoryViewer
    - PUT, PATCH, DELETE: requires IsInventoryManager
    """
    def has_permission(self, request, view):
        if not bool(request.user and hasattr(request.user, 'role')):
            return False
            
        role = request.user.role
        if request.method in SAFE_METHODS or request.method == 'POST':
            return role in ["KHO", "PREMIUM", "QUAN_LY", "KE_TOAN"]
        elif request.method in ['PUT', 'PATCH', 'DELETE']:
            return role in ["PREMIUM", "QUAN_LY"]
            
        return False
