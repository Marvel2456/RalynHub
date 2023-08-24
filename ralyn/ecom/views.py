from django.shortcuts import render, redirect
from . models import *
# Create your views here.

def Index(request):
    number_of_products = 10
    products = Item.objects.all()[:number_of_products]

    context = {
        'products':products,
    }
    return render(request, 'ecom/index.html', context)

def About(request):
    return render(request, 'ecom/about.html')

def Products(request):
    return render(request, 'ecom/products.html')

def Cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
    else:
        items = []
    context = {
        'items':items
    }
    return render(request, 'ecom/cart.html', context)

def Checkout(request):
    pass

def Contact(request):
    return render(request, 'ecom/contact.html')