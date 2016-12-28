from django.contrib.postgres.fields import JSONField
from utils.fields import YAMLMetaField
from django.utils.translation import ugettext_lazy as _


class MetaField(JSONField):
    def __init__(self, verbose_name=None, **kwargs):
        verbose_name = verbose_name or _('metafields')
        kwargs.setdefault('blank', True)
        kwargs.setdefault('default', {})
        super().__init__(verbose_name=verbose_name, **kwargs)

    def deconstruct(self):
        return super().deconstruct()

    def formfield(self, **kwargs):
        defaults = {
            'form_class': YAMLMetaField,
        }
        defaults.update(kwargs)
        return super(JSONField, self).formfield(**defaults)
