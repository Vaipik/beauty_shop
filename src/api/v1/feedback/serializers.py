from rest_framework import serializers

from api.base.serializers import TimeStampedSerializer
from api.v1.users.serializers import UserProductFeedbackSerializer
from core.feedback.models import Feedback

from . import services


class FeedbackSerializer(TimeStampedSerializer, serializers.ModelSerializer):
    """Used to create (leave) new feedback."""

    productId = serializers.UUIDField(source="product")
    userId = serializers.UUIDField(source="user", read_only=True)

    class Meta:
        model = Feedback
        exclude = ["product", "user", "created_at", "updated_at"]

    def create(self, validated_data):  # noqa D102
        user = self.context["request"].user
        return services.create_feedback(user, **validated_data)


class FeedbackProductSerializer(TimeStampedSerializer, serializers.ModelSerializer):
    """Used in product schema to present a feedbacks."""

    user = UserProductFeedbackSerializer()

    class Meta:
        model = Feedback
        fields = ["user", "created_at", "updated_at", "rating", "description"]
