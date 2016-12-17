import datetime
from django.db import models
from redactor.fields import RedactorField
from django.utils.translation import ugettext_lazy as _
from utils.fields import HandleField, ChoiceField, StringField, PositionField
from metafields.models import MetaFieldMixin
from django.utils.functionan import cached_property
from utils.datastructures import List


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


class Option:
    def __init__(self, name, values, selected_value=None):
        self.name = name
        self.values = values
        # TODO How do we solve this the ruby way?
        self.selected_value = selected_value


class ProductManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.prefetch_related('collections_m2m', 'tags_m2m', 'variant_set', 'productimage_set')


class Product(MetaFieldMixin, models.Model):
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    collections_m2m = models.ManyToMany('products.Collection', blank=True)
    body_html = RedactorField(_('description'), blank=True, null=True)
    handle = HandleField(_('handle'), from_field='title')
    metafields_global_description_tag = models.TextField(_('meta description'), blank=True, null=True)
    metafields_global_title_tag = StringField(_('page title'))
    product_type = StringField(_('product type'))  # this might need a related table
    published_at = models.DateTimeField(_('publish on'), help_text=_('publish this product on'), blank=True, null=True)
    published_scope = ChoiceField(_('visability'), choices=SCOPE_CHOICES)
    tags_m2m = models.ManyToManyField('products.ProductTag', verbose_name=_('tags'), blank=True)  # can we implement this as an ArrayField?
    template_suffix = StringField(_('template suffix'))
    title = StringField(_('title'), blank=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    vendor = StringField(_('vendor'), blank=True, null=True)
    option1_name = StringField(_('option #1 name'))
    option2_name = StringField(_('option #2 name'))
    option3_name = StringField(_('option #3 name'))

    objects = ProductManager()

    class Meta:
        ordering = ('title',)
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def __str__(self):
        return self.title

    @cached_property
    def availble(self):
        """
        Returns True if at least one variant is available
        """
        for v in self.variants():
            if v.availble():
                return True
        return False

    @cached_property
    def compare_at_prices(self):
        return [v.compare_at_price for v in self.variants()]

    @cached_property
    def compare_at_price_max(self):
        if self.compare_at_prices:
            return max(self.compare_at_prices)

    @cached_property
    def compare_at_price_min(self):
        if self.compare_at_prices:
            return min(self.compare_at_prices)

    @cached_property
    def compare_at_price_varies(self):
        return self.compare_at_price_max != self.compare_at_price_min

    @cached_property
    def collections(self):
        return self.collections_m2m.all()

    @property
    def content(self):
        return self.body_html

    @property
    def description(self):
        return self.body_html

    @cached_property
    def featured_image(self):
        if self.images:
            return self.image[0].file.url

    @cached_property
    def first_variant(self):
        if self.variants:
            return self.variants[0]

    @cached_property
    def first_available_variant(self):
        for v in self.variants:
            if v.available:
                return v

    def get_absolute_url(self):
        return '/product/{}'.format(self.handle)

    @cached_property
    def images(self):
        return self.productimage_set.all()

    @cached_property
    def options(self):
        names = [self.option1_name, self.option2_name, self.option3_name]
        return List([n for n in names if n])

    @cached_property
    def options_with_values(self):
        opts = []
        if self.option1_name:
            values = [v.option1 for v in self.variants() if v.option1]
            opts.append(Option(self.option1_name, values))
        if self.option2_name:
            values = [v.option2 for v in self.variants() if v.option2]
            opts.append(Option(self.option2_name, values))
        if self.option3_name:
            values = [v.option3 for v in self.variants() if v.option3]
            opts.append(Option(self.option3_name, values))
        return opts

    @cached_property
    def prices(self):
        return [v.price for v in self.variants()]

    @cached_property
    def price_max(self):
        if self.compare_at_prices:
            return max(self.compare_at_prices)

    @cached_property
    def price_min(self):
        if self.prices:
            return min(self.prices)

    @property
    def price(self):
        """
        Alias for price_min
        """
        return self.price_min

    @cached_property
    def price_varies(self):
        return self.price_max != self.price_min

    def selected_variant(self):
        raise NotImplemented

    def selected_or_first_available_variant(self):
        raise NotImplemented

    @cached_property
    def tags(self):
        return [t.name for t in self.tags_m2m.all()]

    @property
    def type(self):
        """
        Alias for product_type
        """
        return self.product_type

    @cached_property
    def url(self):
        """
        Alias for get_absolute_url
        """
        return self.get_absolute_url()

    @cached_property
    def variants(self):
        return self.variant_set.all()


class Variant(MetaFieldMixin, models.Model):
    product = models.ForeignKey(Product, verbose_name=_('product'))
    barcode = StringField(_('barcode'), help_text=_('ISBN, UPC, GTIN, etc.'))
    compare_at_price = models.FloatField(_('compare at price'), blank=True, null=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    fulfillment_service = models.ForeignKey('fullfillments.FulfillmentService', blank=True, null=True)
    grams = models.IntegerField(_('grams'), blank=True, null=True)
    image = models.ForeignKey('products.ProductImage', verbose_name=_('image'), blank=True, null=True)
    next_incoming_date = models.DateField(_('next incoming date'), blank=True, null=True)
    inventory_management = ChoiceField(_('track inventory'), help_text=_('Yashop tracks this products inventory'), choices=INVENTORY_MANAGEMENT_CHOICES)
    inventory_policy = ChoiceField(_('inventory policy'), help_text=_("Allow customers to purchase this product when it's out of stock"), choices=INVENTORY_POLICY_CHOICES)
    inventory_quantity = models.IntegerField(_('inventory stock'), default=0)
    option1 = StringField(_('option #1'))
    option2 = StringField(_('option #2'))
    option3 = StringField(_('option #3'))
    position = PositionField()
    price = models.FloatField(_('price'), blank=True, null=True)
    requires_shipping = models.BooleanField(_('requires shipping'), help_text=_('This product requires shipping'), default=False)
    sku = StringField(_('sku'), help_text=_('Stock Keeping Unit'))
    taxable = models.BooleanField(_('taxable'), default=True)
    title = StringField(_('title'), blank=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    grams = models.FloatField(_('weight in grams'), blank=True, null=True)
    weight_in_unit = models.FloatField(_('weight'), blank=True, null=True)
    weight_unit = ChoiceField(_('weight unit'), choices=UNIT_CHOICES, default='kg')

    class Meta:
        ordering = ('product',)
        verbose_name = _('variant')
        verbose_name_plural = _('variants')

    def __str__(self):
        return self.title

    @cached_property
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

    @cached_property
    def incoming(self):
        return datetime.date.today() >= self.next_incoming_date


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
    product = models.ForeignKey(Product, verbose_name=_('product'))
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
