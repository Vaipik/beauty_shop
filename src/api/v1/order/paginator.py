from rest_framework.pagination import PageNumberPagination


class PaginationForOrder(PageNumberPagination):
    """Class sets specific attributes for paginating a list of Order instances.

    Pass a parameter to change the number of instances displayed -
        http://127.0.0.1:8000/api/v1/orders/?page=2&page_size=5.
    """

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100
