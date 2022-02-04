from django.db import models

# Create your models here.

class Builds(models.Model):
	url 	= models.TextField()
	count 	= models.IntegerField(default=0)
	classes = models.ManyToManyField('Jobs.Jobs')
	updated = models.DateTimeField(auto_now=True)
