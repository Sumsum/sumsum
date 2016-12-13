from django import forms
from django_select2.forms import ModelSelect2Widget, ModelSelect2MultipleWidget


class ProductForm(forms.ModelForm):
    class Meta:
        exclude = []
        widgets = {
            'tags': ModelSelect2MultipleWidget(attrs={'style': 'width:20em'}, search_fields=('title',)),
            'collections': ModelSelect2MultipleWidget(attrs={'style': 'width:20em'}, search_fields=('title',)),
            'type': ModelSelect2Widget(attrs={'style': 'width:20em'}, search_fields=('title',)),
            'vendor': ModelSelect2Widget(attrs={'style': 'width:20em'}, search_fields=('title',))
        }
