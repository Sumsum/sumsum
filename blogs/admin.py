from .models import Blog, Article, Comment
from django.contrib import admin
from django.db.models.expressions import RawSQL
from django.utils.translation import ugettext_lazy as _


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Blog details'), {
            'fields': (
                'title_t',
                'feedburner_location',
            )
        }),
        (_('Comments'), {
            'fields': (
                'commentable',
            ),
        }),
        (_('Search engine listing preview'), {
            'fields': (
                'handle_t',
            ),
            'classes': ('collapse',)
        }),
    )


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [CommentInline]
    list_display = ['title', 'blog', 'user', 'published_at']
    list_filter = ['user', 'blog']
    search_fields = ['title_t']
    fieldsets = (
        (None, {
            'fields': (
                'title_t',
                'body_html_t',
            )
        }),
        (_('Excerpt'), {
            'fields': (
                'summary_html_t',
            ),
            'classes': ('collapse',)
        }),
        (None, {
            'fields': (
                'user',
                'blog',
            ),
        }),
        (_('Visability'), {
            'fields': (
                'published_at',
            ),
        }),
        (_('Organization'), {
            'fields': (
                'tags_t',
            ),
            'classes': ('collapse',)
        }),
        (_('Search engine listing preview'), {
            'fields': (
                'handle_t',
            ),
            'classes': ('collapse',)
        }),
    )
