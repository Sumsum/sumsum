from django import forms
from django.core import validators
from django.db import models
from django.utils.translation import ugettext_lazy as _
from utils.text import slugify


__all__ = ('HandleField',)


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
