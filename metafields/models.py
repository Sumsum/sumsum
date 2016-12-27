from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from utils.datastructures import NSDict
from utils.fields import HStoreField


class MetaFieldsMixin(models.Model):
    metafields_hstore = HStoreField(_('metafields'), help_text=_('Enter key value pairs as namespace.key: value on separate lines.'))

    @cached_property
    def metafields(self):
        return NSDict(self.metafields_hstore)

    class Meta:
        abstract = True
