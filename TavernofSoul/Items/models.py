from django.db import models
from django_mysql.models import ListCharField
from Skills.models import Skills
from django.urls import reverse
# Create your models here.

class Items (models.Model):
    ids         = models.CharField(max_length = 30, db_index=True)
    id_name         = models.CharField(max_length = 100, db_index=True)
    cooldown        = models.IntegerField(default=None, blank=True, null=True) 
    descriptions    = models.TextField(default=None, blank=True, null=True) 
    name            = models.CharField(max_length = 200,default=None, blank=True, null=True) 
    weight          = models.FloatField(blank = True, null = True)
    tradability     = models.CharField(max_length = 5,default=None, blank=True, null=True) 
    type            = models.CharField(max_length = 15,default=None, blank=True, null=True, db_index=True) 
    grade           = models.IntegerField(default=0, blank=True, null=True, db_index=True)
    icon            = models.CharField(max_length = 100,default=None, blank=True, null=True)
    created         = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)
    def get_absolute_url(self):
        return reverse('Items:item', args=[str(self.ids)])
    def compare(self, their):
        if (
            self.ids == their.ids and 
            self.id_name == their.id_name and 
            self.cooldown == their.cooldown and 
            self.name == their.name and 
            self.weight == their.weight and 
            self.tradability == their.tradability and 
            self.type == their.type and 
            self.grade == their.grade and 
            self.icon == their.icon 
            ):
            return True 
        else:
            return False

   


class Equipments (models.Model):
    item            = models.OneToOneField(
                        Items,
                        on_delete=models.CASCADE,
                        primary_key=True,
                    )
    anvil_atk       = ListCharField(base_field=models.IntegerField(),
                    size=41,
                    max_length=(10 * 41),blank=True, null=True
                    )
    anvil_def       = ListCharField(base_field=models.IntegerField(),
                    size=41,
                    max_length=(10 * 41),blank=True, null=True
                    )
    anvil_price     = ListCharField(base_field=models.IntegerField(),
                    size=41,
                    max_length=(10 * 41),blank=True, null=True
                    )
    durability      = models.IntegerField(blank=True, null=True )
    level           = models.IntegerField(blank=True, null=True )
    potential       = models.IntegerField(blank=True, null=True )
    requiredClass   = models.CharField(max_length=10,default=None, blank=True, null=True )
    sockets_limit   = models.IntegerField(blank=True, null=True )
    stars           = models.IntegerField(blank=True, null=True )
    matk            = models.IntegerField(blank=True, null=True )
    patk            = models.IntegerField(blank=True, null=True )
    patk_max        = models.IntegerField(blank=True, null=True )
    mdef            = models.IntegerField(blank=True, null=True )
    pdef            = models.IntegerField(blank=True, null=True )
    transcend_price = ListCharField(base_field=models.IntegerField(),
                    size=10,
                    max_length=(3 * 10),
                    )
    type_attack     = models.CharField(max_length=20,default=None, blank=True, null=True)
    type_equipment  = models.CharField(max_length=20,default=None, blank=True, null=True)
    unidentified    = models.BooleanField()
    unidentifiedRandom = models.BooleanField()

    def is_goddess_armor(self):
        return self.item.grade ==6 and  self.type_equipment in ['Shirt', 'Pants', 'Boots', 'Gloves']


class Equipment_Bonus(models.Model):
    equipment =  models.ForeignKey(Equipments, 
        verbose_name="Equipment_Bonus", on_delete=models.CASCADE, )
    bonus_stat = models.CharField(max_length=30)
    bonus_val = models.TextField()
    def sepparateline(self):
        a =  self.bonus_val
        b = []
        for i in a :
            i.strip()
            if len(i) >0: 
                b.append(i)
        return a

class Cards (models.Model):
    item            = models.OneToOneField(
                        Items,
                        on_delete=models.CASCADE,
                        primary_key=True,
                    ) 
    type_card       = models.CharField(max_length=50,default=None, blank=True, null=True )
    icon            = models.CharField(max_length = 70,default=None, blank=True, null=True)


    def compare(self, their):
        if (
            self.item == their.item and 
            self.type_card == their.type_card and 
            self.icon == their.icon  
            ):
            return True 
        else:
            return False

class Gems (models.Model):
    item            = models.OneToOneField(
                        Items,
                        on_delete=models.CASCADE,
                        primary_key=True,
                    )
    skill           = models.ForeignKey(Skills, on_delete=models.CASCADE, null = True, blank = True, default = None)

    def compare(self, their):
        if (
            self.item == their.item and 
            self.skill == their.skill  
            ):
            return True 
        else:
            return False


class Recipes(models.Model):
    item            = models.OneToOneField(
                        Items,
                        on_delete=models.CASCADE,
                        primary_key=True,
                    )
    def compare(self, their):
        if (
            self.item == their.item  
            ):
            return True 
        else:
            return False


class Item_Recipe_Material(models.Model):
    recipe          =   models.ForeignKey(Recipes, 
        verbose_name="recipe", on_delete=models.CASCADE, )          
    material        = models.ForeignKey(Items, 
        verbose_name="recipe_material", on_delete=models.CASCADE, ) 
    qty             = models.IntegerField()

    def compare(self, their):
        if (
            self.recipe == their.recipe and 
            self.material == their.material and 
            self.qty == their.qty  
            ):
            return True 
        else:
            return False


class Item_Recipe_Target(models.Model):
    recipe          =   models.ForeignKey(Recipes, 
        verbose_name="recipe", on_delete=models.CASCADE, )          
    target          =  models.ForeignKey(Items, 
        verbose_name="target", on_delete=models.CASCADE)
    def compare(self, their):
        if (
            self.recipe == their.recipe and 
            self.target == their.target 
            ):
            return True 
        else:
            return False


class Cubes(models.Model):
    item            = models.OneToOneField(
                        Items,
                        on_delete=models.CASCADE,
                        primary_key=True,
                    )


class Collections(models.Model):
    item            = models.OneToOneField(
                        Items,
                        on_delete=models.CASCADE,
                        primary_key=True,
                    )


class Item_Collection_Material(models.Model):
    collection = models.ForeignKey(Collections, 
        verbose_name="collection", on_delete=models.CASCADE, )  
    material = models.ForeignKey(Items, 
        verbose_name="collection_material", on_delete=models.CASCADE, ) 

class Item_Collection_Bonus(models.Model):
    collection = models.ForeignKey(Collections, 
        verbose_name="collection", on_delete=models.CASCADE, )  
    bonus_stat = models.CharField(max_length=30)
    bonus_val = models.CharField(max_length=30)

class Item_Type(models.Model):
    name = models.CharField(max_length=30)
    is_equipment = models.BooleanField(default=False)

class Books(models.Model):
    item            = models.OneToOneField(
                        Items,
                        on_delete=models.CASCADE,
                        primary_key=True,
                    )
    text            = models.TextField( null = True, blank = True, default = None)


class Equipment_Set(models.Model):
    equipment   = models.ManyToManyField(Equipments)
    ids         = models.CharField(max_length = 30, db_index=True)
    id_name     = models.CharField(max_length = 30, db_index=True)
    name        =  models.CharField(max_length = 50, blank = True, default = None, null = True)
    bonus2      = models.CharField(max_length = 100, blank = True, default = None, null = True)
    bonus3      = models.CharField(max_length = 100, blank = True, default = None, null = True)
    bonus4      = models.CharField(max_length = 100, blank = True, default = None, null = True)
    bonus5      = models.CharField(max_length = 100, blank = True, default = None, null = True)
    bonus6      = models.CharField(max_length = 100, blank = True, default = None, null = True)
    bonus7      = models.CharField(max_length = 100, blank = True, default = None, null = True)
    def compare(self, their):
        if (
            self.equipment == their.equipment and 
            self.ids == their.ids and 
            self.id_name == their.id_name and 
            self.name == their.name and 
            self.bonus2 == their.bonus2 and 
            self.bonus3 == their.bonus3 and 
            self.bonus4 == their.bonus4 and 
            self.bonus5 == their.bonus5 and 
            self.bonus6 == their.bonus6 and 
            self.bonus7 == their.bonus7
            ):
            return True 
        else:
            return False

