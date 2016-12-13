from django.db import models
from redactor.fields import RedactorField
from django.utils.translation import ugettext_lazy as _
from utils.fields import TitleSlugField


WEIGHT_UNITS = (
    ('kg', _('kg')),
    ('g', _('g')),
)


ATTRIBUTE_CHOICES = (
    ('title', _('Product title')),
    ('types__title', _('Product type')),
    ('vendors__title', _('Product vendor')),
    ('price', _('Product price')),
    ('tags__title', _('Product tag')),
    ('compare_at_price', _('Compare at price')),
    ('weight', _('Weight')),
    ('inventory_stock', _('Inventory stock')),
    ('variants__title', _("Variant's title"))
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
    ('manually', _('Manually')),
    ('best_selling', _('By best selling')),
    ('title', _('Alphabetically: A-Z')),
    ('-title', _('Alphabetically: Z-A')),
    ('-price', _('By price: Highest to lowest')),
    ('price', _('By price: Lowest to highest')),
    ('-date', _('By date: Newest to oldest')),
    ('date', _('By date: Oldest to newest')),
)


class ProductManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('type', 'vendor').prefetch_related('collections', 'tags', 'images', 'options')


class Product(models.Model):
    title = models.CharField(_('title'), max_length=255, unique=True)
    slug = TitleSlugField(_('slug'))
    description = RedactorField(_('description'), blank=True)
    price = models.FloatField(_('price'), blank=True, null=True)
    compare_at_price = models.FloatField(_('compare at price'), blank=True, null=True)
    tax = models.FloatField(_('tax percent'), default=25)
    taxable = models.BooleanField(_('taxable'), default=True)
    sku = models.CharField(_('sku'), help_text=_('Stock Keeping Unit'), max_length=255, blank=True)
    barcode = models.CharField(_('barcode'), help_text=_('ISBN, UPC, GTIN, etc.'), max_length=255, blank=True)
    track_inventory = models.BooleanField(_('track inventory'), help_text=_('Yashop tracks this products inventory'), default=False)
    inventory_stock = models.IntegerField(_('inventory stock'), default=0)
    override_inventory_stock = models.BooleanField(_('override inventory stock'), help_text=_("Allow customers to purchase this product when it's out of stock"), default=False)
    requires_shipping = models.BooleanField(_('requires shipping'), help_text=_('This product requires shipping'), default=False)
    weight = models.FloatField(_('weight'), blank=True, null=True)
    weight_unit = models.CharField(_('weight unit'), max_length=255, blank=True, choices=WEIGHT_UNITS)
    page_title = models.CharField(_('page title '), max_length=255, blank=True)
    meta_description = models.TextField(_('meta description'), blank=True)
    show_online = models.BooleanField(_('show online'), help_text=_('This product is visible in the online store'), default=True)
    publish_date = models.DateTimeField(_('publish date'), help_text=_('publish this product on'), blank=True, null=True)
    collections = models.ManyToManyField('products.Collection', blank=True)
    type = models.ForeignKey('products.ProductType', verbose_name=_('product type'), blank=True, null=True)
    vendor = models.ForeignKey('products.ProductVendor', verbose_name=_('vendor'), blank=True, null=True)
    tags = models.ManyToManyField('products.ProductTag', verbose_name=_('tags'), blank=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)
    created = models.DateTimeField(_('created'), auto_now_add=True)

    objects = ProductManager()

    class Meta:
        ordering = ('title',)
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, verbose_name=_('product'), related_name='images')
    file = models.ImageField(_('image'), upload_to='products')
    position = models.IntegerField(_('position'), default=0)

    updated = models.DateTimeField(_('updated'), auto_now=True)
    created = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        ordering = ('created',)
        verbose_name = _('image')
        verbose_name_plural = _('images')

    def __str__(self):
        return self.file.name.split('/')[-1]


class ProductType(models.Model):
    title = models.CharField(_('title'), max_length=255, unique=True)
    slug = TitleSlugField(_('slug'))
    updated = models.DateTimeField(_('updated'), auto_now=True)
    created = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        ordering = ('title',)
        verbose_name = _('product type')
        verbose_name_plural = _('product types')

    def __str__(self):
        return self.title


class ProductVendor(models.Model):
    title = models.CharField(_('title'), max_length=255, unique=True)
    slug = TitleSlugField(_('slug'))
    updated = models.DateTimeField(_('updated'), auto_now=True)
    created = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        ordering = ('title',)
        verbose_name = _('vendor')
        verbose_name_plural = _('vendor')

    def __str__(self):
        return self.title


class ProductTag(models.Model):
    title = models.CharField(_('title'), max_length=255, unique=True)
    slug = TitleSlugField(_('slug'))
    updated = models.DateTimeField(_('updated'), auto_now=True)
    created = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        ordering = ('title',)
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    def __str__(self):
        return self.title


class ProductOption(models.Model):
    product = models.ForeignKey(Product, verbose_name=_('product'), related_name='options')
    title = models.CharField(_('title'), max_length=255, unique=True)
    slug = TitleSlugField(_('slug'))
    position = models.IntegerField(_('position'), default=0)
    updated = models.DateTimeField(_('updated'), auto_now=True)
    created = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        unique_together = (('slug', 'product'), ('title', 'product'))
        ordering = ('position', 'title',)
        verbose_name = _('product option')
        verbose_name_plural = _('product options')

    def __str__(self):
        return self.title


class VariantOption(models.Model):
    variant = models.ForeignKey('products.Variant', verbose_name=_('option'))
    option = models.ForeignKey(ProductOption, verbose_name=_('option'))
    value = models.CharField(_('value'), max_length=255)
    updated = models.DateTimeField(_('updated'), auto_now=True)
    created = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        unique_together = (('variant', 'option'),)
        ordering = ('variant', 'option__position',)
        verbose_name = _('variant option')
        verbose_name_plural = _('variant options')

    def __str__(self):
        return '{} {}:{}'.format(self.variant, self.option, self.value)


class Variant(models.Model):
    product = models.ForeignKey(Product, verbose_name=_('product'), related_name='variants')
    price = models.FloatField(_('price'), blank=True, null=True)
    compare_at_price = models.FloatField(_('compare at price'), blank=True, null=True)
    tax = models.FloatField(_('tax percent'), default=25)
    taxable = models.BooleanField(_('taxable'), default=True)
    sku = models.CharField(_('sku'), help_text=_('Stock Keeping Unit'), max_length=255, blank=True)
    barcode = models.CharField(_('barcode'), help_text=_('ISBN, UPC, GTIN, etc.'), max_length=255, blank=True)
    track_inventory = models.BooleanField(_('track inventory'), help_text=_('Yashop tracks this products inventory'), default=False)
    inventory_stock = models.IntegerField(_('inventory stock'), default=0)
    override_inventory_stock = models.BooleanField(_('override inventory stock'), help_text=_("Allow customers to purchase this product when it's out of stock"), default=False)
    requires_shipping = models.BooleanField(_('requires shipping'), help_text=_('This product requires shipping'), default=False)
    weight = models.FloatField(_('weight'), blank=True, null=True)
    weight_unit = models.CharField(_('weight unit'), max_length=255, blank=True)
    image = models.ImageField(_('image'), upload_to='products', blank=True)
    position = models.IntegerField(_('position'), default=0)
    updated = models.DateTimeField(_('updated'), auto_now=True)
    created = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        ordering = ('product',)
        verbose_name = _('variant')
        verbose_name_plural = _('variants')

    def __str__(self):
        return self.title


class Collection(models.Model):
    title = models.CharField(_('title'), max_length=255, unique=True)
    slug = TitleSlugField(_('slug'))
    description = RedactorField(_('description'), blank=True)
    sort = models.CharField(_('sort'), max_length=255, choices=SORT_CHOICES, blank=True)
    page_title = models.CharField(_('page title '), max_length=255, blank=True)
    meta_description = models.TextField(_('meta description'), blank=True)
    show_online = models.BooleanField(_('show online'), help_text=_('This collection is visible in the online store'), default=True)
    publish_date = models.DateTimeField(_('publish date'), help_text=_('publish this collection on'), blank=True, null=True)
    any_condition = models.BooleanField(_('product match any condition'), default=False)
    updated = models.DateTimeField(_('updated'), auto_now=True)
    created = models.DateTimeField(_('created'), auto_now_add=True)

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
    collection = models.ForeignKey('products.Product', verbose_name=_('collection'))
    product_attribute = models.CharField(_('product attribute'), max_length=255, blank=True, choices=ATTRIBUTE_CHOICES)
    relation = models.CharField(_('relation'), max_length=255, blank=True, choices=RELATION_CHOICES)
    value = models.CharField(_('value'), max_length=255)
    position = models.IntegerField(_('position'), default=0)
    updated = models.DateTimeField(_('updated'), auto_now=True)
    created = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        unique_together = (('collection', 'product_attribute', 'relation', 'value'))
        ordering = ('position', '-created')
        verbose_name = _('collection condition')
        verbose_name_plural = _('collection conditions')

    def __str__(self):
        return '{} - {} {} {}'.format(self.collection, self.product_attribute, self.relation, self.value)
