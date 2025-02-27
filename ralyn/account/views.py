from django.shortcuts import render, redirect
from django.contrib import messages
from account.models import User, Customer
from ecom.models import Order, OrderItem
from account.forms import *
from django.contrib.auth import authenticate, login, logout
from .emails import *
from django.utils.encoding import force_str

# Create your views here.

def RegisterView(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active=False
            user.save()
            activate_email(request, user, form.cleaned_data.get('email'))
            messages.success(request, 'Account successfully created for ')
            return redirect('login')
    return render(request, 'account/register.html')


def ActivateView(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Email verification successful, please login to access your dashboard')
        return redirect ('login')
    else:
        messages.error(request, 'Activation not successful, please try again')
        return redirect('register')



def LoginView(request):
    if request.method =='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome {user.username}')
            return redirect('products')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'account/login.html')


def LogoutView(request):
    logout(request)
    return redirect('index')


def Profile(request):
    customer = request.user.customer
    order_item = OrderItem.objects.filter(order__customer=customer)
    orders = Order.objects.filter(customer=customer)
    order = [order for order in orders if order.get_cart_total > 0]
    total_items = sum([item.quantity for item in order_item]) 
    order_count = len(order)
    form = UpdateCustomerForm(instance=customer)
    if request.method == 'POST':
        form = UpdateCustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profie successfully updated')
            return redirect('profile')
    context = {
        'customer':customer,
        'form':form,
        'orders':orders,
        'order':order,
        'order_count':order_count,
        'total_items':total_items,

    }
    return render(request, 'account/profile.html', context)