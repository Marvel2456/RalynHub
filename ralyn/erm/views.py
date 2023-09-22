from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from ecom.models import Category, Product, Order, OrderItem, ShippingDetail
from erm.forms import *
from account.models import Customer
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
    category = Category.objects.all()
    form = CreateCategoryForm()
    if request.method == 'POST':
        form = CreateCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'category successfully created')
            return redirect('category')
        
    context = {
        'category':category,
        'form':form
    }
    return render(request, 'erm/category.html', context)

def EditCategory(request):
    if request.method == 'POST':
        category = Category.objects.get(id = request.POST.get('uuid'))
        if category != None:
            form = UpdateCategoryForm(request.POST, instance=category)
            if form.is_valid():
                form.save()
                messages.success(request, 'successfully updated')
                return redirect('category')

def deleteCategory(request):
    if request.method == 'POST':
        category = Category.objects.get(id = request.POST.get('uuid'))
        if category != None:
            category.delete()
            messages.success(request, "Successfully deleted")
            return redirect('category')

def addProduct(request):
    form = CreateProductForm()
    if request.method == 'POST':
        form = CreateProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'product successfully created')
            return redirect('product_list')
    context = {
        'form':form
    }
    return render(request, 'erm/add_product.html', context)

def deleteProduct(request):
    if request.method == 'POST':
        product_id = Product.objects.get(id = request.POST.get('uuid'))
        if product_id != None:
            product_id.delete()
            messages.success(request, "Successfully deleted")
            return redirect('product_list')

def ProductList(request):
    product = Product.objects.all()
    context = {'product':product}
    return render(request, 'erm/product_list.html', context)


def ProductDetail(request, pk):
    pass

def UpdateProduct(request, uuid):
    product = Product.objects.get(id=uuid)
    form = UpdateProductForm(instance=product)
    if request.method == 'POST':
        form = UpdateProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    context = {
        'product':product,
        'form':form
    }
    return render(request, 'erm/edit_product.html', context)

def Orders(request):
    orders = Order.objects.all()
    
    context = {
        'orders':orders
    }
    return render(request, 'erm/order.html', context)

def Payment(request):
    pass

def Customers(request):
    customer = Customer.objects.all()
    context = {'customer':customer}
    return render(request, 'erm/users.html', context)