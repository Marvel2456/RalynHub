from django.urls import path
from .import views

urlpatterns = [
    path('', views.Index, name='index'),
    path('about/', views.About, name='about'),
    path('products/', views.Products, name='products'),
    path('contact/', views.Contact, name='contact')
    
]
