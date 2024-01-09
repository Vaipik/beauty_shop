import typing

from rest_framework import permissions

if typing.TYPE_CHECKING:
    from core.user_auth.models import User


class AdminPermission(permissions.BasePermission):
    """Permission for admin user role."""

    def has_permission(self, request, view):
        """Verify that request user has an admin role."""
        user: User = request.user
        if user.role == User.UserRoles.ADMIN:
            return True
