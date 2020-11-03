from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from .models import Users
from phonenumber_field.formfields import PhoneNumberField

class RegistrationForm(UserCreationForm):
    phone_number = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder': ('Phone')}),
                            label=("Phone number"), required=False)
    class Meta:
        model = Users
        fields = ['phone_number', 'password1', 'password2']


# class UserForm(forms.ModelForm):
#     class Meta:
#         model = Users
#         fields = ['phone_number']
#
#         widgets = {
#             'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
#         }
#
#
# class LogForm(forms.ModelForm):
#     class Meta:
#         model = Users
#         fields = ['phone_number']
#
#         widgets = {
#             'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
#         }
