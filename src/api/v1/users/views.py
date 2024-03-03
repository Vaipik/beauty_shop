import typing

from django.contrib.auth import get_user_model
from rest_framework import permissions, viewsets
from rest_framework.decorators import action

from api.base.permissions import AdminPermission, OwnerPermission

from .serializers import UserCreateSerializer, UserProfileSerializer, UserSerializer

if typing.TYPE_CHECKING:
    from core.user_auth.models import User

User: User = get_user_model()


# noinspection PyTestUnpassedFixture
class UserViewSiet(viewsets.ModelViewSet):
    """Basic viewset for user operations."""

    http_method_names = ["get", "post", "patch", "delete"]

    def get_permissions(self):
        """To use a custom permissions."""
        if self.action in {"list", "retrieve", "partial_update", "destroy"}:
            permission_classes = [AdminPermission]
        elif self.action == "me":
            permission_classes = [OwnerPermission]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def get_queryset(self):  # noqa D102
        if getattr(self, "swagger_fake_view", False):  # drf-yasg comp
            return User.objects.none()
        if self.action == "list":
            return User.objects.all()
        if self.action == "me":
            return User.objects.prefetch_related("orders").filter(pk=self.kwargs["pk"])
        return super().get_queryset()

    def get_serializer_class(self):  # noqa D102
        if self.action in {"list", "retrieve", "partial_update", "delete"}:
            return UserSerializer
        if self.action == "create":
            return UserCreateSerializer
        if self.action == "me":
            return UserProfileSerializer
        return super().get_serializer_class()

    @action(["get", "patch"], detail=False)
    def me(self, request, *args, **kwargs):
        """Endpoint that provide full information about user.

        User are able to change only data.
        """
        self.kwargs["pk"] = self.request.user.id
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)
        if request.method == "PATCH":
            return self.partial_update(request, *args, **kwargs)
