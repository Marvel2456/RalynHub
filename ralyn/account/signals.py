from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Customer

@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
       
    if created:
        user = instance
        customer = Customer.objects.create(
            user = user,
            username = user.username,
            email = user.email,
        )

@receiver(post_save, sender=Customer)
def update_user(sender, instance, created, **kwargs):
    customer = instance
    user = customer.user

    if created == False:
        user.email = customer.email
        user.username = customer.username
        user.save()
