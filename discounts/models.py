from django.db import models
from django.utils.translation import ugettext_lazy as _


TYPE_CHOICES = (
    ('fixed_amount', _('SEK')),
    ('percentage', _('% Discount')),
    ('shipping', _('Free shipping')),
)

RESOURCE_CHOICES = (
    ('all', _('all orders')),
    ('minimum_order_amount', _('orders over')),
    ('collection', _('collection')),
    ('product', _('product')),
    ('variant', _('product variant')),
    ('customer_group', _('customer group')),
    ('free_shipping_all', _('Free shipping all countries')),
    ('free_shipping_rest', _('Free shipping rest of the world')),
    ('free_shipping_sweden', _('Free shipping Sweden')),
)


class Discount(models.Model):
    code = models.CharField(_('code'), max_length=255, unique=True)
    total_available = models.PositiveIntegerField(_('total available'), blank=True, null=True)
    one_per_customer = models.BooleanField(_('limit 1 per customer'), default=False)
    start = models.DateField(_('start date'), blank=True, null=True)
    end = models.DateField(_('end date'), blank=True, null=True)
    type = models.CharField(_('type'), max_length=255, blank=True, choices=TYPE_CHOICES)
    value = models.CharField(_('value'), max_length=255)
    resource = models.CharField(_('resource'), max_length=255)
    updated = models.DateTimeField(_('updated'), auto_now=True)
    created = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        ordering = ('-start',)
        verbose_name = _('discount')
        verbose_name_plural = _('discounts')

    def __str__(self):
        return self.code
