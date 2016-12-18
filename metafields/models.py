from django.db import models
from django.utils.translation import ugettext_lazy as _
from utils.text import uncamel
from django.utils.functional import cached_property
from utils.fields import StringField, ChoiceField, TextField


VALUE_CHOICES = (
    ('string', _('String')),
    ('integer', _('Integer')),
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
    description = StringField(_('description'))
    key = StringField(_('key'), max_length=30, required=True)
    namespace = StringField(_('namespace'), max_length=20)
    owner_id = models.PositiveIntegerField(_('owner id'))
    owner_resource = ChoiceField(_('owner resource'), choices=RESOURCE_CHOICES)
    value = TextField(_('value'))
    value_type = ChoiceField(_('value type'), choices=VALUE_CHOICES)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

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
