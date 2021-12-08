from django.db import models

from django.db.models import Q
class Achievements (models.Model):
    ids             = models.CharField(max_length = 30, db_index=True)
    id_name         = models.CharField(max_length = 100,  db_index=True)
    descriptions    = models.TextField()
    desc_title 		= models.TextField()
    group 			= models.CharField(max_length = 100,blank=True, null=True, )
    icon            = models.CharField(max_length = 50, blank=True, null=True, )
    image           = models.CharField(max_length = 50, blank=True, null=True, )
    hidden 			= models.BooleanField(default=False)
    name            = models.TextField( )
    created         = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)
