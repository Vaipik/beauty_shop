from django.db import models
from django.utils.translation import gettext_lazy as _
from core.product.models.base import Base
from core.user_auth.models import User
from django.contrib.auth.models import PermissionsMixin, Group, Permission


class Profile(Base, PermissionsMixin):
    """Profile model."""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_profiles"
    )
    first_name = models.CharField(verbose_name=_("First name"), max_length=255)
    last_name = models.CharField(verbose_name=_("Last name"))
    email = models.EmailField(verbose_name=_("Email address"), unique=True)
    sex = models.CharField(verbose_name=_("User gender"))
    address = models.CharField(verbose_name=_("Address"))

    # Изменение related_name для связей с группами и разрешениями
    groups = models.ManyToManyField(Group, related_name="profile_groups", blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name="profile_user_permissions", blank=True
    )

    class Meta:
        db_table = _("profiles")
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
