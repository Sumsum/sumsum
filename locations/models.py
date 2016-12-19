from django.db import models
from utils.fields import StringField, CountryField
from django.utils.translation import ugettext_lazy as _


class Location(models.Model):
    address1 = StringField(_('address'))
    address2 = StringField(_("address con't"))
    city = StringField(_('city'))
    company = StringField(_('company'))
    country = CountryField(_('country'), blank=True, null=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    last_name = StringField(_('last name'))
    name = StringField(_('name'))
    phone = StringField(_('phone'))
    province = StringField(_('region'))
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    zip = StringField(_('postal / Zip code'))

    class Meta:
        ordering = ('name',)
        verbose_name = _('location')
        verbose_name_plural = _('locations')

    def __str__(self):
        return self.name
