from django.shortcuts import render, redirect
from . models import *
# Create your views here.

def index(request):
    item = Item.objects.all()

    context = {
        'item':item,
    }
    return render(request, 'ecom/index.html', context)