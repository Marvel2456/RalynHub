from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.RegisterView, name='register'),
    path('activate/<uidb64>/<token>/', views.ActivateView, name='activate'),
    path('login/', views.LoginView, name='login'),
    path('logout/', views.LogoutView, name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
                    template_name = 'account/password_reset.html'
                    ), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(
                    template_name = 'account/password_reset_done.html'
                    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
                    template_name = 'account/password_reset_confirm.html'
                    ), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
                    template_name = 'account/password_reset_complete.html'
                    ), name='password_reset_complete'),
    path('change-password/',auth_views.PasswordChangeView.as_view(
                    template_name='account/change_password.html',
                    ), name='change-password'),
    path('profile/', views.Profile, name='profile'),
    
]