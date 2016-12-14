from django.db import models
from users.models import User
from metafields.models import MetaFieldMixin
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField


class Customer(MetaFieldMixin, User):
    class Meta:
        proxy = True

    def last_order_name(self):
        if self.last_order:
            return self.last_order.name

    def order_count(self):
        """
        This probably needs to be normalized
        """
        return self.orders.all().count()

    def total_spent(self):
        # TODO calculate some total number from all orders
        #return self.orders.all()
        pass


class CustomerTag(models.Model):
    name = models.CharField(_('title'), max_length=255, primary_key=True)

    class Meta:
        ordering = ('name',)
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    def __str__(self):
        return self.name


class CustomerAddress(models.Model):
    customer = models.ForeignKey(Customer, verbose_name=_('customer'))
    address1 = models.CharField(_('address'), max_length=255, blank=True, null=True)
    address2 = models.CharField(_("address con't"), max_length=255, blank=True, null=True)
    city = models.CharField(_('city'), max_length=255, blank=True, null=True)
    company = models.CharField(_('company'), max_length=255, blank=True, null=True)
    country_code = CountryField(_('country'), blank=True, null=True)
    first_name = models.CharField(_('first name'), max_length=255, blank=True, null=True)
    last_name = models.CharField(_('last name'), max_length=255, blank=True, null=True)
    name = models.CharField(_('name'), max_length=255, blank=True, null=True)
    phone = models.CharField(_('phone'), max_length=255, blank=True, null=True)
    province = models.CharField(_('region'), max_length=255, blank=True, null=True)
    province_code = models.CharField(_('region code'), max_length=255, blank=True, null=True)
    zip = models.CharField(_('postal / Zip code'), max_length=255, blank=True, null=True)

    @property
    def country(self):
        if self.contry_code:
            return self.country_code.name

    class Meta:
        ordering = ('name',)
        verbose_name = _('customer address')
        verbose_name_plural = _('customer addresses')

    def __str__(self):
        return self.name
