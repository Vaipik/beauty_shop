from rest_framework import viewsets, permissions

from api.base.permissions import AdminPermission
from .serializers import UserSerializer, UserCreateSerializer


class UserViewSiet(viewsets.ModelViewSet):
    """Basic viewset for user operations."""

    def get_permissions(self):
        """To use a custom permissions."""
        if self.action == "list":
            permission_classes = [AdminPermission]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):  # noqa D102
        if self.action == "list":
            return UserSerializer
        return UserCreateSerializer
