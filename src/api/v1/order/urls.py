from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import OrderViewSet, OrderItemViewSet

order_router = SimpleRouter()
order_router.register(prefix="orders", viewset=OrderViewSet, basename="orders")

order_items_router = SimpleRouter()
order_items_router.register(
    prefix="order_items", viewset=OrderItemViewSet, basename="order_items"
)

app_name = "order"

urlpatterns = [
    path("", include(order_router.urls)),
    path("", include(order_items_router.urls)),
]
