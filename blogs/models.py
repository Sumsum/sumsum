from django.db import models
from django.utils.translation import ugettext_lazy as _
from metafields.models import MetaFieldsMixin
from utils.fields import StringField, ChoiceField, HandleField
from django.contrib.postgres.fields import ArrayField
from django.utils.functional import cached_property
from utils.datastructures import List


COMMENTABLE_CHOICES = (
    ('no', _('No')),
    ('moderate', _('Moderate')),
    ('yes', _('Yes')),
)


class Blog(MetaFieldsMixin, models.Model):
    commentable = ChoiceField(_('commentable'), choices=COMMENTABLE_CHOICES)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    feedburner = models.NullBooleanField(_('feedburner'), default=None)
    feedburner_location = models.URLField(_('feedburner location'), blank=True, null=True)
    handle = HandleField(_('handle'), from_field='title', unique=False)
    tags = ArrayField(StringField(_('tag'), required=True), verbose_name=_('tags'), default=[])
    template_suffix = StringField(_('template suffix'))
    title = StringField(_('title'), required=True)

    class Meta:
        ordering = ('title',)
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
