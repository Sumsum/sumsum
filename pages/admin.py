from django.contrib import admin
from .models import Page
from django.utils.translation import ugettext_lazy as _


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_at', 'updated_at')
    fieldsets = (
        (_('Page details'), {
            'fields': (
                'title',
                'title_t',
                'body_html',
            ),
        }),
        (_('Visibility'), {
            'fields': (
                'published_at',
            ),
        }),
        (_('Metafields'), {
            'fields': (
                'metafields_json',
            ),
            #'classes': ('collapse',)
        }),
        (_('Search engine listing preview'), {
            'fields': (
                'handle',
            ),
            'classes': ('collapse',)
        }),
    )
