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
from Monsters.models import Monsters, Item_Monster
import os
import shutil
from Items.models import Items
from Maps.models import Maps
from Jobs.models import Jobs
from Skills.models import Skills
from Attributes.models import Attributes
from django.conf import settings

class Command(BaseCommand):
    
    
    def handle(self,  *args, **kwargs):
        Item_Monster.objects.all().delete()
        try:
            os.remove(os.path.join(settings.JSON_ROOT, 'prev', 'item_monster.json'))
        except:
            pass
        # Items.objects.all().delete()
        # Monsters.objects.all().delete()
        # Maps.objects.all().delete()
        # Jobs.objects.all().delete()
        # Skills.objects.all().delete()
        # Attributes.objects.all().delete()

        