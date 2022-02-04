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
from Jobs.models import Jobs
from Items.models import Items, Equipment_Bonus
from Skills.models import Skills
from django.conf import settings


def importJSON(file):
    if not exists(file):
        return {}
    try:
        with open(file, "r") as f:
            data = json.load(f)
    except:
        logging.error("error in importing file {}".format(file))
        return {}
    return data

class Command(BaseCommand):
    
    
    def handle(self,  *args, **kwargs):
        file = 'items_by_name.json'
        items = importJSON(file)
        
        if settings.REGION == 'jtos':
            vv_name = 'バイボラ秘伝'
        else:
            vv_name = "vaivora vision"
                
        
        all_job = Jobs.objects.all()
        for job in all_job:
            job.vaivora = None
            job.save()
        return
 
        if settings.REGION == 'jtos':
            return

        for i in  items:
            if vv_name in i['Name'].lower() and 'lv4' in  i['Name'].lower() :
                if ['job'] not in i:
                    continue
                job = Jobs.objects.get(ids = i['job'])
                job.vaivora = Items.objects.get(ids = i['$ID'])
                job.save() 
        
            



