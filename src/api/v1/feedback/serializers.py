from rest_framework import serializers

from core.feedback.models import Feedback


class FeedbackSerializer(serializers.ModelSerializer):
    """Feedback description."""

    class Meta:
        model = Feedback
        fields = "__all__"
