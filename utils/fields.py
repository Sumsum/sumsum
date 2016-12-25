from .text import slugify
from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core import validators
from django.db.models.fields.files import ImageFieldFile, ImageField
from django_countries.fields import CountryField as _CountryField
from redactor.fields import RedactorField
from timezone_field import TimeZoneField as _TimeZoneField


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


class WysiwygField(RedactorField):
    def __init__(self, *args, **kwargs):
        required = kwargs.pop('required', False)
        kwargs.setdefault('blank', not required)
        kwargs.setdefault('null', not required)
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        return name, 'django.db.models.TextField', args, kwargs


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


class HandleField(models.CharField):
    default_validators = [validators.validate_slug]
    description = _('Slug (up to %(max_length)s)')

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 50)
        kwargs.setdefault('db_index', True)
        kwargs.setdefault('blank', True)
        kwargs.setdefault('unique', True)
        self.from_field = kwargs.pop('from_field', None)
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        return name, 'django.db.models.CharField', args, kwargs

    def get_internal_type(self):
        return 'SlugField'

    def formfield(self, **kwargs):
        kwargs.setdefault('form_class', forms.SlugField)
        return super().formfield(**kwargs)

    def pre_save(self, obj, add):
        value = self.value_from_object(obj)
        if add or not value:
            # only compute slug from self.from_field if its a new record or if empty value
            value = getattr(obj, self.from_field)
        slug = slugify(value)[:46]
        if self.unique:
            qs = obj.__class__._default_manager.using(obj._state.db)
            qs = qs.filter(**{'%s__startswith' % self.attname: slug})
            if obj.pk:
                qs = qs.exclude(pk=obj.pk)
            invalid = list(qs.values_list(self.attname, flat=True))
            new_slug = slug
            counter = 1
            while True:
                if new_slug not in invalid:
                    break
                new_slug = '%s-%s' % (slug, counter)
                counter += 1
            slug = new_slug
        setattr(obj, self.attname, slug)
        return slug
