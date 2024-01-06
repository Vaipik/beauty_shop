from django.contrib.auth import get_user_model
import factory.fuzzy

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    """User factory with predefined password and standard username.

    If another username is requried call factory as UserFactory(username=username).
    """

    username = "example@email.com"
    password = factory.PostGenerationMethodCall("set_password", "password")
    email = factory.LazyAttribute(
        lambda obj: obj.username if "@" in obj.username else None
    )
    phone = factory.LazyAttribute(
        lambda obj: obj.username if obj.username.isdigit() else None
    )

    class Meta:
        model = User
        django_get_or_create = ("username",)
