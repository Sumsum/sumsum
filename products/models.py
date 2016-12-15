from django.db import models
from redactor.fields import RedactorField
from django.utils.translation import ugettext_lazy as _
from utils.fields import TitleSlugField
from metafields.models import MetaFieldMixin


UNIT_CHOICES = (
    ('oz', _('oz')),
    ('lb', _('lb')),
    ('kg', _('kg')),
    ('g', _('g')),
)


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


FULFILLMENT_CHOICES = (
    ('manual', _('Manual')),
)

INVENTORY_MANAGEMENT_CHOICES = (
    ('blank', _("Don't track inventory'")),
    ('shopify', _("YAShop tracks this product's inventory")),
)

INVENTORY_POLICY_CHOICES = (
    ('deny', _("Do not allow")),
    ('continue', _("Allow")),
)


class ProductManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.prefetch_related('collections', 'tags', 'images', 'options')


class Product(MetaFieldMixin, models.Model):
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    description = RedactorField(_('description'), blank=True, null=True)
    handle = TitleSlugField(_('handle'))
    metafields_global_description_tag = models.TextField(_('meta description'), blank=True, null=True)
    metafields_global_title_tag = models.CharField(_('page title'), max_length=255, blank=True, null=True)
    product_type = models.CharField(_('product type'), max_length=255, blank=True, null=True)  # this might need a related table
    published_at = models.DateTimeField(_('publish on'), help_text=_('publish this product on'), blank=True, null=True)
    published_scope = models.CharField(_('visability'), max_length=50, choices=SCOPE_CHOICES)
    tags_m2m = models.ManyToManyField('products.ProductTag', verbose_name=_('tags'), blank=True)  # can we implement this as an ArrayField?
    template_suffix = models.CharField(_('template suffix'), max_length=255, blank=True, null=True)  # we probably do not need this
    title = models.CharField(_('title'), max_length=255)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    vendor = models.CharField(_('vendor'), blank=True, null=True)

    objects = ProductManager()

    class Meta:
        ordering = ('title',)
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def __str__(self):
        return self.title

    @property
    def body_html(self):
        """
        Alias for description
        """
        return self.description

    @property
    def content(self):
        """
        Alias for description
        """
        return self.description

    def availble(self):
        """
        Returns True if at least one variant is available
        """
        for v in self.variants():
            if v.availble():
                return True
        return False


class Variant(MetaFieldMixin, models.Model):
    product = models.ForeignKey(Product, verbose_name=_('product'), related_name='variants')
    barcode = models.CharField(_('barcode'), help_text=_('ISBN, UPC, GTIN, etc.'), max_length=255, blank=True, null=True)
    compare_at_price = models.FloatField(_('compare at price'), blank=True, null=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    fulfillment_service = models.CharField(_('Fulfillment service'), max_length=50, choices=FULFILLMENT_CHOICES)
    grams = models.IntegerField(_('grams'), blank=True, null=True)
    image = models.ForeignKey('products.ProductImage', verbose_name=_('image'), blank=True, null=True, related_name='variants')
    inventory_management = models.CharField(_('track inventory'), help_text=_('Yashop tracks this products inventory'), max_length=50, choices=INVENTORY_MANAGEMENT_CHOICES, default='blank')
    inventory_policy = models.BooleanField(_('inventory policy'), help_text=_("Allow customers to purchase this product when it's out of stock"), max_length=50, choices=INVENTORY_POLICY_CHOICES, default='deny')
    inventory_quantity = models.IntegerField(_('inventory stock'), default=0)
    option1 = models.CharField(_('option #1'), max_length=255, blank=True, null=True)
    option2 = models.CharField(_('option #2'), max_length=255, blank=True, null=True)
    option3 = models.CharField(_('option #3'), max_length=255, blank=True, null=True)
    position = models.IntegerField(_('position'), default=0)
    price = models.FloatField(_('price'), blank=True, null=True)
    requires_shipping = models.BooleanField(_('requires shipping'), help_text=_('This product requires shipping'), default=False)
    sku = models.CharField(_('sku'), help_text=_('Stock Keeping Unit'), max_length=255, blank=True, null=True)
    taxable = models.BooleanField(_('taxable'), default=True)
    title = models.CharField(_('title'), max_length=255)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    grams = models.FloatField(_('weight in grams'), blank=True, null=True)
    weight_in_unit = models.FloatField(_('weight'), blank=True, null=True)
    weight_unit = models.CharField(_('weight unit'), max_length=50, choices=UNIT_CHOICES, default='kg')

    class Meta:
        ordering = ('product',)
        verbose_name = _('variant')
        verbose_name_plural = _('variants')

    def __str__(self):
        return self.title

    def availble(self):
        """
        Returns True if the variant is available for purchase, or False if it
        not. For a variant to be available, its variant.inventory_quantity must
        be greater than zero or variant.inventory_policy must be set to
        continue. A variant with no variant.inventory_management is also
        considered available.
        """
        if self.inventory_management == 'blank' or self.inventory_policy == 'continue':
            return True
        return self.inventory_quantity > 0


class ProductTag(models.Model):
    name = models.CharField(_('title'), max_length=255, primary_key=True)

    class Meta:
        ordering = ('name',)
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    def __str__(self):
        return self.name


class ProductImage(MetaFieldMixin, models.Model):
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    image = models.ImageField(_('image'), upload_to='products')
    position = models.IntegerField(_('position'), default=0)
    product = models.ForeignKey(Product, verbose_name=_('product'), related_name='images')
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = _('image')
        verbose_name_plural = _('images')

    def __str__(self):
        return self.image.name.split('/')[-1]

    @property
    def src(self):
        return self.image.url

    @property
    def variant_ids(self):
        return list(self.variants.values_list('pk', flat=True))


class CustomCollection(MetaFieldMixin, models.Model):
    body_html = RedactorField(_('description'), blank=True, null=True)
    handle = models.SlugField(_('handle'), unique=True)
    image = models.ImageField(_('image'), upload_to='products')
    published = models.BooleanField(_('published'))
    published_at = models.DateTimeField(_('published at'), help_text=_('publish this collection on'), blank=True, null=True)
    published_scope = models.CharField(_('visability'), max_length=50, choices=SCOPE_CHOICES)
    sort_order = models.CharField(_('sort'), max_length=255, choices=SORT_CHOICES, blank=True)
    template_suffix = models.CharField(_('template suffix'), max_length=255, blank=True, null=True)  # we probably do not need this
    title = models.CharField(_('title'), max_length=255)
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
    collection = models.ForeignKey('products.CustomCollection', verbose_name=_('collection'), related_name='conditions')
    attribute = models.CharField(_('attribute'), max_length=255, blank=True, choices=ATTRIBUTE_CHOICES)
    relation = models.CharField(_('relation'), max_length=255, blank=True, choices=RELATION_CHOICES)
    value = models.CharField(_('value'), max_length=255)
    position = models.IntegerField(_('position'), default=0)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        unique_together = (('collection', 'product_attribute', 'relation', 'value'))
        ordering = ('position', '-created_at')
        verbose_name = _('collection condition')
        verbose_name_plural = _('collection conditions')

    def __str__(self):
        return '{} - {} {} {}'.format(self.collection, self.attribute, self.relation, self.value)
