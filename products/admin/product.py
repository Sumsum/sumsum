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
    extra = 0
    fieldsets = (
        (None, {
            'fields': (
                'position',
            ),
        }),
        (_('Options'), {
            'fields': (
                'option1_t',
                'option2_t',
                'option3_t',
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
    icon = '<i class="fa fa-tags" aria-hidden="true"></i>'
    save_on_top = True
    list_fields = ('title', 'product_type', 'vendor', 'published_at', 'updated_at')
    search_fields = ('title_t', 'product_type', 'vendor')
    inlines = [ProductVariantInline, ProductImageInline]
    #form = ProductForm
    fieldsets = (
        (None, {
            'fields': (
                'title_t',
                'body_html_t',
            ),
            'classes': ('box-primary',)
        }),
        (_('Visability'), {
            'fields': (
                'published_at',
                'published_scope',
            ),
            'classes': ('box-primary',)
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
                'option1_name_t',
                'option2_name_t',
                'option3_name_t',
            ),
            'classes': ('collapsed',)
        }),
        (_('Search engine listing preview'), {
            'fields': (
                'handle_t',
            ),
            'classes': ('box-danger', 'collapsed',)
        }),
        (_('Metafields'), {
            'fields': (
                'metafields_json',
            ),
            'classes': ('collapsed',)
        }),
    )

    #def formfield_for_manytomany(self, db_field, request, **kwargs):
    #    """
    #    Remove the ugly help text that the admin adds by default
    #    """
    #    form_field = super().formfield_for_manytomany(db_field, request, **kwargs)
    #    form_field.help_text = ''
    #    return form_field
