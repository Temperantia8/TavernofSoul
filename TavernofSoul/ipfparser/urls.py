from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:id>', views.item_detail, name='item'),
]
