from django.db import models
from django.utils.translation import ugettext_lazy as _


STATUS_CHOICES = (
    ('pending', _('Pending')),  # The fulfillment is pending.
    ('open', _('Open')),  # The fulfillment has been acknowledged by the service and is in processing.
    ('success', _('Success')),  # The fulfillment was successful.
    ('cancelled', _('Cancelled')),  # The fulfillment was cancelled.
    ('error', _('Error')),  # There was an error with the fulfillment request.
    ('failure', _('Failure')),  # The fulfillment request failed.
)


class TrackingCompany(models.Model):
    name = models.CharField(_('name'), max_length=255)
    tracking_url = models.URLField(_('tracking url'), help_text=_('The base url for tracking a package with tracking number, this string will be used with .format, so place {} or {0} where you want the tracking number.'))

    class Meta:
        ordering = ('name',)
        verbose_name = _('tracking company')
        verbose_name_plural = _('tracking companies')

    def __str__(self):
        return self.name


class Fulfillment(models.Model):
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    # line items
    notify_customer = models.BooleanField(_('notify customer'), default=False)
    order = models.ForeignKey('orders.Order', verbose_name=_('order'))
    receipt_testcase = models.NullBooleanField(_('reciept testcase'), default=None)
    reciept_autorization = models.CharField(_('receipt authorization'), max_length=255, blank=True, null=True)
    status = models.CharField(_('status'), max_lendth=50, choices=STATUS_CHOICES, default='pending')
    tracking_company_rel = models.ForeignKey(TrackingCompany, verbose_name=_('tracking company'))
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    def tracking_company(self):
        return self.tracking_company_rel.name

    def tracking_numbers(self):
        return list(self.trackingnumber_set.values_list('number', flat=True))

    def tracking_number(self):
        return ', '.join(self.tracking_numbers())

    def tracking_urls(self):
        url = self.tracking_company_rel.tracking_url
        return [url.format(nr) for nr in self.tracking_numbers()]

    def tracking_url(self):
        return ', '.join(self.tracking_url())

    def variant_inventory_management(self):
        raise NotImplemented

    def fulfillment_line_items(self):
        raise NotImplemented

    def item_count(self):
        return len(self.fulfillment_line_items())


class TrackingNumber(models.Model):
    fulfillment_rel = models.ForeignKey(Fulfillment, verbose_name=_('fulfillment'))
    number = models.CharField(_('number'), max_length=255)

    class Meta:
        ordering = ('number',)
        verbose_name = _('tracking number')
        verbose_name_plural = _('tracking numbers')

    def __str__(self):
        return self.number
