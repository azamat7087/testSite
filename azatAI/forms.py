from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from .models import Users
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth import authenticate


class RegistrationForm(UserCreationForm):
    phone_number = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder': ('Phone')}),
                            label=("Phone number"), required=False)
    class Meta:
        model = Users
        fields = ['phone_number', 'password1', 'password2']


class LogForm(forms.ModelForm):

    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Users
        fields = ['phone_number', 'password']

        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
    def clean(self):
        phone_number = self.cleaned_data['phone_number']
        password = self.cleaned_data['password']

        if not authenticate(phone_number=phone_number, password=password):
            raise forms.ValidationError("Invalid login")
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
#
