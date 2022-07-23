from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import *


class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class CreateUserWordForm(forms.ModelForm):
    class Meta:
        model = UserWord
        fields = ['word']

        widgets = {
            'word': forms.TextInput(attrs={'class': 'form-control'})
        }


class CreateUserWordDetailForm(forms.ModelForm):
    class Meta:
        model = UserWordDetail
        fields = ['translate', 'word_example']

        widgets = {
            'translate': forms.TextInput(attrs={'class': 'form-control'}),
            'word_example': forms.TextInput(attrs={'class': 'form-control'}),
        }