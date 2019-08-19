from django import forms
from .models import BillingProfile
from django.core.exceptions import NON_FIELD_ERRORS



class BillingProfileForm(forms.ModelForm):
    class Meta:
        model = BillingProfile
        fields = ('email', 'stripe_id', 'subscription_id')

    
    def add_error(self, message):
        self._errors[NON_FIELD_ERRORS] = self.error_class([message])

