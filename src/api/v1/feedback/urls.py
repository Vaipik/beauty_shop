from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import FeedbackViewset

feedback_router = SimpleRouter()
feedback_router.register(
    "feedbacks",
    FeedbackViewset,
    "feedbacks",
)

app_name = "feedback"

urlpatterns = [path("", include(feedback_router.urls))]
