from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    #path('getTree', views.getTree, name = 'getTree'),
    #path('getTreeData', views.getTreeData, name = 'getTreeData'),
    #path('getJob', views.getJob, name = 'getJob')
]
