from django.contrib import admin
from core.user_auth.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = (
        "username",
        "email",
        "phone",
        "created_at",
        "is_active",
        "is_staff",
        "is_superuser",
    )
