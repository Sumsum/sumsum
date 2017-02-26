import bleach
import datetime
import markdown
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from metafields.models import MetaFieldsMixin
from utils.datastructures import List
from utils.fields import StringField, TextField, ChoiceField, TransStringField, TransWysiwygField, TransHandleField, TransTagField
from yashop.middleware import get_request


COMMENTABLE_CHOICES = (
    ('no', _('Comments are disabled')),
    ('moderate', _('Comments are allowed, pending moderation')),
    ('yes', _('Comments are allowed, and are automatically published')),
)

STATUS_CHOICES = (
    ('unapproved', _('Unapproved')),
    ('pubished', _('Published')),
    ('spam', _('Spam')),
    ('removed', _('Removed')),
)


class Blog(MetaFieldsMixin, models.Model):
    commentable = ChoiceField(_('commentable'), choices=COMMENTABLE_CHOICES, help_text=_('Manage how comments are handled on this blog.'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    feedburner_location = models.URLField(_('feedburner url'), blank=True, null=True)
    handle_t = TransHandleField(_('handle'), populate_from='title_t')
    tags_t = TransTagField(_('tag'))
    template_suffix = StringField(_('template suffix'))
    title_t = TransStringField(_('title'), required=True)

    class Meta:
        ordering = ('title_t',)
        verbose_name = _('blog')
        verbose_name_plural = _('blogs')

    def __str__(self):
        return self.title

    @cached_property
    def all_tags(self):
        """
        Returns all tags of all articles of a blog. This includes tags of
        articles that are not in the current pagination view.
        """
        raise NotImplemented

    @cached_property
    def articles(self):
        """
        Returns an array of all articles in a blog.
        """
        raise NotImplemented
        return List()

    @cached_property
    def articles_count(self):
        """
        Returns the total number of articles in a blog. This total does not
        include hidden articles.
        """
        return len(self.articles)

    @cached_property
    def comments_enabled(self):
        """
        Returns true if comments are enabled, or false if they are disabled.
        """
        return self.commentable != 'no'

    @cached_property
    def feedburner(self):
        if self.feedburner_location:
            return True

    def get_absolute_url(self):
        return self.url

    @cached_property
    def moderated(self):
        """
        Returns true if comments are moderated, or false if they are not
        moderated.
        """
        return self.commentable == 'moderate'

    @cached_property
    def adjecant_articles(self):
        raise NotImplemented

    @cached_property
    def next_article(self):
        """
        Returns the URL of the next (older) post.
        Returns false if there is no next article.
        """
        return self.adjecant_articles['next']

    @cached_property
    def previous_article(self):
        """
        Returns the URL of the previous (newer) post.
        Returns false if there is no next article.
        """
        return self.adjecant_articles['previous']

    @cached_property
    def tags(self):
        """
        Returns all tags in a blog. Similar to all_tags,
        but only returns tags of articles that are in the
        filtered view.
        """
        raise NotImplemented

    @cached_property
    def url(self):
        """
        Returns the relative URL of the blog.
        """
        return '/blogs/{}'.format(self.handle)


class ArticleManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('blog')


class Article(MetaFieldsMixin, models.Model):
    user = models.ForeignKey('users.User', verbose_name=_('author'))
    blog = models.ForeignKey('blogs.Blog')
    body_html_t = TransWysiwygField(_('content'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    handle_t = TransHandleField(_('handle'), populate_from='title_t', unique_together=('handle_t', 'blog'))
    image = models.ImageField(_('image'), blank=True, null=True, upload_to='blogs')
    published_at = models.DateTimeField(_('published at'), blank=True, null=True)
    summary_html_t = TransWysiwygField(_('excerpt'))
    tags_t = TransTagField(_('tags'))
    template_suffix = StringField(_('template suffix'))
    title_t = TransStringField(_('title'), required=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    objects = ArticleManager()

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _('article')
        verbose_name_plural = _('articles')

    def __str__(self):
        return self.title

    def save(self, **kwargs):
        self.user = get_request().user
        super().save(**kwargs)

    @cached_property
    def author(self):
        """
        Returns the full name of the article's author.
        """
        return self.user.get_full_name()

    @property
    def content(self):
        """
        Returns the content of an article.
        """
        return self.body_html

    @property
    def excerpt(self):
        """
        Returns the excerpt of an article.
        """
        return self.summary_html

    @cached_property
    def excerpt_or_content(self):
        """
        Returns article.excerpt of an article if it exists. Returns
        article.content if an excerpt does not exist for the article.
        """
        return self.excerpt or self.content

    def get_absolute_url(self):
        return self.url

    @cached_property
    def moderated(self):
        """
        Returns true if the blog that the article belongs to is set to moderate
        comments. Returns false if the blog is not moderated.
        """
        return self.blog.moderated

    @cached_property
    def published(self):
        return datetime.datetime.now() >= self.published_at

    @cached_property
    def url(self):
        return '/blogs/{}/{}-{}'.format(self.blog.handle, self.pk, self.handle)


class Comment(models.Model):
    article = models.ForeignKey('blogs.Article')
    author = StringField(_('author'))
    body = TextField(_('body'), help_text=_('Markdown of a comment.'))
    body_html = TextField(_('body html'), editable=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    email = models.EmailField(_('email'), blank=True, null=True)
    ip = StringField(_('ip'))
    published_at = models.DateTimeField(_('published at'), blank=True, null=True)
    status = ChoiceField(_('status'), choices=STATUS_CHOICES)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    user_agent = StringField(_('user agent'))

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _('comment')
        verbose_name_plural = _('commments')

    def __str__(self):
        return '{} - {} - {}'.format(self.article, self.author, self.created_at.iso_format())

    def get_absolute_url(self):
        return self.url

    @cached_property
    def blog(self):
        return self.article.blog

    @cached_property
    def blog_id(self):
        return self.blog.pk

    @property
    def content(self):
        return self.body_html

    def save(self, **kwargs):
        self.body_html = bleach.clean(markdown.markdown(self.body))
        super().save(**kwargs)

    @cached_property
    def url(self):
        return '{}#{}'.format(self.blog.article.url, self.id)
