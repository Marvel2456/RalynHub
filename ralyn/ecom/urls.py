from django.urls import path
from .import views

urlpatterns = [
    path('products/', views.productIndex, name='products'),
    path('about/', views.About, name='about'),
    path('', views.Index, name='index'),
    path('contact/', views.Contact, name='contact'),
    path('cart/', views.Cart, name='cart'),
    path('checkout/', views.Checkout, name='checkout'),
    path('update_item/', views.UpdateItems, name='update_item'),
    path('update_quantity/', views.updateQuantity, name='update_quantity'),
    # path('process_order/', views.processOrder, name='process_order'),
    path('detail/<str:uuid>/', views.productDetail, name='detail'),
    path('get_categories/', views.get_categories, name='get_categories'),
    path('order_history/', views.orderHistory, name='order_history'),
    path('initiate_payment/', views.initiatePayment, name='initiate_payment'),
    path('<str:ref>/', views.verify_payment, name='verify_payment'),
   

]
