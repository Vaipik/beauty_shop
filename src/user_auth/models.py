from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from user_auth.managers import UserManager
from core.product.models.base import Base


class User(AbstractBaseUser, Base, PermissionsMixin):
    """User model."""

    username = models.CharField(verbose_name=_("Username"), max_length=255, unique=True)
    email = models.EmailField(
        verbose_name=_("Email address"), unique=True, null=True, blank=True
    )
    phone = models.CharField(verbose_name=_("Phone number"), null=True, blank=True)
    created_at = models.DateTimeField(
        verbose_name=_("Date of creation"), auto_now_add=True
    )
    is_active = models.BooleanField(verbose_name=_("Active"), default=True)
    is_staff = models.BooleanField(verbose_name=_("Staff"), default=False)
    is_superuser = models.BooleanField(verbose_name=_("Verified"), default=False)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        db_table = _("users")
        verbose_name = _("User")
        verbose_name_plural = _("users")
        unique_together = ("username", "email", "phone")

    def clean(self):
        """Check an email or phone number."""
        if not self.email and not self.phone:
            raise ValidationError("Email or password must be filled")

    def save(self, *args, **kwargs):
        """Save method, for hashing password."""
        if self._state.adding:  # Checking if the object is being created
            self.set_password(self.password)
        super().save(*args, **kwargs)
