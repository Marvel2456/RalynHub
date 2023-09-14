from django.shortcuts import render, redirect
from . models import *
from django.http import JsonResponse
import json
from account.models import Customer
from .forms import UpdateCustomerForm, CreateReviewForm
from django.contrib import messages
# Create your views here.

def Index(request):
 
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        total_quantity = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        total_quantity = order['get_cart_items']

    product = Product.objects.all()
    context = {
        'product':product,
        'items':items,
        'order':order,
        'total_quantity':total_quantity,
    }
    return render(request, 'ecom/index.html', context)

def About(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        total_quantity = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        total_quantity = order['get_cart_items']

    context ={
        'total_quantity':total_quantity,
    }
    return render(request, 'ecom/about.html', context)

def Products(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        total_quantity = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        total_quantity = order['get_cart_items']

    product = Product.objects.all()
    context = {
        'product':product,
        'items':items,
        'order':order,
        'qty':total_quantity,
        }
    return render(request, 'ecom/products.html', context)

def Cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        total_quantity = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        total_quantity = order['get_cart_items']
    context = {
        'items':items,
        'order':order,
        'qty':total_quantity,
    }
    return render(request, 'ecom/cart.html', context)

def UpdateItems(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print(productId)
    print(action)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, completed=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    context = {

        'qty': order.get_cart_items,
    }
        
    return JsonResponse(context, safe=False)


def updateQuantity(request):
    data = json.loads(request.body)
    input_value = int(data['val'])
    product_Id = data['prod_id']
    
    customer = request.user.customer
    product = Product.objects.get(id=product_Id)
    order, created = Order.objects.get_or_create(customer=customer, completed=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    orderItem.quantity = input_value
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    context = {
        'sub_total':orderItem.get_total,
        'final_total':order.get_cart_total,
        'qty':order.get_cart_items,
    }

    return JsonResponse(context, safe=False)


def Checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
    context = {
        'items':items,
        'order':order
    }
    return render(request, 'ecom/checkout.html', context)

def Contact(request):
    return render(request, 'ecom/contact.html')

def Profile(request):
    customer = request.user.customer
    form = UpdateCustomerForm(instance=customer)
    if request.method == 'POST':
        form = UpdateCustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profie successfully updated')
            return redirect('profile')
    context = {
        'customer':customer,
        'form':form
    }
    return render(request, 'ecom/profile.html', context)


def productDetail(request, uuid):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cart_items = order['get_cart_items']

    product = Product.objects.get(id=uuid)
    
    form = CreateReviewForm()
    if request.method == 'POST':
        form = CreateReviewForm(request.POST or None)
        if form.is_valid():
            review = form.save(commit=False)
            review.customer = request.user.customer
            review.product = product
            review.save()
            messages.success(request, 'review successfully submited')
            return redirect('detail')
    context = {
        'items':items,
        'cart_items':cart_items,
        'product':product,
        'form':form
    }
    return render(request, 'ecom/detail.html', context)