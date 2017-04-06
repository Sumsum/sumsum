import datetime
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from metafields.models import MetaFieldsMixin
from utils.fields import ChoiceField, StringField, PositionField
from sumsum.middleware import get_request


UNIT_CHOICES = (
    ('oz', _('oz')),
    ('lb', _('lb')),
    ('kg', _('kg')),
    ('g', _('g')),
)

INVENTORY_MANAGEMENT_CHOICES = (
    ('blank', _("Don't track inventory")),
    ('shopify', _("Sumsum tracks this product's inventory")),
)

INVENTORY_POLICY_CHOICES = (
    ('deny', _("Do not allow")),
    ('continue', _("Allow")),
)


class ProductVariant(MetaFieldsMixin, models.Model):
    barcode = StringField(_('barcode'), help_text=_('ISBN, UPC, GTIN, etc.'))
    compare_at_price = models.FloatField(_('compare at price'), blank=True, null=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    fulfillment_service = models.ForeignKey('fulfillments.FulfillmentService', blank=True, null=True)
    image = models.ForeignKey('products.ProductImage', verbose_name=_('image'), blank=True, null=True)
    inventory_management = ChoiceField(_('track inventory'), help_text=_('Sumsum tracks this products inventory'), choices=INVENTORY_MANAGEMENT_CHOICES)
    inventory_policy = ChoiceField(_('inventory policy'), help_text=_("Allow customers to purchase this product when it's out of stock"), choices=INVENTORY_POLICY_CHOICES)
    inventory_quantity = models.IntegerField(_('quantity'), default=0)
    next_incoming_date = models.DateField(_('next incoming date'), blank=True, null=True)
    option1 = StringField(_('option #1'))
    option2 = StringField(_('option #2'))
    option3 = StringField(_('option #3'))
    position = PositionField()
    price = models.FloatField(_('price'), default=0)
    product = models.ForeignKey('products.Product', verbose_name=_('product'))
    requires_shipping = models.BooleanField(_('requires shipping'), help_text=_('This product requires shipping'), default=False)
    sku = StringField(_('sku'), help_text=_('Stock Keeping Unit'))
    taxable = models.BooleanField(_('taxable'), default=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    weight_in_unit = models.FloatField(_('weight'), blank=True, null=True)
    weight_unit = ChoiceField(_('weight unit'), choices=UNIT_CHOICES, default='kg')

    class Meta:
        ordering = ('product',)
        verbose_name = _('variant')
        verbose_name_plural = _('variants')

    def __str__(self):
        return self.title

    @cached_property
    def grams(self):
        """
        The weight of the product variant in grams.
        """
        if not self.weight_in_unit:
            return None
        unit_factor = {
            'g': 1,
            'kg': 1000,
            'oz': 28.349523125,
            'lb': 453.59237,
        }
        return unit_factor[self.weight_unit] * self.weight_in_unit

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

    def get_absulute_url(self):
        raise '{}?variant={}'.format(self.product.get_absolute_url(), self.pk)

    @cached_property
    def incoming(self):
        """
        Returns true if the variant has incoming inventory.
        """
        return self.next_incoming_date and self.next_incoming_date >= datetime.date.today()

    def selected(self):
        """
        Returns true if the variant is currently selected by the ?variant= URL
        parameter, or false if it is not.
        """
        request = get_request()
        return self.pk == request.GET.get('variant')

    @cached_property
    def title(self):
        """
        Returns the concatenation of all the variant's option values, joined by
        / characters.
        """
        return ' / '.join(filter(None, [self.option1, self.option2, self.option3]))

    @cached_property
    def url(self):
        return self.get_absolute_url()
