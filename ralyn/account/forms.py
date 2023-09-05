from django.forms import ModelForm
from account.models import User, Customer
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')