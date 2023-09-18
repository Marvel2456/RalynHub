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
