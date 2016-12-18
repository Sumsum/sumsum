from django.db import models
from django.utils.translation import ugettext_lazy as _
from utils.fields import StringField, ChoiceField
from django.utils.functional import cached_property


TYPE_CHOICES = (
    ('fixed_amount', _('SEK')),
    ('percentage', _('% Discount')),
    ('shipping', _('Free shipping')),
)


#RESOURCE_CHOICES = (
#    ('all', _('all orders')),
#    ('minimum_order_amount', _('orders over')),
#    ('collection', _('collection')),
#    ('product', _('product')),
#    ('variant', _('product variant')),
#    ('customer_group', _('customer group')),
#    ('free_shipping_all', _('Free shipping all countries')),
#    ('free_shipping_rest', _('Free shipping rest of the world')),
#    ('free_shipping_sweden', _('Free shipping Sweden')),
#)


RESOURCE_CHOICES = (
    ('product', _('Product')),
    ('smart_collection', _('SmartCollection')),
    ('customersavedsearch', _('CustomerSavedSearch')),
    ('custom_collection', _('CustomCollection')),
)


STATUS_CHIOCES = (
    ('enabled', _('Enabled')),
    ('disabled', _('Disabled')),
    ('depleted', _('Depleted')),
)


class Discount(models.Model):
    applies_once = models.BooleanField(_('limit to one usage'), default=False)
    applies_once_per_customer = models.BooleanField(_('limit 1 per customer'), default=False)
    applies_to_id = models.PositiveIntegerField(_('applies to id'), blank=True, null=True)
    applies_to_resource = ChoiceField(_('applies to resource'), choices=RESOURCE_CHOICES)
    code = StringField(_('code'), required=True, unique=True)
    discount_type = ChoiceField(_('type'), choices=TYPE_CHOICES)
    ends_at = models.DateField(_('end date'), blank=True, null=True)
    minimum_order_amount = models.FloatField(_('minimum order amount'), null=True, blank=True)
    starts_at = models.DateField(_('start date'), blank=True, null=True)
    status = ChoiceField(_('status'), choices=STATUS_CHIOCES)
    times_used = models.PositiveIntegerField(_('times used'), blank=True, null=True)
    usage_limit = models.PositiveIntegerField(_('total available'), blank=True, null=True)
    value = models.FloatField(_('value'), null=True, blank=True)

    class Meta:
        ordering = ('-starts_at', 'code')
        verbose_name = _('discount')
        verbose_name_plural = _('discounts')

    def __str__(self):
        return self.code

    def amount(self):
        """
        Returns the amount of the discount. Use one of the money filters to
        return the value in a monetary format.
        """
        raise NotImplemented

    @cached_property
    def title(self):
        """
        Alias of the discount code
        """
        return self.code

    def total_amount(self):
        """
        Returns the total amount of the discount if it has been applied to
        multiple line items. Use a money filter to return the value in a
        monetary format.
        """
        raise NotImplemented

    def savings(self):
        """
        Returns the amount of the discount's savings. The negative opposite of
        amount. Use one of the money filters to return the value in a monetary
        format.
        """
        raise NotImplemented

    def total_savings(self):
        """
        Returns the total amount of the discount's savings if it has been
        applied to multiple line items. The negative opposite of total_amount.
        Use a money filter to return the value in a monetary format.
        """
        raise NotImplemented

    @cached_property
    def type(self):
        """
        Returns the type of the discount.
        """
        mapping = {
            'fixed_amount': 'FixedAmountDiscount',
            'percentage': 'PercentageDiscount',
            'shipping': 'ShippingDiscount',
        }
        return mapping[self.discount_type]
