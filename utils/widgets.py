from django.forms.widgets import ClearableFileInput


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
