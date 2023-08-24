from django.db import transaction
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import viewsets, status
from rest_framework.response import Response

from core.product.models import ProductOption
from api.v1.product import swagger_examples
from ..serializers import (
    ProductOptionListResponseSerializer,
    ProductOptionCreateRequestSeriliazer,
    ProductOptionCreateResponseSeriliazer,
    ProductOptionPartialUpdateRequestSerializer,
    ProductOptionPatchResponseSerializer,
)
from .. import services


class ProductOptionViewSet(viewsets.ModelViewSet):
    """Viewset for options that are binded for products."""

    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        """Choose which queryset should be queried."""
        if self.action == "list":
            return ProductOption.get_root_nodes()
        if self.action == "retrieve":
            node = ProductOption.objects.get(pk=self.kwargs["pk"])
            return ProductOption.get_tree(node)
        return super().get_queryset()

    def get_serializer_class(self):  # noqa D102
        if self.action == "list":
            return ProductOptionListResponseSerializer
        if self.action == "create":
            return ProductOptionCreateRequestSeriliazer
        if self.action == "partial_update":
            return ProductOptionPartialUpdateRequestSerializer
        return super().get_serializer_class()

    @extend_schema(
        description="This endpoint is used to create an option and suboptions for"
        "products. If you want to create a root of your options tree you"
        "don't need to pass a parent_id, leave it NULL. If you want to"
        "create a suboption than you need to provide a parentId of option"
        "and provide a name for suboption.",
        request=ProductOptionCreateRequestSeriliazer,
        responses=ProductOptionCreateResponseSeriliazer,
        examples=[
            OpenApiExample(
                "Root node",
                summary="Root node",
                description="Leave parent_id as null to create a root node.",
                value={
                    "name": "option name",
                    "parent_id": None,
                },
            ),
            OpenApiExample(
                "Child node",
                summary="Child node",
                description="Provide id of parent node to create a child node.",
                value={
                    "name": "option name",
                    "parent_id": "58b45f63-634a-4c5b-8594-c5729e9aa655",
                },
            ),
        ],
    )
    def create(self, request, *args, **kwargs):  # noqa D102
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        if parent_id := serializer.data.get("parent_id"):
            option = services.create_child_option(serializer.data["name"], parent_id)
        else:
            option = services.create_root_option(serializer.data["name"])

        response = ProductOptionCreateResponseSeriliazer(option)
        return Response(data=response.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        description="Provide all categories that are presented."
        "Note that depth are not limited.",
        examples=swagger_examples.get_nested_examples(),
    )
    def list(self, request, *args, **kwargs):  # noqa D102
        return super().list(request, *args, **kwargs)

    @extend_schema(
        description="Provide all categories that are presented in given category."
        "Note that depth are not limited.",
        examples=swagger_examples.get_nested_examples(),
    )
    def retrieve(self, request, *args, **kwargs):  # noqa D102
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        description="This endpoint is used to make a partial update of category."
        " E.g change category name or move it to another parent category"
        " with all its children. If you want only to change name leave"
        " parent id empty, if you want to move category provide parent id.",
        request=ProductOptionPartialUpdateRequestSerializer,
        responses=ProductOptionPatchResponseSerializer,
        examples=swagger_examples.patch_tree_example(),
    )
    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        """PATCH for the option. Can be removed to another parent or renamed."""
        partial = True
        instance = self.get_queryset()
        request_serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )
        request_serializer.is_valid(raise_exception=True)
        update_cat = services.patch_option(instance, **request.data)
        if request.data.get("parent_id"):
            response_serializer = ProductOptionPatchResponseSerializer(
                update_cat, many=True
            )
        else:
            instance.refresh_from_db()
            response_serializer = ProductOptionPatchResponseSerializer(instance)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """Delete given option and its descendants."""
        instance = self.get_queryset()
        services.delete_option(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
