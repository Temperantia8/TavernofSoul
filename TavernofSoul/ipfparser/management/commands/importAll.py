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
from Buffs.models import Buffs
from Skills.models import Skills
from Attributes.models import Attributes
from Dashboard.models import Version
from Other.models import Achievements
class Command(BaseCommand):
    
    base_path               = settings.JSON_ROOT
    maps_path               = 'maps.json'
    maps_by_name_path       = 'maps_by_name.json'
    maps_by_position_path   = 'maps_by_position.json'
    map_item_path           = 'map_item_path.json'
    map_npc_path            = 'map_npc_path.json'
    map_item_spawn_path     = 'map_item_spawn_path.json'
    jobs_path               = "job.json"
    jobs_by_name_path       = "job_by_name.json"
    attributes_by_name_path = "attributes_by_name.json"
    attributes_path         = "attributes.json"
    skills_path             = "skills.json"
    skills_by_name_path     = "skills_by_name.json"
    item_path               = 'items_by_name.json'
    monster_path            = 'monster.json'
    item_monster_path       = 'item_monster.json'
    npc_path                = 'npc.json'
    item_path               = 'items_by_name.json'
    item_type_path          = 'item_type.json'
    version_path            = 'version.json'
    buff_path               = 'buff.json'
    achieve_path            = 'achievements.json'
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


    def comparer(self,path, ids = ['$ID']):
        base_path = self.base_path
        json_prev = False
        json_now = False
        changes = {'added' : [] ,'removed' : [], 'changed': []}
        if (exists(join(base_path, 'prev', path))):
            with open(join(base_path, 'prev', path)) as f:
                json_prev = json.load(f)
        if (exists(join(base_path, path))):
            with open(join(base_path, path)) as f:
                json_now = json.load(f)
                
        if json_prev == False and json_now:
            pass
            if type(json_now) == type({}):
                changes['added'] = list(json_now.values())
            else:
                changes['added'] = json_now
                
            logging.warning("Change at {} : {} added, {} deleted, {} modified row".format(
                path, len(changes['added']), len(changes['removed']), len(changes['changed'])))
            return changes
            
        elif json_now == json_prev == False:
            logging.warning("file not found {}".format(path))
            return changes
        if (json_now == json_prev):
            logging.warning("no change at {}".format(path))
            
            return changes
        
        
        if type(json_now) == type({}):
            json_now= list(json_now.values())
            json_prev= list(json_prev.values())

        
        dict_now = {}
        for i in json_now:
            if (len(ids)) == 1:
                dict_now[i[ids[0]]] = i
            else:
                if i[ids[0]] not in dict_now:    
                    dict_now[i[ids[0]]] = {i[ids[1]]:  i}
                else :
                    dict_now[i[ids[0]]][i[ids[1]]] = i
        
        dict_prev= {}
        for i in json_prev:
            if (len(ids)) == 1:
                dict_prev[i[ids[0]]] = i
            else:
                if i[ids[0]] not in dict_prev:    
                    dict_prev[i[ids[0]]] = {i[ids[1]]:  i}
                else :
                    dict_prev[i[ids[0]]][i[ids[1]]] = i
                
        if len(ids) == 1:
            for item  in dict_now:
                if item not in dict_prev:
                    changes['added'].append(dict_now[item])
                else:
                    if (dict_now[item] != dict_prev[item]):
                        changes['changed'].append(dict_now[item])
            
            for item in dict_prev:
                if item not in dict_now:
                    changes['removed'].append(dict_prev[item])
        
        else:
            for item in dict_now:
                for atom in dict_now[item]:
                    if item not in dict_prev:
                        changes['added'].append(dict_now[item][atom])
                    elif atom not in dict_prev[item]:
                        changes['added'].append(dict_now[item][atom])
                    else:
                        if (dict_now[item][atom] != dict_prev[item][atom]):
                            changes['changed'].append(dict_now[item][atom])
            for item in dict_prev:
                for atom in dict_prev[item]:
                    if item in dict_now and atom not in dict_now[item]:
                        changes['removed'].append(dict_prev[item][atom])
                    

                
        logging.warning("Change at {} : {} added, {} deleted, {} modified row".format(
            path, len(changes['added']), len(changes['removed']), len(changes['changed'])))
        return changes
        


    def handle(self,  *args, **kwargs):
        logging.basicConfig(level=logging.WARNING)
        update = kwargs['update']
        if update == None:
            update = 1

        ver_json = self.importJSON(join(self.base_path, self.version_path))
        try:
            ver = Version.object.latest('created')
        except:
            ver = Version()
            ver.Version = '000000.ipf'
            ver.save()
        if ver.Version != ver_json['version']:
            ver.version = ver_json['version']
            ver.save()
        
        item_type       = self.importJSON(join(self.base_path,self.item_type_path))
        #get old dir loc
        #to do compare item from old dir, delete same rows
        items           = self.comparer(self.item_path)
        self.importItem(items,item_type, update)
        
        npc             = self.comparer(self.npc_path)
        monster         = self.comparer(self.monster_path)
        self.importMonster(monster, npc, update)
        
        item_monster    = self.comparer(self.item_monster_path, ['Item','Monster'])
        self.importItemMonster(item_monster,update)
        
        map = self.comparer(self.maps_path)
        self.importMap(map, update)
        
        map = self.comparer(self.map_item_path, ['Map', 'Item'])
        self.importMapItem(map, update)
        
        map = self.comparer(self.map_npc_path, ['Map', 'NPC'])
        self.importMapNPC(map, update)
        
        map = self.comparer(self.map_item_spawn_path, ['Map', 'Item'] )
        self.importMapItemSpawn(map, update)
        
        jobs           = self.comparer(self.jobs_path)
        self.importJobs(jobs, update)
        
        skills         = self.importJSON(join(self.base_path,self.skills_path))
        self.importSkills(skills, update)
        
        attrib         = self.comparer(self.attributes_path)
        self.importAttrib(attrib, update)
        
        skillmon = self.comparer('skill_mon.json')
        self.importSkillMon(skillmon, update)
        #to do copy all item to old dir
        #make note about old dir loc
        buff = self.comparer(self.buff_path)
        self.importBuff(buff, update)

        achieve = self.comparer(self.achieve_path)
        self.importAchieve(achieve,update)
        
        source = os.listdir(self.base_path)
        destination = join(self.base_path,"prev")
        for files in source:
            if files.endswith(".json"):
                shutil.copy(join(self.base_path,files),join(destination,files))

            
    
    def importItem(self,items, item_type, update ):
        for i in items['removed']:
            try:
                Items.objects.get(ids= i['$ID']).delete()
            except:
                logging.warning("failed to delete item {} ({})".format(i['Name'], i['$ID']))
        logging.debug("migrating items")
        item_type_db = list(Item_Type.objects.all())  
        dolater = {'RECIPES': [],'COLLECTION': [], 'EQUIPMENT' : [], 'CARD' : [], 'BOOKS' :[] }
        for i in items['added']:
            upd = False
            try:
                handler = Items.objects.get(ids = i['$ID'])
                upd = True
            except:
                handler = Items()
            handler.ids             = i['$ID']
            handler.id_name         = i['$ID_NAME']
            handler.cooldown        = i['TimeCoolDown']
            handler.descriptions    = i['Description']
            handler.name            = i['Name']
            handler.weight          = 0 if i['Weight'] == '' else i['Weight']
            handler.tradability     = i['Tradability']
            handler.type            = i['Type']
            if i['Type'] not in item_type_db:
                try:
                    type_handler = Item_Type.objects.get(name = i['Type'])
                except:
                    type_handler = Item_Type()
                type_handler.name = i['Type']
                type_handler.save()
                item_type_db.append(i['Type'])
            handler.grade           = i['Grade']
            handler.icon            = i['Icon']
            handler.save()
            if i['$ID_NAME'] in item_type['EQUIPMENT']:
                dolater['EQUIPMENT'].append([handler,i.copy(), upd])
                #self.makeEQ(handler,i,item_type_db, upd)
            elif i['$ID_NAME'] in item_type['CARD']:
                dolater['CARD'].append([handler,i.copy(), upd])
                #self.makeCard(handler,i,item_type_db, upd)
            elif i['$ID_NAME'] in item_type['RECIPES']:
                dolater['RECIPES'].append([handler,i.copy(), upd])
            elif i['$ID_NAME'] in item_type['COLLECTION']:
                dolater['COLLECTION'].append([handler,i.copy(),  upd])
            elif i['$ID_NAME'] in item_type['BOOKS']:
                dolater['BOOKS'].append([handler,i.copy(), upd])
                 #self.makeBook(handler,i,item_type_db, upd)
        
        for i in dolater['RECIPES']:
            self.makeRecipe(i[0], i[1], item_type_db, i[2])
        
        for i in dolater['COLLECTION']:
            self.makeCollection(i[0], i[1], item_type_db,i[2])

        for i in dolater['EQUIPMENT']:
            self.makeEQ(i[0], i[1], item_type_db,i[2])

        for i in dolater['CARD']:
            self.makeCard(i[0], i[1], item_type_db,i[2])

        for i in dolater['BOOKS']:
            self.makeBook(i[0], i[1], item_type_db,i[2])
        
        for i in items['changed']:
            try:
                handler = Items.objects.get(ids = i['$ID'])
            except:
                handler = Items()
            handler.ids             = i['$ID']
            handler.id_name         = i['$ID_NAME']
            handler.cooldown        = i['TimeCoolDown']
            handler.descriptions    = i['Description']
            handler.name            = i['Name']
            handler.weight          = 0 if i['Weight'] == '' else i['Weight']
            handler.tradability     = i['Tradability']
            handler.type            = i['Type']
            if i['Type'] not in item_type_db:
                try:
                    type_handler = Item_Type.objects.get(name = i['Type'])
                except:
                    type_handler = Item_Type()
                type_handler.name = i['Type']
                type_handler.save()
                item_type_db.append(i['Type'])
            handler.grade           = i['Grade']
            if i['Grade']          == "":
                handler.grade = 1
            handler.icon            = i['Icon']
            handler.save()
            if i['$ID_NAME'] in item_type['EQUIPMENT']:
                self.makeEQ(handler,i,item_type_db, upd = True)
            elif i['$ID_NAME'] in item_type['CARD']:
                self.makeCard(handler,i,item_type_db, upd = True)
            elif i['$ID_NAME'] in item_type['RECIPES']:
                self.makeRecipe(handler,i,item_type_db, upd = True)
            elif i['$ID_NAME'] in item_type['COLLECTION']:
                self.makeCollection(handler,i,item_type_db, upd = True)
            elif i['$ID_NAME'] in item_type['BOOKS']:
                self.makeBook(handler,i,item_type_db, upd = True)
                
        
           
        
    def makeEQ(self, item, i, item_type_db,upd = False):
        try:
            handler = Equipments.objects.get(item = item)
        except:
            handler = Equipments()
            handler.item = item
            
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
            try:
                type_handler = Item_Type.objects.get(name = i['Type'])
            except:
                type_handler = Item_Type()
            type_handler.name = i['TypeEquipment']
            type_handler.is_equipment = True
            type_handler.save()
            item_type_db.append(i['TypeEquipment'])
        handler.unidentified    = i['Unidentified']
        handler.unidentifiedRandom = i['UnidentifiedRandom']
        Equipment_Bonus.objects.filter(equipment = handler).delete()
        handler.save()
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
        handler.save()
    
    def makeCard(self, item, i, item_type_db,upd = False):
        try:
            handler = Cards.objects.get(item = item)
        except:
            handler = Cards()
            handler.item = item
        handler.icon = i['IconTooltip']
        
        handler.type_card = i['TypeCard']
        handler.save()
    
    def makeRecipe(self, item, i, item_type_db,upd = False):
        
        if ('Link_Materials' not in i):
            logging.warning("invalid recipe {}".format(i['Name']))
            logging.warning(i)
            return
        
        try:
            handler = Recipes.objects.get(item = item)
        except:
            handler = Recipes()
            handler.item = item
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
            logging.warn("[RCP] {} ({}) didnt have target".format(i['Name'], i['$ID_NAME']))
    
    def makeCollection(self, item, i, item_type_db,upd = False):
        if ('Link_Items' not in i):
            logging.warning("invalid recipe {}".format(i['Name']))
            return
        try:
            handler = Collections.objects.get(item = item)
        except:
            handler = Collections()
            handler.item = item
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
            logging.warn("[RCP] {} ({}) didnt have target".format(i['Name'], i['$ID_NAME']))

    def makeBook (self, item, i, item_type_db,upd = False):
        try:
            handler = Books.objects.get(item = item)
        except:
            handler = Books()
            handler.item = item
        if 'Text' in i:
            handler.text = i['Text']
        else:
            handler.text = None
        handler.save()
     
    def importMonster(self,monster, npc, update ):
        for i in monster['removed']:
            try:
                Monsters.objects.get(ids= i['$ID']).delete()
            except:
                logging.warning("failed to delete monster {} ({})".format(i['Name'], i['$ID']))
        for i in monster['added'] + monster['changed']:
            try:
                handler                 = Monsters.objects.get(ids= i['$ID'])
            except:
                handler = Monsters()
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
        
       
        
        for i in npc['removed']:
            try:
                Monsters.objects.get(ids= i['$ID']).delete()
            except:
                logging.warning("failed to delete monster {} ({})".format(i['Name'], i['$ID']))
        for i in npc['added']:
            try:
                handler                 = Monsters.objects.get(ids= i['$ID'])
            except:
                handler = Monsters()
            
            handler.ids             = i['$ID']
            handler.id_name         = i['$ID_NAME']            
            handler.descriptions    = i['Description']
            handler.icon            = i['Icon']
            handler.name            = i['Name']
            handler.save()
        
        for i in npc['changed']:
            handler                 = Monsters.objects.get(ids= i['$ID'])
            handler.ids             = i['$ID']
            handler.id_name         = i['$ID_NAME']            
            handler.descriptions    = i['Description']
            handler.icon            = i['Icon']
            handler.name            = i['Name']
            handler.save()
        
        
           
        
        
    def importItemMonster(self,item_monster, update ):
        for i in item_monster['removed']:
            try:
                Item_Monster(monster__ids = i['Monster'], item__ids = i['Item']).delete().delete()
            except:
                logging.warning("failed to delete item_monster {} ({})".format(i['Item'], i['Monster']))
        for i in item_monster['added'] + item_monster['changed']:
            try:
                handler                     = Item_Monster(monster__ids = i['Monster'], item__ids = i['Item'])
            except:
                handler = Item_Monster()
            handler.monster             = Monsters.objects.get(ids = i['Monster'])
            handler.item                = Items.objects.get(ids = i['Item'])
            handler.chance              = i['Chance']
            handler.qty_min             = i['Quantity_MIN']
            handler.qty_max             = i['Quantity_MAX']
            handler.save()
        
        

    
            
    def importMap (self,map, update ):
        for i in map['removed']:
            try:
                Maps(monster__ids = i['Monster'], item__ids = i['Item']).delete().delete()
            except:
                logging.warning("failed to delete map {} ({})".format(i['Name'], i['$ID']))
        for i in map['added'] + map['changed'] :
            try:
                handler = Maps.objects.get(ids= i['$ID'])
            except:
                handler = Maps()
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
        
        

    
    def importMapItem (self,map, update ):
        for i in map['removed']:
            try:
                m = Maps.objects.get(ids = i['Map'])
                it = Items.objects.get(ids = i['Item'])
            except:
                logging.warning("map {} or item {} not found".format(i['Map'], i['Item']))
                continue
            Map_Item.objects.get(map= m, item = it).delete()
        for i in map['added'] + map['changed']:
           
            try:
                m = Maps.objects.get(ids = i['Map'])
                it = Items.objects.get(ids = i['Item'])
            except:
                logging.warning("map {} or item {} not found".format(i['Map'], i['Item']))
                continue
            try:
                handler = Map_Item.objects.get(map= m, item = it)
            except:
                handler = Map_Item()
            handler.chance          = i['Chance']
            handler.item            = it
            handler.map             = m
            handler.qty_max         = i['Quantity_MAX']
            handler.qty_min         = i['Quantity_MIN']
            handler.save()
        
        
            
    
    
    def importMapItemSpawn (self,map, update ):
        for i in map['removed']:
            try:
                m = Maps.objects.get(ids = i['Map'])
                it = Items.objects.get(ids = i['Item'])
                Map_Item_Spawn.objects.get(map= m, item = it).delete()
            except:
                logging.warning("map {} or item {} not found".format(i['Map'], i['Item']))
                continue
        for i in map['added'] +  map['changed']:
          
            try:
                m = Maps.objects.get(ids = i['Map'])
                it = Items.objects.get(ids = i['Item'])
            except:
                logging.warning("map {} or item {} not found".format(i['Map'], i['Item']))
                continue
            try:
                handler = Map_Item_Spawn.objects.get(map= m, item = it)
            except:
                handler = Map_Item_Spawn()
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
         
        
        

            
    
    
    def importMapNPC (self,map, update ):
        for i in map['removed']:
            try:
                m = Maps.objects.get(ids = i['Map'])
                it = Monsters.objects.get(ids = i['NPC'])
                Map_NPC.objects.get(map= m, item = it).delete()
            except:
                logging.warning("map {} or item {} not found".format(i['Map'], i['NPC']))
                continue
        for i in map['added'] + map['changed']:
            
            try:
                m = Maps.objects.get(ids = i['Map'])
                it = Monsters.objects.get(ids = i['NPC'])
            except:
                logging.warning("map {} or item {} not found".format(i['Map'], i['NPC']))
                continue
            try:
                handler = Map_NPC.objects.get(map= m, monster = it)
            except:
                handler = Map_NPC()
            handler.population      = i['Population']
            handler.monster         = it
            handler.map             = m
            pos = []
            for posit in i['Positions']:
                for po in posit:
                    pos.append(po)
            handler.time_respawn    = i['TimeRespawn']
            handler.positions        = pos
            try:
                handler.save()
            except:
                logging.warning(len(handler.positions))
                logging.warning(handler.positions)
            
        
        

            
            
    
    def importJobs(self,jobs, update ):
        for i in jobs['removed']:
            try:
                Jobs.objects.get(ids= i['$ID']).delete()
            except:
                logging.warning("failed to delete jon {} ({})".format(i['Name'], i['$ID']))
        for i in jobs['added'] + jobs['changed']:
            try:
                handler = Jobs.objects.get(ids= i['$ID'])
            except:
                handler = Jobs()
            handler.ids             = i['$ID']
            handler.id_name         = i['$ID_NAME']            
            handler.name            = i['Name']
            handler.is_starter      = i['IsStarter']
            handler.job_tree        = i['JobTree']
            handler.icon            = i['Icon']
            handler.descriptions    = i['Description']
            handler.save()
            
        
        
            
            
        
    
    def importSkills(self,skills, update ):
        logging.debug("migrating monsters")
        count = 0
        count_all = len(skills)
        table = Skills
        all_item = table.objects.values_list('ids')
        json_item = []
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
            if (i['RequiredStanceCompanion'].lower() == 'yes'):
                handler.is_riding       = True
            else:
                handler.is_riding       = False
            handler.effect          = i['Effect']
            handler.element         = i['Element']
            handler.max_lv          = i['MaxLevel']
            handler.unlock          = i['UnlockClassLevel']
            handler.overheat        = i['OverHeat']
            handler.job             = Jobs.objects.get(ids = i['Link_Job'])
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
            if 'CoolDown' in i:
                try:
                    for h in i['CoolDown']:
                        h = int(h)
                except:
                    i['CoolDown'] = None
                handler.cooldown_lv     = i['CoolDown'] 
            handler.job = Jobs.objects.get(ids = i['Link_Job'])
            handler.stance = i['RequiredStance']
            handler.save()
            
            
            count+=1
        self.deleteMe(all_item, json_item, table, 'Skills')
        
    def importAttrib (self,attrib, update ):
        for i in attrib['removed']:
            try:
                Attributes.objects.get(ids= i['$ID']).delete()
            except:
                logging.warning("failed to delete attrib {} ({})".format(i['Name'], i['$ID']))

        for i in attrib['added'] + attrib['changed']:
            try:
                handler = Attributes.objects.get(ids= i['$ID'])
                if (i['LevelMax']==-1):
                    attrib['removed'].append(i)
                    continue
                
            except:
                handler = Attributes()
                if (i['LevelMax']==-1):
                    continue
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
            
        
        
            
            
    def importSkillMon(self, skillmon, update):
        for i in skillmon['removed']:
            try:
                Skill_Monster.objects.get(ids= i['$ID']).delete()
            except:
                logging.warning("failed to delete skillmon {} ({})".format(i['Name'], i['$ID']))
            
        for i in skillmon['added'] +skillmon['changed'] :
            try:
                handler = Skill_Monster.objects.get(ids= i['$ID'])
            except:
                handler = Skill_Monster()
            link_mon = []
            handler.ids             = i['$ID']
            handler.id_name         = i['$ID_NAME']            
            handler.name            = i['Name']
            try:
                handler.sfr             = int(i['SFR'])
            except:
                handler.sfr             = 0
            handler.element         = i['Attribute']
            handler.cooldown        = int(i['CD'])
            handler.aar             = i['AAR']
            handler.save()
            for monster in i['Monster']:
                try:
                    link_mon.append(Monsters.objects.get(ids = monster))
                except:
                    logging.warning("monster(ids) {} not found (for skill)".format(monster))
            for mon in link_mon:
                handler.monsters.add(mon)
            handler.save()
            
        
            
    def importBuff(self, buff, update):
        for i in buff['removed']:
            try:
                Buffs.objects.get(ids= i['$ID']).delete()
            except:
                logging.warning("failed to delete buff {} ({})".format(i['Name'], i['$ID']))
            
        for i in buff['added'] +buff['changed'] :
            try:
                handler = Buffs.objects.get(ids= i['$ID'])
            except:
                handler = Buffs()
            link_mon = []
            handler.ids             = i['$ID']
            handler.id_name         = i['$ID_NAME']            
            handler.name            = i['Name']
            handler.icon            = i['Icon']
            handler.descriptions    = i['Description']
            handler.applytime       = i['ApplyTime']
            handler.group1          = i['Group1']
            handler.group2          = i['Group2']
            handler.group3          = i['Group3']
            handler.groupindex      = i['GroupIndex']
            handler.overbuff        = i['OverBuff']
            handler.userremove      = i['UserRemove']
            handler.keyword         = i['Keyword']
            handler.save()
            

            
    def importAchieve(self, achieve, update):
        for i in achieve['removed']:
            try:
                Achievements.objects.get(ids= i['$ID']).delete()
            except:
                logging.warning("failed to delete achievements {} ({})".format(i['Name'], i['$ID']))
            
        for i in achieve['added'] +achieve['changed'] :
            try:
                handler = Achievements.objects.get(ids= i['$ID'])
            except:
                handler = Achievements()
            link_mon = []
            handler.ids             = i['$ID']
            handler.id_name         = i['$ID_NAME']            
            handler.name            = i['Name']
            handler.icon            = i['Icon']
            if ('Image' in i):
                handler.image           = i['Image']
            handler.hidden          = i['Hidden']
            handler.descriptions    = i['Desc']
            handler.desc_title      = i['DescTitle']
            handler.group           = i['Group']
            handler.save()
