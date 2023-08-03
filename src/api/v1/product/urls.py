from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import ProductViewSet, ProductCategoryOptionViewSet, ProductCategoryViewSet

product_router = SimpleRouter()
product_router.register(prefix="products", viewset=ProductViewSet, basename="products")

category_router = SimpleRouter()
category_router.register(
    prefix="categories", viewset=ProductCategoryViewSet, basename="categories"
)

option_router = SimpleRouter()
option_router.register(
    prefix="options", viewset=ProductCategoryOptionViewSet, basename="options"
)

app_name = "product"

urlpatterns = [
    path("", include(product_router.urls)),
    path("", include(category_router.urls)),
    path("", include(option_router.urls)),
]
