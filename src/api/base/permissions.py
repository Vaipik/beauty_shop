import typing

<<<<<<< HEAD
from django.contrib.auth import get_user_model
=======
>>>>>>> e286ce8 (rewrite auth without djoser)
from rest_framework import permissions

if typing.TYPE_CHECKING:
    from core.user_auth.models import User

<<<<<<< HEAD
User: User = get_user_model()

=======
>>>>>>> e286ce8 (rewrite auth without djoser)

class AdminPermission(permissions.BasePermission):
    """Permission for admin user role."""

    def has_permission(self, request, view):
        """Verify that request user has an admin role."""
        user: User = request.user
        if user.role == User.UserRoles.ADMIN:
            return True
<<<<<<< HEAD


class OwnerPermission(permissions.BasePermission):
    """Object-level permission to only allow owners of an object to edit it."""

    def has_object_permission(self, request, view, obj):
        """Check that user are the owner."""
        return obj.pk == request.user.pk
=======
>>>>>>> e286ce8 (rewrite auth without djoser)
