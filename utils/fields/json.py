from .yaml import YAMLJSONField
from django import forms
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.template.loader import render_to_string
from django.utils.text import mark_safe
from django.utils.translation import get_language
from django.utils.functional import curry


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


def get_field_translation(self, field):
    data = getattr(self, field.attname)
    value = data.get(get_language(), None)
    if not value:
        value = data.get(settings.LANGUAGE_CODE, None)
    return value


class TransStringWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = []
        attrs = attrs or {}
        attrs.setdefault('class', '')
        attrs['class'] += ' vTextField'
        for code, name in settings.LANGUAGES:
            widgets.append(forms.TextInput(attrs=attrs))
        super().__init__(widgets, attrs)

    def decompress(self, value):
        value = value or {}
        data_list = []
        for code, lang in settings.LANGUAGES:
            data_list.append(value.get(code, None))
        return data_list

    def format_output(self, rendered_widgets):
        labels = [name for code, name in settings.LANGUAGES]
        rows = list(zip(labels, rendered_widgets))
        html = render_to_string('utils/transstring.html', {'rows': rows})
        return mark_safe(html)


class TransStringFormField(forms.MultiValueField):
    """
    Multi language form field, required means the first language is required,
    require_all_fields means that all fields are required.
    """
    widget = TransStringWidget

    def __init__(self, label=None, max_length=None, min_length=None, strip=True, require_all_fields=False, required=False, *args, **kwargs):
        self.max_length = max_length
        self.min_length = min_length
        self.strip = strip
        fields = []
        required_field = required or require_all_fields
        for code, name in settings.LANGUAGES:
            f = forms.CharField(
                max_length=max_length, min_length=min_length,
                strip=strip, required=required_field,
                *args, **kwargs
            )
            fields.append(f)
            if not require_all_fields:
                required_field = False
        kwargs['label'] = label
        kwargs['required'] = required or require_all_fields
        kwargs['require_all_fields'] = require_all_fields
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
        self.require_all_fields = kwargs.pop('require_all_fields', False)
        kwargs.setdefault('blank', not required)
        kwargs.setdefault('null', not required)
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        return name, 'django.contrib.postgres.fields.jsonb.JSONField', args, kwargs

    def formfield(self, **kwargs):
        kwargs.setdefault('form_class', TransStringFormField)
        kwargs.setdefault('max_length', self.max_length)
        kwargs.setdefault('require_all_fields', self.require_all_fields)
        return super().formfield(**kwargs)

    def contribute_to_class(self, cls, *args, **kwargs):
        super().contribute_to_class(cls, *args, **kwargs)
        if self.column:
            attr = self.attname.rsplit('_', 1)[0]
            if not getattr(cls, attr, None):
                setattr(cls, attr, property(curry(get_field_translation, field=self)))
