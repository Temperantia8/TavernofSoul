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
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
import logging
import json
from os.path import join, exists
from Items.models import Items
from Monsters.models import Monsters, Item_Monster, Skill_Monster

class Command(BaseCommand):
    item_path = join(settings.JSON_ROOT, 'items_by_name.json')
    monster_path = join(settings.JSON_ROOT, 'monster.json')
    item_monster_path = join(settings.JSON_ROOT, 'item_monster.json')
    npc_path = join(settings.JSON_ROOT, 'npc.json')

    
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
        parser.add_argument('-m', '--monsters', type=int, help='update monster')
        parser.add_argument('-im', '--item_monsters', type=int, help='update item_monsters')
        parser.add_argument('-npc', '--npc', type=int, help='update item_monsters')
        parser.add_argument('-ms', '--monskill', type=int, help='update monskill')
        parser.add_argument('-all', '--all_item', type=bool, help='update all item')
       
    
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

        monster = self.importJSON(self.monster_path)
        item_monster = self.importJSON(self.item_monster_path)
        npc = self.importJSON(self.npc_path)
        skillmon = self.importJSON(join(settings.JSON_ROOT, 'skill_mon.json'))
        if kwargs['all_item']:
            self.importMonster(monster, update)
            self.importItemMonster(item_monster,update)
            self.importNPC(npc, update)
            return 
        if kwargs['monsters']:
            self.importMonster(monster, update)
        if (kwargs['item_monsters']):
            self.importItemMonster(item_monster,update)
        if (kwargs['npc']):
            self.importNPC(npc, update)
        if (kwargs['monskill']):
            self.importSkillMon(skillmon, update)
    
    
    def importMonster(self,monster, update ):
        logging.debug("migrating monsters")
        count = 0
        count_all = len(monster.values())
        
        for i in monster.values() :
            flag_u = False
            try :
                old_hand = Monsters.objects.get(ids= i['$ID']) 
                handler = Monsters.objects.get(ids= i['$ID'])
                flag_u = True
                if update == 0:
                    logging.info("skipping ({}/{})  {}".format(count,count_all,i['Name']))
                    
                else:
                    logging.info("updating ({}/{})  {}".format(count,count_all,i['Name']))
            except:
                handler = Monsters()
                logging.info("inserting ({}/{})  {}".format(count,count_all,i['Name']))
            
            if flag_u and update == 0:
                count+=1
                continue
            
            handler.ids             = i['$ID']
            handler.id_name         = i['$ID_NAME']            
            handler.armor           = i['Armor']
            handler.descriptions    = i['Description']
            handler.element         = i['Element']
            handler.exp             = i['EXP']
            handler.exp_class       = i['EXPClass']
            handler.icon            = i['Icon']
            handler.level           = i['Level']
            handler.name            = i['Name']
            handler.race            = i['Race']
            handler.rank            = i['Rank']
            handler.size            = i['Size']
            handler.accuracy        = i['Stat_Accuracy']
            handler.matk_max        = i['Stat_ATTACK_MAGICAL_MAX']
            handler.matk_min        = i['Stat_ATTACK_MAGICAL_MIN']
            handler.patk_max        = i['Stat_ATTACK_PHYSICAL_MIN']
            handler.patk_min        = i['Stat_ATTACK_PHYSICAL_MAX']
            handler.blockpen        = i['Stat_BlockPenetration']
            handler.block           = i['Stat_BlockRate']
            handler.critdmg         = i['Stat_CriticalDamage']
            handler.critdef         = i['Stat_CriticalDefense']
            handler.critrate        = i['Stat_CriticalRate']
            handler.mdef            = i['Stat_DEFENSE_MAGICAL']
            handler.pdef            = i['Stat_DEFENSE_PHYSICAL']
            handler.eva             = i['Stat_Evasion']
            handler.hp              = i['Stat_HP']
            handler.stat_dex        = i['Stat_DEX']
            handler.stat_int        = i['Stat_INT']
            handler.stat_spr        = i['Stat_SPR']
            handler.stat_str        = i['Stat_STR']
            handler.stat_con        = i['Stat_CON']

            if (flag_u == True and old_hand.compare(handler)):
                count+=1
                continue
            handler.save()
            count+=1
        
    def importItemMonster(self,item_monster, update ):
        logging.debug("migrating monsters")
        count = 0
        count_all = len(item_monster)
        
        # Item_Monster.objects.all().delete()
        for i in item_monster :
            try:
                mon = Monsters.objects.get(ids = i['Monster'])
                item = Items.objects.get(ids = i['Item'])
            except:
                logging.warning('monster {} or item {} not found'.format(i['Monster'], i['Item']))
            flag_u = False
            try :
                old_hand = Item_Monster.objects.get(monster= mon, item = item) 
                handler = Item_Monster.objects.get(monster= mon, item = item)
                flag_u = True
                if update == 0:
                    logging.info("skipping ({}/{})  ".format(count,count_all))
                    
                else:
                    logging.info("updating ({}/{})  ".format(count,count_all))
            except:
                handler = Item_Monster()
                logging.info("inserting ({}/{})  ".format(count,count_all))
            
            if flag_u and update == 0:
                count+=1
                continue
            try:
                handler.monster             = Monsters.objects.get(ids = i['Monster'])
                handler.item                = Items.objects.get(ids = i['Item'])
                handler.chance              = i['Chance']
                handler.qty_min             = i['Quantity_MIN']
                handler.qty_max             = i['Quantity_MAX']
                if not (flag_u == True and old_hand.compare(handler)):
                    handler.save()
                
                count = count+1
            except:
                logging.warn("item = {}".format(i['Monster']))
    

    def importNPC (self,npc, update ):
        logging.debug("migrating monsters")
        count = 0
        count_all = len(npc.values())
        
        for i in npc.values() :
            flag_u = False
            try :
                old_hand = Monsters.objects.get(ids= i['$ID']) 
                handler = Monsters.objects.get(ids= i['$ID'])
                flag_u = True
                if update == 0:
                    logging.info("skipping ({}/{})  {}".format(count,count_all,i['Name']))
                    
                else:
                    logging.info("updating ({}/{})  {}".format(count,count_all,i['Name']))
            except:
                handler = Monsters()
                logging.info("inserting ({}/{})  {}".format(count,count_all,i['Name']))
            
            if flag_u and update == 0:
                count+=1
                continue
            
            handler.ids             = i['$ID']
            handler.id_name         = i['$ID_NAME']            
            handler.descriptions    = i['Description']
            handler.icon            = i['Icon']
            handler.name            = i['Name']
            if (flag_u == True and old_hand.compare(handler)):
                count+=1
                continue
            handler.save()
            count+=1

    def importSkillMon(self, skillmon, update):
        logging.debug("migrating monsters")
        count = 0
        count_all = len(skillmon.values())
        
        for i in skillmon.values() :
            flag_u = False
            link_mon = []
            
            try :
                old_hand = Skill_Monster.objects.get(ids= i['$ID']) 
                handler = Skill_Monster.objects.get(ids= i['$ID'])
                flag_u = True
                if update == 0:
                    logging.info("skipping ({}/{})  {}".format(count,count_all,i['Name']))
                    
                else:
                    logging.info("updating ({}/{})  {}".format(count,count_all,i['Name']))
            except:
                handler = Skill_Monster()
                logging.info("inserting ({}/{})  {}".format(count,count_all,i['Name']))
            
            if flag_u and update == 0:
                count+=1
                continue
            
            handler.ids             = i['$ID']
            handler.id_name         = i['$ID_NAME']            
            handler.name            = i['Name']
            try:
                handler.sfr             = int(i['SFR'])
            except:
                handler.sfr             = 0
            handler.element         = i['Attribute']
            handler.hit_count         = i['HitCount']
            handler.aar         = i['AAR']
            handler.cooldown        = int(i['CD'])
            if (flag_u == True and old_hand.compare(handler)):
                count+=1
                continue
            try:
                handler.save()
            except:
                logging.warn("something is wrong ids {}".format(i['$ID']))
                continue

            for monster in i['Monster']:
                try:
                    link_mon.append(Monsters.objects.get(ids = monster))
                except:
                    logging.warning("monster(ids) {} not found (for skill)".format(monster))
            for mon in link_mon:
                handler.monsters.add(mon)
            handler.save()
            count+=1