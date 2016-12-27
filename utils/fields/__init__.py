from .hstore import HStoreField  # NOQA
from .yaml import YAMLJSONField, YAMLTextField  # NOQA
from .handle import HandleField  # NOQA
from django.db import models
from django.db.models.fields.files import ImageFieldFile, ImageField
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField as _CountryField
from timezone_field import TimeZoneField as _TimeZoneField
from redactor.widgets import RedactorEditor
from django import forms
from django.conf import settings


class TimeZoneField(_TimeZoneField):
    def __init__(self, verbose_name=None, **kwargs):
        required = kwargs.pop('required', False)
        kwargs.setdefault('blank', not required)
        kwargs.setdefault('null', not required)
        super().__init__(verbose_name=verbose_name, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(_TimeZoneField, self).deconstruct()
        kwargs.pop('choices')
        return name, 'django.db.models.CharField', args, kwargs


class ImageFieldFile(ImageFieldFile):
    @property
    def src(self):
        return self.url


class ImageField(ImageField):
    attr_class = ImageFieldFile


class CountryField(_CountryField):
    def deconstruct(self):
        name, path, args, kwargs = super(_CountryField, self).deconstruct()
        kwargs.pop('choices')  # we don't want to put all those choices in the migrations
        return name, 'django.db.models.CharField', args, kwargs


class PositionField(models.PositiveSmallIntegerField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('verbose_name', _('position'))
        kwargs.setdefault('default', 0)
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs.pop('default')  # no need for default
        return name, 'django.db.models.PositiveSmallIntegerField', args, kwargs


class ChoiceField(models.CharField):
    description = _('String (up to %(max_length)s)')

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 50)
        kwargs.setdefault('blank', True)
        kwargs.setdefault('null', True)
        if 'default' not in kwargs and kwargs.get('choices'):
            kwargs['default'] = kwargs['choices'][0][0]
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs.pop('choices', None)  # this just clutters the migrations
        kwargs.pop('default', None)  # this is not something we need in the migratons, no
        return name, 'django.db.models.CharField', args, kwargs


class StringField(models.CharField):
    description = _('String (up to %(max_length)s)')

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 255)
        required = kwargs.pop('required', False)
        kwargs.setdefault('blank', not required)
        kwargs.setdefault('null', not required)
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        return name, 'django.db.models.CharField', args, kwargs


class TextField(models.TextField):
    def __init__(self, *args, **kwargs):
        required = kwargs.pop('required', False)
        kwargs.setdefault('blank', not required)
        kwargs.setdefault('null', not required)
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        return name, 'django.db.models.TextField', args, kwargs


class WysiwygWidget(RedactorEditor):
    @property
    def media(self):
        js = (
            'redactor/jquery.redactor.init.js',
            'redactor/redactor{0}.js'.format('' if settings.DEBUG else '.min'),
            'redactor/langs/{0}.js'.format(self.options.get('lang', 'en')),
        )
        if 'plugins' in self.options:
            plugins = self.options.get('plugins')
            for plugin in plugins:
                js = js + (
                    'redactor/plugins/{0}.js'.format(plugin),
                )
        css = {
            'all': (
                'redactor/css/redactor.css',
                'utils/redactor/redactor.css',
            )
        }
        return forms.Media(css=css, js=js)


class WysiwygField(TextField):
    def __init__(self, *args, **kwargs):
        redactor_options = kwargs.pop('redactor_options', {})
        upload_to = kwargs.pop('upload_to', '')
        allow_file_upload = kwargs.pop('allow_file_upload', True)
        allow_image_upload = kwargs.pop('allow_image_upload', True)
        self.widget = WysiwygWidget(
            redactor_options=redactor_options,
            upload_to=upload_to,
            allow_file_upload=allow_file_upload,
            allow_image_upload=allow_image_upload,
            attrs={'height': '10em'},
        )
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = self.widget
        return super().formfield(**kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        return name, 'django.db.models.TextField', args, kwargs
