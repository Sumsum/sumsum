from .product import Product  # NOQA
from .variant import Variant  # NOQA
from django.db import models
from django.utils.functionan import cached_property
from django.utils.translation import ugettext_lazy as _
from metafields.models import MetaFieldMixin
from redactor.fields import RedactorField
from utils.fields import HandleField, ChoiceField, StringField, PositionField


ATTRIBUTE_CHOICES = (
    ('product__title', _('Product title')),
    ('product__product_type', _('Product type')),
    ('product__vendor', _('Product vendor')),
    ('price', _('Product price')),
    ('product__tags__name', _('Product tag')),
    ('compare_at_price', _('Compare at price')),
    ('weight', _('Weight')),
    ('inventory_quantity', _('Inventory stock')),
    ('title', _("Variant's title"))
)


RELATION_CHOICES = (
    ('', _('Is equal to')),
    ('exclude:', _('is not equal to')),
    ('__gt', _('is greater than')),
    ('__lt', _('is less than')),
    ('__istartswith', _('starts with')),
    ('__icontains', _('contains')),
    ('exclude:__icontains', _('does not contain')),
)


SORT_CHOICES = (
    ('manual', _('Manually')),
    ('best-selling', _('By best selling')),
    ('alpha-asc', _('Alphabetically: A-Z')),
    ('alpha-desc', _('Alphabetically: Z-A')),
    ('price-desc', _('By price: Highest to lowest')),
    ('price-asc', _('By price: Lowest to highest')),
    ('created-desc', _('By date: Newest to oldest')),
    ('created', _('By date: Oldest to newest')),
)


SCOPE_CHOICES = (
    ('global', _('Online store')),
)


class ProductTag(models.Model):
    name = StringField(_('title'), required=True)

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
        return self.variant_set.all()


class Collection(MetaFieldMixin, models.Model):
    body_html = RedactorField(_('description'), blank=True, null=True)
    handle = HandleField(_('handle'), from_field='title')
    image = models.ImageField(_('image'), upload_to='products')
    published = models.BooleanField(_('published'))
    published_at = models.DateTimeField(_('published at'), help_text=_('publish this collection on'), blank=True, null=True)
    published_scope = ChoiceField(_('visability'), choices=SCOPE_CHOICES)
    sort_order = ChoiceField(_('sort'), choices=SORT_CHOICES)
    template_suffix = StringField(_('template suffix'))
    title = StringField(_('title'), required=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    # fields not in Shopify API
    products_match_any_condition = models.BooleanField(_('products can match any condition'), default=False)

    class Meta:
        ordering = ('-title',)
        verbose_name = _('collection')
        verbose_name_plural = _('collections')

    def __str__(self):
        return self.title


class CollectionCondition(models.Model):
    """
    We include products in collections according to the conditions defined here which
    means that we need to recalculate the collections everytime a product is updated.
    We also need to re calculate whenever a rule is updated.
    """
    collection = models.ForeignKey('products.Collection', verbose_name=_('collection'), related_name='conditions')
    attribute = ChoiceField(_('attribute'), choices=ATTRIBUTE_CHOICES)
    relation = ChoiceField(_('relation'), choices=RELATION_CHOICES)
    value = StringField(_('value'), blank=False)
    position = PositionField()
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        unique_together = (('collection', 'attribute', 'relation', 'value'))
        ordering = ('position', '-created_at')
        verbose_name = _('collection condition')
        verbose_name_plural = _('collection conditions')

    def __str__(self):
        return '{} - {} {} {}'.format(self.collection, self.attribute, self.relation, self.value)
