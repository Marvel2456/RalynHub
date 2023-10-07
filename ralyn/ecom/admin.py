from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(ShippingDetail)
admin.site.register(Remark)
admin.site.register(Review)
admin.site.register(PaymentHistory)
admin.site.register(Contact)