from django.db import models
from os.path import join, exists
from django.conf import settings
from django.urls import reverse
# Create your models here.

class Buffs(models.Model):
    ids             = models.CharField(max_length = 30, db_index = True)
    id_name         = models.CharField(max_length = 100, db_index = True)
    icon            = models.CharField(max_length = 50, blank=True, null=True,)
    name            = models.CharField(max_length = 100)
    descriptions    = models.TextField( blank=True, null=True,)
    keyword         = models.TextField( blank=True, null=True,)
    created         = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)
    applytime 		= models.IntegerField(default = 0, blank=True, null=True,)
    group1 			= models.CharField(max_length = 30, blank=True, null=True,)
    group2 			= models.CharField(max_length = 30, blank=True, null=True,)
    group3 			= models.CharField(max_length = 30, blank=True, null=True,)
    groupindex 		= models.CharField(max_length = 30, blank=True, null=True,)
    overbuff		= models.IntegerField(default = 0)
    userremove  	= models.BooleanField(default= False)

    fields          = [
                'ids',
                'id_name',
                'icon',
                'name',
                'descriptions',
                'keyword',
                'created',
                'updated',
                'applytime',
                'group1',
                'group2',
                'group3',
                'groupindex',
                'overbuff',
                'userremove',]
                
    def iconExists(self):
        if self.icon == None:
            return False
        return exists (join(settings.STATIC_ROOT, 'icons', self.icon))

    def duration(self):
        return "0 s" if self.applytime == "" or self.applytime == None else str(int(self.applytime/1000)) + " s"

    def readableKeyword(self):
        return "  ".join(self.keyword.split(";"))
   
    def durationSec(self):
        return str(int(self.duration/1000))+" s"

    def get_absolute_url(self):
        return reverse('Buffs:buffs', args=[str(self.ids)])
