import json
from .models import *

def cookieCart(request):
    
    try:
        cart = json.loads(request.COOKIES['cart'])
        
    except:
        cart = {}
    print ('Cart:', cart)
    items = []
    order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
    total_quantity = order['get_cart_items']

    for i in cart:
        try:
            total_quantity += cart[i]['quantity']

            product = Product.objects.get(id=i)
            sub_total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += sub_total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL,
                    },
                'quantity':cart[i]['quantity'],
                'get_total':sub_total,
                    }
            items.append(item)
        except:
            pass
    return {'items':items, 'order':order, 'total_quantity':total_quantity}

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        total_quantity = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        order = cookieData['order']
        items = cookieData['items']
        total_quantity = cookieData['total_quantity']
    return {'order':order, 'items':items, 'total_quantity':total_quantity}


def guestOrder(request, data):
    print('User is not authenticated')
    print('COOKIES:', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(
        email=email
    )
    customer.name = name
    customer.save()
    order =  Order.objects.create(
        customer = customer,
        completed = False,
    )

    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        orderitem = OrderItem.objects.create(
            order = order,
            product = product,
            quantity = item['quantity'],
            # price = product.price,
        )

    return customer, order
