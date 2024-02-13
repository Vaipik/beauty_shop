from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (
    CurrencyViewSet,
    ProductCategoryViewSet,
    ProductCurrencyViewSet,
    ProductImageViewSet,
    ProductManufacturerViewSet,
    ProductOptionViewSet,
    ProductViewSet,
)

manufacturer_router = SimpleRouter()
manufacturer_router.register(
    prefix="manufacturers", viewset=ProductManufacturerViewSet, basename="manufacturers"
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

currency_router = SimpleRouter()
currency_router.register(
    prefix="currencies", viewset=CurrencyViewSet, basename="currencies"
)

product_currency_router = SimpleRouter()
product_currency_router.register(
    prefix="product_currencies",
    viewset=ProductCurrencyViewSet,
    basename="product_currencies",
)

app_name = "product"

urlpatterns = [
    path("", include(product_router.urls)),
    path("", include(category_router.urls)),
    path("", include(option_router.urls)),
    path("", include(image_router.urls)),
    path("", include(manufacturer_router.urls)),
    path("", include(currency_router.urls)),
    path("", include(product_currency_router.urls)),
]
