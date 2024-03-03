from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (
    CurrencyViewSet,
    ProductCategoryViewSet,
    ProductImageViewSet,
    ProductManufacturerViewSet,
    ProductOptionViewSet,
    ProductViewSet,
)

products_router = SimpleRouter()
products_router.register(
    prefix="manufacturers", viewset=ProductManufacturerViewSet, basename="manufacturers"
)
products_router.register(prefix="products", viewset=ProductViewSet, basename="products")
products_router.register(
    prefix="categories", viewset=ProductCategoryViewSet, basename="categories"
)
products_router.register(
    prefix="options", viewset=ProductOptionViewSet, basename="options"
)
products_router.register(
    prefix="images", viewset=ProductImageViewSet, basename="images"
)
products_router.register(
    prefix="currencies", viewset=CurrencyViewSet, basename="currencies"
)


app_name = "product"

urlpatterns = [
    path("", include(products_router.urls)),
]
