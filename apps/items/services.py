"""
Service layer encapsulating business logic for Item operations.

Keeps views lean and separates data persistence logic from request handling.
"""
from .models import Item


def create_item(validated_data: dict) -> Item:
    """Create and return a new Item instance from validated data."""
    return Item.objects.create(**validated_data)


def update_item(item: Item, validated_data: dict) -> Item:
    """
    Update an existing Item instance with validated data.

    Saves the instance and returns it.
    """
    for attr, value in validated_data.items():
        setattr(item, attr, value)
    item.save()
    return item


def delete_item(item: Item) -> None:
    """Permanently delete an Item from the database."""
    item.delete()


def activate_item(item: Item) -> Item:
    """Activate an item (set is_active=True)."""
    item.mark_active()
    return item


def deactivate_item(item: Item) -> Item:
    """Deactivate an item (set is_active=False)."""
    item.mark_inactive()
    return item