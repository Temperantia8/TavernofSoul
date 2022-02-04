"""TavernofSoul URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap # new
from Attributes.models import Attributes
from Buffs.models import Buffs
from Items.models import Items
from Jobs.models import Jobs
from Skills.models import Skills
from Maps.models import Maps
from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from django.conf import settings
class StaticViewSitemap(Sitemap):
    def items(self):
        return ['Dashboard:index', 
            'Items:index', 
            'Skills:index', 
            'Buffs:index', 
            'Jobs:index',
            'Attributes:index',
            'Planner:index',
            'Other:achieve'
            ]
    def location(self, item):
        return reverse(item)

sitemaps = {
    'static'     : StaticViewSitemap,
    "attributes" : GenericSitemap({'queryset' : Attributes.objects.all()}),
    "buffs"      : GenericSitemap({'queryset' : Buffs.objects.all()}),
    "items"      : GenericSitemap({'queryset' : Items.objects.all()}),
    "jobs"       : GenericSitemap({'queryset' : Jobs.objects.all()}),
    "maps"       : GenericSitemap({'queryset' : Maps.objects.all()}),
    "skills"     : GenericSitemap({'queryset' : Skills.objects.all()}),


}

urlpatterns = [
    path('', include(('Dashboard.urls',"Dashboard"),namespace = "Dashboard")),    
    path('items/', include(('Items.urls',"Items"),namespace = "Items")),   
    path('monsters/', include(('Monsters.urls',"Monsters"),namespace = "Monsters")), 
    path('maps/', include(('Maps.urls',"Maps"),namespace = "Maps")), 
    path('jobs/', include(('Jobs.urls',"Jobs"),namespace = "Jobs")), 
    path('skills/', include(('Skills.urls',"Skills"),namespace = "Skills")), 
    path('attributes/', include(('Attributes.urls',"Attributes"),namespace = "Attributes")), 
    path('buffs/', include(('Buffs.urls',"Buffs"),namespace = "Buffs")), 
    path('planner/', include(('Planner.urls',"Planner"),namespace = "Planner")), 
    path('other/', include(('Other.urls',"Other"),namespace = "Other")), 
    #path('changes/', include(('ipfparser.urls',"Parser"),namespace = "Parser")), 
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},name='django.contrib.sitemaps.views.sitemap'),
    path('market/', include(('Market.urls',"Market"),namespace = "Market"))


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
