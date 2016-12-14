from django.contrib import admin
from .models import MetaField


@admin.register(MetaField)
class MetaFieldAdmin(admin.ModelAdmin):
    list_display = ('key', 'namespace', 'owner_resource', 'owner_id')
    list_filter = ('namespace', 'owner_resource')
