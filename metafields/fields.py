from django import forms
from utils.fields import JSONField
from utils.fields import YAMLJSONField


class YAMLMetaField(YAMLJSONField):
    """
    YAML Metafields form field
    """
    def to_python(self, value):
        obj = super().to_python(value)
        for k, v in obj.items():
            if not isinstance(k, str):
                raise forms.ValidationError('Error "{}" is not a sting key.'.format(k))
            if '.' not in k:
                raise forms.ValidationError('Error "{}" key is missing namespace denoted with a "."'.format(k))
            if not isinstance(v, (str, int)):
                raise forms.ValidationError('Error "{}" is not a string or integer value.'.format(v))
        return obj


class MetaField(JSONField):
    """
    Metafields models field
    """
    def deconstruct(self):
        name, path, args, kwargs = super(JSONField, self).deconstruct()
        return name, 'django.contrib.postgres.fields.jsonb.JSONField', args, kwargs

    def formfield(self, **kwargs):
        kwargs.setdefault('form_class', YAMLMetaField)
        return super().formfield(**kwargs)
