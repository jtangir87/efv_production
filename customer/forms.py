from django import forms
from .models import BillingProfile
from django.core.exceptions import NON_FIELD_ERRORS

MONTH_CHOICES = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']


class BillingProfileForm(forms.ModelForm):
    class Meta:
        model = BillingProfile
        fields = ('first_name', 'last_name', 'email', 'address_one', 'address_two', 'city', 'state', 'zip_code', 'stripe_id', 'subscription_id')
        widgets = {
            'address_one': forms.TextInput(attrs={'class':'form-control'}),
            'address_two': forms.TextInput(attrs={'class':'form-control'}),
            'city': forms.TextInput(attrs={'class':'form-control'}),
            'state': forms.TextInput(attrs={'class':'form-control'}),
        }  
    
    def add_error(self, message):
        self._errors[NON_FIELD_ERRORS] = self.error_class([message])

class BillingProfileFormTest(forms.ModelForm):
    credit_card = forms.IntegerField(required=True)
    cvv = forms.IntegerField(required=True)
    exp_month = forms.ChoiceField(choices=[MONTH_CHOICES], required=True)
    exp_year = forms.ChoiceField(choices=((str(x), x) for x in range(2019,2039)), required=False)

    class Meta:
        model = BillingProfile
        fields = ('first_name', 'last_name', 'email', 'address_one', 'address_two', 'city', 'state', 
                'zip_code', 'stripe_id', 'subscription_id')

    
    def add_error(self, message):
        self._errors[NON_FIELD_ERRORS] = self.error_class([message])