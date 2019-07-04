from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class UserSignUpForm(UserCreationForm):
    phone_number = forms.CharField(required=True)

    class Meta:
        fields = ('username','first_name','last_name','email','phone_number', 'password1','password2')
        model = get_user_model()

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['email'].label = 'Email Address'


class CreateUserForm(UserCreationForm):
    phone_number = forms.CharField(required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number', 
            'is_staff',
        ]
        help_texts = {
            'username': "Required. Letters, digits and @/./+/-/_ only.",
            'is_staff': "Designates whether the user can control admin functions of the site.",
            "is_active": "Unselect instead of deleting accounts.",
        }

class UpdateUserForm(UserChangeForm):
    phone_number = forms.CharField(required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number', 
            'is_staff',
            'is_active',
        ]
        help_texts = {
            'username': "Required. Letters, digits and @/./+/-/_ only.",
            'is_staff': "Designates whether the user can control admin functions of the site.",
            "is_active": "Unselect instead of deleting accounts.",
        }