from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from metafields.models import MetaFieldMixin
from utils.fields import HandleField, StringField, ChoiceField, RedactorField
from utils.datastructures import List
from yashop.middleware import get_request
from django.contrib.postgres.fields import ArrayField


PUBLICATION_CHOICES = (
    ('global', _('Online store')),
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
        return qs.prefetch_related('collections_m2m', 'tags_m2m', 'productvariant_set', 'productimage_set')


class Product(MetaFieldMixin, models.Model):
    body_html = RedactorField(_('description'))
    collections_m2m = models.ManyToManyField('products.CustomCollection', through='products.Collect', blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    handle = HandleField(_('handle'), from_field='title')
    # sh*pify probably has a related table implementation, is this good enough?
    option1_name = StringField(_('option #1 name'))
    option2_name = StringField(_('option #2 name'))
    option3_name = StringField(_('option #3 name'))
    product_type = StringField(_('product type'))  # this might need a related table
    published = models.BooleanField(_('published'), default=True)
    published_at = models.DateTimeField(_('published at'), help_text=_('publish this product on'), blank=True, null=True)
    published_scope = ChoiceField(_('visability'), choices=PUBLICATION_CHOICES)
    tags = ArrayField(StringField(_('tag'), required=True), verbose_name=_('tags'), default=[])
    template_suffix = StringField(_('template suffix'))
    title = StringField(_('title'), blank=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    vendor = StringField(_('vendor'), blank=True, null=True)

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
        Returns true if a product is available for purchase. Returns falseif
        all of the products variants' inventory_quantity values are zero or
        less, and their inventory_policy is not set to "Allow users to purchase
        this item, even if it is no longer in stock."
        """
        for v in self.variants():
            if v.availble():
                return True
        return False

    @cached_property
    def compare_at_prices(self):
        return List([v.compare_at_price for v in self.variants()])

    @cached_property
    def compare_at_price_max(self):
        """
        Returns the highest compare at price. Use one of the money filters to
        return the value in a monetary format.
        """
        if self.compare_at_prices:
            return max(self.compare_at_prices)

    @cached_property
    def compare_at_price_min(self):
        """
        Returns the lowest compare at price. Use one of the money filters to
        return the value in a monetary format.
        """
        if self.compare_at_prices:
            return min(self.compare_at_prices)

    @cached_property
    def compare_at_price_varies(self):
        """
        Returns true if the compare_at_price_min is different from the
        compare_at_price_max. Returns false if they are the same.
        """
        return self.compare_at_price_max != self.compare_at_price_min

    @cached_property
    def collections(self):
        return List(self.collections_m2m.all())

    @property
    def content(self):
        """
        Alias for body_html
        """
        return self.body_html

    @property
    def description(self):
        """
        Alias for body_html
        """
        return self.body_html

    @cached_property
    def featured_image(self):
        """
        Returns the relative URL of the product's featured image.
        """
        if self.images:
            return self.image[0].file.url

    @cached_property
    def first_variant(self):
        if self.variants:
            return self.variants[0]

    @cached_property
    def first_available_variant(self):
        """
        Returns the variant object of the first product variant that is
        available for purchase. In order for a variant to be available, its
        variant.inventory_quantity must be greater than zero or
        variant.inventory_policy must be set to continue. A variant with no
        inventory_policy is considered available.
        """
        for v in self.variants:
            if v.available:
                return v

    def get_absolute_url(self):
        return '/products/{}'.format(self.handle)

    @cached_property
    def images(self):
        """
        Returns an array of the product's images. Use the product_img_url
        filter to link to the product image on Shopify's Content Delivery
        Network.
        """
        return List(self.productimage_set.all())

    @cached_property
    def options(self):
        """
        Returns an array of the product's option names.
        """
        names = [self.option1_name, self.option2_name, self.option3_name]
        return List([n for n in names if n])

    @cached_property
    def options_with_values(self):
        """
        Returns an array of the product's options including their available and
        currently selected values.
        """
        opts = List()
        if self.option1_name:
            values = [v.option1 for v in self.variants if v.option1]
            opts.append(Option(self.option1_name, values))
        if self.option2_name:
            values = [v.option2 for v in self.variants if v.option2]
            opts.append(Option(self.option2_name, values))
        if self.option3_name:
            values = [v.option3 for v in self.variants if v.option3]
            opts.append(Option(self.option3_name, values))
        return opts

    @property
    def price(self):
        """
        Alias for price_min
        """
        return self.price_min

    @cached_property
    def price_max(self):
        """
        Returns the highest price of the product. Use one of the money filters
        to return the value in a monetary format.
        """
        if self.prices:
            return max(self.prices)

    @cached_property
    def price_min(self):
        """
        Returns the lowest price of the product. Use one of the money filters
        to return the value in a monetary format.
        """
        if self.prices:
            return min(self.prices)

    @cached_property
    def price_varies(self):
        """
        Returns true if the product's variants have varying prices. Returns
        false if all of the product's variants have the same price.
        """
        return self.price_max != self.price_min

    @cached_property
    def prices(self):
        return [v.price for v in self.variants()]

    @cached_property
    def selected_variant(self):
        """
        Returns the variant object of the currently-selected variant if there
        is a valid ?variant= parameter in the URL. Returns nil if there is not.
        """
        request = get_request()
        variant_id = request.GET.get('variant')
        for v in self.variants:
            if variant_id == v.pk:
                return v

    @cached_property
    def selected_or_first_available_variant(self):
        """
        Returns the variant object of the currently-selected variant if there
        is a valid ?variant= query parameter in the URL. If there is no
        selected variant, the first available variant is returned. In order for
        a variant to be available, its variant.inventory_quantity must be
        greater than zero or variant.inventory_policy must be set to continue.
        A variant with no inventory_management is considered available.
        """
        request = get_request()
        if 'variant' in request.GET:
            return self.selected_variant
        return self.first_available_variant

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
        """
        Returns an array the product's variants.
        """
        return List(self.productvariant_set.all())
