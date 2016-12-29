import yaml
from django import forms
from django.contrib.postgres.fields import JSONField
from django.forms.widgets import Textarea
from django.template.loader import render_to_string


class YAMLWidget(Textarea):
    class Media:
        css = {'all': ['utils/ace/yaml.css']}
        js = ['utils/ace/ace.js']

    def render(self, name, value, attrs=None, read_only=False, language='yaml'):
        res = super().render(name, value, attrs)
        return res + render_to_string('utils/ace.html', {
            'id': attrs['id'],
            'read_only': read_only,
            'language': language,
        })


class YAMLJSONField(forms.CharField):
    widget = YAMLWidget

    def to_python(self, value):
        value = value.strip()
        try:
            obj = yaml.load(value)
        except Exception as e:
            raise forms.ValidationError('Error: {}'.format(e))
        if obj in self.empty_values:
            return {}
        if not isinstance(obj, dict):
            raise forms.ValidationError('Error: "{}" is not in the correct format.'.format(value))
        return obj

    def prepare_value(self, value):
        if value in self.empty_values:
            return ''
        if isinstance(value, str):
            return value
        return yaml.dump(value, default_flow_style=False)


class YAMLTextField(forms.CharField):
    widget = YAMLWidget

    def to_python(self, value):
        value = value.strip()
        if value in self.empty_values:
            return None
        try:
            yaml.load(value)
        except Exception as e:
            raise forms.ValidationError('Error: {}'.format(e))
        return value


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
