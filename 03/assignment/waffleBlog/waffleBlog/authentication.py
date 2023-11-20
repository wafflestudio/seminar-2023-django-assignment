from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User, AnonymousUser


class CustomTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        # Perform the usual token authentication
        user, token = super().authenticate(request)

        # Check if the user is an admin
        if user and user.is_staff:
            return user, None  # Bypass token authentication for admin user

        # If the user is not an admin and token authentication failed, return None
        if not user and not token:
            return AnonymousUser()

        # If the user is not an admin and token authentication succeeded, return user and token
        return user, token
