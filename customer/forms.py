from django import forms
from .models import BillingProfile

class BillingProfileForm(forms.ModelForm):
    class Meta:
        model = BillingProfile
        fields = ('first_name', 'last_name', 'email', 'address_one', 'address_two', 'city', 'state', 'zip_code')
        widgets = {
            'address_one': forms.TextInput(attrs={'class':'form-control'}),
            'address_two': forms.TextInput(attrs={'class':'form-control'}),
            'city': forms.TextInput(attrs={'class':'form-control'}),
            'state': forms.TextInput(attrs={'class':'form-control'}),
        }  
