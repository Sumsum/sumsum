from .fields import MetaField
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from utils.datastructures import NSDict


class MetaFieldsMixin(models.Model):
    metafields_json = MetaField(_('metafields'), help_text=_('Enter key value pairs as namespace.key: value on separate lines.'))

    @cached_property
    def metafields(self):
        return NSDict(self.metafields_json)

    class Meta:
        abstract = True
