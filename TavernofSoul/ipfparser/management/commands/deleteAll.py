# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 14:08:20 2021

@author: Temperantia
"""


from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
import logging
import json
from os.path import join, exists
from Monsters.models import Monsters, Item_Monster, Skill_Monster
import os
import shutil
from Items.models import Items, Equipments, Equipment_Bonus, Cards, Recipes, Books
from Items.models import Item_Recipe_Material, Item_Recipe_Target, Item_Type
from Items.models import Collections, Item_Collection_Material, Item_Collection_Bonus
from Maps.models import Maps, Map_Item, Map_NPC,Map_Item_Spawn
from Jobs.models import Jobs
from Skills.models import Skills
from Attributes.models import Attributes
class Command(BaseCommand):
    
    
    def handle(self,  *args, **kwargs):
        Items.objects.all().delete()
        Monsters.objects.all().delete()
        Maps.objects.all().delete()
        Jobs.objects.all().delete()
        Skills.objects.all().delete()
        Attributes.objects.all().delete()

        