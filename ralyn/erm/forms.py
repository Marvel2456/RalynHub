from django.forms import ModelForm
from django import forms
from ecom.models import *


class CreateProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'main_image', 'image1', 'image2', 'image3', 'image4', 'category', 'description', 'price', 'store_quantity')

        widgets = {
                'category' : forms.Select(attrs={'class':'form-select form-control', 'placeholder':'Category'}),
        }

class CreateCategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'