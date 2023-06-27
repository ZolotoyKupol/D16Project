from django.urls import path
from . import views
from .views import confirmation, subscribe_newsletter
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('confirmation/', confirmation, name='confirmation'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('create_ad/', views.create_ad, name='create_ad'),
    path('edit_ad/<int:ad_id>/', views.edit_ad, name='edit_ad'),
    path('ad/<int:ad_id>/send-response/', views.send_response, name='send_response'),
    path('private/', views.private_page, name='private_page'),
    path('subscribe-newsletter/', subscribe_newsletter, name='subscribe_newsletter'),
]


