from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.models import PermissionsMixin, Group, Permission

from core.product.models.base import Base

from . import constants

User = get_user_model()


class Profile(Base, PermissionsMixin):
    """Profile model."""

    class GenderChoices(models.TextChoices):
        """Human genders."""

        MALE = "M", _("Male")
        FEMALE = "F", _("Female")
        UNKNOWN = "U", _("U")

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_profile"
    )
    first_name = models.CharField(
        verbose_name=_("First name"),
        max_length=constants.USER_FIRST_NAME_MAX_LENGTH,
    )
    last_name = models.CharField(
        verbose_name=_("Last name"), max_length=constants.USER_LAST_NAME_MAX_LENGTH
    )
    email = models.EmailField(verbose_name=_("Email address"), unique=True)
    sex = models.CharField(
        verbose_name=_("Gender"),
        max_length=1,
        choices=GenderChoices.choices,
    )
    address = models.CharField(verbose_name=_("Address"))  # Maybe must be as fk.

    # Изменение related_name для связей с группами и разрешениями
    # Напевно це не є потрібним, бо ми робимо власну адмінку.
    groups = models.ManyToManyField(Group, related_name="profile_groups", blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name="profile_user_permissions", blank=True
    )

    class Meta:
        db_table = "user_profiles"
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
