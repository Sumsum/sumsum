from django.contrib.postgres.fields import HStoreField
from .yaml import YAMLJSONField


class HStoreField(HStoreField):
    def __init__(self, verbose_name=None, **kwargs):
        kwargs.setdefault('blank', True)
        kwargs.setdefault('default', {})
        super().__init__(verbose_name=verbose_name, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        return name, 'django.contrib.postgres.fields.HStoreField', args, kwargs

    def formfield(self, **kwargs):
        kwargs.setdefault('form_class', YAMLJSONField)
        return super().formfield(**kwargs)
