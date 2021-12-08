from django.db import models
from django_mysql.models import ListCharField
from Items.models import Items
from Monsters.models import Monsters
from django.db.models import Q
from django.urls import reverse
class Maps(models.Model):
    ids         = models.CharField(max_length = 20, db_index=True)
    id_name         = models.CharField(max_length = 100)
    icon            = models.CharField(max_length = 50, blank=True, null=True, )
    name            = models.CharField(max_length = 100, blank=True, null=True, )
    has_cm          = models.BooleanField(default=False)
    has_warp        = models.BooleanField(default=False)
    level           = models.IntegerField(default=-1)
    max_elite       = models.IntegerField(default=-1)
    max_hate        = models.IntegerField(default=-1)
    star            = models.IntegerField(default=-1)
    type            = models.CharField(max_length = 10)
    map_link        = ListCharField(base_field=models.CharField(max_length=20),
                    size=10,
                    max_length=(20 * 11),
                    )
    created         = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)
    def compare(self, their):
        if (
            self.ids == their.ids and 
            self.id_name == their.id_name and 
            self.icon == their.icon and 
            self.name == their.name and 
            self.has_cm == their.has_cm and 
            self.has_warp == their.has_warp and 
            self.level == their.level and
            self.max_elite == their.max_elite and
            self.max_hate == their.max_hate and
            self.star == their.star and
            self.type == their.type and
            self.map_link == their.map_link

            ):
            return True 
        else:
            return False
    def get_absolute_url(self):
        return reverse('Maps:maps', args=[str(self.ids)])


class Map_Item(models.Model):
    map             =  models.ForeignKey(Maps, on_delete=models.CASCADE, )
    item            = models.ForeignKey(Items, on_delete=models.CASCADE, )
    chance          = models.FloatField(default=0, blank=True, null=True, )
    qty_max         = models.IntegerField(default=0, blank=True, null=True, )
    qty_min         = models.IntegerField(default=0, blank=True, null=True, )
    def compare(self, their):
        if (
            self.map == their.map and 
            self.item == their.item and 
            self.chance == their.chance and 
            self.qty_max == their.qty_max and 
            self.qty_min == their.qty_min 
            

            ):
            return True 
        else:
            return False
    def chance_readable(self):
        return ("%.6f" % self.chance)


class Map_NPC(models.Model):
    map             =  models.ForeignKey(Maps, on_delete=models.CASCADE, )
    monster         =  models.ForeignKey(Monsters,on_delete=models.CASCADE, )
    positions       = ListCharField(base_field=models.CharField(max_length=700),
                    size=7,
                    max_length=(700 * 8),
                    )
    population      = models.IntegerField()
    time_respawn    = models.FloatField()
    def compare(self, their):
        if (
            self.map == their.map and 
            self.monster == their.monster and 
            self.positions == their.positions and 
            self.population == their.population and 
            self.time_respawn == their.time_respawn 
            ):
            return True 
        else:
            return False
    

class Map_Item_Spawn(models.Model):
    map             =  models.ForeignKey(Maps, on_delete=models.CASCADE, )
    item            =  models.ForeignKey(Items,  on_delete=models.CASCADE, )
    positions       = ListCharField(base_field=models.CharField(max_length=20),
                    size=10,
                    max_length=(20 * 11),
                    )
    population      = models.IntegerField()
    time_respawn    = models.FloatField()
    
