from rest_framework import pagination

from api.base import constants


class CustomLimitOffsetPagination(pagination.LimitOffsetPagination):
    """Provide default values for pagination."""

    default_limit = constants.DEFAULT_LIMIT
    max_limit = constants.MAX_LIMIT
