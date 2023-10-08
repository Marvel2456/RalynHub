from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from ecom.models import Category, Product, Order, Contact, ShippingDetail, PaymentHistory, Customer
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
    products = Product.objects.all()
    customers = Customer.objects.all()
    successfull_order = PaymentHistory.objects.filter(paid=True).all()
    pending_order = PaymentHistory.objects.filter(paid=False).all()

    all_products = products.count()
    all_customers = customers.count()
    all_pending_order = pending_order.count()
    all_successfull_order = successfull_order.count()
    context = {
        'all_products': all_products,
        'all_customers': all_customers,
        'all_successfull_order': all_successfull_order,
        'all_pending_order': all_pending_order 
    }
    return render(request, 'erm/dashboard.html', context)

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


def Customers(request):
    customer = Customer.objects.all()
    context = {'customer':customer}
    return render(request, 'erm/users.html', context)

def orderHistory(request):
    payment = PaymentHistory.objects.all()
    context = {
        'payment': payment
    }
    return render(request, 'erm/order.html', context)

def ShippingAddress(request):
    address = ShippingDetail.objects.all()
    return render(request, 'erm/shipping.html', {'address':address})

def shippingDetail(request, uuid):
    address = ShippingDetail.objects.get(id=uuid)
    return render(request, 'erm/shipping_detail.html', {'address':address})

def contacts(request):
    contact = Contact.objects.all()
    return render(request, 'erm/contact_list.html', {'contact':contact})

def contactDetail(request, uuid):
    contact = Contact.objects.get(id=uuid)
    return render(request, 'erm/contact_detail.html', {'contact':contact})

def deleteContact(request):
    if request.method == 'POST':
        contact_id = Contact.objects.get(id = request.POST.get('uuid'))
        if contact_id != None:
            contact_id.delete()
            messages.success(request, "Successfully deleted")
            return redirect('contact_list')
        
def deleteShipping(request):
    if request.method == 'POST':
        address = ShippingDetail.objects.get(id = request.POST.get('id'))
        if address != None:
            address.delete()
            messages.success(request, "Successfully deleted")
            return redirect('shipping')