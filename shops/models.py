from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from utils.fields import StringField, CountryField, ChoiceField, TimeZoneField
from utils.choices import CURRENCY_CHOICES


PLAN_CHOICES = (
    ('trial', _('Trail')),
    ('affiliate', _('Trial from Partner')),
    ('basic', _('Basic Shopify')),
    ('professional', _('Shopify')),
    ('unlimited', _('Advanced Shopify')),
    ('enterprise', _('Shopify Plus')),
)


class Shop(models.Model):
    address1 = StringField(_('address'))
    address2 = StringField(_("address con't"))
    city = StringField(_('city'))
    country_code = CountryField(_('country'), blank=True, null=True)
    province = StringField(_('region'))
    province_code = StringField(_('region code'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    customer_email = models.EmailField(_('customer email'), blank=True, null=True)
    currency = ChoiceField(_('currency'), choices=CURRENCY_CHOICES)
    domain = StringField(_('domain'))
    email = models.EmailField(_('email'), blank=True, null=True)
    google_apps_domain = StringField(_('google apps domain'))
    google_apps_login_enabled = models.NullBooleanField(_('google apps login enabled'), default=None)
    latitude = models.FloatField(_('latitude'), blank=True, null=True)
    longitude = models.FloatField(_('longitude'), blank=True, null=True)
    money_format = StringField(_('money format'))
    money_with_currency_format = StringField(_('money with currency format'))
    myshopify_domain = StringField(_('my shopify domain'))
    name = StringField(_('name'))
    plan_name = ChoiceField(_('plan name'), choices=PLAN_CHOICES)
    password_enabled = models.BooleanField(_('password enabled'), default=False)
    phone = StringField(_('phone'))
    primary_locale = StringField(_('primary locale'), max_length=2)
    province = StringField(_('region'))
    province_code = StringField(_('region code'))
    shop_owner = StringField(_('shop owner'))
    force_ssl = models.BooleanField(_('force ssl'), default=False)
    tax_shipping = models.BooleanField(_('tax shipping'), default=True)
    taxes_included = models.NullBooleanField(_('taxes included'), default=True)
    iana_timezone = TimeZoneField(_('timezone'))
    zip = StringField(_('postal / Zip code'))

    @cached_property
    def has_storefront(self):
        """
        Indicates whether the shop has web-based storefront or not.
        """
        raise NotImplemented

    @cached_property
    def setup_required(self):
        """
        Indicates whether the shop has any outstanding setup steps or not.
        """
        raise NotImplemented

    @cached_property
    def timezone(self):
        """
        The name of the timezone the shop is in.
        """
        # do something with self.iana_timezone
        raise NotImplemented

    @cached_property
    def source(self):
        """
        ?
        """
        return None

    @cached_property
    def has_discounts(self):
        """
        Indicates if any active discounts exist for the shop.
        """
        raise NotImplemented

    @cached_property
    def has_gift_cards(self):
        """
        Indicates if any active gift cards exist for the shop.
        """
        raise NotImplemented

    @cached_property
    def plan_display_name(self):
        """
        The display name of the Shopify plan the shop is on.
        """
        return self.get_plan_name_display()

    @cached_property
    def country_name(self):
        """
        The shop's normalized country name.
        """
        if self.contry_code:
            return self.country_code.name

    @property
    def country(self):
        """
        Alias to country_name
        """
        return self.country_name

    @cached_property
    def street(self):
        """
        Returns the combined values of the Address1 and Address2 fields of the
        address.
        """
        return ' '.join(filter(None, self.address1, self.address2))

    @cached_property
    def summary(self):
        """
        Returns a summary of the shop's address:

        150 Elgin Street, Ottawa, Ontario, Canada

        The summary takes the form street, city, state/province, country.
        """
        return ', '.join([self.street, self.city, self.province, self.country])
