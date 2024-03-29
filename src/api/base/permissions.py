import typing

from django.contrib.auth import get_user_model
from rest_framework import permissions

if typing.TYPE_CHECKING:
    from core.user_auth.models import User

User: User = get_user_model()


class AdminPermission(permissions.BasePermission):
    """Permission for admin user role."""

    def has_permission(self, request, view):
        """Verify that request user has an admin role."""
        user: User = request.user
        if user.role == User.UserRoles.ADMIN:
            return True


class OwnerPermission(permissions.BasePermission):
    """Object-level permission to only allow owners of an object to edit it."""

    def has_object_permission(self, request, view, obj):
        """Check that user are the owner."""
        return obj.pk == request.user.pk


class StaffPermission(permissions.BasePermission):
    """Permission class to control access for staff members."""

    def has_permission(self, request, view):
        """Verify that request user has an admin or manager role."""
        user: User = request.user
        if request.auth:
            return user.role in {User.UserRoles.ADMIN, User.UserRoles.MANAGER}

    def has_object_permission(self, request, view, obj):
        """Verify that request user has an admin or manager role for specific object."""
        user: User = request.user
        if request.auth:
            return user.role in {User.UserRoles.ADMIN, User.UserRoles.MANAGER}
