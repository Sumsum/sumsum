import datetime
import hashlib
import uuid
from django.db import models
from utils.fields import StringField, ChoiceField, TextField
from django.utils.translation import ugettext_lazy as _
from utils.choices import CURRENCY_CHOICES
from django.utils.functional import cached_property
from utils.datastructures import List


CANCEL_CHOICES = (
    (None, ''),
    ('customer', _('The customer changed or cancelled the order')),
    ('fraud', _('The order was fraudulen')),
    ('inventory', _('Items in the order were not in inventory')),
    ('other', _('The order was cancelled for a reason not in the list above')),
)


FINANCIAL_STATUS_CHOICES = (
    ('pending', _('Pending')),
    ('autorized', _('Authorized')),
    ('partially_paid', _('Partially paid')),
    ('paid', _('Paid')),
    ('partially_refunded', _('Partially refunded')),
    ('refunded', _('Refunded')),
    ('voided', _('Voided')),
)

FULFILLMENT_STATUS_CHOICES = (
    ('fulfilled', _('All lines fulfilled')),  # Every line item in the order has been fulfilled.
    ('null', _('No lines fulfilled')),  # None of the line items in the order have been fulfilled.
    ('partial', _('Some lines fulfilled')),  # At least one line item in the order has been fulfilled.
)

PROCESSING_CHOICES = (
    ('checkout', _('Checkout')),
    ('direct', _('Direct')),
    ('manual', _('Manual')),
    ('offsite', _('Offsite')),
    ('express', _('Express')),
)


def get_token():
    return hashlib.md5(str(uuid.uuid1()).encode('utf8')).hexdigest()


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
    billing_address = models.ForeignKey('customers.CustomerAddress', related_name='order_billing_address_set')
    browser_ip = StringField(_('browser ip'))
    buyer_accepts_marketing = models.BooleanField(_('buyer accepts marketing'), default=False)
    cancel_reason = ChoiceField(_('cancel reason'), choices=CANCEL_CHOICES)
    cancelled_at = models.DateTimeField(_('cancelled at'), blank=True, null=True)
    cart_token = StringField(_('cart token'), required=True)
    client_details = models.ForeignKey('orders.ClientDetail', verbose_name=_('client details'))
    closed_at = models.DateTimeField(_('closed at'), blank=True, null=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    currency = ChoiceField(_('currency'), choices=CURRENCY_CHOICES)
    customer = models.ForeignKey('customers.Customer', blank=True, null=True, related_name='order_billing_addresss_set')
    discounts_m2m = models.ManyToManyField('discounts.Discount', blank=True)
    email = models.EmailField(_('email'), blank=True, null=True)
    financial_status = ChoiceField(_('financial status'), choices=FINANCIAL_STATUS_CHOICES)
    fulfillment_status = ChoiceField(_('fulfilment status'), choices=FULFILLMENT_STATUS_CHOICES)
    tags_m2m = models.ManyToManyField('orders.Tag', blank=True)
    landing_site = models.URLField(_('landing site'), blank=True, null=True)
    # line items
    location = models.ForeignKey('locations.Location', blank=True, null=True)
    order_number = models.PositiveIntegerField(_('number'), editable=False)  # its nice to be searchable
    note = TextField(_('note'))
    processed_at = models.DateTimeField(_('processed at'), blank=True)
    processing_method = ChoiceField(_('processing method'), choices=PROCESSING_CHOICES)
    referring_site = models.URLField(_('referring site'), blank=True, null=True)
    # Do we need to lock this value somehow, infact all related models should be 'locked' on finalization
    shipping_address = models.ForeignKey('customers.CustomerAddress', blank=True, null=True, related_name='order_shipping_address_set')
    source_name = StringField(_('source name'), default='api')
    subtotal_price = models.FloatField(_('subtotal price'))
    taxes_included = models.BooleanField(_('taxes included'))
    token = models.CharField(_('token'), max_length=32, default=get_token, editable=False)
    # All of these total fields are probably better of being calculated values, let's keep
    # normalizing at a minimum since it requires more thinking power
    total_discounts = models.FloatField(_('total discounts'), default=0)
    total_line_items_price = models.FloatField(_('total line items price'))
    total_price = models.FloatField(_('total price'))
    total_tax = models.FloatField(_('total tax'))
    total_weight = models.FloatField(_('total weight'))
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    user = models.ForeignKey('users.User', blank=True, null=True)
    order_status_url = models.URLField(_('order status url'), blank=True, null=True)

    @cached_property
    def cancel_reason_label(self):
        return self.get_cancel_reason_label()

    @cached_property
    def cancelled(self):
        return self.cancelled_at is not None

    @cached_property
    def customer_url(self):
        """
        Returns the URL of the customer's account page.
        https://help.shopify.com/themes/liquid/objects/order#order-customer_url
        """
        raise NotImplemented

    @cached_property
    def discounts(self):
        return List(self.discounts_m2m.all())

    @cached_property
    def discount_codes(self):
        codes = []
        for d in self.discouns:
            codes.append({
                'amount': d.amount(),
                'code': d.code,
                'type': d.discount_type,
            })
        return codes

    @cached_property
    def financial_status_label(self):
        return self.get_financial_status_label()

    @cached_property
    def fulfillment_status_label(self):
        return self.get_fulfillment_status_label()

    @cached_property
    def fulfillments(self):
        return List(self.fullfillment_set.all())

    @property
    def gateway(self):
        """
        Deprecated as of July 14, 2014. This information is instead available
        on transactions The payment gateway used.
        """
        return ''

    @cached_property
    def name(self):
        """
        The customer's order name as represented by a number.
        """
        return '#{}'.format(self.number)

    @cached_property
    def note_attributes(self):
        return List(self.noteattributes_set.all())

    @cached_property
    def number(self):
        """
        Numerical identifier unique to the shop. A number is sequential and
        starts at 1000.

        The example shows number 1, it is a little unclear what this is for.
        """
        return self.pk

    @cached_property
    def payment_details(self):
        """
        Deprecated.
        This information is instead available on transactions An object
        containing information about the payment.
        """
        return {
            "avs_result_code": None,
            "credit_card_bin": None,
            "cvv_result_code": None,
            "credit_card_number": None,
            "credit_card_company": None,
        }

    @cached_property
    def payment_gateway_names(self):
        """
        This should fetch information from the related transaction
        """
        raise NotImplemented

    @cached_property
    def refunds(self):
        """
        The list of refunds applied to the order.
        """
        #return List(self.refund_set.all())
        raise NotImplemented

    def save(self, **kwargs):
        self.order_number = self.pk + 999
        if not self.processed_at:
            self.processed_at = datetime.datetime.now()
        super().save(**kwargs)

    @cached_property
    def shipping_lines(self):
        """
        An array of shipping_line objects, each of which details the shipping
        methods used.

        """
        raise NotImplemented

    @cached_property
    def tags(self):
        return List([t.name for t in self.tags_m2m.all()])

    @cached_property
    def tax_lines(self):
        """
        An array of tax_line objects, each of which details the total taxes
        applicable to the order.

        https://help.shopify.com/api/reference/order#tax-lines-property
        """
        raise NotImplemented

    @cached_property
    def tax_price(self):
        return self.total_tax


class Tag(models.Model):
    name = StringField(_('title'), required=True, primary_key=True)

    class Meta:
        ordering = ('name',)
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    def __str__(self):
        return self.name


class NoteAttributes(models.Model):
    order = models.ForeignKey('orders.Order')
    name = StringField(_('name'), required=True)
    value = StringField(_('value'), required=True)

    class Meta:
        unique_together = ('order', 'name')
        ordering = ('name',)
        verbose_name = _('note attribute')
        verbose_name_plural = _('note attributes')

    def __str__(self):
        return '{} - {}'.format(self.order, self.name)
