from core.user_auth.models import User
from django.db.models import Q


class AuthBackend(object):
    """Auth class."""

    supports_object_permissions = True
    supports_anonymous_user = False
    supports_inactive_user = False

    def get_user(self, id):
        """Get a user."""
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist:
            return None

    def authenticate(self, request, username, password):
        """Authenticate a user."""
        try:
            user = User.objects.get(
                Q(username=username) | Q(email=username) | Q(phone=username)
            )

        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user

        else:
            return None
