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
            return redirect('dashboard')
        
        else:
            messages.info(request, 'Email or Password is not correct')

    return render(request, 'erm/login.html')

def logoutView(request):
    logout(request)
    return redirect('login')

def Dashboard(request):
    return render(request, 'erm/dashboard.html')

def Categories(request):

    return render(request, 'erm/category.html')

def addCategory(request):
    return render(request, 'erm/category.html')


def addProduct(request):
    return render(request, 'erm/add_product.html')

def ProductList(request):
    return render(request, 'erm/product_list.html')

def ProductGrid(request):
    return render(request, 'erm/product_grid.html')

def ProductDetail(request, pk):
    pass

def Orders(request):
    pass

def Payment(request):
    pass