import factory.fuzzy
from factory import SubFactory

from core.cart.models.cart import Cart
from core.user_auth.factories import UserFactory


class CartFactory(factory.django.DjangoModelFactory):
    """Cart factory."""

    class Meta:
        model = Cart

    user = SubFactory(UserFactory)
    is_active = True
