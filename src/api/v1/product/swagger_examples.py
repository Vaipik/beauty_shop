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
            "New parent id",
            summary="Response with changed parent id",
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
        ),
    ]
