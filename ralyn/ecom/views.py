from django.shortcuts import render, redirect
from . models import *
# Create your views here.

def index(request):
    number_of_products = 10
    products = Item.objects.all()[:number_of_products]

    context = {
        'products':products,
    }
    return render(request, 'ecom/index.html', context)