"""
Custom filtering for the Item model using django-filter.
"""
import django_filters
from .models import Item


class ItemFilter(django_filters.FilterSet):
    """
    FilterSet for Item model.

    Allows filtering items by:
    - is_active (boolean)
    - item_type (choice of GOODS/SERVICE)
    """
    is_active = django_filters.BooleanFilter(field_name='is_active')
    item_type = django_filters.ChoiceFilter(
        field_name='item_type',
        choices=Item.ItemType.choices
    )

    class Meta:
        model = Item
        fields = ['is_active', 'item_type']