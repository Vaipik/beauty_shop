from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from ..serializers import ProductOutputDetailSerializer, ProductOutputListSerializer
from .. import services


class ProductViewSet(viewsets.ModelViewSet):
    """Represent product routes. PUT method is excluded because of NULL."""

    serializer_class = ProductOutputDetailSerializer
    http_method_names = ["get", "post", "patch", "delete"]

    def get_serializer_class(self):
        """Different endpoints require different serializers."""
        if self.action == "list":
            return ProductOutputListSerializer
        if self.action == "retrieve":
            return ProductOutputDetailSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        """Different serializers require different querysets."""
        if self.action == "list":
            return services.get_list_products()
        if self.action == "retrieve":
            return services.get_detail_product(self.kwargs["pk"])

        return super().get_queryset()

    @extend_schema(
        # override default docstring extraction
        description="Return a list of products."
        "Note that products have only one image - main image.",
    )
    def list(self, request):  # noqa D102
        # your non-standard behaviour
        return super().list(request)

    # def create(self, request, *args, **kwargs):
    #     pass
    @extend_schema(
        description="ddada",
        responses=ProductOutputDetailSerializer,
    )
    def retrieve(self, request, pk=None):  # noqa D102
        return super().retrieve(request, pk)

    def partial_update(self, request, pk=None):  # noqa D102
        pass

    def destroy(self, request, pk=None):  # noqa D102
        pass
