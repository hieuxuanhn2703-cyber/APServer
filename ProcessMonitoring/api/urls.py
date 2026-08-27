from django.urls import path, include
from .views import HealthCheckView
from .auth_views import AppUserTokenObtainView, AppUserTokenRefreshView, UserProfileView

app_name = 'api'

urlpatterns = [
    path('health/', HealthCheckView.as_view(), name='health-check'),
    path('auth/token/', AppUserTokenObtainView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', AppUserTokenRefreshView.as_view(), name='token_refresh'),
    path('auth/me/', UserProfileView.as_view(), name='user_profile'),
    
    # Inventory API
    path('inventory/', include('Inventory.api.urls', namespace='inventory_api')),
    
    # Accounting API
    path('accounting/', include('Accounting.api.urls')),
]
