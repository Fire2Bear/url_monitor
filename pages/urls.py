# coding: UTF-8
from django.urls import path

from pages import views, cbv

app_name = 'pages'
urlpatterns = [
    path('page-list/', views.page_list, name="page_list"),
    path('page-verifications-<int:page_id>/', views.page_verifications, name="page_verifications"),
    path('new-page/', views.new_page, name="new_page"),
    path('delete-page-<int:pk>/', cbv.PageDeleteView.as_view(), name="delete_page"),
]