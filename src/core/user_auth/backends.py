from uuid import UUID

from django.contrib.auth.backends import BaseBackend
from django.db.models import Q

from core.user_auth.models import User


class AuthBackend(BaseBackend):
    """Custom backend to perform auth using email or phone."""

    def get_user(self, user_id: UUID) -> User | None:
        """Required method for custom auth backend.

        See: https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#writing-an-authentication-backend
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def authenticate(self, request, username=None, password=None) -> User | None:
        """Required method for custom auth backend.

        See: https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#writing-an-authentication-backend
        """
        try:
            user = User.objects.get(
                Q(username=username) | Q(email=username) | Q(phone=username)
            )

        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user

        return None
