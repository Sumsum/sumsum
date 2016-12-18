from django.db import models
from utils.fields import StringField, ChoiceField
from django.utils.translation import ugettext_lazy as _
from utils.choices import CURRENCY_CHOICES


CANCEL_CHOICES = (
    (None, ''),
    ('customer', _('The customer changed or cancelled the order')),
    ('fraud', _('The order was fraudulen')),
    ('inventory', _('Items in the order were not in inventory')),
    ('other', _('The order was cancelled for a reason not in the list above')),
)


class ClientDetail(models.Model):
    accept_language = StringField(_('accept language'))
    browser_height = StringField(_('browser height'))
    browser_ip = StringField(_('browser ip'))
    browser_width = StringField(_('browser width'))
    session_hash = StringField(_('sessian hash'))
    user_agent = StringField(_('user agent'))

    class Meta:
        ordering = ('pk',)
        verbose_name = ('client detail')
        verbose_name_plural = ('client details')

    def __str__(self):
        return 'ClientDetail.{}'.format(self.pk)


class Order(models.Model):
    billing_address = models.ForeignKey('customer.CustomerAddress')
    browser_ip = StringField(_('browser ip'))
    buyer_accepts_marketing = models.BooleanField(_('buyer accepts marketing'), default=False)
    cancel_reason = ChoiceField(_('cancel reason'), choices=CANCEL_CHOICES)
    cancelled_at = models.DateTimeField(_('cancelled at'), blank=True, null=True)
    cart_token = StringField(_('cart token'), required=True)
    client_details = models.ForeignKey('orders.ClientDetail', verbose_name=_('client details'))
    closed_at = models.DateTimeField(_('closed at'), blank=True, null=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    currency = ChoiceField(_('currency'), choices=CURRENCY_CHOICES)
    customer = models.ForeignKey('customers.Customer', blank=True, null=True)

