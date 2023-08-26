from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import (
    ProductViewSet,
    ProductOptionViewSet,
    ProductCategoryViewSet,
    ProductImageViewSet,
    ProductManufacturerViewSet,
)

manufacturer_router = SimpleRouter()
manufacturer_router.register(
    prefix="manufacturer", viewset=ProductManufacturerViewSet, basename="manufacturer"
)

product_router = SimpleRouter()
product_router.register(prefix="products", viewset=ProductViewSet, basename="products")

category_router = SimpleRouter()
category_router.register(
    prefix="categories", viewset=ProductCategoryViewSet, basename="categories"
)

option_router = SimpleRouter()
option_router.register(
    prefix="options", viewset=ProductOptionViewSet, basename="options"
)

image_router = SimpleRouter()
image_router.register(prefix="images", viewset=ProductImageViewSet, basename="images")


app_name = "product"

urlpatterns = [
    path("", include(product_router.urls)),
    path("", include(category_router.urls)),
    path("", include(option_router.urls)),
    path("", include(image_router.urls)),
    path("", include(manufacturer_router.urls)),
]
