from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from utils.choices import CURRENCY_CHOICES
from utils.fields import StringField, CountryField, ChoiceField, TimeZoneField, TextField
from metafields.models import MetaFieldsMixin


PLAN_CHOICES = (
    ('trial', _('Trail')),
    ('affiliate', _('Trial from Partner')),
    ('basic', _('Basic Shopify')),
    ('professional', _('Shopify')),
    ('unlimited', _('Advanced Shopify')),
    ('enterprise', _('Shopify Plus')),
)


PAYMENT_TYPES_CHOICES = (
    ('visa', _('Visa')),
    ('master', _('Master card')),
    ('american_express', _('American express')),
    ('paypal', _('PayPal')),
    ('jcb', _('Jcb')),
    ('diners_club', _('Diners Club')),
    ('maestro', _('Maestro')),
    ('discover', _('Discover')),
    ('dankort', _('Dankort')),
    ('forbrugsforeningen', _('Forbrugsforeningen')),
    ('dwolla', _('Dwolla')),
    ('bitcoin', _('Bitcoin')),
    ('dogecoin', _('Dogecoin')),
    ('litecoin', _('Litecoin')),
)


class Shop(MetaFieldsMixin, models.Model):
    address1 = StringField(_('address'))
    address2 = StringField(_("address con't"))
    city = StringField(_('city'))
    county_taxes = models.NullBooleanField(_('county taxes'))
    country_code = CountryField(_('country'), blank=True, null=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    currency = ChoiceField(_('currency'), choices=CURRENCY_CHOICES)
    customer_email = models.EmailField(_('customer email'), blank=True, null=True)
    description = TextField(_('description'))
    domain = StringField(_('domain'))
    email = models.EmailField(_('email'), blank=True, null=True)
    enabled_payment_types = ArrayField(ChoiceField(_('payment type'), choices=PAYMENT_TYPES_CHOICES), verbose_name=_('enabled payment types'), default=[])
    force_ssl = models.BooleanField(_('force ssl'), default=False)
    google_apps_domain = StringField(_('google apps domain'))
    google_apps_login_enabled = models.NullBooleanField(_('google apps login enabled'), default=None)
    iana_timezone = TimeZoneField(_('timezone'))
    latitude = models.FloatField(_('latitude'), blank=True, null=True)
    longitude = models.FloatField(_('longitude'), blank=True, null=True)
    money_format = StringField(_('money format'))
    money_with_currency_format = StringField(_('money with currency format'))
    myshopify_domain = StringField(_('my shopify domain'))
    name = StringField(_('name'))
    navigation = JSONField(_('navigation'), default={})
    password_enabled = models.BooleanField(_('password enabled'), default=False)
    password_message = TextField(_('password message'))
    phone = StringField(_('phone'))
    plan_name = ChoiceField(_('plan name'), choices=PLAN_CHOICES)
    primary_locale = StringField(_('primary locale'), max_length=10)
    permanent_domain = StringField(_('permanent domain'))
    province = StringField(_('region'))
    province_code = StringField(_('region code'))
    shop_owner = StringField(_('shop owner'))
    tax_shipping = models.BooleanField(_('tax shipping'), default=True)
    taxes_included = models.NullBooleanField(_('taxes included'), default=True)
    live_theme = models.ForeignKey('shops.Theme', verbose_name=_('live theme'), blank=True, null=True, related_name='shop_live_theme')
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    zip = StringField(_('postal / Zip code'))

    class Meta:
        verbose_name = _('shop')
        verbose_name_plural = _('shops')
        ordering = ('name',)

    def __str__(self):
        return self.name

    @cached_property
    def collections_count(self):
        """
        Returns the number of collections in a shop.
        """
        raise NotImplemented

    @property
    def country(self):
        """
        Alias to country_name
        """
        return self.country_name

    @cached_property
    def country_name(self):
        """
        The shop's normalized country name.
        """
        if self.contry_code:
            return self.country_code.name

    @cached_property
    def country_upper(self):
        """
        Returns the country in the shop's address using uppercase letters.
        """
        return self.country.upper()

    def get_absolute_url(self):
        return self.url

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
    def has_storefront(self):
        """
        Indicates whether the shop has web-based storefront or not.
        """
        raise NotImplemented

    @cached_property
    def locale(self):
        """
        Returns the locale that the shop is currently displayed in (ex: en, fr,
        pt-BR).
        """
        return self.primary_locale

    @cached_property
    def plan_display_name(self):
        """
        The display name of the Shopify plan the shop is on.
        """
        return self.get_plan_name_display()

    @cached_property
    def products_count(self):
        """
        Returns the number of products in a shop.
        """
        raise NotImplemented

    @cached_property
    def setup_required(self):
        """
        Indicates whether the shop has any outstanding setup steps or not.
        """
        raise NotImplemented

    @cached_property
    def secure_url(self):
        """
        Returns the full URL of a shop prepended by the https protocol.
        Example: https://johns-apparel.com
        """
        return 'https://{}'.format(self.domain)

    @cached_property
    def source(self):
        """
        ?
        """
        return None

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

    @cached_property
    def timezone(self):
        """
        The name of the timezone the shop is in.
        """
        # do something with self.iana_timezone
        raise NotImplemented

    @cached_property
    def types(self):
        """
        Returns an array of all unique product types in a shop.
        """
        raise NotImplemented

    @cached_property
    def url(self):
        """
        Returns the full URL of a shop.
        Example: http://johns-apparel.com
        """
        return 'http://{}'.format(self.domain)

    @cached_property
    def vendors(self):
        """
        Returns an array of all unique vendors in a shop.
        """
        raise NotImplemented


class Theme(models.Model):
    name = StringField(_('name'), required=True)
    path = StringField(_('path relative template directory'), required=True)
    settings = JSONField(_('settings'), default={})
    shop = models.ForeignKey('shops.Shop')

    class Meta:
        verbose_name = _('theme')
        verbose_name_plural = _('themes')
        ordering = ('shop', 'name')

    def __str__(self):
        return '{} - {}'.format(self.shop, self.name)
