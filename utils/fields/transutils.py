from django.conf import settings
from django.utils.translation import get_language


def get_field_translation(self, field):
    data = getattr(self, field.attname)
    value = data.get(get_language(), None)
    if not value:
        value = data.get(settings.LANGUAGE_CODE, None)
    return value
