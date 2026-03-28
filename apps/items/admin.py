from django.contrib import admin
from django.utils.html import format_html

from .models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):

    list_display  = [
        'name', 'item_type', 'unit', 'hsn_code',
        'selling_price', 'cost_price', 'tax_preference',
        'is_active', 'created_at',
    ]
    list_filter   = ['item_type', 'tax_preference', 'is_active', 'selling_account', 'purchase_account']
    search_fields = ['name', 'hsn_code', 'selling_description', 'purchase_description']
    readonly_fields = ['id', 'created_at', 'updated_at', '_image_preview']
    list_per_page   = 50
    ordering        = ['-created_at']

    fieldsets = (
        ('Basic Information', {  
            'fields': (
                'id', 'name', 'item_type', 'unit',
                'image', '_image_preview',
                'hsn_code', 'tax_preference',
            ),
        }),
        ('Selling Information', {
            'fields': ('selling_price', 'selling_account', 'selling_description'),
        }),
        ('Purchase Information', {
            'fields': ('cost_price', 'purchase_account', 'purchase_description'),
        }),
        ('Tax Rates', {
            'fields': ('intra_state_tax_rate', 'inter_state_tax_rate'),
        }),
        ('Status & Audit', {
            'fields': ('is_active', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    @admin.display(description='Image Preview')
    def _image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:120px; border-radius:4px;" />',
                obj.image.url,
            )
        return '—'

    actions = ['make_active', 'make_inactive']

    @admin.action(description='Mark selected items as Active')
    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} item(s) marked as active.")

    @admin.action(description='Mark selected items as Inactive')
    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} item(s) marked as inactive.")