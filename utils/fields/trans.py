from .base import WysiwygWidget
from django import forms
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.core import exceptions
from django.template.loader import render_to_string
from django.utils.functional import curry
from django.utils.text import mark_safe
from django.utils.translation import get_language
from inspect import signature, getmro
from utils.text import slugify


__all__ = (
    'TransWidget', 'TransFormField',
    'TransStringField', 'TransHandleField', 'TransTextField',
    'TransWysiwygField', 'TransTagField'
)


def field_value(value, code):
    if not value:
        return None
    if code in value:
        return value[code]
    if settings.LANGUAGE_CODE in value:
        return value[settings.LANGUAGE_CODE]


def valid_field_kwargs(field, kwargs):
    valid_keys = set()
    for cls in getmro(field):
        valid_keys.union(set(signature(cls.__init__).parameters.keys()))
    valid_keys = valid_keys - set(['self', 'args', 'kwargs'])
    valid_kwargs = {}
    for k, v in kwargs.items():
        if k in valid_keys:
            valid_kwargs[k] = v
    return valid_kwargs


class TransWidget(forms.MultiWidget):
    template_name = 'utils/trans_widget.html'

    def __init__(self, widget):
        widgets = (widget,) * len(settings.LANGUAGES)
        super().__init__(widgets)

    def decompress(self, value):
        value = value or {}
        return [value.get(code) for code, name in settings.LANGUAGES]

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        labels = [n for code, n in settings.LANGUAGES]
        context['rows'] = list(zip(labels, context['widget']['subwidgets']))
        return context

    class Media:
        css = {'all': ['utils/trans.css']}


class TransFormField(forms.MultiValueField):
    """
    Multi language form field, required means the first language is required,
    require_all_fields means that all fields are required.
    """
    def __init__(self, label=None, require_all_fields=False, required=False,
            base_field=None, base_widget=None, **kwargs):
        required = required or require_all_fields
        self.widget = TransWidget(base_widget)
        field_kwargs = valid_field_kwargs(base_field, kwargs)
        field_kwargs['required'] = required
        fields = []
        for code, name in settings.LANGUAGES:
            fields.append(base_field(**field_kwargs))
            if not require_all_fields:
                field_kwargs['required'] = False
        super().__init__(fields, label=label,
                require_all_fields=require_all_fields, required=required)

    def prepare_value(self, value):
        if isinstance(value, dict):
            for field, code in zip(self.fields, value.keys()):
                value[code] = field.prepare_value(value[code])
        return value

    def compress(self, data_list):
        data_list = data_list or []
        value = {}
        for j, v in enumerate(data_list):
            code, __ = settings.LANGUAGES[j]
            value[code] = v
        return value


class TransBaseField(JSONField):
    """
    Tranlation fields need to subclass this
    """
    form_class = TransFormField
    base_field = None
    base_widget = None
    max_length = None

    def __init__(self, verbose_name=None, max_length=None, required=False,
            require_all_fields=False, form_class=None, base_field=None,
            base_widget=None, populate_from=None, **kwargs):
        self.base_field = base_field or self.base_field
        if self.base_field is None:
            raise exceptions.ValidationError('base_field cannot be None')
        self.base_widget = base_widget or self.base_widget
        if self.base_widget is None:
            raise exceptions.ValidationError('base_widget cannot be None')
        self.max_length = max_length or self.max_length
        self.form_class = form_class or self.form_class
        self.formfield_defaults = {
            'base_field': self.base_field,
            'base_widget': self.base_widget,
            'form_class': self.form_class,
            'require_all_fields': require_all_fields,
            'max_length': self.max_length,
        }
        defaults = {
            'blank': not required,
            'null': not required,
            'verbose_name': verbose_name,
            'max_length': self.max_length,
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
            attr = self.attname[:-2]
            if not hasattr(cls, attr):
                def get_translation(self, field):
                    value = getattr(self, field.attname)
                    return field_value(value, get_language())
                setattr(
                    cls, attr,
                    property(curry(get_translation, field=self))
                )


# ~~~~~~~~~~~
# StringField
# ~~~~~~~~~~~
class TextInputWidget(forms.TextInput):
    def __init__(self, attrs=None):
        attrs = attrs or {}
        attrs.setdefault('class', 'vTextField')
        super().__init__(attrs=attrs)


class TransStringField(TransBaseField):
    base_field = forms.CharField
    base_widget = TextInputWidget
    max_length = 255


# ~~~~~~~~~~~
# HandleField
# ~~~~~~~~~~~
class TransHandleField(TransBaseField):
    base_field = forms.CharField
    base_widget = TextInputWidget
    max_length = 50

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('db_index', True)
        self.populate_from = kwargs.pop('populate_from', None)
        self.unique_together = set(kwargs.pop('unique_together', []))
        if 'unique' in kwargs:
            self.unique_together.add(kwargs.pop('unique'))
        super().__init__(*args, **kwargs)

    def pre_save(self, obj, add):
        value_t = self.value_from_object(obj) or {}
        handle_t = {}
        for code, name in settings.LANGUAGES:
            value = value_t.get(code, None)
            if add or not value:
                value = field_value(getattr(obj, self.populate_from), code)
            if value is None:
                continue
            handle = slugify(value)[:(self.max_length - 4)]
            if self.unique_together:
                model = obj.__class__
                qs = model._default_manager.using(obj._state.db)
                for field_name in self.unique_together:
                    if field_name != self.attname:
                        continue
                    lookup = field_name
                    value = getattr(obj, field_name)
                    if field_name.endswith('_t'):
                        lookup = '{}__{}'.format(lookup, code)
                        value = field_value(value, code)
                    if value is None:
                        continue
                    qs = qs.filter(**{lookup: value})
                if obj.pk:
                    qs = qs.exclude(pk=obj.pk)
                base_handle = handle
                counter = 1
                while True:
                    try:
                        qs.get(**{'{}__{}'.format(self.attname, code): handle})
                    except model.DoesNotExist:
                        break
                    handle = '-'.join([base_handle, counter])
                    counter += 1
            handle_t[code] = handle
        setattr(obj, self.attname, handle_t)
        return handle_t


# ~~~~~~~~~
# TextField
# ~~~~~~~~~
class TextareaWidget(forms.Textarea):
    def __init__(self, attrs=None):
        attrs = attrs or {}
        attrs.setdefault('class', 'vLargeTextField')
        super().__init__(attrs=attrs)


class TransTextField(TransBaseField):
    base_field = forms.CharField
    base_widget = TextareaWidget


# ~~~~~~~~~~~~
# WysiwygField
# ~~~~~~~~~~~~
class TransWysiwygField(TransBaseField):
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


class TransTagField(TransBaseField):
    base_field = TagField
    base_widget = TextInputWidget
