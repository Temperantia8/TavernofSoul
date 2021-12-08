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
from Monsters.models import Monsters
from Maps.models import Maps, Map_Item, Map_NPC,Map_Item_Spawn

class Command(BaseCommand):
    base_path               = settings.JSON_ROOT
    maps_path               = join(base_path, 'maps.json')
    maps_by_name_path       = join(base_path, 'maps_by_name.json')
    maps_by_position_path   = join(base_path, 'maps_by_position.json')
    map_item_path           = join(base_path, 'map_item_path.json')
    map_npc_path            = join(base_path, 'map_npc_path.json')
    map_item_spawn_path     = join(base_path, 'map_item_spawn_path.json')
    
    
    def importJSON(self,file):
        if not exists(file):
            return {}
        try:
            with open(file, "r") as f:
                data = json.load(f)
        except:
            logging.error("error in importing file {}".format(file))
            return {}
        return data
    

    def add_arguments(self, parser):
        parser.add_argument('-u', '--update', type=int, help='Indicate wether ignore any \
                            existing data or update them')
        parser.add_argument('-all', '--all_item', type=int, help='all')
        parser.add_argument('-mm', '--mapMonster', type=int, help='mapMonster')
        parser.add_argument('-m', '--maps', type=int, help='maps')
        parser.add_argument('-is', '--itemSpawn', type=int, help='itemSpawn')
       
    
    def escaper(self,string):
        string = str(string)
        escaped = string.translate(str.maketrans({"-":  r"\-",
                                              "]":  r"\]",
                                              "\\": r"\\",
                                              "^":  r"\^",
                                              "$":  r"\$",
                                              "*":  r"\*",
                                              ".":  r"\.",
                                              "'" : r"\'",
                                              '"' : r'\"',
                                              ',' :r''
                                              
                                              }))
        return escaped
        
    def handle(self,  *args, **kwargs):
        logging.basicConfig(level=logging.DEBUG)
        update = kwargs['update']
        if update == None:
            update = 1
        if kwargs['all_item']:
            map = self.importJSON(self.maps_path)
            self.importMap(map, update)
            map = self.importJSON(self.map_item_path)
            self.importMapItem(map, update)
            map = self.importJSON(self.map_npc_path)
            self.importMapNPC(map, update)
            map = self.importJSON(self.map_item_spawn_path)
            self.importMapItemSpawn(map, update)
        if kwargs['maps']:
            map = self.importJSON(self.maps_path)
            self.importMap(map, update)
            
        if kwargs['mapMonster']:
            map = self.importJSON(self.map_npc_path)
            self.importMapNPC(map, update)
        if kwargs['itemSpawn']:
            map = self.importJSON(self.map_item_spawn_path)
            self.importMapItemSpawn(map, update)
    
    def importMap (self,map, update ):
        logging.debug("migrating monsters")
        count = 0
        count_all = len(map.values())
        
        for i in map.values() :
            flag_u = False
            try :
                handler = Maps.objects.get(ids= i['$ID'])
                flag_u = True
                if update == 0:
                    logging.info("skipping ({}/{})  {}".format(count,count_all,i['Name']))
                    
                else:
                    logging.info("updating ({}/{})  {}".format(count,count_all,i['Name']))
            except:
                handler = Maps()
                logging.info("inserting ({}/{})  {}".format(count,count_all,i['Name']))
            
            if flag_u and update == 0:
                count+=1
                continue
            
            handler.ids            = i['$ID']
            handler.id_name        = i['$ID_NAME']            
            handler.icon           = (i['$ID_NAME'] + ".png").lower()
            handler.name           = i['Name']
            handler.has_cm         = i['HasChallengeMode']
            handler.has_warp       = i['HasWarp']
            handler.level          = i['Level']
            handler.max_elite      = i['Prop_EliteMonsterCapacity']
            handler.max_hate       = i['Prop_MaxHateCount']
            handler.star           = i['Stars']
            handler.type           = i['Type']
            handler.map_link       = i['Link_Maps']
            handler.save()
            count+=1
    
    def importMapItem (self,map, update ):
        logging.debug("migrating map item drop")
        count = 0
        count_all = len(map)
        for i in map :
            flag_u = False
            
            try:
                m = Maps.objects.get(ids = i['Map'])
                it = Items.objects.get(ids = i['Item'])
            except:
                logging.warning("map {} or item {} not found".format(i['Map'], i['Item']))
                continue
            try :
                handler = Map_Item.objects.get(map= m, item = it)
                flag_u = True
            except:
                handler = Map_Item()
                
            
            if flag_u and update == 0:
                count+=1
                continue
            
            
            handler.chance          = i['Chance']
            handler.item            = it
            handler.map             = m
            handler.qty_max         = i['Quantity_MAX']
            handler.qty_min         = i['Quantity_MIN']
            handler.save()
            count+=1 
    
    
    def importMapItemSpawn (self,map, update ):
        logging.debug("migrating map item spawn")
        count = 0
        count_all = len(map)
        Map_Item_Spawn.objects.all().delete()
        for i in map :
            flag_u = False
            
            try:
                m = Maps.objects.get(ids = i['Map'])
                it = Items.objects.get(ids = i['Item'])
            except:
                logging.warning("map {} or item {} not found".format(i['Map'], i['Item']))
                continue
            try :
                handler = Map_Item_Spawn.objects.get(map= m, item = it)
                flag_u = True
            except:
                handler = Map_Item_Spawn()
                
            
            if flag_u and update == 0:
                count+=1
                continue
            
            
            handler.population      = i['Population']
            handler.item            = it
            handler.map             = m
            handler.time_respawn    = i['TimeRespawn']
            pos = []
            for posit in i['Positions']:
                for po in posit:
                    pos.append(po)
            handler.positions        = pos
            handler.save()
            count+=1 
    
    
    def importMapNPC (self,map, update ):
        logging.debug("migrating map npc")
        count = 0
        count_all = len(map)
        Map_NPC.objects.all().delete()
        for i in map:
            flag_u = False
            try:
                m = Maps.objects.get(ids = i['Map'])
                it = Monsters.objects.get(ids = i['NPC'])
            except:
                logging.warning("map {} or NPC {} not found".format(i['Map'], i['NPC']))
                continue
            try :
                handler = Map_NPC.objects.get(map= m, item = it)
                flag_u = True
            except:
                handler = Map_NPC()
                
            
            if flag_u and update == 0:
                count+=1
                continue
            
            
            handler.population      = i['Population']
            handler.monster         = it
            handler.map             = m
            pos = []
            for posit in i['Positions']:
                for po in posit:
                    pos.append(po)
            handler.time_respawn    = i['TimeRespawn']
            handler.positions        = pos
            handler.save()
            count+=1 
    