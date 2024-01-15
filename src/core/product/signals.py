from django.db.models import Avg, Subquery, OuterRef
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.feedback.models import Feedback
from core.product.models import Product


@receiver(post_save, sender=Feedback)
def update_product_rating(sender, instance, created, **kwargs):
    """Recalculate average product rating each time new feedback appears."""
    if created:
        product_id = instance.product.pk
        Product.objects.filter(pk=product_id).update(
            rating=Subquery(
                Feedback.objects.filter(product_id=OuterRef("id"))
                .values("product_id")
                .annotate(avg_rating=Avg("rating"))
                .values("avg_rating")[:1]
            )
        )
