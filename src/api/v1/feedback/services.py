import typing
from uuid import UUID

from django.contrib.auth import get_user_model

from core.feedback.models import Feedback
from core.order.models import Order

if typing.TYPE_CHECKING:
    from core.user_auth.models import User

User: User = get_user_model()


def check_product_in_order(product_id, user_id) -> bool:
    """Check if user has ordered product and order in success state."""
    return Order.objects.filter(
        status=Order.OrderStatus.SUCCESS, user_id=user_id, items__product__id=product_id
    ).exists()


def create_feedback(
    user: User, description: str, product: UUID, rating: int
) -> Feedback:
    """Create a new feedback in the db.

    description, product and rating are obtained via unpacking validated data
    :param user: owner.
    :param description: feedback description
    :param product: product id
    :param rating: value from 1 to 5 that should be validated by dj validators.
    :return:
    """
    return Feedback.objects.create(
        description=description,
        rating=rating,
        product_id=product,
        user=user,
    )
