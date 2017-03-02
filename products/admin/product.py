from .forms import ProductForm
from django.contrib import admin
from django.db import models
from django.utils.translation import ugettext_lazy as _
from products.models import Product, ProductVariant, ProductImage
from utils.widgets import AdminImageWidget


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    formfield_overrides = {
        models.ImageField: {'widget': AdminImageWidget},
    }
    fields = ('file', 'position', 'alt')


class ProductVariantInline(admin.StackedInline):
    model = ProductVariant
    extra = 1
    fieldsets = (
        (None, {
            'fields': (
                'position',
            ),
        }),
        (_('Options'), {
            'fields': (
                'option1',
                'option2',
                'option3',
                'image',
            ),
            'classes': ('collapse',)
        }),
        (_('Pricing'), {
            'fields': (
                ('price', 'compare_at_price'),
                'taxable',
            ),
        }),
        (_('Inventory'), {
            'fields': (
                ('sku', 'barcode'),
                ('inventory_management', 'inventory_quantity'),
                'inventory_policy',
                'next_incoming_date',
            ),
        }),
        (_('Shipping'), {
            'fields': (
                'requires_shipping',
                ('weight_in_unit', 'weight_unit'),
                'fulfillment_service',
            ),
        }),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">local_offer</i>'
    save_on_top = True
    list_fields = ('title', 'product_type', 'vendor', 'published_at', 'updated_at')
    search_fields = ('title', 'product_type', 'vendor')
    inlines = [ProductVariantInline, ProductImageInline]
    #form = ProductForm
    fieldsets = (
        (None, {
            'fields': (
                'title',
                'body_html',
            )
        }),
        (_('Visability'), {
            'fields': (
                'published_at',
                'published_scope',
            ),
        }),
        (_('Organization'), {
            'fields': (
                'product_type',
                #'collections_m2m',
                'vendor',
                'tags',
            ),
        }),
        (_('Options'), {
            'fields': (
                'option1_name',
                'option2_name',
                'option3_name',
            ),
            'classes': ('collapse',)
        }),
        (_('Search engine listing preview'), {
            'fields': (
                'handle',
            ),
            'classes': ('collapse',)
        }),
        (_('Metafields'), {
            'fields': (
                'metafields_json',
            ),
            'classes': ('collapse',)
        }),
    )

    #def formfield_for_manytomany(self, db_field, request, **kwargs):
    #    """
    #    Remove the ugly help text that the admin adds by default
    #    """
    #    form_field = super().formfield_for_manytomany(db_field, request, **kwargs)
    #    form_field.help_text = ''
    #    return form_field
