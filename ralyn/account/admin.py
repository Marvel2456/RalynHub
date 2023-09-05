from django.contrib import admin
from account.models import User, Customer
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'username', 'is_staff']

admin.site.register(User, CustomUserAdmin)
admin.site.register(Customer)


