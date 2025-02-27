from django.db import models, transaction
from django.contrib.auth import get_user_model
import uuid
import secrets
from account.models import User, Customer
from .paystack import Paystack
from datetime import datetime

# Create your models here.

class Category(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=225, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=255, blank=True, null=True)
    main_image = models.ImageField(upload_to='item/image', blank=True, null=True)
    image1 = models.ImageField(upload_to='item/image', blank=True, null=True)
    image2 = models.ImageField(upload_to='item/image', blank=True, null=True)
    image3 = models.ImageField(upload_to='item/image', blank=True, null=True)
    image4 = models.ImageField(upload_to='item/image', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    store_quantity = models.PositiveIntegerField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    is_popular = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.main_image.url
        except:
            url = ''
        return url
    @property
    def image1URL(self):
        try:
            url = self.image1.url
        except:
            url = ''
        return url
    @property
    def image2URL(self):
        try:
            url = self.image2.url
        except:
            url = ''
        return url
    @property
    def image3URL(self):
        try:
            url = self.image3.url
        except:
            url = ''
        return url
    @property
    def image4URL(self):
        try:
            url = self.image4.url
        except:
            url = ''
        return url

class Order(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    ordered_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False, blank=True, null=True)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.customer)
    
    @property
    def shipping(self):
        shipping = True
        orderitems = self.orderitem_set.all()
        for items in orderitems:
            if items in orderitems:
                shipping = True
        return shipping
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
#  should look for a way to add shipping cost dynamically or manually and update the grand total with shipping included

class OrderItem(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

# Add is popular boolean field to the product to create a list of all the popular products

class ShippingDetail(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=225, blank=True, null=True)
    city = models.CharField(max_length=225, blank=True, null=True)
    state = models.CharField(max_length=225, blank=True, null=True)
    zipcode = models.CharField(max_length=225, blank=True, null=True)
    phone = models.CharField(max_length=225, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.address)

    
class Remark(models.Model):
    client_name = models.CharField(max_length=225, blank=True, null=True)
    picture = models.ImageField(upload_to='remark/image', blank=True, null=True)
    client_remark = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.client_name
    

class Review(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.customer.username} - {self.created_at}'
    

class Contact(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=225, blank=True, null=True)
    email = models.CharField(max_length=225, blank=True, null=True)
    subject = models.CharField(max_length=225, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.created_at}'
    

class PaymentHistory(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False) 
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    email = models.EmailField()
    ref = models.CharField(max_length=200, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    paid = models.BooleanField(default=False, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'payment histories'

    def __str__(self) -> str:
        return f'{self.customer.email} - {self.order} - {self.amount} - {self.date}'

    
    def save(self, *args, **kwargs):
        with transaction.atomic():
            while not self.ref:
                ref = secrets.token_urlsafe(50)
                object_with_similar_ref = PaymentHistory.objects.select_for_update().filter(ref=ref)
                if not object_with_similar_ref.exists():
                    self.ref = ref
        
            return super().save(*args, **kwargs)
    
    def amount_value(self):
        return int(float(self.amount) * 100)

    def verify_payment(self):
        paystack = Paystack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:
            if result['amount'] / 100 == self.amount:
                self.paid = True
                self.order.completed = True
                self.order.transaction_id = datetime.now()
                self.order.save()
            self.save()
        if self.paid:
            return True
        return False

