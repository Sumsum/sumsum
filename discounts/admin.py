from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import Discount


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('code', 'times_used', 'starts_at', 'ends_at')
    icon = '<i class="fa fa-gift" aria-hidden="true"></i>'
    fieldsets = (
        (None, {
            'fields': (
                'code',
            )
        }),
        (_('Conditions'), {
            'fields': (
                'discount_type',
                'value',
                'applies_to_resource',
                'applies_to_id',
                'minimum_order_amount',
            )
        }),
        (_('Usage limits'), {
            'fields': (
                'usage_limit',
                'applies_once_per_customer',
            )
        }),
        (_('Date Range'), {
            'fields': (
                'starts_at',
                'ends_at',
            )
        }),
    )
