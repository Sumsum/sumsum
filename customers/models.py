from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from metafields.models import MetaFieldMixin
from users.models import User
from utils.fields import StringField, CountryField


class CustomerManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        qs.prefetch_related('customeraddress_set', 'tags_m2m').select_related('default_address')


class Customer(MetaFieldMixin, User):
    objects = CustomerManager()

    class Meta:
        proxy = True

    @cached_property
    def addresses(self):
        """
        Returns an array of all addresses associated with a customer. See
        customer_address for a full list of available attributes.
        """
        return list(self.customeraddress_set.all())

    @cached_property
    def addresses_count(self):
        """
        Returns the number of addresses associated with a customer.
        """
        return len(self.addresses)

    @cached_property
    def default_address(self):
        """
        Returns the default customer_address.
        """
        if self.addresses:
            return self.addresses[0]

    @cached_property
    def has_account(self):
        """
        Returns true if the email associated with an order is also tied to a
        customer account. Returns false if it is not. Helpful in email
        templates. In the theme, that will always be true.
        """
        return True

    @cached_property
    def last_order(self):
        """
        Returns the last order placed by the customer, not including test
        orders.
        """
        if self.orders_count:
            return self.orders[0]

    @cached_property
    def last_order_id(self):
        """
        The id of the customer's last order.
        """
        if self.last_order:
            return self.last_order.pk

    @cached_property
    def last_order_name(self):
        """
        The name of the customer's last order. This is directly related to the
        Order's name field.
        """
        if self.last_order:
            return self.last_order.name

    @cached_property
    def name(self):
        """
        Alias for get_full_name
        """
        return self.get_full_name()

    @cached_property
    def orders(self):
        """
        Returns an array of all orders placed by the customer.
        """
        return list(self.order_set.all())

    @cached_property
    def orders_count(self):
        """
        Returns the total number of orders a customer has placed.
        """
        return len(self.orders)

    @cached_property
    def tags(self):
        """
        Returns the list of tags associated with the customer.
        """
        return [t.name for t in self.tags_m2m.all()]

    @cached_property
    def total_spent(self):
        """
        Returns the total amount spent on all orders.
        """
        raise NotImplemented


class CustomerAddress(models.Model):
    address1 = StringField(_('address'))
    address2 = StringField(_("address con't"))
    city = StringField(_('city'))
    company = StringField(_('company'))
    country_code = CountryField(_('country'), blank=True, null=True)
    customer = models.ForeignKey(Customer, verbose_name=_('customer'), blank=True, null=True)
    first_name = StringField(_('first name'))
    last_name = StringField(_('last name'))
    phone = StringField(_('phone'))
    province = StringField(_('region'))
    province_code = StringField(_('region code'))
    zip = StringField(_('postal / Zip code'))

    class Meta:
        ordering = ('first_name', 'last_name')
        verbose_name = _('customer address')
        verbose_name_plural = _('customer addresses')

    def __str__(self):
        return self.name

    @cached_property
    def country_name(self):
        if self.contry_code:
            return self.country_code.name

    @property
    def country(self):
        """
        Alias to country_name
        """
        return self.country_name

    @cached_property
    def latitude(self):
        """
        https://help.shopify.com/api/reference/order
        latitude: The latitude of the billing address.
        """
        raise NotImplemented

    @cached_property
    def longitude(self):
        """
        https://help.shopify.com/api/reference/order
        The longitude of the billing address.
        """
        raise NotImplemented

    @cached_property
    def name(self):
        """
        Returns the full name
        """
        return ' '.join(filter(None, [self.first_name, self.last_name]))

    @cached_property
    def street(self):
        """
        Returns the combined values of the Address1 and Address2 fields of the
        address.
        """
        return ' '.join(filter(None, self.address1, self.address2))


class Tag(models.Model):
    name = StringField(_('title'), required=True, primary_key=True)

    class Meta:
        ordering = ('name',)
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    def __str__(self):
        return self.name
