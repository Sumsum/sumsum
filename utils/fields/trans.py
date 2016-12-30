from .base import WysiwygWidget
from django import forms
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.core import exceptions
from django.template.loader import render_to_string
from django.utils.functional import curry
from django.utils.text import mark_safe
from django.utils.translation import get_language
from inspect import signature


__all__ = ('TransStringField', 'TransWysiwygField', 'TransTagField')


def get_field_translation(self, field):
    data = getattr(self, field.attname)
    try:
        return data.get(get_language())
    except AttributeError:
        return data.get(settings.LANGUAGE_CODE, None)


def valid_kwargs(f, kwargs):
    valid_kwargs = {}
    for key in signature(f).parameters.keys():
        if key in kwargs:
            valid_kwargs[key] = kwargs[key]
    return valid_kwargs


class TransWidget(forms.MultiWidget):
    template = 'utils/trans_widget.html'

    def __init__(self, widget):
        widgets = (widget,) * len(settings.LANGUAGES)
        super().__init__(widgets)

    def decompress(self, value):
        value = value or {}
        data_list = []
        for code, lang in settings.LANGUAGES:
            data_list.append(value.get(code, None))
        return data_list

    def format_output(self, rendered_widgets):
        labels = [name for code, name in settings.LANGUAGES]
        rows = list(zip(labels, rendered_widgets))
        html = render_to_string(self.template, {'rows': rows})
        return mark_safe(html)


class TransFormField(forms.MultiValueField):
    """
    Multi language form field, required means the first language is required,
    require_all_fields means that all fields are required.
    """
    def __init__(self, require_all_fields=False, required=False,
            base_field=None, base_widget=None, **kwargs):
        required = required or require_all_fields
        self.widget = TransWidget(base_widget)
        field_kwargs = valid_kwargs(base_field.__init__, kwargs)
        field_kwargs['required'] = required
        fields = []
        for code, name in settings.LANGUAGES:
            fields.append(base_field(**field_kwargs))
            if not require_all_fields:
                field_kwargs['required'] = False
        super().__init__(fields, require_all_fields=require_all_fields,
                required=required)

    def prepare_value(self, value):
        if isinstance(value, dict):
            for field, code in zip(self.fields, value.keys()):
                value[code] = field.prepare_value(value[code])
        return value

    def compress(self, data_list):
        data_list = data_list or []
        value = {}
        for j, v in enumerate(data_list):
            code = settings.LANGUAGES[j][0]
            value[code] = v
        return value


class TransField(JSONField):
    form_class = TransFormField
    base_field = None
    base_widget = None
    max_length = None

    def __init__(self, verbose_name=None, max_length=None, required=False,
            require_all_fields=False, form_class=None, base_field=None,
            base_widget=None, **kwargs):
        base_field = base_field or self.base_field
        if base_field is None:
            raise exceptions.ValidationError('base_field cannot be None')
        base_widget = base_widget or self.base_widget
        if base_widget is None:
            raise exceptions.ValidationError('base_widget cannot be None')
        max_length = max_length or self.max_length
        self.formfield_defaults = {
            'base_field': base_field,
            'base_widget': base_widget,
            'form_class': form_class or self.form_class,
            'require_all_fields': require_all_fields,
            'max_length': max_length,
        }
        defaults = {
            'blank': not required,
            'null': not required,
            'verbose_name': verbose_name,
            'max_length': max_length,
        }
        defaults.update(kwargs)
        super().__init__(**defaults)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs.pop('max_length', None)  # remove all kwargs not applicable for JSONField
        return name, 'django.contrib.postgres.fields.jsonb.JSONField', args, kwargs

    def formfield(self, **kwargs):
        defaults = self.formfield_defaults.copy()
        defaults.update(**kwargs)
        return super().formfield(**defaults)

    def contribute_to_class(self, cls, *args, **kwargs):
        super().contribute_to_class(cls, *args, **kwargs)
        if self.column:
            attr = self.attname.rsplit('_', 1)[0]
            if not getattr(cls, attr, None):
                setattr(cls, attr, property(curry(get_field_translation, field=self)))


# ~~~~~~~~~~~
# StringField
# ~~~~~~~~~~~
class TextInputWidget(forms.TextInput):
    def __init__(self, attrs=None):
        attrs = attrs or {}
        attrs.setdefault('class', 'vTextField')
        super().__init__(attrs=attrs)


class TransStringField(TransField):
    base_field = forms.CharField
    base_widget = TextInputWidget
    max_length = 255


# ~~~~~~~~~~~~
# WysiwygField
# ~~~~~~~~~~~~
class TransWysiwygField(TransField):
    base_field = forms.CharField
    base_widget = WysiwygWidget


# ~~~~~~~~
# TagField
# ~~~~~~~~
class TagField(forms.Field):
    def clean(self, value):
        tags = set(tag.strip() for tag in value.split(','))
        return sorted(filter(None, tags))

    def prepare_value(self, value):
        if value in self.empty_values:
            return ''
        if isinstance(value, str):
            return value
        return ', '.join(value)


class TransTagField(TransField):
    base_field = TagField
    base_widget = TextInputWidget
