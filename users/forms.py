from django import forms
from django.forms import PasswordInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=128, min_length=1)
    password = forms.CharField(
        widget=PasswordInput(attrs={"color": "red"}), min_length=1, max_length=64
    )
