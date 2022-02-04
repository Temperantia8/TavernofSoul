from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    #path('', views.index2, name='index'),
    #path('getTree', views.getTree, name = 'getTree'),
    #path('getTreeData', views.getTreeData, name = 'getTreeData'),
    path('', views.index, name='index'),
    path('getJob', views.getJob, name = 'getJob'),
    path('test', views.index2, name='test')
]

# if settings.REGION == 'test':
#     urlpatterns.append(path('', views.index2, name='index'))

# else:
#     urlpatterns.append(path('', views.index, name='index'))
