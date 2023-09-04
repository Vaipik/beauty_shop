from django.dispatch import receiver
from djoser.signals import user_registered
from core.user_profile.models import Profile


@receiver(user_registered, dispatch_uid="create_profile")
def create_profile(sender, user, request, **kwargs):
    """We create a user profile after registration."""
    data = request.data

    Profile.objects.create(
        user=user,
        first_name=data.get("first_name", ""),
        last_name=data.get("last_name", ""),
        email=data.get("email", ""),
    )
