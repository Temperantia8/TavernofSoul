# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 14:08:20 2021

@author: Temperantia
"""

from itertools import islice
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
import logging
import json
from os.path import join, exists
from Monsters.models import Monsters, Item_Monster, Skill_Monster,Buff_Skill_Monster
import os
import shutil
from Items.models import Items, Equipments, Equipment_Bonus, Cards, Recipes, Books, Equipment_Set
from Items.models import Item_Recipe_Material
from Items.models import Collections, Item_Collection_Material, Item_Collection_Bonus
from Items.models import Goddess_Reinforce_Mat, Goddess_Reinforce_Chance
from Items.models import Eq_Reinf, Eq_TC

from Maps.models import Maps, Map_Item, Map_NPC,Map_Item_Spawn
from Jobs.models import Jobs
from Buffs.models import Buffs
from Skills.models import Skills,Buff_Skill
from Attributes.models import Attributes
from Dashboard.models import Version
from Other.models import Achievements


def bulk_op(operation, objs, batch_size, fields = False):
    count = 0
    leng = len(objs)
    batch_size = int(batch_size)
    
    while True:
        logging.warning("---- bulk %s %s / %s | %s" %('update' if fields else 'insert',  batch_size * count, leng, count))

        batch = list(islice(objs,count* batch_size, (count+1) * batch_size))
        if not batch:
            break
        if fields:
            operation(batch, fields, batch_size)    
        else:
            operation(batch, batch_size)
        count+=1

class Command(BaseCommand):
    
    base_path               = settings.JSON_ROOT
    maps_path               = 'maps.json'
    maps_by_name_path       = 'maps_by_name.json'
    maps_by_position_path   = 'maps_by_position.json'
    map_item_path           = 'map_item.json'
    map_npc_path            = 'map_npc.json'
    map_item_spawn_path     = 'map_item_spawn.json'
    jobs_path               = "jobs.json"
    jobs_by_name_path       = "jobs_by_name.json"
    attributes_by_name_path = "attributes_by_name.json"
    attributes_path         = "attributes.json"
    skills_path             = "skills.json"
    skills_by_name_path     = "skills_by_name.json"
    item_path               = 'items_by_name.json'
    monster_path            = 'monsters.json'
    item_monster_path       = 'item_monster.json'
    npc_path                = 'npcs.json'
    item_path               = 'items_by_name.json'
    item_type_path          = 'item_type.json'
    version_path            = 'version.json'
    buff_path               = 'buff.json'
    achieve_path            = 'achievements.json'
    all_dic                 = {}
    
    
    
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

        buff = self.comparer(self.buff_path)
        self.importBuff(buff)

        jobs           = self.comparer(self.jobs_path)
        self.importJobs(jobs)
    
        
        skills         = self.comparer(self.skills_path)
        self.importSkillsWithComparer(skills)
        
        attrib         = self.comparer(self.attributes_path)
        self.importAttrib(attrib)

        skills      = { i.name.lower() : i.job for i in Skills.objects.all() }
        all_dic_k = sorted(skills, key=lambda k: len(k))
        all_dic_sorted = {}
        for i in all_dic_k:
            all_dic_sorted[i] = skills[i]
        skills = all_dic_sorted


        classes     = { i.name.lower() : i for i in Jobs.objects.all()}
        skills.update(classes)
        self.all_dic = skills

        items           = self.comparer(self.item_path)
        self.importItem(items,item_type)
        
        npc             = self.comparer(self.npc_path)
        monster         = self.comparer(self.monster_path)
        self.importMonster(monster, npc)
        
        item_monster    = self.comparer(self.item_monster_path, ['Item','Monster'])
        self.importItemMonster(item_monster)
        
        map = self.comparer(self.maps_path)
        self.importMap(map)
        
        map = self.comparer(self.map_item_path, ['Map', 'Item'])
        self.importMapItem(map)
        
        map = self.comparer(self.map_npc_path, ['Map', 'NPC'])
        self.importMapNPC(map)
        
        map = self.comparer(self.map_item_spawn_path, ['Map', 'Item'] )
        self.importMapItemSpawn(map)
        
        skillmon = self.comparer('skill_mon.json')
        self.importSkillMon(skillmon)
        


        achieve = self.comparer(self.achieve_path)
        self.importAchieve(achieve)
        self.importGoddess()
        self.importEQSet()

        source = os.listdir(self.base_path)
        destination = join(self.base_path,"prev")
        for files in source:
            if files.endswith(".json"):
                shutil.copy(join(self.base_path,files),join(destination,files))

        
    items = {}
    def importItem(self,items, item_type ):
        for i in items['removed']:
            try:
                Items.objects.get(ids= i['$ID']).delete()
            except:
                logging.warning("failed to delete item {} ({})".format(i['Name'], i['$ID']))
        logging.debug("migrating items")
        dolater = {'RECIPES': [],'COLLECTION': [], 'EQUIPMENT' : [], 'CARD' : [], 'BOOKS' :[] }
        bulk_insert = {}
        bulk_upd    = {}
        items_all   = {i.ids : i for i in Items.objects.all()}

        for i in items['added'] + items['changed']:
            upd = False
            if i['$ID'] in items_all:
                handler = items_all[i['$ID']]
                upd = True
            else:
                handler = Items()
            handler.ids             = i['$ID']
            handler.id_name         = i['$ID_NAME']
            handler.cooldown        = i['TimeCoolDown']
            handler.descriptions    = i['Description']
            handler.name            = i['Name']
            handler.weight          = 0 if i['Weight'] == '' else i['Weight']
            handler.tradability     = i['Tradability']
            handler.type            = i['Type']
            handler.grade           = i['Grade']
            handler.icon            = i['Icon']
            # handler.save()
            if i['$ID_NAME'] in item_type['EQUIPMENT']:
                dolater['EQUIPMENT'].append([handler,i.copy(), upd])
                #self.makeEQ(handler,i,  upd)
            elif i['$ID_NAME'] in item_type['CARD']:
                dolater['CARD'].append([handler,i.copy(), upd])
                #self.makeCard(handler,i,  upd)
            elif i['$ID_NAME'] in item_type['RECIPES']:
                dolater['RECIPES'].append([handler,i.copy(), upd])
            elif i['$ID_NAME'] in item_type['COLLECTION']:
                dolater['COLLECTION'].append([handler,i.copy(),  upd])
            elif i['$ID_NAME'] in item_type['BOOKS']:
                dolater['BOOKS'].append([handler,i.copy(), upd])
                 #self.makeBook(handler,i,  upd)
            if upd:
                bulk_upd[handler.ids] = handler
            else:
                bulk_insert[handler.ids] = handler
        
        bulk_op(Items.objects.bulk_create, bulk_insert.values(), 1000)
        bulk_op(Items.objects.bulk_update, bulk_upd.values(), 1000, Items.fields)
        self.items = {i.ids : i for i in Items.objects.all()}
        del(bulk_insert)
        del(bulk_upd)
                
        logging.warning("-- parsing recipes" )
        mat_bulk = []
        for i in dolater['RECIPES']:
            self.makeRecipe(i[0], i[1],   i[2])
        # bulk_op(Item_Recipe_Material, mat_bulk,1000)
        
        
        logging.warning("-- parsing collection" )
        for i in dolater['COLLECTION']:
            self.makeCollection(i[0], i[1],  i[2])


        logging.warning("-- parsing equipment" )
        bulks = []
        anvil_handler_ins   = []
        anvil_handler_upd   = []
        tc_handler_ins      = []
        tc_handler_upd      = []
        bonus_handler       = []
        for i in dolater['EQUIPMENT']:
            bulks.append(self.makeEQ(i[0], i[1],  i[2]))
        for i in bulks:
            anvil_handler_ins   += i[0]
            anvil_handler_upd   += i[1]
            tc_handler_ins      += i[2]
            tc_handler_upd      += i[3]
            bonus_handler       += i[4]

        logging.warning("-- importing anvils" )
        bulk_op(Eq_Reinf.objects.bulk_create, anvil_handler_ins, 1000)
        bulk_op(Eq_Reinf.objects.bulk_update, anvil_handler_upd, 1000,  ['price', 'addatk'])
        logging.warning("-- importing transcends" )
        bulk_op(Eq_TC.objects.bulk_update, tc_handler_upd, 1000,  ['price', 'tc'])
        bulk_op(Eq_TC.objects.bulk_create, tc_handler_ins, 1000,  )
        logging.warning("-- importing bonus" )
        bulk_op(Equipment_Bonus.objects.bulk_create, bonus_handler, 1000)

        logging.warning("-- parsing cards" )
        for i in dolater['CARD']:
            self.makeCard(i[0], i[1],  i[2])

        logging.warning("-- parsing books" )
        for i in dolater['BOOKS']:
            self.makeBook(i[0], i[1],  i[2])
                
        
           
        
    def makeEQ(self, item, i,  upd = False):
        item = self.items[item.ids]
        try:
            handler = Equipments.objects.get(item = item)
        except:
            handler = Equipments()
            handler.item = item
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
        handler.type_attack     = i['TypeAttack']
        handler.type_equipment  = i['TypeEquipment']
        handler.unidentified    = i['Unidentified']
        handler.unidentifiedRandom = i['UnidentifiedRandom']
        handler.model           = i['model']
        handler.save()

        anvil_handler_upd = []
        anvil_handler_ins = []
        anvil_obj = {i.anvil: i for i in Eq_Reinf.objects.filter(equipment = handler)}
        if i['AnvilATK']:
            for h in range(len(i['AnvilATK'])):
                if h+1 in anvil_obj:
                    eq_handler = anvil_obj[h+1]
                    if eq_handler.price == i['AnvilPrice'][h] and eq_handler.addatk == i['AnvilATK'][h]:
                        continue
                    eq_handler.price         = i['AnvilPrice'][h]
                    eq_handler.addatk        = i['AnvilATK'][h]
                    anvil_handler_upd.append(eq_handler)
                else:
                    eq_handler = Eq_Reinf(equipment = handler, anvil = h+1)
                    eq_handler.price         = i['AnvilPrice'][h]
                    eq_handler.addatk        = i['AnvilATK'][h]
                    anvil_handler_ins.append(eq_handler)

        if i['AnvilDEF']:
            for h in range(len(i['AnvilDEF'])):
                if h+1 in anvil_obj:
                    eq_handler = anvil_obj[h+1]
                    if eq_handler.price == i['AnvilPrice'][h] and eq_handler.addatk == i['AnvilDEF'][h]:
                        continue
                    eq_handler.price         = i['AnvilPrice'][h]
                    eq_handler.addatk        = i['AnvilDEF'][h]
                    anvil_handler_upd.append(eq_handler)
                else:
                    eq_handler           = Eq_Reinf(equipment = handler, anvil = h+1)
                    eq_handler.price         = i['AnvilPrice'][h]
                    eq_handler.addatk        = i['AnvilDEF'][h]
                    anvil_handler_ins.append(eq_handler)
                # eq_handler.save()
                # anvil_handler.append(eq_handler)



        # Eq_Reinf.objects.bulk_update(anvil_handler_upd, ['price', 'addatk'])
        # Eq_Reinf.objects.bulk_create(anvil_handler_ins)

        tc_handler_upd = []
        tc_handler_ins = []
        # Eq_TC.objects.filter(equipment = handler).delete()
        tc_obj = {i.tc: i for i in Eq_TC.objects.filter(equipment = handler)}
        if i['TranscendPrice']:
            for h in range(len(i['TranscendPrice'])):
                if h+1 in tc_obj:
                    eq_handler = tc_obj[h+1]
                    if (eq_handler.price == i['TranscendPrice'][h]):
                        continue
                    eq_handler.price = i['TranscendPrice'][h]
                    tc_handler_upd.append(eq_handler)
                else:
                    eq_handler = Eq_TC(equipment = handler, tc = h+1)
                    eq_handler.price = i['TranscendPrice'][h]
                    tc_handler_ins.append(eq_handler)
                # eq_handler.save()
                

        # Eq_TC.objects.bulk_update(bulk_handler_upd, ['price', 'tc'])
        # Eq_TC.objects.bulk_create(bulk_handler_ins)

        Equipment_Bonus.objects.filter(equipment = handler).delete()
        bonus_handler = []
        all_dic = self.all_dic

        if (i['Bonus']):
            for b in i['Bonus']:
                bonus = Equipment_Bonus(equipment = handler)
                bonus.bonus_stat = b[0]
                bonus.bonus_val  = b[1]
                bonus_handler.append(bonus)


            if settings.REGION == 'jtos':
                vv_name = 'バイボラ秘伝'
            else:
                vv_name = "vaivora vision"

            #if vv_name in i['Name'].lower() and 'lv4' in  i['Name'].lower() and settings.REGION != 'jtos':
            #    for bonus in i['Bonus']:                
            #        if 'job' not in i:
            #            continue
            #        job = Jobs.objects.get(ids = i['job'])
            #        job.vaivora = handler
            #        job.save() 


        return [anvil_handler_ins, anvil_handler_upd, tc_handler_ins, tc_handler_upd, bonus_handler]


    def makeCard(self, item, i,  upd = False):
        item = self.items[item.ids]
        try:
            handler = Cards.objects.get(item = item)
        except:
            handler = Cards()
            handler.item = item
        handler.icon = i['IconTooltip']
        
        handler.type_card = i['TypeCard']
        handler.save()
    
    def makeRecipe(self, item, i,  upd = False):
        item = self.items[item.ids]
        if ('Link_Materials' not in i):
            return
        
        if upd:
            handler = Recipes.objects.get(item = item)
        else:
            handler = Recipes()
            handler.item = item
            handler.target = Items.objects.get(id_name = i['Link_Target'])
            handler.save()
        # Item_Recipe_Material.objects.filter(recipe = handler).delete()

        materials = {i.material.id_name : i for i in  Item_Recipe_Material.objects.filter(recipe = handler)}

        for link in i['Link_Materials']:
            try:
                if (link['Item'] in materials):
                    mat = materials[link['Item']]
                    if mat.qty == link['Quantity']:
                        continue
                else:
                    mat             = Item_Recipe_Material(recipe = handler)
                    mat.material    = Items.objects.get(id_name = link['Item'])
                mat.qty         = link['Quantity']
                mat.save()
            except:
                logging.warn("[RCP] {} ({}) material not found ({})".format(i['Name'], i['$ID_NAME'], link['Item']))
        # return mat
        
    
    def makeCollection(self, item, i,  upd = False):
        item = self.items[item.ids]
        if ('Link_Items' not in i):
            logging.warning("invalid recipe {}".format(i['Name']))
            return
        if upd:
            handler = Collections.objects.get(item = item)
        else:
            handler = Collections()
            handler.item = item
            handler.save()

        # Item_Collection_Material.objects.filter(collection = handler).delete()
        materials = {i.material.id_name : i for i in  Item_Collection_Material.objects.filter(collection = handler)}
        bulk = []
        for link in i['Link_Items']:
            try:
                if link in materials:
                    continue
                mat             = Item_Collection_Material(collection = handler)
                mat.material    = Items.objects.get(id_name = link)
                # mat.save()
                bulk.append(mat)
            except:
                logging.warn("[RCP] {} ({}) material not found ({})".format(i['Name'], i['$ID_NAME'], link))
        Item_Collection_Material.objects.bulk_create(bulk)
        
        try:
            if (i['Bonus']):
                Item_Collection_Bonus.objects.filter(collection = handler).delete()
                bulk = []
                for b in i['Bonus']:
                    bonus = Item_Collection_Bonus(collection = handler)
                    bonus.bonus_stat = b[0]
                    bonus.bonus_val  = b[1]
                    # bonus.save()
                    bulk.append(bonus)
                Item_Collection_Bonus.objects.bulk_create(bulk)
        except:
            logging.warn("[RCP] {} ({}) didnt have target".format(i['Name'], i['$ID_NAME']))

    def makeBook (self, item, i,  upd = False):
        item = self.items[item.ids]
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
     
    def importMonster(self,monster, npc ):
        for i in monster['removed']:
            try:
                Monsters.objects.get(ids= i['$ID']).delete()
            except:
                logging.warning("failed to delete monster {} ({})".format(i['Name'], i['$ID']))

        bulk_upd    = []
        bulk_ins    = []
        # mons        = {i.ids :i for i in Monsters.objects.all()}
        for i in monster['added'] + monster['changed']:
            try:
                handler = Monsters.objects.get(ids= i['$ID'])
                upd     = True
            except:
                handler = Monsters()
                upd     = False
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
            # handler.save()
            if upd:
                bulk_upd.append(handler)
            else:
                bulk_ins.append(handler)

        for i in npc['removed']:
            try:
                Monsters.objects.get(ids= i['$ID']).delete()
            except:
                logging.warning("failed to delete monster {} ({})".format(i['Name'], i['$ID']))

        for i in npc['added'] +  npc['changed']:
            try:
                handler                 = Monsters.objects.get(ids= i['$ID'])
                upd     = True
            except:
                handler = Monsters()
                upd     = False
            handler.ids             = i['$ID']
            handler.id_name         = i['$ID_NAME']            
            handler.descriptions    = i['Description']
            handler.icon            = i['Icon']
            handler.name            = i['Name']
            # handler.save()
            if upd:
                bulk_upd.append(handler)
            else:
                bulk_ins.append(handler)
        
        bulk_op(Monsters.objects.bulk_create, bulk_ins,100)
        bulk_op(Monsters.objects.bulk_update, bulk_upd,100, Monsters.fields)
        
        
           
        
        
    def importItemMonster(self,item_monster ):
        for i in item_monster['removed']:
            try:
                Item_Monster(monster__ids = i['Monster'], item__ids = i['Item']).delete()
            except:
                logging.warning("failed to delete item_monster {} ({})".format(i['Item'], i['Monster']))

        bulk_upd    = []
        bulk_ins    = []
        for i in item_monster['added'] + item_monster['changed']:
            try:
                handler = Item_Monster.objects.get(monster__ids = i['Monster'], item__ids = i['Item'])
                upd     = True
            except:
                handler = Item_Monster()
                upd     = False
            handler.monster             = Monsters.objects.get(ids = i['Monster'])
            handler.item                = Items.objects.get(ids = i['Item'])
            handler.chance              = i['Chance']
            handler.qty_min             = i['Quantity_MIN']
            handler.qty_max             = i['Quantity_MAX']
            if upd:
                bulk_upd.append(handler)
            else:
                bulk_ins.append(handler)

        bulk_op(Item_Monster.objects.bulk_create, bulk_ins,1000)
        bulk_op(Item_Monster.objects.bulk_update, bulk_upd,1000, ['monster','item','chance','qty_min','qty_max'])
        
    def importMap (self,map ):
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
        
    def importMapItem (self,map ):
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
        
    def importMapItemSpawn (self,map ):
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
         
    def importMapNPC (self,map ):
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
            
        
        

            
            
    
    def importJobs(self,jobs ):
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
            
        
        
            
    def importSkillsWithComparer(self, skills):
        for i in skills['removed']:
            try:
                Skills.objects.get(ids= i['$ID']).delete()
            except:
                logging.warning("failed to delete Skills {} ({})".format(i['Name'], i['$ID']))
        for i in skills['added'] + skills['changed']:
            try:
                handler = Skills.objects.get(ids= i['$ID'])
            except:
                handler = Skills()
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
                handler.is_riding       = 2
            elif (i['RequiredStanceCompanion'].lower() == 'both'):
                handler.is_riding       = 1
            else:
                handler.is_riding       = 0
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

            for buff in i['TargetBuffs']:
                buff = buff.split(';')
                
                try:
                    h = Buffs.objects.get(id_name = buff[0])
                except:
                    continue
                try:
                    handler_buff = Buff_Skill.objects.get(skill= handler, buff = h )
                except:
                    handler_buff = Buff_Skill(skill= handler, buff = h )
                handler_buff.duration = buff[1]
                # print(buff)
                handler_buff.chance = buff[2]

                # quit()
                handler_buff.save()
                
            
        
        
    def importAttrib (self,attrib ):
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
                    #logging.warning("skill not found {}".format(h))
                    pass
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
                    logging.warning("class not found {}".format(h))
                    pass
            for job in handler.job.all(): # for deletions
                if job.ids not in added_jobs:
                    handler.job.remove(job)
            handler.save()
            
        
        
            
            
    def importSkillMon(self, skillmon):
        for i in skillmon['removed']:
            try:
                Skill_Monster.objects.get(ids= i['$ID']).delete()
            except:
                logging.warning("failed to delete skillmon {} ({})".format(i['Name'], i['$ID']))
        
        bulk_upd = []
        bulk_ins = []
        for i in skillmon['added'] +skillmon['changed'] :
            try:
                handler = Skill_Monster.objects.get(ids= i['$ID'])
                upd = True
            except:
                handler = Skill_Monster()
                upd = False
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
            # handler.save()
            if(upd):
                bulk_upd.append(handler)
            else:
                bulk_ins.append(handler)
        bulk_op(Skill_Monster.objects.bulk_create, bulk_ins, 1000)
        bulk_op(Skill_Monster.objects.bulk_update, bulk_upd, 1000, ['ids', 'id_name', 'name', 'sfr', 'element', 'cooldown', 'aar'])
        mon          = {i['ids'] : i['id'] for i in Monsters.objects.values('id', 'ids')}
        skillmon_obj = {i.ids : i for i in Skill_Monster.objects.all()}

        for i in skillmon['added'] +skillmon['changed'] :
            handler = skillmon_obj[i['$ID']]
            link_mon = []
            for monster in i['Monster']:
                try:
                    link_mon.append(mon[str(monster)])
                except:
                    logging.warning("monster(ids) {} not found (for skill)".format(monster))
            # for monmon in link_mon:
            handler.monsters.set(link_mon)
            # handler.save()
            for buff in i['TargetBuffs']:
               
                buff = buff.split(';')
                #print(buff)
                try:
                    h = Buffs.objects.get(id_name = buff[0])
                except:
                    continue
                try:
                    handler_buff = Buff_Skill_Monster.objects.get(skill= handler, buff = h )
                except:
                    handler_buff = Buff_Skill_Monster(skill= handler, buff = h )
                handler_buff.duration = buff[1]
                handler_buff.chance = buff[2]
                handler_buff.save()
                
    def importBuff(self, buff):
        for i in buff['removed']:
            try:
                Buffs.objects.get(ids= i['$ID']).delete()
            except:
                logging.warning("failed to delete buff {} ({})".format(i['Name'], i['$ID']))
        bulk = {'upd' : [], 'create' : []}
        for i in buff['added'] +buff['changed'] :
            try:
                handler = Buffs.objects.get(ids= i['$ID'])
                key = 'upd'
            except:
                handler = Buffs()
                key = 'create'
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
            bulk[key].append(handler)
            # handler.save()
        bulk_op(Buffs.objects.bulk_create,bulk['create'],1000)
        bulk_op(Buffs.objects.bulk_update,bulk['upd'],1000, Buffs.fields)

            
    def importAchieve(self, achieve):
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
    
    def importEQSet(self):
        file    = 'equipment_sets.json'
        eq_set  = self.comparer(file)
        for i in eq_set['removed']:
            try:
                Equipment_Set.objects.get(ids= i['$ID']).delete()
            except:
                logging.warning("failed to delete achievements {} ({})".format(i['Name'], i['$ID']))
            
        for i in eq_set['added'] +eq_set['changed'] :
            try:
                handler = Equipment_Set.objects.get(ids = i['$ID'])
            except:
                handler = Equipment_Set(ids = i['$ID'])

            handler.bonus2 = i['Bonus2']
            handler.bonus3 = i['Bonus3']
            handler.bonus4 = i['Bonus4']
            handler.bonus5 = i['Bonus5']
            handler.bonus6 = i['Bonus6']
            handler.bonus7 = i['Bonus7']
            handler.name   = i['Name']
            handler.id_name = i['$ID_NAME']
            handler.save()
            for i in i['Link_Items']:
                eq_handler = Equipments.objects.get(item__id_name = i)
                handler.equipment.add(eq_handler)
