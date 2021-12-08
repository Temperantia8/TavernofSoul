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

from Items.models import Items, Equipments, Equipment_Bonus, Cards, Recipes, Books
from Items.models import Item_Recipe_Material, Item_Recipe_Target, Item_Type
from Items.models import Collections, Item_Collection_Material, Item_Collection_Bonus
from Maps.models import Maps, Map_Item, Map_NPC,Map_Item_Spawn
from Jobs.models import Jobs
from Skills.models import Skills, Stance
from Attributes.models import Attributes
class Command(BaseCommand):
    item_path = join(settings.JSON_ROOT, 'items_by_name.json')
    monster_path = join(settings.JSON_ROOT, 'monster.json')
    item_monster_path = join(settings.JSON_ROOT, 'item_monster.json')
    npc_path = join(settings.JSON_ROOT, 'npc.json')
    item_path = join(settings.JSON_ROOT, 'items_by_name.json')
    item_type_path = join(settings.JSON_ROOT, 'item_type.json')
    base_path               = settings.JSON_ROOT
    maps_path               = join(base_path, 'maps.json')
    maps_by_name_path       = join(base_path, 'maps_by_name.json')
    maps_by_position_path   = join(base_path, 'maps_by_position.json')
    map_item_path           = join(base_path, 'map_item_path.json')
    map_npc_path            = join(base_path, 'map_npc_path.json')
    map_item_spawn_path     = join(base_path, 'map_item_spawn_path.json')
    jobs_path               = join(base_path, "job.json")
    jobs_by_name_path       = join(base_path, "job_by_name.json")
    attributes_by_name_path = join (base_path, "attributes_by_name.json")
    attributes_path         = join (base_path, "attributes.json")
    skills_path             = join(base_path, "skills.json")
    skills_by_name_path     = join(base_path, "skills_by_name.json")
    
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
        logging.basicConfig(level=logging.WARNING)
        update = kwargs['update']
        if update == None:
            update = 1

        monster = self.importJSON(self.monster_path)
        item_monster = self.importJSON(self.item_monster_path)
        npc = self.importJSON(self.npc_path)
        items = self.importJSON(self.item_path)
        item_type = self.importJSON(self.item_type_path)
    
        jobs           = self.importJSON(self.jobs_path)
        attrib         = self.importJSON(self.attributes_path)
        skills         = self.importJSON(self.skills_path)
        
        #get old dir loc
        #to do compare item from old dir, delete same rows
        
        self.importItem(items, update)
        self.importEq(items,item_type, update)
        self.importCard(items, item_type, update)
        self.importRecipe(items, item_type, update)
        self.importCollection(items, item_type, update)
        self.importBook(items, item_type, update)
        self.importMonster(monster, npc, update)

        map = self.importJSON(self.maps_path)
        self.importMap(map, update)
        map = self.importJSON(self.map_item_path)
        self.importMapItem(map, update)
        map = self.importJSON(self.map_npc_path)
        self.importMapNPC(map, update)
        map = self.importJSON(self.map_item_spawn_path)
        self.importMapItemSpawn(map, update)
        self.importJobs(jobs, update)
        self.importSkills(skills, update)
        self.importAttrib(attrib, update)
        skillmon = self.importJSON(join(settings.JSON_ROOT, 'skill_mon.json'))
        self.importSkillMon(skillmon, update)
        #to do copy all item to old dir
        #make note about old dir loc
    
    
    def deleteMe(self, all_item, json_item, table, name):
        item_to_delete = []
        for item in all_item:
            if item[0] not in json_item:
                item_to_delete.append(item[0])
        
        for ids in item_to_delete:
            try:
                logging.warn("deleting from {} where ids ={}".format(name, ids))
                item = table.objects.get(ids = ids)
                icon= item.icon
                item.delete()
            except:
                logging.warn(" delete error ids {}".format(ids))

            
    
    def importItem(self,items, update ):
        logging.debug("migrating items")
        count = 0
        count_all = len(items.values())
        
        item_type_db = list(Item_Type.objects.all())    
        i = []
        all_item_ids = Items.objects.values_list('ids')
        
        json_item_ids = []
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
            json_item_ids.append(i['$ID'])
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
        json_item_ids.append('00000000')
        json_item_ids.append('00000001')
        self.deleteMe(all_item_ids, json_item_ids, Items, "Items")
        
        
                
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
            
    def importMonster(self,monster, npc, update ):
        logging.debug("migrating monsters")
        count = 0
        count_all = len(monster.values())
        table = Monsters
        all_item = table.objects.values_list('ids')
        json_item = []
        for i in monster.values() :
            flag_u = False
            try :
                handler = Monsters.objects.get(ids= i['$ID'])
                flag_u = True
                if update == 0:
                    logging.info("skipping ({}/{})  {}".format(count,count_all,i['Name']))
                    
                else:
                    logging.info("updating ({}/{})  {}".format(count,count_all,i['Name']))
            except:
                handler = Monsters()
                logging.info("inserting ({}/{})  {}".format(count,count_all,i['Name']))
            
            json_item.append(str(i['$ID']))
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
            handler.save()
            count+=1
            
        logging.debug("migrating npc")
        count = 0
        count_all = len(npc.values())
        for i in npc.values() :
            flag_u = False
            try :
                handler = Monsters.objects.get(ids= i['$ID'])
                flag_u = True
                if update == 0:
                    logging.info("skipping ({}/{})  {}".format(count,count_all,i['Name']))
                    
                else:
                    logging.info("updating ({}/{})  {}".format(count,count_all,i['Name']))
            except:
                handler = Monsters()
                logging.info("inserting ({}/{})  {}".format(count,count_all,i['Name']))
            
            json_item.append(str(i['$ID']))
            if flag_u and update == 0:
                count+=1
                continue
            
            handler.ids             = i['$ID']
            handler.id_name         = i['$ID_NAME']            
            handler.descriptions    = i['Description']
            handler.icon            = i['Icon']
            handler.name            = i['Name']
            handler.save()
            count+=1
        self.deleteMe( all_item, json_item, Monsters, "Monsters")
        
        
    def importItemMonster(self,item_monster, update ):
        logging.debug("migrating monsters")
        count = 0
        count_all = len(item_monster)

        Item_Monster.objects.all().delete()
        for i in item_monster :
            flag_u = False
            
            handler = Item_Monster()
            logging.info("inserting ({}/{})  {}".format(count,count_all,i['Monster']))
            
            if flag_u and update == 0:
                count+=1
                continue
            try:
                handler.monster             = Monsters.objects.get(ids = i['Monster'])
                handler.item                = Items.objects.get(ids = i['Item'])
                handler.chance              = i['Chance']
                handler.qty_min             = i['Quantity_MIN']
                handler.qty_max             = i['Quantity_MAX']
                handler.save()
                count = count+1
            except:
                logging.warn("item = {}".format(i['Monster']))
    
            
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
    
    def importJobs(self,jobs, update ):
        logging.debug("migrating monsters")
        count = 0
        count_all = len(jobs.values())
        table = Jobs
        all_item = table.objects.values_list('ids')
        json_item = []
        for i in jobs.values() :
            flag_u = False
            try :
                handler = Jobs.objects.get(ids= i['$ID'])
                flag_u = True
                if update == 0:
                    logging.info("skipping ({}/{})  {}".format(count,count_all,i['Name']))
                    
                else:
                    logging.info("updating ({}/{})  {}".format(count,count_all,i['Name']))
            except:
                handler = Jobs()
                logging.info("inserting ({}/{})  {}".format(count,count_all,i['Name']))
            
            if flag_u and update == 0:
                count+=1
                continue
            json_item.append(str(i['$ID']))
            handler.ids             = i['$ID']
            handler.id_name         = i['$ID_NAME']            
            handler.name            = i['Name']
            handler.is_starter      = i['IsStarter']
            handler.job_tree        = i['JobTree']
            handler.icon            = i['Icon']
            handler.descriptions    = i['Description']
            handler.save()
            count+=1
        self.deleteMe(all_item, json_item, table, 'Jobs')
        
        
    def importSkills(self,skills, update ):
        logging.debug("migrating monsters")
        count = 0
        count_all = len(skills)
        stances_db = list(Skills.objects.all())
        stances  = {}
        table = Skills
        all_item = table.objects.values_list('ids')
        json_item = []
        for s in stances_db:
            stances[s.name] = s
        for i in skills.values() :
            flag_u = False
            try :
                handler = Skills.objects.get(ids= i['$ID'])
                flag_u = True
                if update == 0:
                    logging.info("skipping ({}/{})  {}".format(count,count_all,i['Name']))
                    
                else:
                    logging.info("updating ({}/{})  {}".format(count,count_all,i['Name']))
            except:
                handler = Skills()
                logging.info("inserting ({}/{})  {}".format(count,count_all,i['Name']))
            
            if flag_u and update == 0:
                count+=1
                continue
            if i['Link_Job'] == None:
                continue
            json_item.append(str(i['$ID']))
            handler.ids             = i['$ID']
            handler.id_name         = i['$ID_NAME']            
            handler.name            = i['Name']
            handler.icon            = i['Icon']
            handler.descriptions    = i['Description']
            if 'BasicCoolDown' in i:
                handler.cooldown        = i['BasicCoolDown']
            else:
                handler.cooldown        = 0
            handler.sp              = i['BasicSP']
            
            handler.effect          = i['Effect']
            handler.element         = i['Element']
            handler.max_lv          = i['MaxLevel']
            handler.unlock          = i['UnlockClassLevel']
            handler.overheat        = i['OverHeat']
            
            if 'sfr' in i:
                handler.sfr             = i['sfr']
            if 'CaptionRatio' in i:
                try:
                    for h in i['CaptionRatio']:
                        h = int(h)
                except:
                    i['CaptionRatio'] = None
                handler.captionratio1   = i['CaptionRatio']
            if 'CaptionRatio2' in i:
                try:
                    for h in i['CaptionRatio2']:
                        h = int(h)
                except:
                    i['CaptionRatio2'] = None
                handler.captionratio2   = i['CaptionRatio2']
            if 'CaptionRatio3' in i:
                try:
                    for h in i['CaptionRatio3']:
                        h = int(h)
                except:
                    i['CaptionRatio3'] = None
                handler.captionratio3   = i['CaptionRatio3']
            if 'CaptionTime' in i:
                try:
                    for h in i['CaptionTime']:
                        h = int(h)
                except:
                    i['CaptionTime'] = None
                handler.captiontime     = i['CaptionTime']
            if 'SkillSR' in i:
                try:
                    for h in i['SkillSR']:
                        h = int(h)
                except:
                    i['SkillSR'] = None
                handler.skillsr     = i['SkillSR'] 
            if 'SpendItemCount' in i:
                try:
                    for h in i['SpendItemCount']:
                        h = int(h)
                except:
                    i['SpendItemCount'] = None
                handler.spenditemcount  = i['SpendItemCount'] 
            if 'SpendPoison' in i:
                try:
                    for h in i['SpendPoison']:
                        h = int(h)
                except:
                    i['SpendPoison'] = None
                handler.spendpoison     = i['SpendPoison'] 
            if 'SpendSP' in i:
                try:
                    for h in i['SpendSP']:
                        h = int(h)
                except:
                    i['SpendSP'] = None
                handler.spendsp     = i['SpendSP'] 
            handler.save()
            for h in i['RequiredStance']:
                if h['Name'] not in stances:
                    stance = Stance()
                    stance.icon = h['Icon']
                    stance.name = h['Name']
                    stance.save()
                    stances[stance.name] = stance
                else:
                    stance = stances[h['Name']]
                handler.stance.add(stance)
            handler.job = Jobs.objects.get(ids = i['Link_Job'])
            handler.save()
            count+=1
        self.deleteMe(all_item, json_item, table, 'Skills')

    def importAttrib (self,attrib, update ):
        logging.debug("migrating monsters")
        count = 0
        count_all = len(attrib.values())
        table = Attributes
        all_item = table.objects.values_list('ids')
        json_item = []
        for i in attrib.values() :
            flag_u = False
            try :
                handler = Attributes.objects.get(ids= i['$ID'])
                flag_u = True
                if update == 0:
                    logging.info("skipping ({}/{})  {}".format(count,count_all,i['Name']))
                    
                else:
                    logging.info("updating ({}/{})  {}".format(count,count_all,i['Name']))
            except:
                handler = Attributes()
                logging.info("inserting ({}/{})  {}".format(count,count_all,i['Name']))
            
            if flag_u and update == 0:
                count+=1
                continue
            if (i['LevelMax'] == -1):
                continue
            json_item.append(str(i['$ID']))
            handler.ids             = i['$ID']
            handler.id_name         = i['$ID_NAME']            
            handler.descriptions    = i['Description']
            handler.icon            = i['Icon']
            handler.name            = i['Name']
            handler.descriptions_required = i['DescriptionRequired']
            handler.is_toggleable   = i['IsToggleable']
            handler.max_lv          = i['LevelMax']
            handler.save()
            added_skill = []
            for h in i['Link_Skills']:
                try:
                    skill = Skills.objects.get(id_name = h)
                    handler.skill.add(skill)
                    added_skill.append(skill.ids)
                except:
                    logging.warning("skill not found {}".format(h))
            for skill in handler.skill.all():
                if skill.ids not in added_skill:
                    handler.skill.remove(skill)
            added_jobs = []
            for h in i['Link_Jobs']:
                try:
                    job = Jobs.objects.get(ids = h)
                    handler.job.add(job)
                    added_jobs.append(job.ids)
                except:
                    logging.warning("skill not found {}".format(h))
            for job in handler.job.all():
                if job.ids not in added_jobs:
                    handler.job.remove(job)
            handler.save()
            count+=1
        
        #print(all_item) print(json_item)
        self.deleteMe(all_item, json_item, table, 'Attributes')
            
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