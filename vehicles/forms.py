from django import forms
from bootstrap_datepicker_plus import DatePickerInput
from .models import DamageReport

class DamageForm(forms.ModelForm):
    class Meta:
        model = DamageReport
        fields = [
            "vehicle",
            "date",
            "driver",
            "description",
        ]
        widgets ={
            'date': DatePickerInput(format='%m-%d-%Y')
        }
