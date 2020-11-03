from django import forms
from .models import *


class UserForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['phone_number']

        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }


class LogForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['phone_number']

        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
