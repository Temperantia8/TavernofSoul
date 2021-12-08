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
from Items.models import Items, Equipments, Equipment_Bonus, Cards, Recipes, Books
from Items.models import Item_Recipe_Material, Item_Recipe_Target, Item_Type
from Items.models import Collections, Item_Collection_Material, Item_Collection_Bonus
from Items.models import Equipment_Set


class Command(BaseCommand):
    item_path               = join(settings.JSON_ROOT, 'items_by_name.json')
    item_type_path          = join(settings.JSON_ROOT, 'item_type.json')
    base_path               = settings.JSON_ROOT
    maps_path               = join(base_path, 'maps.json')
    maps_by_name_path       = join(base_path, 'maps_by_name.json')
    maps_by_position_path   = join(base_path, 'maps_by_position.json')
    map_item_path           = join(base_path, 'map_item_path.json')
    map_npc_path            = join(base_path, 'map_npc_path.json')
    map_item_spawn_path     = join(base_path, 'map_item_spawn_path.json')
    eqSet                   = join(base_path, 'equipment_setss.json')
    
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
        parser.add_argument('-i', '--item', type=bool, help='update item')
        parser.add_argument('-eq', '--equipments', type=bool, help='update equipments')
        parser.add_argument('-ca', '--cards', type=bool, help='update cards')
        parser.add_argument('-r', '--recipes', type=bool, help='update recipes')
        parser.add_argument('-co', '--collections', type=bool, help='update collection')
        parser.add_argument('-all', '--all_item', type=bool, help='update all item')
        parser.add_argument('-b', '--books', type=bool, help='update books')
        parser.add_argument('-eqs', '--equipmentset', type=bool, help='update equipmentset')
    
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
        

        items = self.importJSON(self.item_path)
        item_type = self.importJSON(self.item_type_path)
        eqset = self.importJSON(self.eqSet)
        if kwargs['all_item']:
            self.importItem(items, update)
            self.importEq(items,item_type, update)
            self.importCard(items, item_type, update)
            self.importRecipe(items, item_type, update)
            self.importCollection(items, item_type, update)
            self.importBook(items, item_type, update)
            return 
        if kwargs['item']:
            self.importItem(items, update)
        if (kwargs['equipments']):
            self.importEq(items,item_type, update)
        if kwargs['cards']:
            self.importCard(items, item_type, update)
        if kwargs['recipes']:
            self.importRecipe(items, item_type, update)
        if kwargs['collections']:
            self.importCollection(items, item_type, update)
        if kwargs['books']:
            self.importBook(items, item_type, update)
        if kwargs['equipmentset']:
            self.importEqSet(eqset, update)
   
    
    
    def importItem(self,items, update ):
        logging.debug("migrating items")
        count = 0
        count_all = len(items.values())
        
        item_type_db = list(Item_Type.objects.all())    
        i = []
        for z in item_type_db:
            i.append(z.name)
        item_type_db = i
        
        for i in items.values() :
            flag_u = False
            try :
                handler = Items.objects.get(ids= i['$ID'])
                flag_u = True
                if update == 0:
                    logging.info("skipping ({}/{})  {}".format(count,count_all,i['Name']))
                    
                else:
                    logging.info("updating ({}/{})  {}".format(count,count_all,i['Name']))
            except:
                handler = Items()
                logging.info("inserting ({}/{})  {}".format(count,count_all,i['Name']))
            
            if flag_u and update == 0:
                count+=1
                continue
            

            handler.ids             = i['$ID']
            handler.id_name         = i['$ID_NAME']
            handler.cooldown        = i['TimeCoolDown']
            handler.descriptions    = i['Description']
            handler.name            = i['Name']
            handler.weight          = 0 if i['Weight'] == '' else i['Weight']
            handler.tradability     = i['Tradability']
            handler.type            = i['Type']
            if i['Type'] not in item_type_db:
                type_handler = Item_Type()
                type_handler.name = i['Type']
                type_handler.save()
                item_type_db.append(i['Type'])
            handler.grade           = i['Grade']
            handler.icon            = i['Icon']

            handler.save()
            count+=1
                
    def importEq(self, items,item_type, update):
        logging.debug("linking equipments")
        count = 0
        
        item_type_db = list(Item_Type.objects.all())    
        i = []
        for z in item_type_db:
            i.append(z.name)
        item_type_db = i
        
        eqs = []
        for i in items.values():
            if i['$ID_NAME'] in item_type['EQUIPMENT']:
                eqs.append(i)
        count_all = len(eqs)
        for i in eqs :
            flag_u = False
            try:
                item = Items.objects.get(id_name = i['$ID_NAME'])
                
            except:
                logging.warn("[EQ]item not found {}".format(i['$ID_NAME']))
                continue
            try :
                handler = Equipments.object.get(item = item)
                flag_u = True
                if update == 0:
                    logging.info("skipping ({}/{})  {}".format(count,count_all,i['Name']))
                    
                else:
                    logging.info("updating ({}/{})  {}".format(count,count_all,i['Name']))
                    
            except :
                handler = Equipments()
                handler.item = item
                logging.info("extending ({}/{})  {}".format(count,count_all,i['Name']))
                
                
            if flag_u and update == 0:
                count+=1
                continue
            if not ('AnvilATK' in i ):
                logging.warn("[EQ]item not extended {}".format(i['$ID_NAME']))
                continue
            handler.anvil_atk       = i['AnvilATK'] 
            handler.anvil_def       = i['AnvilDEF'] 
            handler.anvil_price     = i['AnvilPrice'] 
           
            
            handler.durability      = i['Durability']
            handler.level           = i['Level']
            handler.potential       = i['Potential']
            handler.requiredClass   = i['RequiredClass']
            handler.sockets_limit   = i['SocketsLimit']
            handler.stars           = i['Stars']
            handler.matk            = i['Stat_ATTACK_MAGICAL']            
            handler.patk            = i['Stat_ATTACK_PHYSICAL_MIN']
            handler.patk_max        = i['Stat_ATTACK_PHYSICAL_MAX']
            handler.mdef            = i['Stat_DEFENSE_MAGICAL']
            handler.pdef            = i['Stat_DEFENSE_PHYSICAL']
            handler.transcend_price = i['TranscendPrice']
            handler.type_attack     = i['TypeAttack']
            handler.type_equipment  = i['TypeEquipment']
            if i['TypeEquipment'] not in item_type_db:
                type_handler = Item_Type()
                type_handler.name = i['TypeEquipment']
                type_handler.is_equipment = True
                type_handler.save()
                item_type_db.append(i['TypeEquipment'])
            handler.unidentified    = i['Unidentified']
            handler.unidentifiedRandom = i['UnidentifiedRandom']
            handler.save()
            

            Equipment_Bonus.objects.filter(equipment = handler).delete()
            if (i['Bonus']):
                for b in i['Bonus']:
                    bonus = Equipment_Bonus(equipment = handler)
                    bonus.bonus_stat = b[0]
                    #try:
                    #    bonus.bonus_val  = b[1].replace('{img green_up_arrow 16 16}', '▲')\
                    #                            .replace('{img green_down_arrow 16 16}', '▼')
                    #except:
                    bonus.bonus_val  = b[1]
                    bonus.save()
            count+=1
    
    def importCard(self, items, item_type, update):
        logging.debug("linking cards")
        count = 0
        
        cards = []
        for i in items.values():
            if i['$ID_NAME'] in item_type['CARD']:
                cards.append(i)
        count_all = len(cards)
        for i in cards :
            flag_u = False
            try:
                item = Items.objects.get(id_name = i['$ID_NAME'])
                
            except:
                logging.warn("[EQ]item not found {}".format(i['$ID_NAME']))
                continue
            try :
                handler = Cards.object.get(item = item)
                flag_u = True
                if update == 0:
                    logging.info("skipping ({}/{})  {}".format(count,count_all,i['Name']))
                    
                else:
                    logging.info("updating ({}/{})  {}".format(count,count_all,i['Name']))
                    
            except :
                handler = Cards()
                handler.icon = i['IconTooltip']
                handler.item = item
                logging.info("extending ({}/{})  {}".format(count,count_all,i['Name']))
                
                
            if flag_u and update == 0:
                count+=1
                continue
        
            handler.type_card = i['TypeCard']
            handler.save()
            count+=1
            
    def importRecipe(self, items, item_type, update):
        logging.debug("linking recipes")
        count = 0
        
        recipes = []
        for i in items.values():
            if i['$ID_NAME'] in item_type['RECIPES']:
                recipes.append(i)
        count_all = len(recipes)
        for i in recipes :
            flag_u = False
            try:
                item = Items.objects.get(id_name = i['$ID_NAME'])
                
            except:
                logging.warn("[EQ]item not found {}".format(i['$ID_NAME']))
                continue
            try :
                handler = Recipes.objects.get(item = item)
                flag_u = True
                if update == 0:
                    logging.info("skipping ({}/{})  {}".format(count,count_all,i['Name']))
                    
                else:
                    logging.info("updating ({}/{})  {}".format(count,count_all,i['Name']))
                    
            except :
                handler = Recipes()
                handler.item = item
                logging.info("extending ({}/{})  {}".format(count,count_all,i['Name']))
                
                
            if flag_u and update == 0:
                count+=1
                continue
            if not ('Link_Materials' in i):
                count+=1
                logging.warn("[RCP] {} ({}) didnt have materials".format(i['Name'], i['$ID_NAME']))
                continue
            
            handler.save()
            Item_Recipe_Material.objects.filter(recipe = handler).delete()
            for link in i['Link_Materials']:
                try:
                    mat             = Item_Recipe_Material(recipe = handler)
                    mat.material    = Items.objects.get(id_name = link['Item'])
                    mat.qty         = link['Quantity']
                    mat.save()
                except:
                    logging.warn("[RCP] {} ({}) material not found ({})".format(i['Name'], i['$ID_NAME'], link['Item']))
            
            Item_Recipe_Target.objects.filter(recipe = handler).delete()
            try:
                target = Item_Recipe_Target(recipe = handler)
                
                target.target = Items.objects.get(id_name = i['Link_Target'])
                target.save()
            except:
                count+=1
                logging.warn("[RCP] {} ({}) didnt have target".format(i['Name'], i['$ID_NAME']))
                continue
            
            count+=1
        
    def importCollection(self, items, item_type, update):
        logging.debug("linking recipes")
        count = 0
        
        collection = []
        for i in items.values():
            if i['$ID_NAME'] in item_type['COLLECTION']:
                collection.append(i)
        count_all = len(collection)
        for i in collection :
            flag_u = False
            try:
                item = Items.objects.get(id_name = i['$ID_NAME'])
                
            except:
                logging.warn("[EQ]item not found {}".format(i['$ID_NAME']))
                continue
            try :
                handler = Collections.objects.get(item = item)
                flag_u = True
                if update == 0:
                    logging.info("skipping ({}/{})  {}".format(count,count_all,i['Name']))
                    
                else:
                    logging.info("updating ({}/{})  {}".format(count,count_all,i['Name']))
                    
            except :
                handler = Collections()
                handler.item = item
                logging.info("extending ({}/{})  {}".format(count,count_all,i['Name']))
                
                
            if flag_u and update == 0:
                count+=1
                continue
            if not ('Link_Items' in i):
                count+=1
                logging.warn("[RCP] {} ({}) didnt have materials".format(i['Name'], i['$ID_NAME']))
                continue
            
            handler.save()
            Item_Collection_Material.objects.filter(collection = handler).delete()
            for link in i['Link_Items']:
                try:
                    mat             = Item_Collection_Material(collection = handler)
                    mat.material    = Items.objects.get(id_name = link)
                    mat.save()
                except:
                    logging.warn("[RCP] {} ({}) material not found ({})".format(i['Name'], i['$ID_NAME'], link))
            
            Item_Collection_Bonus.objects.filter(collection = handler).delete()
            try:
                if (i['Bonus']):
                    for b in i['Bonus']:
                        bonus = Item_Collection_Bonus(collection = handler)
                        bonus.bonus_stat = b[0]
                        bonus.bonus_val  = b[1]
                        bonus.save()
            except:
                count+=1
                logging.warn("[RCP] {} ({}) didnt have target".format(i['Name'], i['$ID_NAME']))
                continue
            
            count+=1
            
    def importBook(self, items,item_type, update):
        
        books = []
        for i in items.values():
            if i['$ID_NAME'] in item_type['BOOKS']:
                books.append(i)
        count_all = len(books)
        count = 1
        for i in books :
            flag_u = False
            try:
                item = Items.objects.get(id_name = i['$ID_NAME'])
                
            except:
                logging.warn("[Books]item not found {}".format(i['$ID_NAME']))
                continue
            try :
                handler = Equipments.object.get(item = item)
                flag_u = True
                if update == 0:
                    logging.info("skipping ({}/{})  {}".format(count,count_all,i['Name']))
                    
                else:
                    logging.info("updating ({}/{})  {}".format(count,count_all,i['Name']))
                    
            except :
                handler = Books()
                handler.item = item
                logging.info("extending ({}/{})  {}".format(count,count_all,i['Name']))
                
                
            if flag_u and update == 0:
                count+=1
                continue
            
            if 'Text' in i:
                handler.text = i['Text']
            else:
                handler.text = None
            handler.save()
            count+=1
    
    def importEqSet(self, eqSet, update):
        logging.debug("creating equipment sets")
        count = 0
        count_all = len(eqSet)
        for title in eqSet :
            i = eqSet[title]
            flag_u = False
            link_item = []
            for item in i['Link_Items']:
                try:
                    link_item.append(Items.objects.get(id_name = item).equipments)    
                except:
                    logging.warn("[EQ]item not found {}".format(i['$ID_NAME']))
                continue
            try :
                handler = Equipment_Set.object.get(ids = i['$ID'])
                flag_u = True
                if update == 0:
                    logging.info("skipping ({}/{})  {}".format(count,count_all,i['Name']))
                    
                else:
                    logging.info("updating ({}/{})  {}".format(count,count_all,i['Name']))
                    
            except :
                handler = Equipment_Set()
                logging.info("extending ({}/{})  {}".format(count,count_all,i['Name']))
                
                
            if flag_u and update == 0:
                count+=1
                continue
            #print(i)
            handler.ids             = i['$ID']
            handler.id_name         = i['$ID_NAME']
            handler.name            = i['Name']
            handler.bonus2          = i['Bonus2']
            handler.bonus3          = i['Bonus3']
            handler.bonus4          = i['Bonus4']
            handler.bonus5          = i['Bonus5']
            handler.bonus6          = i['Bonus6']
            handler.bonus7          = i['Bonus7']
            handler.save()

            for i in link_item:
                handler.equipment.add(i)
            handler.save()

            count+=1
