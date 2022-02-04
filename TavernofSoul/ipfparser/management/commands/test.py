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
from Items.models import Goddess_Reinforce_Mat, Goddess_Reinforce_Chance


class Command(BaseCommand):
    
    base_path               = settings.JSON_ROOT
    
    def importJSON(self, file):
        if not exists(file):
            return {}
        try:
            with open(file, "r") as f:
                data = json.load(f)
        except:
            logging.error("error in importing file {}".format(file))
            return {}
        return data


    
    def handle(self,  *args, **kwargs):
        Goddess_Reinforce_Mat.objects.all().delete()
        Goddess_Reinforce_Chance.objects.all().delete()
        self.importGoddess()


    def importGoddess(self):
        mat_path        = 'goddess_reinf_mat.json'
        reinf_path      = 'goddess_reinf.json' 
        item_dic        = {}
        mats            = self.importJSON(join(self.base_path, mat_path))
        #with open(reinf_path,'r')as f:
        #    mats = json.load(f)
        for lv in mats:
            for eq in mats[lv]:
                for anv in mats[lv][eq]:
                    for mat in mats[lv][eq][anv]:
                        if mat not in item_dic:
                            item =  Items.objects.get(id_name = mat)
                            item_dic[mat] = item 
                        item = item_dic[mat]
                        try:
                            handler = Goddess_Reinforce_Mat.objects.get(lv=lv, anvil=anv, mat = item, eq_type = eq)
                        except:
                            handler = Goddess_Reinforce_Mat(lv=lv, anvil=anv, mat = item, eq_type = eq)
                        handler.mat_count = mats[lv][eq][anv][mat]
                        handler.save() 
                    
        reinf       = self.importJSON(join(self.base_path,reinf_path))
        for lv in reinf:
            for anvil in reinf[lv]:
                cur = reinf[lv][int(anvil['ClassID'])-1]
                
                try:
                    handler = Goddess_Reinforce_Chance.objects.get(lv=lv, anvil=int(anvil['ClassID']))
                except:
                    handler = Goddess_Reinforce_Chance(lv=lv, anvil=int(anvil['ClassID']))
                if 'AddAtk' in cur:
                    handler.addatk = cur['AddAtk']
                if 'AddAccAtk' in cur:
                    handler.addacc = cur['AddAccAtk']
                
                handler.chance = int(cur['BasicProp']) / 100000
                handler.save()