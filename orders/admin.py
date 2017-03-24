from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_distplay = ('number', 'processed_at', 'customer__first_name', 'financial_status', 'fulfillment_status', 'total_price')
    icon = '<i class="fa fa-inbox" aria-hidden="true"></i>'
