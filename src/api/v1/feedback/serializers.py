from rest_framework import serializers

from api.base.serializers import TimeStampedSerializer
from api.v1.users.serializers import UserProductFeedbackSerializer
from core.feedback.models import Feedback


class FeedbackSerializer(TimeStampedSerializer, serializers.ModelSerializer):
    """Used to create (leave) new feedback."""

    productId = serializers.UUIDField(source="product")
    userId = serializers.UUIDField(source="user", read_only=True)

    class Meta:
        model = Feedback
        exclude = ["product", "user", "created_at", "updated_at"]


class FeedbackProductSerializer(TimeStampedSerializer, serializers.ModelSerializer):
    """Used in product schema to present a feedbacks."""

    user = UserProductFeedbackSerializer()

    class Meta:
        model = Feedback
        fields = ["user", "created_at", "updated_at", "rating", "description"]
