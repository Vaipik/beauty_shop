from django.db import transaction
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from api.base.permissions import StaffPermission
from api.v1.product import services, swagger_examples
from api.v1.product.serializers import (
    ProductOptionCreateResponseSeriliazer,
    TreeCreateUpdateSerializer,
    TreeListResponseSerializer,
)
from core.product.models import ProductOption


class ProductOptionViewSet(viewsets.ModelViewSet):
    """Viewset for options that are binded for products."""

    http_method_names = ["get", "post", "patch", "delete"]

    def get_permissions(self):
        """To use a custom permissions."""
        if self.action in {"create", "partial_update", "destroy"}:
            permission_classes = [StaffPermission]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """Choose which queryset should be queried."""
        if self.action == "list":
            return ProductOption.get_root_nodes()
        if self.action == "retrieve":
            node = ProductOption.objects.get(pk=self.kwargs["pk"])
            return ProductOption.get_tree(node)
        if self.action in {"partial_update", "destroy"}:
            return ProductOption.objects.get(pk=self.kwargs["pk"])
        return super().get_queryset()

    def get_serializer_class(self):  # noqa D102
        if self.action == "list":
            return TreeListResponseSerializer
        if self.action in {"create", "partial_update"}:
            return TreeCreateUpdateSerializer
        return super().get_serializer_class()

    @extend_schema(
        description="This endpoint is used to create an option and suboptions for"
        "products. If you want to create a root of your options tree you"
        "don't need to pass a parentId, leave it NULL. If you want to"
        "create a suboption than you need to provide a parentId of option"
        "and provide a name for suboption.",
        request=TreeCreateUpdateSerializer,
        responses=ProductOptionCreateResponseSeriliazer,
        examples=[
            OpenApiExample(
                "Root node",
                summary="Root node",
                description="Leave parentId as null to create a root node.",
                value={
                    "name": "option name",
                    "parentId": None,
                },
            ),
            OpenApiExample(
                "Child node",
                summary="Child node",
                description="Provide id of parent node to create a child node.",
                value={
                    "name": "option name",
                    "parentId": "58b45f63-634a-4c5b-8594-c5729e9aa655",
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

        if parent_id := serializer.data.get("parentId"):
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
        request=TreeCreateUpdateSerializer,
        responses=TreeListResponseSerializer,
        examples=swagger_examples.update_tree_example(),
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
        update_option = services.update_option(
            option=instance,
            name=request.data.get("name"),
            parent_id=request.data.get("parentId"),
            to_root=request.data.get("toRoot", False),
        )
        if request.data.get("parentId") or request.data.get("toRoot"):
            response_serializer = TreeListResponseSerializer(update_option, many=True)
        else:
            # if only name was changed -> not neccessary to return whole tree.
            instance.refresh_from_db()
            response_serializer = TreeListResponseSerializer(instance)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """Delete given option and its descendants."""
        instance = self.get_queryset()
        services.delete_option(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
