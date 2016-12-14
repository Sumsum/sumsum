from django import forms
from .models import CustomerAddress
from django.contrib.admin.widgets import AdminTextInputWidget


def get_customer_admin_form():
    attrs = {}
    for name, f in forms.fields_for_model(CustomerAddress).items():
        if isinstance(f, forms.CharField):
            f.widget = AdminTextInputWidget()
        attrs['address_{}'.format(name)] = f
    return type('CustomerAdminFormBase', (forms.ModelForm,), attrs)


class CustomerAdminForm(get_customer_admin_form()):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        obj = kwargs.get('instance', None)
        if obj and obj.default_address:
            for name in forms.fields_for_model(CustomerAddress).keys():
                self.fields['address_{}'.format(name)].initial = getattr(obj.default_address, name)

    def clean(self):
        super().clean()
        self.default_address_data = {}
        for key, value in self.cleaned_data.items():
            if key.startswith('address_') and value:
                self.default_address_data[key[8:]] = value
        return self.cleaned_data
