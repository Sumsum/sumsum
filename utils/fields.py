from .text import slugify
from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core import validators


class TitleSlugField(models.CharField):
    default_validators = [validators.validate_slug]
    description = _("Slug (up to %(max_length)s)")

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 50)
        # Set db_index=True unless it's been set manually.
        if 'db_index' not in kwargs:
            kwargs['db_index'] = True
        if 'blank' not in kwargs:
            kwargs['blank'] = True
        if 'unique' not in kwargs:
            kwargs['unique'] = True
        self.allow_unicode = kwargs.pop('allow_unicode', False)
        if self.allow_unicode:
            self.default_validators = [validators.validate_unicode_slug]
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if kwargs.get("max_length") == 50:
            del kwargs['max_length']
        if self.db_index is False:
            kwargs['db_index'] = False
        else:
            del kwargs['db_index']
        if self.allow_unicode is not False:
            kwargs['allow_unicode'] = self.allow_unicode
        if self.blank is False:
            kwargs['blank'] = False
        else:
            del kwargs['blank']
        if self.unique is False:
            kwargs['unique'] = False
        else:
            del kwargs['unique']
        return name, path, args, kwargs

    def get_internal_type(self):
        return "SlugField"

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.SlugField, 'allow_unicode': self.allow_unicode}
        defaults.update(kwargs)
        return super().formfield(**defaults)

    def pre_save(self, obj, add):
        value = self.value_from_object(obj)
        if add or not value:
            # only compute slug from title if its a new record or if empty value
            value = obj.title
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
