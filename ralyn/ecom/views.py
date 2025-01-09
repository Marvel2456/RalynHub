from django.shortcuts import render, redirect
from . models import *
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from account.models import Customer
from .forms import UpdateCustomerForm, CreateReviewForm, ShippingForm, PaymentForm
from django.contrib import messages
from .utils import cookieCart, cartData, guestOrder
from django.core.paginator import Paginator
from django.conf import settings
import pytz
from django.core.cache import cache
from django.db.models import Prefetch

# Create your views here.

def get_categories(request):
    categories = Category.objects.all().values('id', 'name')
    return JsonResponse(list(categories), safe=False)

def productIndex(request):
    data = cartData(request)
    order = data['order']
    items = data['items']
    total_quantity = data['total_quantity']
    
    category = request.GET.get('category')

    cache_key = f'products_{category}'
    products = cache.get(cache_key)

    if not products:
        if category is None:
            products = Product.objects.all().only('id', 'name', 'main_image', 'price', 'category')
        else:
            products = Product.objects.filter(category__name=category).only('id', 'name', 'main_image', 'price', 'category')
        
        cache.set(cache_key, products, 60 * 15)

    product_contains_query = request.GET.get('product')

    if product_contains_query:
        products = products.filter(name__icontains=product_contains_query)

    categories = cache.get('categories')
    if not categories:
        categories = Category.objects.all()
        cache.set('categories', categories, 60 * 15)

    paginator = Paginator(products, 2)
    page = request.GET.get('page')
    product_page = paginator.get_page(page)
    nums = "a" * product_page.paginator.num_pages
    
    context = {
        'products': products,
        'items': items,
        'order': order,
        'total_quantity': total_quantity,
        'product_page': product_page,
        'nums': nums,
        'categories': categories,
    }
    return render(request, 'ecom/products.html', context)

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

def Index(request):
    prod_list = Product.objects.all()[:6]
    context = {
        'prod_list':prod_list,
        }
    return render(request, 'ecom/index.html', context)

def Cart(request):
    data = cartData(request)
    order = data['order']
    items = data['items']
    total_quantity = data['total_quantity']
        

    context = {
        'items':items,
        'order':order,
        'total_quantity':total_quantity,
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

        'total_quantity': order.get_cart_items,
    }
        
    return JsonResponse(context, safe=False)


def updateQuantity(request):
    
    if request.user.is_authenticated:
        data = json.loads(request.body)
        input_value = int(data['val'])
        product_Id = str(data['prod_id'])
        
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
        'total_quantity':order.get_cart_items,
    }

    return JsonResponse(context, safe=False)

def Checkout(request):
    data = cartData(request)
    order = data['order']
    items = data['items']
    total_quantity = data['total_quantity']
    customer = request.user.customer
    form = ShippingForm()
    form_submitted = False

    try:
        shipping = ShippingDetail.objects.get(order=order)
        form = ShippingForm(instance=shipping)
    except ShippingDetail.DoesNotExist:
        form = ShippingForm()
        
    if request.method == 'POST':
        form = ShippingForm(request.POST)
        if form.is_valid():
            shipping = form.save(commit=False)
            shipping.order = order
            shipping.customer = customer
            shipping.save()
            order.save()
            form_submitted = True
            messages.success(request, "Shipping address updated")

    context = {
        'form':form,
        'customer': customer,
        'items':items,
        'order':order,
        'total_quantity':total_quantity,
        'form_submitted': form_submitted,
    }
    return render(request, 'ecom/checkout.html', context)



def initiatePayment(request):
    data = cartData(request)
    order = data['order']
    items = data['items']
    total_quantity = data['total_quantity']
    pk = settings.PAYSTACK_PUBLIC_KEY
    customer = Customer.objects.get(user=request.user)
    if request.method == 'POST':
        amount = request.POST['amount']
        email = request.POST['email']
		

        payment = PaymentHistory.objects.create(amount=amount, order=order, email=email, customer=customer)
        payment.save()
        print("Amount:", amount)
        print("Order:", order)

        context = {
            'order': order,
            'items': items,
            'total_quantity': total_quantity,
            'customr':customer,
			'payment': payment,
			'field_values': request.POST,
			'paystack_pub_key': pk,
			'amount_value': payment.amount_value(),
		}
        return render(request, 'ecom/make_payment.html', context)
    
    
   
    return render(request, 'ecom/payment.html', {'order':order})


def verify_payment(request, ref):
    customer = request.user.customer
    payment = PaymentHistory.objects.filter(customer=customer).get(ref=ref)
    verified = payment.verify_payment()

    if verified:
	    return redirect('products')
   

def contact(request):
    contactss = Contact.objects.all()
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        contactss = Contact(name=name, email=email, subject=subject, message=message)

        contactss.save()

        messages.success(request, 'Your request has been submitted thank you')
        return redirect('index')
    return render(request, 'ecom/index.html')

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
    data = cartData(request)
    order = data['order']
    items = data['items']
    total_quantity = data['total_quantity']

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
        'order':order,
        'items':items,
        'total_quantity':total_quantity,
        'product':product,
        'form':form,
    }
    return render(request, 'ecom/detail.html', context)

def orderHistory(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order = Order.objects.filter(customer=customer)
        
        context = {
            'order':order,
        }
        return render(request, 'ecom/order_history.html', context)
    else:
        return render(request, 'ecom/non_auth_user_message.html')
    
def productReview(request):
    pass







    
