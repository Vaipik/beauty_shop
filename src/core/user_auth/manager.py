from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Custom user manager to perform auth using email or phone."""

    use_in_migrations = True

    def _create_user(
        self, username=None, email=None, phone=None, password=None, **kwargs
    ):
        """Create and save a User with the given email and password."""
        if not username:
            if not email and not phone:
                raise ValueError(_("The given email/phone must be set"))

        if email:
            email = self.normalize_email(email)

            if not username:
                username = email

            user = self.model(email=email, username=username, **kwargs)

        if phone:
            if not username:
                username = phone

            user = self.model(username=username, phone=phone, **kwargs)

        if kwargs.get("is_superuser"):
            user = self.model(username=username, **kwargs)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, phone=None, **kwargs):
        """Create common user."""
        kwargs.setdefault("is_superuser", False)
        return self._create_user(
            username=username, email=email, password=password, phone=phone, **kwargs
        )

    def create_superuser(self, username, password, **kwargs):
        """Create superuser."""
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_active", True)
        kwargs.setdefault("role", "A")  # admin

        if kwargs.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username=username, password=password, **kwargs)
