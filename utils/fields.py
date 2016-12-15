from .text import slugify
from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core import validators, exceptions


class ChoiceField(models.CharField):
    description = _('String (up to %(max_length)s)')

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 50)
        if 'choices' not in kwargs:
            raise exceptions.ValidationError(_('ChoiceField must specify `choices`.'))
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if kwargs.get('max_length') == 50:
            del kwargs['max_length']
        return name, path, args, kwargs


class StringField(models.CharField):
    description = _('String (up to %(max_length)s)')

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 255)
        kwargs['blank'] = kwargs.get('blank', True)
        kwargs['null'] = kwargs.get('null', True)
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if kwargs.get('max_length') == 255:
            del kwargs['max_length']
        if self.blank is True:
            del kwargs['blank']
        else:
            kwargs['blank'] = False
        if self.null is True:
            del kwargs['null']
        else:
            kwargs['null'] = False
        return name, path, args, kwargs


class HandleField(models.CharField):
    default_validators = [validators.validate_slug]
    description = _('Slug (up to %(max_length)s)')

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 50)
        # Set db_index=True unless it's been set manually.
        kwargs['db_index'] = kwargs.get('kwargs', True)
        kwargs['blank'] = kwargs.get('blank', True)
        kwargs['unique'] = kwargs.get('unique', True)
        if 'from_field' not in kwargs:
            raise exceptions.ValidationError(_('HandleField must specify `from_field`.'))
        self.from_field = kwargs.pop('from_field')
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if kwargs.get('max_length') == 50:
            del kwargs['max_length']
        if self.db_index is True:
            del kwargs['db_index']
        else:
            kwargs['db_index'] = False
        if self.blank is True:
            del kwargs['blank']
        else:
            kwargs['blank'] = False
        if self.unique is True:
            del kwargs['unique']
        else:
            kwargs['unique'] = False
        return name, path, args, kwargs

    def get_internal_type(self):
        return 'SlugField'

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.SlugField, 'allow_unicode': self.allow_unicode}
        defaults.update(kwargs)
        return super().formfield(**defaults)

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
