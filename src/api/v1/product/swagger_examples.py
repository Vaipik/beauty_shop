from drf_spectacular.utils import OpenApiExample


def get_nested_examples():
    """To use in drf-spectacular examples for GET request MPNode."""
    return [
        OpenApiExample(
            "CategoryResponse",
            summary="Example SubCategory Response",
            value=[
                {
                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "name": "Root Category 1",
                    "children": [
                        {
                            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
                            "name": "Sub Category 1.1",
                            "children": [
                                {
                                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa8",
                                    "name": "Sub Category 1.1.1",
                                    "children": [],
                                }
                            ],
                        }
                    ],
                },
                {
                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "name": "Root Category 2",
                    "children": [
                        {
                            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
                            "name": "Sub Category 2.1",
                            "children": [
                                {
                                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa8",
                                    "name": "Sub Category 2.1.1",
                                    "children": [],
                                }
                            ],
                        }
                    ],
                },
            ],
        )
    ]


def get_created_tree_examples():
    """To use in drf-spectacular examples for POST request MPNode."""
    return [
        OpenApiExample(
            "Root node",
            summary="Root node",
            description="Leave parentId as null to create a root node.",
            value={
                "name": "root name",
                "parentId": None,
            },
        ),
        OpenApiExample(
            "Child node",
            summary="Child node",
            description="Provide id of parent node to create a child node.",
            value={
                "name": "child name",
                "parentId": "58b45f63-634a-4c5b-8594-c5729e9aa655",
            },
        ),
    ]


def update_tree_example():
    """Response for PATCHed MP tree."""
    return [
        OpenApiExample(
            name="Move to root",
            summary="Move node to root",
            description="Moves node and it nested nodes to root.",
            value=[
                {
                    "name": "You can change name if u want.",
                    "parentId": "You can leave this field as null or not provide.",
                    "toRoot": True,
                }
            ],
            request_only=True,
        ),
        OpenApiExample(
            name="Move to another parent node",
            summary="Move to another parent",
            description="Moves node and it nested nodes to another parent.",
            value=[
                {
                    "name": "You can change name if u want.",
                    "parentId": "ID of new parent.",
                    "toRoot": "You can leave this field as false or not provide.",
                }
            ],
            request_only=True,
        ),
        OpenApiExample(
            name="Change name",
            summary="Change node name",
            description="Change node name ",
            value=[
                {
                    "name": "New node name",
                    "parentId": "You can leave this field as null or not provide.",
                    "toRoot": "You can leave this field as false or not provide.",
                }
            ],
            request_only=True,
        ),
        OpenApiExample(
            "Response when moved to root or another parent",
            summary="Node was moved",
            description="Return whole tree with changed node",
            value=[
                {
                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "name": "Root Category 1",
                    "children": [
                        {
                            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
                            "name": "Sub Category 1.1",
                            "children": [
                                {
                                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa8",
                                    "name": "Sub Category 1.1.1",
                                    "children": [],
                                }
                            ],
                        }
                    ],
                },
                {
                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "name": "Root Category 2",
                    "children": [
                        {
                            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
                            "name": "Sub Category 2.1",
                            "children": [
                                {
                                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa8",
                                    "name": "Sub Category 2.1.1",
                                    "children": [],
                                }
                            ],
                        }
                    ],
                },
            ],
            response_only=True,
        ),
        OpenApiExample(
            "New name",
            summary="Response with changed name",
            description="Return a category with children",
            value={
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "name": "NEW NAME OF CATEGORY",
                "children": [
                    {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
                        "name": "Sub Category 1.1",
                        "children": [
                            {
                                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa8",
                                "name": "Sub Category 1.1.1",
                                "children": [],
                            }
                        ],
                    }
                ],
            },
            response_only=True,
        ),
    ]
