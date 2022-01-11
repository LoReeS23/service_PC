from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User as User_auth
from django.forms import ModelForm

from service_app.models import MotherBoard, Processor, GraphicCard, Disc, Memory, PowerSupply, Case, PC

all_parts_type = [
    (1, 'Motherboard'),
    (2, 'Processor'),
    (3, 'Graphic Card'),
    (4, 'Disc'),
    (5, 'Memory'),
    (6, 'Power Supply'),
    (7, 'Case')
]


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)
    password_repeat = forms.CharField(max_length=50, widget=forms.PasswordInput)

    def clean(self):
        data = super().clean()
        if data.get('password') != data.get('password_repeat'):
            raise ValidationError("hasla nie sa takie same")
        return data


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)

    def clean(self):
        data = super().clean()
        self.user = authenticate(**data)
        if self.user is None:
            raise ValidationError('Niepoprawne dane')
        return data


class AddPartForm(forms.Form):
    part = forms.ChoiceField(choices=all_parts_type)


class CreatePCForm(ModelForm):
    class Meta:
        exclude = ['user', 'price', ]
        model = PC

