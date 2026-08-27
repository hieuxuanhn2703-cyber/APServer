from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from Working.auth_utils import verify_credentials
from ProcessMonitoring.api.permissions import IsAuthenticatedAppUser

def get_tokens_for_user(user):
    refresh = RefreshToken()
    refresh['user_id'] = user.id
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class AppUserTokenObtainView(APIView):
    """
    Takes a set of user credentials (account and password) and returns an access and refresh JWT token
    to prove the authentication of those credentials.
    """
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        account = request.data.get('account')
        password = request.data.get('password')
        
        if not account or not password:
            return Response({"error": "Vui lòng cung cấp tài khoản và mật khẩu."}, status=status.HTTP_400_BAD_REQUEST)
            
        user = verify_credentials(account, password)
        if user:
            if not user.is_approved:
                return Response({"error": "Tài khoản chưa được duyệt."}, status=status.HTTP_403_FORBIDDEN)
            tokens = get_tokens_for_user(user)
            return Response(tokens, status=status.HTTP_200_OK)
            
        return Response({"error": "Tài khoản hoặc mật khẩu không đúng."}, status=status.HTTP_401_UNAUTHORIZED)

class AppUserTokenRefreshView(TokenRefreshView):
    """
    Takes a refresh type JSON web token and returns an access type JSON web
    token if the refresh token is valid.
    """
    pass

class UserProfileView(APIView):
    """
    Returns the authenticated user's profile information.
    """
    permission_classes = [IsAuthenticatedAppUser]
    
    def get(self, request, *args, **kwargs):
        user = request.user
        return Response({
            "id": user.id,
            "account": user.account,
            "name": user.name,
            "role": user.role,
        })
