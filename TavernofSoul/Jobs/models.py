from django.db import models
from django.urls import reverse
from enum import Enum
# Create your models here.


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
    def compare(self, their):
        if (
            self.ids == their.ids and 
            self.id_name == their.id_name and 
            self.name == their.name and 
            self.descriptions == their.descriptions and 
            self.is_starter == their.is_starter and 
            self.job_tree == their.job_tree and 
            self.icon == their.icon  
            ):
            return True 
        else:
            return False
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

