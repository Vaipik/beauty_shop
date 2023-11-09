from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _

from core.base.models import Base, TimeStampedBase
from core.user_auth.manager import UserManager


class User(Base, TimeStampedBase, AbstractBaseUser):
    """Extend standart user to provide extra roles."""

    class UserRoles(models.TextChoices):
        """Extra roles."""

        MANAGER = "M", _("Manager")
        CONSULTANT = "C", _("Consultant")
        CUSTOMER = "U", _("Customer")
        ADMIN = "A", _("Administrator")

    username = models.CharField(
        max_length=255,  # same as email
        unique=True,
        verbose_name=_("Email or mobile number"),
    )
    email = models.EmailField(
        max_length=255,
        verbose_name=_("Email address"),
        blank=True,
        null=True,
    )
    phone = models.CharField(
        max_length=10,  # 01234567890
        verbose_name=_("Mobile phone"),
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(
        default=True,
    )
    role = models.CharField(
        max_length=1,
        verbose_name=_("User role"),
        choices=UserRoles.choices,
        default=UserRoles.CUSTOMER,
    )

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        unique_together = ["username", "email", "phone"]
