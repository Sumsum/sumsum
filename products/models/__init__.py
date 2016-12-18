from .collection import CustomCollection, CollectionCondition  # NOQA
from .product import Product  # NOQA
from .variant import ProductVariant  # NOQA
from django.db import models
from django.utils.functionan import cached_property
from django.utils.translation import ugettext_lazy as _
from metafields.models import MetaFieldMixin
from utils.fields import StringField, PositionField


PUBLICATION_CHOICES = (
    ('global', _('Online store')),
)


class Tag(models.Model):
    name = StringField(_('title'), required=True, primary_key=True)

    class Meta:
        ordering = ('name',)
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    def __str__(self):
        return self.name


class ProductImage(MetaFieldMixin, models.Model):
    alt = StringField(_('alt text'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    file = models.ImageField(_('image'), upload_to='products')
    position = PositionField()
    product = models.ForeignKey('products.Product', verbose_name=_('product'))
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = _('product image')
        verbose_name_plural = _('product images')

    def __str__(self):
        return self.image.name.split('/')[-1]

    @cached_property
    def attached_to_variant(self):
        # we could use .count but then the prefetch will not have cached
        # the queryset result
        return bool(len(self.variants_m2m.all()))

    def get_absolute_url(self):
        return self.file.url

    @cached_property
    def src(self):
        return self.file.url

    @cached_property
    def variant_ids(self):
        return [v.pk for v in self.variants]

    @cached_property
    def variants(self):
        return list(self.variant_set.all())
