from django.forms import ModelForm
from django import forms
from . models import Review, ShippingDetail, PaymentHistory
from account.models import Customer


class UpdateCustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ('username', 'name', 'phone_number')


class CreateReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ('message',)


class ShippingForm(ModelForm):
    class  Meta:
        model = ShippingDetail
        fields = ('address', 'city', 'state', 'zipcode', 'phone')

class PaymentForm(ModelForm):
    class Meta:
        model = PaymentHistory
        fields = ('amount',)