from django import forms

class TrialSignUpForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=True, label='First Name')
    last_name = forms.CharField(max_length=100, required=True, label='Last Name')
    company_name = forms.CharField(max_length=100, required=True, label='Company Name')
    email = forms.EmailField(max_length=100, required=True, label='Email Address')
    phone_number = forms.CharField(max_length=15, required=True)
