from django.contrib import admin
from core.user_profile.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ("user", "first_name", "last_name", "email", "sex", "address")
