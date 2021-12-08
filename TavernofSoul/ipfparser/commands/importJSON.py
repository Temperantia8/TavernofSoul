# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 14:08:20 2021

@author: Temperantia
"""

"""
#run this first if from spyder (dev purpose)

import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TavernofSoul.settings")
django.setup()

"""

from django.core.management.base import BaseCommand
from django.conf import settings
import logging
import json
from os.path import join, exists
from Items.models import Items
import asyncio

class Command(BaseCommand):
    item_path = join(settings.JSON_ROOT, 'items_by_name.json')
    
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
    
def escaper(string):
    string = str(string)
    escaped = string.translate(str.maketrans({"-":  r"\-",
                                          "]":  r"\]",
                                          "\\": r"\\",
                                          "^":  r"\^",
                                          "$":  r"\$",
                                          "*":  r"\*",
                                          ".":  r"\.",
                                          "'" : r"\'",
                                          '"' : r'\"'
                                          
                                          }))
    return escaped
    def handle(self, **options):
        log = logging.getLogger("migrator")
        log.setLevel("INFO")
        
        log.isEnabledFor(20)
        items = self.importJSON(self.item_path)
        
        """
        ===========================================================
        """
        log.info("migrating items")
        for i in items.values() :
            
            try :
                handler = Items.get(id_name= i['$ID_NAME'])
                log.info("updating {}".format(i['Name']))
            except:
                handler = Items()
                log.info("inserting {}".format(i['Name']))
            handler                 = Items()
            handler.ids             = i['$ID']
            handler.id_name 	    = i['$ID_NAME']
            handler.cooldown	    = i['TimeCoolDown']
            handler.descriptions    = i['Description']
            handler.name	        = i['Name']
            handler.weight 	    	= i['Weight']
            handler.tradability		= i['Tradability']
            handler.type 			= i['Type']
            handler.grade 			= i['Grade']
            handler.icon            = i['Icon']
            handler.save()
        
