from .collection import CustomCollection, CollectionRule  # NOQA
from .product import Product  # NOQA
from .variant import ProductVariant  # NOQA
from django.contrib.postgres.fields import HStoreField
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from utils.fields import StringField, PositionField


PUBLICATION_CHOICES = (
    ('global', _('Online store')),
)


class ProductImage(models.Model):
    alt = StringField(_('alt text'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    file = models.ImageField(_('image'), upload_to='products')
    metafields = HStoreField()
    position = PositionField()
    product = models.ForeignKey('products.Product', verbose_name=_('product'))
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _('product image')
        verbose_name_plural = _('product images')

    def __str__(self):
        return self.src

    @cached_property
    def attached_to_variant(self):
        """
        Returns true if the image has been associated with a
        variant. Returns false otherwise. This can be used in cases
        where you want to create a gallery of images that are not
        associated with variants.
        """
        return bool(len(self.productvariant_set.all()))

    def get_absolute_url(self):
        return self.file.url

    @cached_property
    def src(self):
        """
        Returns the relative path of the product image. This is the
        same as outputting {{ image }}
        """
        return self.file.url

    @cached_property
    def variant_ids(self):
        return [v.pk for v in self.variants]

    @cached_property
    def variants(self):
        """
        Returns the variant object(s) that the image is associated with.
        """
        return list(self.productvariant_set.all())
