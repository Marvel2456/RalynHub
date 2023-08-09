from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=225, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='item/image', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    store_quantity = models.PositiveIntegerField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.name


class OrderItem(models.Model):
    pass

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


# Add is popular boolean field to the product to create a list of all the popular products
