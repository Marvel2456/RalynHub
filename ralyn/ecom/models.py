from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

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
    image = models.ImageField(upload_to='item/image', blank=True, null=True)
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
            url = self.image.url
        except:
            url = ''
        return url

class Order(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    Ordered_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False, blank=True, null=True)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.user.email
    
    @property
    def shipping(self):
        shipping = False
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
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=225, blank=True, null=True)
    city = models.CharField(max_length=225, blank=True, null=True)
    state = models.CharField(max_length=225, blank=True, null=True)
    zipcode = models.CharField(max_length=225, blank=True, null=True)
    phone = models.CharField(max_length=225, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

    
class Remark(models.Model):
    client_name = models.CharField(max_length=225, blank=True, null=True)
    picture = models.ImageField(upload_to='remark/image', blank=True, null=True)
    client_remark = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.client_name
    

