"""
Serializers for the Item model.

Separate serializers for write operations (create/update) and read operations
(list/retrieve) to control field exposure and validation.
"""
from rest_framework import serializers
from .models import Item


class ItemWriteSerializer(serializers.ModelSerializer):
    """
    Used for creating and updating items.

    Contains only writable fields. Performs business validation:
    - selling_price must not be less than cost_price.
    """

    class Meta:
        model = Item
        fields = [
            'name', 'item_type', 'unit', 'image', 'hsn_code',
            'tax_preference', 'selling_price', 'selling_account',
            'selling_description', 'cost_price', 'purchase_account',
            'purchase_description', 'intra_state_tax_rate', 'inter_state_tax_rate',
        ]

    def validate(self, attrs):
        """
        Cross-field validation.

        Raises a ValidationError if selling_price is set and is lower than
        cost_price.
        """
        selling_price = attrs.get('selling_price')
        cost_price = attrs.get('cost_price')

        if selling_price is not None and cost_price is not None:
            if selling_price < cost_price:
                raise serializers.ValidationError(
                    {"selling_price": "Selling price cannot be less than cost price."}
                )
        return attrs


class ItemDetailSerializer(serializers.ModelSerializer):
    """
    Used for reading item details (list and retrieve actions).

    Includes read-only display fields for choices (e.g., 'item_type_display')
    and all system fields (uid, created_at, updated_at, is_active).
    """
    item_type_display = serializers.CharField(source='get_item_type_display', read_only=True)
    tax_preference_display = serializers.CharField(source='get_tax_preference_display', read_only=True)
    selling_account_display = serializers.CharField(source='get_selling_account_display', read_only=True)
    purchase_account_display = serializers.CharField(source='get_purchase_account_display', read_only=True)

    class Meta:
        model = Item
        fields = [
            'uid', 'name', 'item_type', 'item_type_display', 'unit', 'image',
            'hsn_code', 'tax_preference', 'tax_preference_display',
            'selling_price', 'selling_account', 'selling_account_display',
            'selling_description', 'cost_price', 'purchase_account',
            'purchase_account_display', 'purchase_description',
            'intra_state_tax_rate', 'inter_state_tax_rate',
            'is_active', 'created_at', 'updated_at',
        ]