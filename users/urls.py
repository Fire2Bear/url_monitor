# coding: UTF-8
from django.urls import path

from users import views

app_name = 'users'
urlpatterns = [
    path(r'hello/', views.hello, name="hello"),
    path('register/', views.register, name="register"),
    path('logout/', views.logout_view, name="logout"),
    path('login/', views.login_view, name="login"),
    path('myaccount/', views.myaccount, name="myaccount"),
    path('account-settings/', views.account_settings, name="account_settings"),
]
