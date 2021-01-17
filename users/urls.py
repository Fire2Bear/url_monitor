# coding: UTF-8
from django.urls import path

from users import views

app_name = 'users'
urlpatterns = [
    path(r'hello/', views.hello, name="hello"),

]
