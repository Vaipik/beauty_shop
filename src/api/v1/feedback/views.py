import typing

from django.contrib.auth import get_user_model
from rest_framework import viewsets

from api.base.permissions import AdminPermission
from core.feedback.models import Feedback
from .permissions import LeaveFeedbackPermission
from .serializers import FeedbackSerializer

if typing.TYPE_CHECKING:
    from core.user_auth.models import User

User: User = get_user_model()


class FeedbackViewset(viewsets.ModelViewSet):
    """Endpoints for leaving feedbacks."""

    http_method_names = ["get", "patch", "post", "delete"]
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

    def get_permissions(self):  # noqa D102
        if self.action in {"list", "destroy"}:
            permission_classes = [AdminPermission]
        else:  # post(create) & patch(partial_update):
            permission_classes = [LeaveFeedbackPermission]
        return [permission() for permission in permission_classes]
