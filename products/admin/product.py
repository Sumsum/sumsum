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


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    save_on_top = True
    inlines = [ProductImageInline]
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
                'published',
                'published_at',
                'published_scope',
            ),
            'classes': ('collapse',)
        }),
        (_('Organization'), {
            'fields': (
                'product_type',
                #'collections_m2m',
                'vendor',
                'tags',
            ),
            'classes': ('collapse',)
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
        #(_('Pricing'), {
        #    'fields': (
        #        ('price', 'compare_at_price'),
        #        ('tax', 'taxable'),
        #    )
        #}),
        #(_('Inventory'), {
        #    'fields': (
        #        'requires_shipping',
        #        ('weight', 'weight_unit'),
        #        'taxable',
        #    ),
        #    'classes': ('collapse',)
        #}),
        #(_('Search engine listing preview'), {
        #    'fields': (
        #        'page_title',
        #        ('meta_description'),
        #        'slug',
        #    ),
        #    'classes': ('collapse',)
        #}),
    )

    #def formfield_for_manytomany(self, db_field, request, **kwargs):
    #    """
    #    Remove the ugly help text that the admin adds by default
    #    """
    #    form_field = super().formfield_for_manytomany(db_field, request, **kwargs)
    #    form_field.help_text = ''
    #    return form_field
