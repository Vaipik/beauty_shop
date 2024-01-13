from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.base.models import Base, TimeStampedBase

User = get_user_model()


class Feedback(Base, TimeStampedBase):
    """Describe a feedback that user are able to leave if user order was successful."""

    description = models.TextField(verbose_name=_("feedback description"))
    rating = models.IntegerField(
        validators=[
            MinValueValidator(limit_value=0, message=_("rating can't be less than 1.")),
            MaxValueValidator(
                limit_value=5, message=_("rating can't be greater than 5.")
            ),
        ]
    )
    product = models.ForeignKey(
        to="product.Product", related_name="feedbacks", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        to=User, on_delete=models.DO_NOTHING, related_name="feedbacks"
    )

    class Meta:
        db_table = "feedbacks"
        verbose_name = _("Feedback")
        verbose_name_plural = _("Feedbacks")
