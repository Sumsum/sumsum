from django.contrib import auth
from django_select2.forms import Select2Widget, ModelSelect2MultipleWidget
from django import forms


class UserChangeForm(auth.forms.UserChangeForm):
    class Meta:
        widgets = {
            'country': Select2Widget(attrs={'style': 'width:20em'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
            'tags': ModelSelect2MultipleWidget(attrs={'style': 'width:20em'}, search_fields=('title',))
        }
