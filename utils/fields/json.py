from django.contrib.postgres.fields import JSONField
from django import forms
from django.conf import settings
from .yaml import YAMLJSONField


class JSONField(JSONField):
    def __init__(self, verbose_name=None, **kwargs):
        kwargs.setdefault('blank', True)
        kwargs.setdefault('default', {})
        super().__init__(verbose_name=verbose_name, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        return name, 'django.contrib.postgres.fields.jsonb.JSONField', args, kwargs

    def formfield(self, **kwargs):
        kwargs.setdefault('form_class', YAMLJSONField)
        return super().formfield(**kwargs)


class TransStringWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = []
        for code, name in settings.LANGUAGES:
            widgets.append(forms.TextInput())
        super().__init__(widgets, attrs)

    def decompress(self, value):
        value = value or {}
        data_list = []
        for code, lang in settings.LANGUAGES:
            data_list.append(value.get(code, None))
        return data_list


class TransStringFormField(forms.MultiValueField):
    widget = TransStringWidget

    def __init__(self, label=None, max_length=None, min_length=None, strip=True, *args, **kwargs):
        self.max_length = max_length
        print(max_length, min_length, 'stasrtas')
        self.min_length = min_length
        self.strip = strip
        fields = []
        for code, name in settings.LANGUAGES:
            fields.append(
                forms.CharField(
                    label=name,
                    max_length=max_length, min_length=min_length,
                    strip=strip,
                    *args, **kwargs
                )
            )
        super().__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        data_list = data_list or []
        value = {}
        for j, v in enumerate(data_list):
            code = settings.LANGUAGES[j][0]
            value[code] = v
        return value


class TransStringField(JSONField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 255)
        required = kwargs.pop('required', False)
        kwargs.setdefault('blank', not required)
        kwargs.setdefault('null', not required)
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        return name, 'django.contrib.postgres.fields.jsonb.JSONField', args, kwargs

    def formfield(self, **kwargs):
        kwargs.setdefault('form_class', TransStringFormField)
        return super().formfield(**kwargs)
