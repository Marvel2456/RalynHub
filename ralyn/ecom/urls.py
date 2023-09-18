from django.urls import path
from .import views

urlpatterns = [
    path('', views.Index, name='index'),
    path('about/', views.About, name='about'),
    path('products/', views.Products, name='products'),
    path('contact/', views.Contact, name='contact'),
    path('cart/', views.Cart, name='cart'),
    path('checkout/', views.Checkout, name='checkout'),
    path('update_item/', views.UpdateItems, name='update_item'),
    path('update_quantity/', views.updateQuantity, name='update_quantity'),
    path('process_order/', views.processOrder, name='process_order'),
    path('profile/', views.Profile, name='profile' ),
    path('detail/<str:uuid>/', views.productDetail, name='detail'),
    path('get_categories/', views.get_categories, name='get_categories'),
]
