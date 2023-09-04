from django.urls import path
from . import views

urlpatterns = [
   path('login/', views.loginView, name='admin_login'),
   path('dashboard/', views.Dashboard, name='dashboard'),
   path('product_list/', views.ProductList, name='product_list'),
   path('product_grid/', views.ProductGrid, name='product_grid'),
   path('add_product/', views.addProduct, name='add_product'),
   path('product_detail/', views.ProductDetail, name='product_detail'),
   path('category/', views.Categories, name='category'),
   path('add_category', views.addCategory, name='add_category'),
   
]
