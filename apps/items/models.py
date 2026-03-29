"""
Database models for the Items app.

Contains the central Item model along with its choices and business logic.
"""
import uuid

from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

# Validator for HSN/SAC code – exactly 6 digits
hsn_code_validator = RegexValidator(
    regex=r'^\d{6}$',
    message=_('HSN/SAC code must be exactly 6 numeric digits (e.g., 010101).')
)

sku_validator = RegexValidator(
        regex=r'^[A-Za-z0-9]{1,12}$',
        message=_('SKU must be alphanumeric and up to 12 characters (no symbols).')
    )


class Item(models.Model):
    """
    Represents a product or service that can be bought or sold.

    Contains all fields necessary for inventory, accounting, and tax
    calculations (GST). Provides helper methods to toggle active status.
    """

    class ItemType(models.TextChoices):
        """Type of item: physical goods or intangible service."""
        GOODS = 'GOODS', _('Goods')
        SERVICE = 'SERVICE', _('Service')

    class TaxPreference(models.TextChoices):
        """Tax treatment under GST."""
        TAXABLE = 'TAXABLE', _('Taxable')
        NON_TAXABLE = 'NON_TAXABLE', _('Non-Taxable')
        EXEMPT = 'EXEMPT', _('Exempt')
        OUT_OF_SCOPE = 'OUT_OF_SCOPE', _('Out of Scope')

    class SellingAccount(models.TextChoices):
        """Account head to use when selling this item."""
        SALES = 'SALES', _('Sales')
        SALES_RETURN = 'SALES_RETURN', _('Sales Return')
        GENERAL_INCOME = 'GENERAL_INCOME', _('General Income')
        INTEREST_INCOME = 'INTEREST_INCOME', _('Interest Income')
        OTHER_INCOME = 'OTHER_INCOME', _('Other Income')
        SHIPPING_INCOME = 'SHIPPING_INCOME', _('Shipping Income')

    class PurchaseAccount(models.TextChoices):
        """Account head to use when purchasing this item."""
        COST_OF_GOODS_SOLD = 'COST_OF_GOODS_SOLD', _('Cost of Goods Sold')
        PURCHASES = 'PURCHASES', _('Purchases')
        PURCHASE_RETURN = 'PURCHASE_RETURN', _('Purchase Return')
        FREIGHT = 'FREIGHT', _('Freight')
        OTHER_EXPENSE = 'OTHER_EXPENSE', _('Other Expense')
        
    class InventoryValuationMethod(models.TextChoices):
        """Method used to value inventory."""
        FIFO = 'FIFO', _('FIFO (First-In-First-Out)')
        LIFO = 'LIFO', _('LIFO (Last-In-First-Out)')
        WEIGHTED_AVERAGE = 'WEIGHTED_AVERAGE', _('Weighted Average')

    class InventoryAccount(models.TextChoices):
        """Account head for inventory asset."""
        INVENTORY = 'INVENTORY', _('Inventory Asset')
        RAW_MATERIALS = 'RAW_MATERIALS', _('Raw Materials')
        WORK_IN_PROGRESS = 'WORK_IN_PROGRESS', _('Work in Progress')
        FINISHED_GOODS = 'FINISHED_GOODS', _('Finished Goods')

    # Basic Information
    uid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True,
        help_text="Unique identifier used in API endpoints."
    )
    name = models.CharField(max_length=255, unique=True, db_index=True)
    item_type = models.CharField(
        max_length=10,
        choices=ItemType.choices,
        default=ItemType.GOODS,
    )
    unit = models.CharField(max_length=50, default='Nos')
    image = models.ImageField(
        upload_to='items/images/',
        null=True,
        blank=True,
    )
    hsn_code = models.CharField(
        max_length=6,
        validators=[hsn_code_validator],
        null=True,
        blank=True,
        help_text=_('6-digit HSN code (Goods) or SAC code (Services)'),
    )
    tax_preference = models.CharField(
        max_length=20,
        choices=TaxPreference.choices,
        default=TaxPreference.TAXABLE,
    )
    
    sku = models.CharField(
        max_length=12,
        unique=True,
        blank=True,
        null=True,
        validators=[sku_validator],
        help_text=_('Stock Keeping Unit – unique identifier for the item.'),
    )
    item_description = models.TextField(
        blank=True,
        default='',
        help_text=_('Detailed description of the item.'),
    )

    # Selling Information
    selling_price = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        null=True,
        blank=True
    )
    selling_account = models.CharField(
        max_length=30,
        choices=SellingAccount.choices,
        default=SellingAccount.SALES,
    )
    selling_description = models.TextField(blank=True, default='')

    # Purchase Information
    cost_price = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        null=True,
        blank=True
    )
    purchase_account = models.CharField(
        max_length=30,
        choices=PurchaseAccount.choices,
        default=PurchaseAccount.COST_OF_GOODS_SOLD,
    )
    purchase_description = models.TextField(blank=True, default='')

    # Tax Rates (GST)
    intra_state_tax_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text=_('CGST + SGST rate for intra-state supply (%)'),
    )
    inter_state_tax_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text=_('IGST rate for inter-state supply (%)'),
    )
    
    track_inventory = models.BooleanField(
        default=False,
        help_text=_('Enable inventory tracking for this item.'),
    )
    inventory_account = models.CharField(
        max_length=30,
        choices=InventoryAccount.choices,
        blank=True,
        null=True,
        help_text=_('Account head for inventory asset. Required when track_inventory is True.'),
    )
    inventory_valuation_method = models.CharField(
        max_length=30,
        choices=InventoryValuationMethod.choices,
        blank=True,
        null=True,
        help_text=_('Method used to value inventory. Required when track_inventory is True.'),
    )
    reorder_point = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text=_('Minimum stock level that triggers a reorder (in base unit).'),
    )

    # System Fields
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'items'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['item_type', 'is_active']),
            models.Index(fields=['hsn_code']),
            models.Index(fields=['tax_preference']),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_item_type_display()})"
    
    def clean(self):
        """
        Enforce inventory-related business rules.
        When tracking is disabled, clear the inventory fields automatically.
        When tracking is enabled, require both fields.
        """
        if not self.track_inventory:
            # Auto‑clear the fields – this ensures data consistency
            self.inventory_account = None
            self.inventory_valuation_method = None
        else:
            if not self.inventory_account:
                raise ValidationError({
                    'inventory_account': _('This field is required when tracking inventory.')
                })
            if not self.inventory_valuation_method:
                raise ValidationError({
                    'inventory_valuation_method': _('This field is required when tracking inventory.')
                })
                
    def save(self, *args, **kwargs):
        """Run full validation before saving."""
        self.full_clean()  # calls clean() and field validators
        super().save(*args, **kwargs)

    def mark_inactive(self) -> None:
        """Set the item as inactive and update timestamp."""
        self.is_active = False
        self.save(update_fields=['is_active', 'updated_at'])

    def mark_active(self) -> None:
        """Set the item as active and update timestamp."""
        self.is_active = True
        self.save(update_fields=['is_active', 'updated_at'])