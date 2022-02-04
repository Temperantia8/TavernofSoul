from django.urls import path
from django.conf import settings
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
]

if settings.REGION=='test':
    urlpatterns = [
        path('', views.index, name = 'market'),
        path('postMarket', csrf_exempt(views.post), name = 'postMarket'),
    ]    