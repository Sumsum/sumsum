from django.contrib import admin
from .models import Page
from django.utils.translation import ugettext_lazy as _


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    icon = '<i class="fa fa-file-text" aria-hidden="true"></i>'
    list_display = ('title', 'published_at', 'updated_at')
    fieldsets = (
        (_('Page details'), {
            'fields': (
                'title_t',
                'body_html_t',
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
            'classes': ('box-primary', 'collapsed',)
        }),
        (_('Search engine listing preview'), {
            'fields': (
                'handle_t',
            ),
            'classes': ('box-danger', 'collapsed',)
        }),
    )
