from .models import Blog, Article, Comment
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'commentable']
    search_fields = ['title_t']
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


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ('created_at', 'body', 'summary')
    fields = ('created_at', 'summary', 'status')

    def summary(self, obj):
        return '{} {}: {}'.format(obj.name, obj.email, obj.html)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [CommentInline]
    list_display = ['title_t', 'blog', 'user', 'published_at']
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


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'summary', 'status']
    list_filter = ['article__blog', 'article']
    search_fields = ['author', 'body', 'email', 'article__title']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        (None, {
            'fields': (
                'created_at',
                'article',
                'author',
                'email',
                'body',
                'status',
            )
        }),
        (_('Details'), {
            'fields': (
                'ip',
                'user_agent',
                'updated_at',
                'published_at',
            ),
            'classes': ('collapse',),
        }),
    )

    def summary(self, obj):
        return '{} {}: {}'.format(obj.name, obj.email, obj.html)
