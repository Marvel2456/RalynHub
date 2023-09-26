from django.shortcuts import render, redirect
from . models import *
from django.http import JsonResponse
import json
import datetime
import requests
from django.views.decorators.csrf import csrf_exempt
from account.models import Customer
from .forms import UpdateCustomerForm, CreateReviewForm
from django.contrib import messages
from .utils import cookieCart, cartData, guestOrder
from django.core.paginator import Paginator
from django.conf import settings
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

    if category is None:
        products = Product.objects.all()
    else:
        products = Product.objects.filter(category__name=category)

    product_contains_query = request.GET.get('product')

    if product_contains_query != '' and product_contains_query is not None:
        products = products.filter(name__icontains=product_contains_query)

    categories = Category.objects.all()

    paginator = Paginator(products, 2)
    page = request.GET.get('page')
    product_page = paginator.get_page(page)
    nums = "a" * product_page.paginator.num_pages
    
    context = {
        'products':products,
        'items':items,
        'order':order,
        'total_quantity':total_quantity,
        'product_page':product_page,
        'nums':nums,
        'categories':categories,
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
    product = Product.objects.all()
    context = {
        'product':product,
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
    # orderItem = OrderItem.objects.get(id=request.POST['orderItemId'])
    if request.user.is_authenticated:
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
        'total_quantity':order.get_cart_items,
    }

    return JsonResponse(context, safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        
    else:
        customer, order = guestOrder(request, data)
        
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.completed = True
    order.save()

    if order.shipping == True:
        ShippingDetail.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            state = data['shipping']['state'],
            city = data['shipping']['city'],
            zipcode = data['shipping']['zipcode'],
            phone = data['shipping']['phone'],
        )

    return JsonResponse('Payment completed', safe=False)


def Checkout(request):
    data = cartData(request)
    order = data['order']
    items = data['items']
    total_quantity = data['total_quantity']

    context = {
        'items':items,
        'order':order,
        'total_quantity':total_quantity,
    }
    return render(request, 'ecom/checkout.html', context)


# def make_payment(request, uuid):
#     order = Order.objects.get(id=uuid)
#     if request.method == "POST":
#         amount = order.get_cart_total
#         email = order.customer.email

#         pk = settings.PAYSTACK_PUBLIC_KEY

#         payment = PaymentHistory.objects.create(amount=amount, email=email)
#         payment.save()

#         context = {
#             'payment': payment,
#             'field_values': request.POST,
#             'paystack_pub_key': pk,
#             'amount_value': payment.amount_value() if payment else 0,
#             'order':order,
#         }
#         return render(request, 'ecom/checkout.html', context)

# def verify_payment(request, ref):
#     payment = PaymentHistory.objects.get(ref=ref)
#     paid = payment.verify_payment()

#     if paid:
#         payment.save()
#         messages.success(request, "Payment successful")
#         return redirect('index')

@csrf_exempt
def initiatePayment(request):
    order_id = request.data.get('order_id')
    if request.method == 'POST':

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
             return JsonResponse({'error': 'Invalid order ID'}, status=400)
            
        amount = order.get_cart_total
        email = order.customer.email
       
        paystack_secret_key = settings.PAYSTACK_SECRET_KEY

        
        paystack_url = 'https://api.paystack.co/transaction/initialize'
        headers = {
            'Authorization': f'Bearer {paystack_secret_key}',
            'Content-Type': 'application/json',
        }
        data = {
            'amount': amount * 100,  # Amount in kobo (multiply by 100)
            'email': email,
        }
        response = requests.post(paystack_url, json=data, headers=headers)

        if response.status_code == 200:
            data = response.json()
            
            return JsonResponse({'data': data})
        else:
            return JsonResponse({'error': 'Payment initialization failed'}, status=400)
    
    

@csrf_exempt
def paystackCallback(request):
    if request.method == "POST":
        try:
            callback_data = json.loads(request.body.decode('utf-8'))

            payment_status = callback_data.get("status")
            order_id = callback_data.get("order_id")
            paystack_charge_id = callback_data.get("paystack_charge_id")
            paystack_access_code = callback_data.get("paystack_access_code")

            if payment_status == "success":
                try:
                    payment_history = PaymentHistory.objects.get(order__id=order_id)

                    payment_history.paystack_charge_id = paystack_charge_id
                    payment_history.paystack_access_code = paystack_access_code
                    payment_history.paid = True

                    payment_history.save()

                    return JsonResponse({"message": "Payment successfully updated."}, status=200)

                except PaymentHistory.DoesNotExist:
                    return JsonResponse({"message": "Payment history not found."}, status=404)
            else:
                return JsonResponse({"message": "Payment not successful."}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON data in the request."}, status=400)
    else:
        return JsonResponse({"message": "Invalid request method."}, status=405)


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
    customer = request.user.customer
    order = Order.objects.filter(customer=customer)
    
    context = {
        'order':order,
    }

    return render(request, 'ecom/order_history.html', context)