from django.contrib import admin
from .models import Blog, Article, Comment
from django.utils.translation import ugettext_lazy as _


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    pass


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [CommentInline]

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
        (_('visability'), {
            'fields': (
                'published_at',
            ),
        }),
        (_('organization'), {
            'fields': (
                'tags_t',
            ),
        }),
    )
