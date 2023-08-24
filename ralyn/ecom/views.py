from django.shortcuts import render, redirect
from . models import *
# Create your views here.

def Index(request):
    number_of_products = 10
    products = Product.objects.all()[:number_of_products]

    context = {
        'products':products,
    }
    return render(request, 'ecom/index.html', context)

def About(request):
    return render(request, 'ecom/about.html')

def Products(request):
    product = Product.objects.all()
    context = {'product':product}
    return render(request, 'ecom/products.html', context)

def Cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(user=customer, completed=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
    context = {
        'items':items,
        'order':order
    }
    return render(request, 'ecom/cart.html', context)

def Checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(user=customer, completed=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
    context = {
        'items':items,
        'order':order
    }
    return render(request, 'ecom/checkout.html', context)

def Contact(request):
    return render(request, 'ecom/contact.html')