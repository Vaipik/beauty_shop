import typing

from django.contrib.auth import get_user_model
import factory.fuzzy

if typing.TYPE_CHECKING:
    from core.user_auth.models import User

User: User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    """User factory with predefined password and standard username.

    If another username is requried call factory as UserFactory(username=username).
    Default user role is set to customer.
    """

    username = "example@email.com"
    password = factory.PostGenerationMethodCall("set_password", "password")
    email = factory.LazyAttribute(
        lambda obj: obj.username if "@" in obj.username else None
    )
    phone = factory.LazyAttribute(
        lambda obj: obj.username if obj.username.isdigit() else None
    )
    role = User.UserRoles.CUSTOMER

    class Meta:
        model = User
        django_get_or_create = ("username",)
