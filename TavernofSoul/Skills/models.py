from django.db import models
from Jobs.models import Jobs
from django_mysql.models import ListCharField
from django.urls import reverse
# class Stance (models.Model):
#     icon = models.CharField(max_length = 30, blank=True, null=True,) 
#     name = models.CharField(max_length = 30, blank=True, null=True,) 

# Create your models here.
class Skills (models.Model):
    ids             = models.CharField(max_length = 30, db_index=True)
    id_name         = models.CharField(max_length = 100)
    icon            = models.CharField(max_length = 50) 
    name            = models.CharField(max_length = 30) 
    cooldown        = models.IntegerField() 
    cooldown_lv     = ListCharField(base_field=models.IntegerField(),
                    size=10,
                    max_length=(20 * 11), blank=True, null=True,
                    ) 
    sp              = models.IntegerField()
    sfr             = ListCharField(base_field=models.IntegerField(),
                    size=10,
                    max_length=(20 * 11), blank=True, null=True,
                    )
    descriptions    = models.TextField( blank=True, null=True,) 
    effect          = models.TextField( blank=True, null=True,) 
    element         = models.CharField(max_length = 30) 
    max_lv          = models.IntegerField( default =-1) 
    unlock          = models.IntegerField( default =0)  
    overheat        = models.IntegerField( default =0)
    captionratio1   = ListCharField(base_field=models.IntegerField(),
                    size=10,
                    max_length=(20 * 11), blank=True, null=True,
                    )
    captionratio2   = ListCharField(base_field=models.IntegerField(),
                    size=10,
                    max_length=(20 * 11), blank=True, null=True,
                    )
    captionratio3   = ListCharField(base_field=models.IntegerField(),
                    size=10,
                    max_length=(20 * 11), blank=True, null=True,
                    )
    captiontime     = ListCharField(base_field=models.IntegerField(),
                    size=10,
                    max_length=(20 * 11), blank=True, null=True,
                    )
    skillsr        = ListCharField(base_field=models.IntegerField(),
                    size=10,
                    max_length=(20 * 11), blank=True, null=True,
                    )
    spenditemcount   = ListCharField(base_field=models.IntegerField(),
                    size=10,
                    max_length=(20 * 11), blank=True, null=True,
                    )
    spendsp         = ListCharField(base_field=models.IntegerField(),
                    size=10,
                    max_length=(20 * 11), blank=True, null=True,
                    )
    spendpoison     = ListCharField(base_field=models.IntegerField(),
                    size=10,
                    max_length=(20 * 11), blank=True, null=True,
                    )
    other   = ListCharField(base_field=models.CharField(max_length=50),
                    size=3,
                    max_length=(51 * 3), blank=True, null=True,
                    )
    job             = models.ForeignKey(Jobs, on_delete=models.CASCADE,blank=True, null=True, )       
    # stance          = models.ManyToManyField(Stance, )
    stance          = models.TextField() 
    created         = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)
    is_riding       = models.BooleanField()
    def stance_readable(self):
        return " ".join(self.stance.split(";")) 
    def get_absolute_url(self):
        return reverse('Skills:skills', args=[str(self.ids)])
