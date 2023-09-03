from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from ecom.models import Category, Product, Order, OrderItem, ShippingDetail
# Create your views here.


def loginView(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
           
            messages.success(request, f'Welcome {user.email}')
            return redirect('index')
        
        else:
            messages.info(request, 'Email or Password is not correct')

    return render(request, 'erm/login.html')

def logoutView(request):
    logout(request)
    return redirect('login')

def Dashboard(request):
    pass

def Categories(request):
    pass

def CategoryDetail(request):
    pass

def Products(request):
    pass

def ProductDetail(request, pk):
    pass

def Orders(request):
    pass

def Payment(request):
    pass