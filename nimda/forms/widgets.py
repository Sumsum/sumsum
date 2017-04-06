from django import forms


class NimdaDateWidget(forms.DateInput):
    template_name = 'admin/widgets/date.html'


class NimdaTimeWidget(forms.TimeInput):
    template_name = 'admin/widgets/time.html'
