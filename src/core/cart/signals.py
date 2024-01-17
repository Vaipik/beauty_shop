from django.db.models.signals import post_save
from django.dispatch import receiver

from api.v1.cart.services.cart import delete_cart
from core.cart.models import CartItem
from core.cart.models.cart import Cart
from core.order.models import Order
from core.product.models import Product


@receiver(post_save, sender=Product)
def update_cart_prices(sender, instance, **kwargs):
    """Update prices in the active carts when a product price changes."""
    cart_is_active = Cart.objects.filter(is_active=True)
    for cart in cart_is_active:
        CartItem.objects.filter(cart=cart, product=instance).update(
            price=instance.price
        )


@receiver(post_save, sender=Order)
def delete_cart_after_order(sender, instance, created, **kwargs):
    """Make the cart inactive after creating an order."""
    if created:
        cart = Cart.objects.filter(user=instance.user, is_active=True).first()
        if cart:
            delete_cart(cart)
