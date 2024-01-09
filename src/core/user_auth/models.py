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

    class UserSex(models.TextChoices):
        """Extra roles."""

        MALE = "M", _("Male")
        FEMALE = "F", _("Female")
        UNDEFINED = "U", _("Undefined")

    username = models.CharField(
        max_length=255,  # same as email
        unique=True,
        verbose_name=_("Email or mobile number"),
    )
    first_name = models.CharField(
        max_length=255,
        verbose_name=_("First name"),
        null=True,
    )
    last_name = models.CharField(
        max_length=255,
        verbose_name=_("Last name"),
        null=True,
    )
    sex = models.CharField(
        max_length=1,
        verbose_name=_("Sex"),
        choices=UserSex.choices,
        default=UserSex.UNDEFINED,
    )
    email = models.EmailField(
        max_length=255,
        verbose_name=_("Email address"),
        blank=True,
        null=True,
        unique=True,
    )
    phone = models.CharField(
        max_length=10,  # 01234567890
        verbose_name=_("Mobile phone"),
        blank=True,
        null=True,
        unique=True,
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
    is_staff = models.BooleanField(default=False)  # required by djoser
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        db_table = "auth_user"
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        unique_together = ["username", "email", "phone"]
