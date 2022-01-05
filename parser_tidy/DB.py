# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 09:20:20 2021

@author: Temperantia

everything goes here
temporary database from parse and make json database to be inserted to mysql
"""
from os.path import join, exists,getmtime
import os
import logging
import json
import shutil
def is_ascii(item):
    try:
        item.decode('ascii')
    except UnicodeDecodeError:
        return False
    return True

class ToS_DB():
    BASE_PATH_INPUT                 = None
    BASE_PATH_OUTPUT                = None
    STATIC_ROOT                     = None
    PATH_BUILD_ASSETS_ICONS         = None
    PATH_BUILD_ASSETS_IMAGES_MAPS   = None
    PATH_INPUT_DATA                 = None
    PATH_INPUT_DATA_LUA             = None
    transaltion_path                = None
    region                          = None
    
    EQUIPMENT_IES   = ['item_equip.ies',
                        'item_Equip_EP12.ies',
                        'item_Equip_EP13.ies',
                        'item_event_equip.ies',]
    ITEM_IES = {
        "item.ies"                  :'01',
        'item_colorspray.ies'       :'02',
        'item_gem.ies'              :'03',
        'item_Equip.ies'            :'04',
        'item_Equip_EP12.ies'       :'05',
        'item_premium.ies'          :'06',
        'item_quest.ies'            :'07',
        'recipe.ies'                :'08',
        'item_EP12.ies'             :'09',
        'item_gem_relic.ies'        :'10',
        'item_gem_bernice.ies'      :'11',
        'item_GuildHousing.ies'     :'12',
        'item_PersonalHousing.ies'  :'13',
        'item_HiddenAbility.ies'    :'14',
        'item_event.ies'            :'15', 
        'item_event_Equip.ies'      :'16', 
        'item_EP13.ies'             :'17',
        'item_Equip_EP13.ies'       :'17',
        'item_Reputation.ies'       :'18',
        }
    
    file_dict = {}
    
    
    data_build = ['assets_icons', 'maps', 'maps_by_name', 'maps_by_position']
        
    data = {
       'dictionary'          : {},
       'items'               : {},
       'items_by_name'       : {},
       'cubes_by_stringarg'  : {},
       'equipment_sets'      : {},
       'item_type'           : {},
       'equipment_sets_by_name' : {},
       'assets_icons'        : {},
       'jobs'                : {},
       'jobs_by_name'        : {},
       'attributes'          : {},
       'attributes_by_name'  : {},
       'skills'              : {},
       'skills_by_name'      : {},
       'monsters'            : {},
       'monsters_by_name'    : {},
       'item_monster'        : [],
       'npcs'                : {},
       'npcs_by_name'        : {},
       'maps'                : {},
       'maps_by_name'        : {},
       'maps_by_position'    : {},
       'map_item'            : [],
       'map_npc'             : [],
       'map_item_spawn'      : [],
       'skill_mon'           : {},
       'equipment_grade_ratios' : {},
       'buff'                : {},
       'achievements'        : {},
       'charxp'              : {},
       'petxp'               : {},
       'assisterxp'          : {},
       'goddess_reinf_mat'   : {},
       'goddess_reinf'       : {}
       }
    
    
    def build(self, region):
        region = region.lower()
        self.BASE_PATH_INPUT                 = join("..", "TavernofSoul", "JSON_{}".format(region))
        self.BASE_PATH_OUTPUT                = join( "..", "TavernofSoul", "JSON_{}".format(region))
        #self.STATIC_ROOT                     = '/home/tavp7339/www/itos/static'
        self.STATIC_ROOT                     = join("..", "TavernofSoul", "staticfiles_itos")
        self.PATH_BUILD_ASSETS_ICONS         = join (self.STATIC_ROOT,"icons")
        self.PATH_BUILD_ASSETS_IMAGES_MAPS   = join (self.STATIC_ROOT,"maps")
        self.PATH_INPUT_DATA                 = join('..','{}_unpack'.format(region))
        self.PATH_INPUT_DATA_LUA             = join('..','{}_unpack'.format(region))
        if region == 'itos':
            self.transaltion_path                = join ("..","Translation", 'English')
        elif region == 'jtos':
            self.transaltion_path                = join ("..","Translation", 'Japanese')
        else:
            self.transaltion_path                = "."
            
        self.directoryDictionary(self.PATH_INPUT_DATA)
        
        
        for i in self.data_build:
            path = "%s.json"%(i)
            path = join(self.BASE_PATH_INPUT, path)
            self.data[i] = self.importJSON(path)
        
    def export(self):
        for i in self.data:
            path = "{}.json".format(i)
            self.printJSON(self.data[i],path)
    
    
    def export_one(self, file):
        i = file
        path = "{}.json".format(i)
        self.printJSON(self.data[i],path)
    
    def reverseDict(self, dicts):
        a = {}
        for i in dicts.keys():
            a [dicts[i]] =  i
        return a
    
    """
    utility functions
    """
    
        
    def directoryDictionary(self, base_dir):
        #os.path.getmtime(path)
        items = os.listdir(base_dir)
        for i in items:
            path = os.path.join(base_dir, i)
            if os.path.isdir(path):
                self.directoryDictionary(path)
            else:
                il = i.lower()
                time        = os.path.getmtime(path)
                mini_dict   ={'time': time, 'name' : i, 'path': path}
                if il in self.file_dict and time > self.file_dict[il]['time']:
                    self.file_dict[il] = mini_dict
                else:
                    self.file_dict[il] = mini_dict
                
    
    def translate(self, key):
        if self.transaltion_path == None:
            return self.data['dictionary'][key]
        key = key.replace('"', '')
        if (self.data['dictionary']=={}):
            logging.debug('dictionary is empty')
            return key
        if not self.data['dictionary']:
            return key
    
        if key != '' and key not in self.data['dictionary']:
            #logging.warn('Missing translation for key: %s', key)
            return key
        if key == '':
            return ''
            
        return self.data['dictionary'][key]
    
        
    
    def parse_entity_icon(self,icon):
        icon = icon.lower()
        icon_found = None
    
        if icon == '':
            return None
    
        if icon in self.data['assets_icons']:
            icon_found = icon
        elif 'icon_' + icon in self.data['assets_icons']:
            icon_found = 'icon_' + icon
        elif icon +'_f' in self.data['assets_icons']:
            icon_found = icon + '_f'
        elif icon + '_m' in self.data['assets_icons']:
            icon_found = icon + '_m'
    
        if icon_found is not None:
            #constants.assets_icons_used.append(icon_found)
            return self.data['assets_icons'][icon_found]
        else:
            # Note: there's nothing we can do about this :'(
            #logging.debug('Missing icon: %s', icon)
            return icon

 

    def printJSON(self, item, file):
        file_input = join (self.BASE_PATH_INPUT, file)
        #file_output = join(self.BASE_PATH_OUTPUT, file)
        with open(file_input, "w") as f:
            json.dump(item,f)
        #shutil.copy(file_input, file_output)
        
        
    def importJSON(self,  file):
        
        if not exists(file):
            logging.warn("not exists{}".format(file))
            return {}
        try:
            with open(file, "r") as f:
                data = json.load(f)
        except:
            logging.error("error in importing file {}".format(file))
            return {}
        return data
    
    def getNPCbyName(self, name):
        if name in self.data['monsters_by_name']:
            return self.data['monsters_by_name'][name], 'mon'
        elif name in self.data['npcs_by_name']:
            return self.data['npcs_by_name'][name], 'npc'
        else:
            return None
    def getMonbySkill(self, skill):
        returned_mon_id = []
        for mon in self.data['monsters']:
            
            mon = self.data['monsters'][mon]
            if 'SkillType' not in mon:
                logging.warning("skill type not in mon {}".format(mon['$ID']))
                continue
            if mon['SkillType'].lower() == skill.lower():
                returned_mon_id.append(mon['$ID'])
        if returned_mon_id == []:
            skill = 'mon_'+skill
        for mon in self.data['monsters']:
            mon = self.data['monsters'][mon]
            if 'SkillType' not in mon:
                logging.warning("skill type not in mon {}".format(mon['$ID']))
                continue
            if mon['SkillType'].lower() == skill.lower():
                returned_mon_id.append(mon['$ID'])    
        return returned_mon_id
"""
enums
"""
    
class TOSElement():
    DARK = 'Dark'
    EARTH = 'Earth'
    FIRE = 'Fire'
    HOLY = 'Holy'
    ICE = 'Ice'
    LIGHTNING = 'Lightning'
    MELEE = 'None'
    POISON = 'Poison'
    SOUL = 'Soul'

    @staticmethod
    def to_string(value):
        return {
            TOSElement.DARK: 'Dark',
            TOSElement.EARTH: 'Earth',
            TOSElement.FIRE: 'Fire',
            TOSElement.HOLY: 'Holy',
            TOSElement.ICE: 'Ice',
            TOSElement.LIGHTNING: 'Lightning',
            TOSElement.MELEE: 'None',
            TOSElement.POISON: 'Poison',
            TOSElement.SOUL: 'Soul',
        }[value]

    @staticmethod
    def value_of(string):
        return {
            'DARK': TOSElement.DARK,
            'EARTH': TOSElement.EARTH,
            'FIRE': TOSElement.FIRE,
            'HOLY': TOSElement.HOLY,
            'ICE': TOSElement.ICE,
            'LIGHTING': TOSElement.LIGHTNING,
            'LIGHTNING': TOSElement.LIGHTNING,
            'MELEE': TOSElement.MELEE,
            'POISON': TOSElement.POISON,
            'SOUL': TOSElement.SOUL,
            '': None
        }[string.upper()]


class TOSAttackType():
    BUFF = 'Buff'
    MAGIC = 'Magic'
    MISSILE = 'Missile'
    MISSILE_BOW = 'Bow'
    MISSILE_CANNON = 'Cannon'
    MISSILE_GUN = 'Gun'
    MELEE = 'Physical'
    MELEE_PIERCING = 'Piercing'
    MELEE_SLASH = 'Slash'
    MELEE_STRIKE = 'Strike'
    MELEE_THRUST = 'Thrust'
    TRUE = 'True Damage'
    UNKNOWN = ''
    RESPONSIVE = "Responsive"
    @staticmethod
    def to_string(value):
        return {
            TOSAttackType.BUFF: 'Buff',
            TOSAttackType.MAGIC: 'Magic',
            TOSAttackType.MISSILE: 'Missile',
            TOSAttackType.MISSILE_BOW: 'Bow',
            TOSAttackType.MISSILE_CANNON: 'Cannon',
            TOSAttackType.MISSILE_GUN: 'Gun',
            TOSAttackType.MELEE: 'Physical',
            TOSAttackType.MELEE_PIERCING: 'Piercing',
            TOSAttackType.MELEE_SLASH: 'Slash',
            TOSAttackType.MELEE_STRIKE: 'Strike',
            TOSAttackType.MELEE_THRUST: 'Thrust',
            TOSAttackType.TRUE: 'True Damage',
            TOSAttackType.UNKNOWN: '',
            TOSAttackType.RESPONSIVE: "Responsive",
        }[value]

    @staticmethod
    def value_of(string):
        return {
            'RESPONSIVE' : TOSAttackType.RESPONSIVE, #whats this?
            'ARIES': TOSAttackType.MELEE_PIERCING,
            'ARROW': TOSAttackType.MISSILE_BOW,
            'CANNON': TOSAttackType.MISSILE_CANNON,
            'GUN': TOSAttackType.MISSILE_GUN,
            'HOLY': None,  # HotFix: obsolete skill #40706 uses it
            'MAGIC': TOSAttackType.MAGIC,
            'MELEE': TOSAttackType.MELEE,
            'MISSILE': TOSAttackType.MISSILE,
            'SLASH': TOSAttackType.MELEE_SLASH,
            'STRIKE': TOSAttackType.MELEE_STRIKE,
            'THRUST': TOSAttackType.MELEE_THRUST,
            'TRUEDAMAGE': TOSAttackType.TRUE,
            '': TOSAttackType.UNKNOWN
        }[string.upper()]
