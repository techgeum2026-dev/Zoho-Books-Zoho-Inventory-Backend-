"""
API views for Item management.

Provides standard CRUD operations plus custom actions (activate/deactivate)
using a ViewSet.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from .models import Item
from .serializers import ItemWriteSerializer, ItemDetailSerializer
from .filters import ItemFilter
from .pagination import ItemPagination
from . import services


class ItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Item CRUD operations.

    - Uses UUID as lookup field (uid).
    - Supports filtering (ItemFilter) and search (name field).
    - Returns different serializers for write vs read actions.
    - Adds custom endpoints: /{uid}/activate/ and /{uid}/deactivate/.
    """
    queryset = Item.objects.all()
    lookup_field = 'uid'
    lookup_value_regex = r'[0-9a-f-]{36}'  # Ensure UUID format
    pagination_class = ItemPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ItemFilter
    search_fields = ['name']

    def get_serializer_class(self):
        """
        Return the appropriate serializer based on the action.

        Write actions (create, update, partial_update) use ItemWriteSerializer.
        Read actions (list, retrieve, etc.) use ItemDetailSerializer.
        """
        if self.action in ('create', 'update', 'partial_update'):
            return ItemWriteSerializer
        return ItemDetailSerializer

    def create(self, request, *args, **kwargs):
        """
        Override create to return the full detail serializer after creation.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = services.create_item(serializer.validated_data)
        # Return the detail representation (includes all fields)
        return Response(
            ItemDetailSerializer(item, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        """
        Override update to return the full detail serializer after update.
        """
        partial = kwargs.pop('partial', False)
        item = self.get_object()
        serializer = self.get_serializer(item, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        item = services.update_item(item, serializer.validated_data)
        return Response(
            ItemDetailSerializer(item, context={'request': request}).data,
            status=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        """Soft delete is not used; we permanently delete the item."""
        item = self.get_object()
        services.delete_item(item)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'], url_path='activate')
    def activate(self, request, uid=None):
        """
        Custom action to activate an item (set is_active=True).

        Accepts POST to /items/{uid}/activate/.
        """
        item = self.get_object()
        services.activate_item(item)
        return Response({"detail": "Item activated successfully."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='deactivate')
    def deactivate(self, request, uid=None):
        """
        Custom action to deactivate an item (set is_active=False).

        Accepts POST to /items/{uid}/deactivate/.
        """
        item = self.get_object()
        services.deactivate_item(item)
        return Response({"detail": "Item deactivated successfully."}, status=status.HTTP_200_OK)