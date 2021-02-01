# coding: UTF-8
from django.urls import path

from verifications import views

app_name = 'verifications'

urlpatterns = [
    path('new-verification/', views.new_verification, name="new_verification"),

]
