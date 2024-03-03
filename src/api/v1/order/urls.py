from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import OrderItemViewSet, OrderViewSet

order_router = SimpleRouter()
order_router.register(prefix="orders", viewset=OrderViewSet, basename="orders")
order_router.register(
    prefix="order_items", viewset=OrderItemViewSet, basename="order_items"
)

app_name = "order"

urlpatterns = [
    path("", include(order_router.urls)),
]
