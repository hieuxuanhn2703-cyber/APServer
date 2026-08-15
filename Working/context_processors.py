from .auth_utils import get_current_user

def auth_context(request):
    user = get_current_user(request)
    if not user:
        return {
            'app_user': None,
            'user': None,
            'is_premium': False,
            'is_manager': False,
        }
    return {
        'app_user': user,
        'user': user,
        'is_premium': user.role == 'PREMIUM',
        'is_manager': user.role in ['QUAN_LY', 'PREMIUM'],
    }
