from django.urls import path, include
from rest_framework.routers import SimpleRouter
from api.v1.cart.view.cart import ShoppingCartViewSet

cart_router = SimpleRouter()
cart_router.register(prefix="cart", viewset=ShoppingCartViewSet, basename="cart")

app_name = "cart"

urlpatterns = [
    path("", include(cart_router.urls)),
]
