from django.db import models
from django_mysql.models import ListCharField
from Items.models import Items
from django.db.models import Q
class Monsters (models.Model):
    ids             = models.CharField(max_length = 30, db_index=True)
    id_name         = models.CharField(max_length = 100,  db_index=True)
    armor           = models.CharField(max_length = 30, blank=True, null=True, )
    descriptions    = models.TextField()
    element         = models.CharField(max_length = 30, blank=True, null=True, )
    exp             = models.IntegerField(default=0, blank=True, null=True, )
    exp_class       = models.IntegerField(default=0, blank=True, null=True, )
    icon            = models.CharField(max_length = 50, blank=True, null=True, )
    level           = models.IntegerField(default=0, blank=True, null=True, )
    name            = models.CharField(max_length = 100, )
    race            = models.CharField(max_length = 30, blank=True, null=True, )
    rank            = models.CharField(max_length = 15, blank=True, null=True, )
    size            = models.CharField(max_length = 15, blank=True, null=True, )
    accuracy        = models.IntegerField(default=0, blank=True, null=True, )
    matk_max        = models.IntegerField(default=0, blank=True, null=True, )
    matk_min        = models.IntegerField(default=0, blank=True, null=True, )
    patk_max        = models.IntegerField(default=0, blank=True, null=True, )
    patk_min        = models.IntegerField(default=0, blank=True, null=True, )
    blockpen        = models.IntegerField(default=0, blank=True, null=True, )
    block           = models.IntegerField(default=0, blank=True, null=True, )
    critdmg         = models.IntegerField(default=0, blank=True, null=True, )
    critdef         = models.IntegerField(default=0, blank=True, null=True, )
    critrate        = models.IntegerField(default=0, blank=True, null=True, )
    mdef            = models.IntegerField(default=0, blank=True, null=True, )
    pdef            = models.IntegerField(default=0, blank=True, null=True, )
    eva             = models.IntegerField(default=0, blank=True, null=True, )
    hp              = models.IntegerField(default=0, blank=True, null=True, )
    stat_dex        = models.IntegerField(default=0, blank=True, null=True, )
    stat_int        = models.IntegerField(default=0, blank=True, null=True, )
    stat_spr        = models.IntegerField(default=0, blank=True, null=True, )
    stat_str        = models.IntegerField(default=0, blank=True, null=True, )
    stat_con        = models.IntegerField(default=0, blank=True, null=True, )
    created         = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)

    fields          = [
                        'ids',
                        'id_name',
                        'armor',
                        'descriptions',
                        'element',
                        'exp',
                        'exp_class',
                        'icon',
                        'level',
                        'name',
                        'race',
                        'rank',
                        'size',
                        'accuracy',
                        'matk_max',
                        'matk_min',
                        'patk_max',
                        'patk_min',
                        'blockpen',
                        'block',
                        'critdmg',
                        'critdef',
                        'critrate',
                        'mdef',
                        'pdef',
                        'eva',
                        'hp',
                        'stat_dex',
                        'stat_int',
                        'stat_spr',
                        'stat_str',
                        'stat_con',
                    ]


    def is_npc(self):
        return self.rank == None or self.rank=='NPCNPC'
    def is_mon(self):
        return self.rank == 'Normal' or self.rank == 'Boss'
    def is_misc(self):
        return self.rank not in [None, 'Normal', 'Boss', 'NPC' ]


class Item_Monster(models.Model):
    monster         =  models.ForeignKey(Monsters, 
        verbose_name="monster_item_monster", on_delete=models.CASCADE, )
    item            = models.ForeignKey(Items, 
        verbose_name="monster_item_item", on_delete=models.CASCADE, )
    chance          = models.FloatField(default=0, blank=True, null=True, )
    qty_max         = models.IntegerField(default=0, blank=True, null=True, )
    qty_min         = models.IntegerField(default=0, blank=True, null=True, )
    def compare(self, their):
        if (
            self.monster == their.monster and 
            self.item == their.item and 
            self.chance == their.chance and 
            self.qty_max == their.qty_max and 
            self.qty_min == their.qty_min
            ):
            return True 
        else:
            return False


class Skill_Monster(models.Model):
    monsters        =  models.ManyToManyField(Monsters)
    ids             = models.CharField(max_length = 30, db_index=True)
    id_name         = models.CharField(max_length = 70,  db_index=True)
    name            = models.CharField(max_length = 100, )
    element         = models.CharField(max_length = 30) 
    cooldown        = models.IntegerField(blank=True, null=True,) 
    sfr             = models.IntegerField(blank=True, null=True,) 
    aar             = models.IntegerField(blank=True, null=True, default=50) 
    hit_count       = models.IntegerField(blank=True, null=True, default=1)
    def buffs(self):
        return Buff_Skill_Monster.objects.filter(skill = self)

    def cd_in_sec (self):
        return str(int(self.cooldown/1000)) + "s"

class Buff_Skill_Monster(models.Model):
    chance          = models.FloatField()
    duration        = models.FloatField()
    buff            = models.ForeignKey('Buffs.Buffs', on_delete=models.CASCADE)
    skill           = models.ForeignKey(Skill_Monster, on_delete=models.CASCADE)
