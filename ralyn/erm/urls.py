from django.urls import path
from . import views

urlpatterns = [
   path('login/', views.loginView, name='admin_login'),
   path('dashboard/', views.Dashboard, name='dashboard'),
   path('product_list/', views.ProductList, name='product_list'),
   path('add_product/', views.addProduct, name='add_product'),
   path('product_detail/', views.ProductDetail, name='product_detail'),
   path('category/', views.Categories, name='category'),  
   path('user/', views.Customers, name='user'),
   path('edit_product/<str:uuid>/', views.UpdateProduct, name='edit_product'),
   path('delete_product/', views.deleteProduct, name='delete_product'),
   path('edit_category/', views.EditCategory, name='edit_category'),
   path('delete_category/', views.deleteCategory, name='delete_category'),
   path('order/', views.Orders, name='order'),
]
