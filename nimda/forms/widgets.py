from django import forms


class NimdaDateWidget(forms.DateInput):
    template_name = 'admin/widgets/date.html'

    def __init__(self):
        super().__init__(attrs={'class': 'form-control pull-right datepicker'})


class NimdaTimeWidget(forms.TimeInput):
    template_name = 'admin/widgets/time.html'

    def __init__(self):
        super().__init__(attrs={'class': 'form-control timepicker'})
