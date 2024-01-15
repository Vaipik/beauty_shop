from rest_framework import permissions

from .services import check_product_in_order


class LeaveFeedbackPermission(permissions.BasePermission):
    """Permission that allow user to leave feedback.

    User are able to leave feedback ONLY if order is completed and product is in order
    list.
    """

    def has_permission(self, request, view):
        """Verify that request user has compeleted order and product is in list."""
        product_id = request.data["product"]
        user_id = request.user.pk
        if not check_product_in_order(product_id, user_id):
            return False
        return True
