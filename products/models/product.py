from django.db import models
from django.utils.functionan import cached_property
from django.utils.translation import ugettext_lazy as _
from metafields.models import MetaFieldMixin
from redactor.fields import RedactorField
from utils.datastructures import List
from utils.fields import HandleField, ChoiceField, StringField


SCOPE_CHOICES = (
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
