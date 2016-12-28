from django.contrib.postgres.fields import JSONField
from .yaml import YAMLJSONField


class JSONField(JSONField):
    def __init__(self, verbose_name=None, **kwargs):
        kwargs.setdefault('blank', True)
        kwargs.setdefault('default', {})
        super().__init__(verbose_name=verbose_name, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        return name, 'django.contrib.postgres.fields.JSONField', args, kwargs

    def formfield(self, **kwargs):
        kwargs.setdefault('form_class', YAMLJSONField)
        return super().formfield(**kwargs)
