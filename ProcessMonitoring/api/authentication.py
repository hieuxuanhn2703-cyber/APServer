from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import exceptions
from Working.models import AppUser

class AppUserJWTAuthentication(JWTAuthentication):
    """
    Custom JWT Authentication that authenticates against the custom AppUser model
    instead of the default Django auth.User model.
    """
    
    def get_user(self, validated_token):
        """
        Returns an active AppUser based on the payload of a validated token.
        """
        try:
            user_id = validated_token['user_id']
        except KeyError:
            raise exceptions.AuthenticationFailed('Token contained no recognizable user identification', code='token_not_valid')

        try:
            user = AppUser.objects.get(id=user_id)
        except AppUser.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found', code='user_not_found')

        if not user.is_approved:
            raise exceptions.AuthenticationFailed('User is not approved', code='user_inactive')

        return user
