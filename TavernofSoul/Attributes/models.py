from django.db import models
from Jobs.models import Jobs
from Skills.models import Skills
from django.urls import reverse

# Create your models here.

class Attributes (models.Model):
    ids                     = models.CharField(max_length = 30, db_index=True)
    id_name                 = models.CharField(max_length = 50) 
    descriptions            = models.TextField() 
    descriptions_required   = models.TextField(blank=True, null= True) 
    icon                    = models.CharField(max_length = 70,default=None, blank=True, null=True)
    is_toggleable           = models.BooleanField()
    max_lv                  = models.IntegerField()
    name                    = models.CharField(max_length = 150) 
    skill                   = models.ManyToManyField(Skills)
    job                     = models.ManyToManyField(Jobs)
    created         = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)

    def compare(self, their):
        if (
            self.ids == their.ids and 
            self.id_name == their.id_name and 
            self.name == their.name and 
            self.descriptions == their.descriptions and 
            self.descriptions_required == their.descriptions_required and 
            self.icon == their.icon and 
            self.is_toggleable == their.is_toggleable and 
            self.max_lv == their.max_lv  
            
            ):
            return True 
        else:
            return False

    def get_absolute_url(self):
        return reverse('Attributes:attributes', args=[str(self.ids)])