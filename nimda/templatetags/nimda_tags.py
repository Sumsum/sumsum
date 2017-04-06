import hashlib
import json
import os
import random
from django import template
from django.apps import apps
from django.conf import settings
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper, FilteredSelectMultiple, AdminSplitDateTime
from django.core.cache import cache
from django.forms import Select, SelectMultiple
from django.forms.utils import flatatt
from django.utils.html import conditional_escape, format_html
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from nimda.forms.widgets import NimdaDateWidget, NimdaTimeWidget
from rest_framework import serializers
from django.contrib import admin


register = template.Library()


class DistException(Exception):
    pass


@register.simple_tag
def dist(arg):
    ext = os.path.splitext(arg)[1].lower()
    path = 'dist/{0}'.format(arg)
    key = 'dist:{}'.format(path)
    md5 = cache.get(key)
    if not md5 or settings.DEBUG:
        full_path = os.path.join(settings.BASE_DIR, path)
        with open(full_path, encoding='utf8') as fp:
            md5 = hashlib.md5(fp.read().encode('utf8')).hexdigest()[:6]
        cache.set(key, md5, timeout=None)
    full_path = '{0}{1}'.format(settings.CDN_URL, path)
    if ext == '.js':
        tag = '{0}?{1}'.format(full_path, md5)
    elif ext == '.css':
        tag = '{0}?{1}'.format(full_path, md5)
    elif ext in ['.jpg', '.png', '.svg']:
        tag = '<img src="{0}?{1}">'.format(full_path, md5)
    else:
        raise DistException('Invalid argument: {0}'.format(arg))
    return mark_safe(tag)


def serialize_model(obj):
    class ModelSerializer(serializers.ModelSerializer):
        class Meta:
            model = obj.__class__
    return ModelSerializer(obj).data


@register.simple_tag(takes_context=True)
def original(context):
    user = context.get('user')
    if not user or not user.is_active:
        return ''
    if not (user.is_superuser or user.is_staff):
        return ''
    obj = context.get('original')
    if not obj:
        return ''
    data = serialize_model(obj)
    tag = '<script>window.original = {0}</script>'.format(json.dumps(data))
    return mark_safe(tag)


@register.filter
def render_field_label(field):
    contents = field.label
    widget = field.field.widget
    id_ = widget.attrs.get('id') or field.auto_id
    if id_:
        attrs = {}
        css_classes = []
        id_for_label = widget.id_for_label(id_)
        if id_for_label:
            attrs['for'] = id_for_label
        if field.field.required:
            css_classes.append('required')
        attrs['class'] = ' '.join(css_classes)
        attrs = flatatt(attrs)
        contents = format_html('<label{}>{}</label>', attrs, contents)
    else:
        contents = conditional_escape(contents)
    return mark_safe(contents)


@register.inclusion_tag('admin/includes/help_text.html')
def help_text(field):
    return {'help_text': field.field.help_text}


@register.filter
def col_width(field):
    widget = field.field.widget
    if hasattr(widget, 'is_wide') and widget.is_wide:
        return 12
    if isinstance(widget, AdminSplitDateTime):
        return 12
    return 6


@register.filter
def form_class(field):
    widget = field.field.widget
    if isinstance(widget, AdminSplitDateTime):
        return ''
    return 'form-group'


@register.filter
def render_field(field):
    widget = field.field.widget

    if isinstance(widget, (Select, SelectMultiple, RelatedFieldWidgetWrapper)):
        # nested widget
        if hasattr(widget, 'widget'):
            if isinstance(widget.widget, FilteredSelectMultiple):
                widget = SelectMultiple()
                field.field.widget.widget = widget
            else:
                widget = widget.widget
        if hasattr(field, 'no_select2') and widget.no_select2:
            return field
        # remove unwanted help text
        rmthis = str(_('Hold down "Control", or "Command" on a Mac, to select more than one.'))
        field.help_text = str(field.help_text).replace(rmthis, '')
        widget.attrs['class'] = 'form-control select2'

    elif isinstance(widget, AdminSplitDateTime):
        widget.widgets = [
            NimdaDateWidget(attrs={'class': 'form-control datepickerInput'}),
            NimdaTimeWidget(attrs={'class': 'form-control timepickerInput'}),
        ]

    else:
        widget.attrs['class'] = 'form-control'

    return field


@register.filter
def inline_td_classes(field):
    css_classes = field.field.widget.attrs.get('class', '').split(' ')
    css_classes.append(field.field.widget.attrs.get('type', ''))
    if field.name:
        css_classes.append(field.name)
    return ' '.join(css_classes)


@register.inclusion_tag('admin/includes/sidebar_menu.html', takes_context=True)
def sidebar_menu(context):
    registry = {}
    for model, model_admin in admin.site._registry.items():
        app_label = model._meta.app_label
        object_name = model._meta.object_name
        registry['{}.{}'.format(app_label, object_name)] = model_admin

    app_list = []
    for app in context['available_apps']:
        app_config = apps.get_app_config(app['app_label'])
        if hasattr(app_config, 'icon'):
            app['icon'] = app_config.icon
        else:
            app['icon'] = '<i class="fa fa-folder" aria-hidden="true"></i>'
        models = []
        for model in app['models']:
            admin_model = registry['{}.{}'.format(app['app_label'], model['object_name'])]
            if hasattr(admin_model, 'icon'):
                model['icon'] = admin_model.icon
            else:
                model['icon'] = '<i class="fa fa-folder" aria-hidden="true"></i>'
            models.append(model)
        app['models'] = models
        app_list.append(app)
    return {'app_list': app_list}


@register.inclusion_tag('admin/includes/model_summary.html', takes_context=True)
def model_summary(context):
    if 'app_list' in context:
        colors = ['aqua', 'green', 'red', 'white', 'black']
        random.seed('nimdalhc')
        random.shuffle(colors)
        models = []
        for j, app in enumerate(context['app_list']):
            for m in app['models']:
                cidx = j % len(colors)
                model = apps.get_model(app['app_label'], m['object_name'])
                models.append({
                    'name': m['name'],
                    'count': model._default_manager.all().count(),
                    'color': colors[cidx],
                    'url': m['admin_url']
                })
        return {'models': models}
