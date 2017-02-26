import json
from django import forms
from django.forms.widgets import ClearableFileInput
from django.template.loader import render_to_string


class AdminImageWidget(ClearableFileInput):
    template_with_initial = (
        '<p class="file-upload">'
        '%(initial_text)s: <img src="%(initial_url)s" height="90"> '
        '%(clear_template)s<br />%(input_text)s: %(input)s'
        '</p>'
    )

    template_with_clear = (
        '<span class="clearable-file-input">'
        '%(clear)s <label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label>'
        '</span>'
    )


class SirTrevorWidget(forms.Textarea):
    block_types = ('Product', 'Markup', 'Video', 'Heading', 'Text', 'Image')

    def __init__(self, attrs=None, block_types=None):
        self.block_types = block_types or self.block_types
        super().__init__(attrs)

    class Media:
        css = {'all': (
            'utils/sir-trevor/sir-trevor.min.css',
        )}
        js = (
            'utils/sir-trevor/sir-trevor.min.js',
        )

    def render(self, name, value, attrs=None):
        res = super().render(name, value, attrs)
        res += render_to_string('utils/sir_trevor.html', {
            'id': attrs['id'],
            'block_types': json.dumps(self.block_types),
        })
        return res
