from django.urls import path

from . import views

urlpatterns = [
    path('achieve', views.achieve, name='achieve'),
]
