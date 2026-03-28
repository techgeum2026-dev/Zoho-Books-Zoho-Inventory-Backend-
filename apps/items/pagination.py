"""
Custom pagination for the Item API endpoints.
"""
from rest_framework.pagination import PageNumberPagination


class ItemPagination(PageNumberPagination):
    """
    Pagination class for items.

    Default page size: 25.
    Clients can override with `page_size` query parameter, up to 100 items.
    """
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100