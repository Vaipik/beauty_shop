from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import UserViewSiet

users_router = SimpleRouter()
users_router.register("users", UserViewSiet, "users")

app_name = "users"

urlpatterns = [
    path("", include(users_router.urls)),
]
