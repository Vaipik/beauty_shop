from django.urls import path, include

urlpatterns = [
    path("", include("api.v1.product.urls")),
    path("", include("api.v1.order.urls")),
]
