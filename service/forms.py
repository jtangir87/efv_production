from django import forms
from bootstrap_datepicker_plus import DatePickerInput
from .models import ServiceRecord

class SchedServiceForm(forms.ModelForm):
    class Meta:
        model = ServiceRecord
        fields = ('vehicle', 'description', 'date', 'mileage')
        widgets = {
            'date': DatePickerInput(format='%m-%d-%Y'),
        }
