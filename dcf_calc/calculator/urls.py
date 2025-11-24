# calculator/urls.py
from django.urls import path
from .views import dcf_view

urlpatterns = [
    path('', dcf_view, name='dcf_form'),
]
