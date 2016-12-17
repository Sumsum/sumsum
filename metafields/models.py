from django.db import models
from django.utils.translation import ugettext_lazy as _
from utils.text import uncamel
from django.utils.functional import cached_property


VALUE_CHOICES = (
    ('integer', _('Integer')),
    ('string', _('String')),
)


RESOURCE_CHOICES = (
    ('blog', _('Blog')),
    ('custom-collection', _('Custom Collection')),
    ('customer', _('Customer')),
    ('order', _('Order')),
    ('page', _('Page')),
    ('product', _('Product')),
    ('product-variant', _('Product Variant')),
)


class MetaField(models.Model):
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    description = models.CharField(_('description'), max_length=255, blank=True, null=True)
    key = models.CharField(_('key'), max_length=30)
    namespace = models.CharField(_('namespace'), max_length=20, blank=True, null=True)
    owner_id = models.PositiveIntegerField(_('owner id'))
    owner_resource = models.CharField(_('owner resource'), max_length=50, choices=RESOURCE_CHOICES)
    value_type = models.CharField(_('value type'), max_length=50, choices=VALUE_CHOICES)
    value = models.TextField(_('value'))

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _('metafield')
        verbose_name_plural = _('metafields')

    def __str__(self):
        if self.namespace:
            return '{}.{} for {}.{}'.format(self.namespace, self.key, self.owner_resource, self.owner_id)
        return '{} for {}.{}'.format(self.key, self.owner_resource, self.owner_id)


class MetaFieldMixin:
    @cached_property
    def metafields(self):
        return MetaField.objects.filter(
            owner_resource=uncamel(self.__class__.__name__),
            owner_id=self.pk
        )
