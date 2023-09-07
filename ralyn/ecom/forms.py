from django.forms import ModelForm
from django import forms
from account.models import Customer


class UpdateCustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ('username', 'name', 'phone_number')