from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from metafields.models import MetaFieldsMixin
from utils.fields import StringField, RedactorField, HandleField
from yashop.middleware import get_request


class Page(MetaFieldsMixin, models.Model):
    author = models.ForeignKey('users.User', verbose_name=_('author'))
    body_html = RedactorField(_('description'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    handle = HandleField(_('handle'), from_field='title', unique=False)
    published_at = models.DateTimeField(_('published at'), blank=True, null=True)
    shop = models.ForeignKey('shops.Shop', blank=True, null=True)
    template_suffix = StringField(_('template suffix'))
    title = StringField(_('title'), required=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        unique_together = ('handle', 'shop')
        ordering = ('title',)
        verbose_name = _('page')
        verbose_name_plural = _('pages')

    def __str__(self):
        return self.title

    @property
    def content(self):
        return self.body_html

    def get_absolute_url(self):
        return self.url

    def save(self, **kwargs):
        self.author = get_request().user
        super().save(**kwargs)

    @cached_property
    def url(self):
        return '/pages/{}'.format(self.handle)
