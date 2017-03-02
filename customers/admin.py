from django.contrib import admin
from .models import Customer, CustomerAddress
from django.utils.translation import ugettext_lazy as _


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">contacts</i>'
    fieldsets = (
        (_('Customer overview'), {
            'fields': (
                'first_name',
                'last_name',
                'email',
                'accepts_marketing',
                'tax_exempt',
            )
        }),
        (_('Address'), {
            'fields': (
                'address_first_name',
                'address_last_name',
                'address_company',
                'address_phone',
                'address_address1',
                'address_address2',
                'address_city',
                'address_zip',
                'address_country_code',
                'address_province',
            )
        }),
        (_('Notes'), {
            'fields': (
                'note',
            )
        }),
        (_('tags'), {
            'fields': (
                'tags',
            )
        }),
    )

    #def save_related(self, request, form, formsets, change):
    #    super().save_related(request, form, formsets, change)
    #    obj = form.instance
    #    if form.default_address_data:
    #        if obj.default_address:
    #            for attr, value in form.default_address_data:
    #                setattr(obj.default_address, attr, value)
    #            obj.default_address_data.save()
    #        else:
    #            form.default_address_data['customer'] = obj
    #            CustomerAddress.objects.create(**form.default_address_data)


@admin.register(CustomerAddress)
class CustomerAddressAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">contact_mail</i>'
    pass
