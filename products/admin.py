from django.contrib import admin
from .models import Product, ProductImage, ProductTag, ProductVendor, ProductType
from django.utils.translation import ugettext_lazy as _
from utils.widgets import AdminImageWidget
from django.db import models
from .forms import ProductForm


@admin.register(ProductTag)
class ProductTagAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductVendor)
class ProductVendorAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    pass


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    formfield_overrides = {
        models.ImageField: {'widget': AdminImageWidget},
    }


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    save_on_top = True
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductImageInline]
    form = ProductForm
    fieldsets = (
        (None, {
            'fields': (
                'show_online',
                'title',
                'description',
            )
        }),
        (_('Organization'), {
            'fields': (
                'type',
                'vendor',
                'collections',
                'tags',
            )
        }),
        (_('Pricing'), {
            'fields': (
                ('price', 'compare_at_price'),
                ('tax', 'taxable'),
            )
        }),
        (_('Inventory'), {
            'fields': (
                'requires_shipping',
                ('weight', 'weight_unit'),
                'taxable',
            ),
            'classes': ('collapse',)
        }),
        (_('Search engine listing preview'), {
            'fields': (
                'page_title',
                ('meta_description'),
                'slug',
            ),
            'classes': ('collapse',)
        }),
    )

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """
        Remove the ugly help text that the admin adds by default
        """
        form_field = super().formfield_for_manytomany(db_field, request, **kwargs)
        form_field.help_text = ''
        return form_field
