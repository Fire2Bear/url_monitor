# coding: UTF-8
from django.urls import path

from verification_results import views

app_name = 'verification_results'

urlpatterns = [
    path('verification-results-<int:page_id>/',
         views.verification_results_by_page,
         name="verification_results_by_page"
         ),

]
