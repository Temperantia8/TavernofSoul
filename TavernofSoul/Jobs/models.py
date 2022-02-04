from django.db import models
from django.urls import reverse
from enum import Enum
# Create your models here.
# from Skills.models import Equipments
from django.apps import apps


class Jobs(models.Model):
    ids             = models.CharField(max_length = 30, db_index = True)
    id_name         = models.CharField(max_length = 30)
    icon            = models.CharField(max_length = 30)
    job_tree        = models.CharField(max_length = 15)
    name            = models.CharField(max_length = 30)
    is_starter      = models.BooleanField( default = False)
    descriptions    = models.TextField()
    created         = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)
    vaivora         = models.ForeignKey('Items.Equipments', on_delete=models.SET_NULL, null = True, blank = True, default = None)
    
    def get_absolute_url(self):
        return reverse('Jobs:jobs', args=[str(self.ids)])

def getJobsByName():
    jobs = Jobs.objects.all()
    jobsByName = {}
    for job in jobs:
        cur = {}
        cur ['ids'] = job.ids 
        cur ['name'] = job.name 
        cur ['is_starter'] = job.is_starter
        cur ['job_tree'] = job.job_tree
        jobsByName['ids'] = cur
    return jobsByName

