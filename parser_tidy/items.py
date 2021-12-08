# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 11:18:38 2021

@author: Temperantia
"""
import os
from os.path import exists
import logging
from DB import ToS_DB as constants
import csv
import io
import luautil
from math import floor
import xml.etree.ElementTree as ET
# from shared.ipf/item_calculate.lua
EQUIPMENT_STAT_COLUMNS = [
    'MINATK',
    'MAXATK',
    'ADD_MINATK',
    'ADD_MAXATK',
    'ADD_MATK',
    'ADD_DEF',
    'ADD_MDEF',
    'DEF',
    'MDEF',
    'PATK',
    'MATK',
    'CRTHR',
    'CRTATK',
    'CRTDR',
    'HR',
    'DR',
    'ADD_HR',
    'ADD_DR',
    'STR',
    'DEX',
    'CON',
    'INT',
    'MNA',
    'SR',
    'SDR',
    'CRTMATK',
    'MHR',
    'ADD_MHR',
    'MGP',
    'AddSkillMaxR',
    'SkillRange',
    'SkillWidthRange',
    'SkillAngle',
    'BlockRate',
    'BLK',
    'BLK_BREAK',
    'MSPD',
    'KDPow',
    'MHP',
    'MSP',
    'MSTA',
    'RHP',
    'RSP',
    'RSPTIME',
    'RSTA',
    'ADD_CLOTH',
    'ADD_LEATHER',
    'ADD_CHAIN',
    'ADD_IRON',
    'ADD_GHOST',
    'ADD_SMALLSIZE',
    'ADD_MIDDLESIZE',
    'ADD_LARGESIZE',
    'ADD_FORESTER',
    'ADD_WIDLING',
    'ADD_VELIAS',
    'ADD_PARAMUNE',
    'ADD_KLAIDA',
    'Aries',
    'Slash',
    'Strike',
    'AriesDEF',
    'SlashDEF',
    'StrikeDEF',
    'ADD_FIRE',
    'ADD_ICE',
    'ADD_POISON',
    'ADD_LIGHTNING',
    'ADD_SOUL',
    'ADD_EARTH',
    'ADD_HOLY',
    'ADD_DARK',
    'RES_FIRE',
    'RES_ICE',
    'RES_POISON',
    'RES_LIGHTNING',
    'RES_SOUL',
    'RES_EARTH',
    'RES_HOLY',
    'RES_DARK',
    'LootingChance',
    'RareOption_MainWeaponDamageRate',
    'RareOption_MainWeaponDamageRate',
    'RareOption_SubWeaponDamageRate' ,
    'RareOption_BossDamageRate',
    'RareOption_MeleeReducedRate',
    'RareOption_MagicReducedRate',
    'RareOption_PVPDamageRate',
    'RareOption_PVPReducedRate',
    'RareOption_CriticalDamage_Rate',
    'RareOption_CriticalHitRate',
    'RareOption_CriticalDodgeRate',
    'RareOption_HitRate',
    'RareOption_DodgeRate',
    'RareOption_BlockBreakRate',
    'RareOption_BlockRate',
]

equipment_grade_ratios = {}
log = logging.getLogger("parse.items")
log.setLevel("INFO")

goddess_anvil     = [219,219,219,219,219,
                     238,238,238,238,238,
                     256,256,256,256,256,
                     275,275,275,275,275,
                     294,294,294,294,294,
                     294,294,294,294,294,]
goddess_scale     = [3,3,3,3,3,
                     5,5,5,5,5,
                     7,7,7,7,7,
                     8,8,8,8,8,
                     10,11,12,13,14,
                     15,16,17,18,19                    
                     ]
goddess_gabija    = [263,263,263,263,450,
                     450,450,450,450,673,
                     673,673,673,673,927,
                     927,1212,1523,1861,2224,
                     2586,2948,3311,3673,4036,
                     4398,4760,5123,5485,5848]

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
                                          '"' : r'\"',
                                          ',' :r''
                                          
                                          }))
    return escaped
def parse(c = None, from_scratch = True):
       
    if c == None:
        c = constants()
        c.build()
        luautil.init()
    if (from_scratch):
        c.data['items'] = {}
        c.data['items_by_name'] = {}
        c.cubes_by_stringarg = {}
        c.equipment_sets = {}
        
        parse_items(c, "item.ies", '01')
        parse_items(c, 'item_colorspray.ies', '02')
        parse_items(c, 'item_gem.ies', '03')
        parse_items(c, 'item_Equip.ies', '04')
        parse_items(c, 'item_Equip_EP12.ies', '05')
        parse_items(c, 'item_premium.ies', '06')
        parse_items(c, 'item_quest.ies', '07')
        parse_items(c, 'recipe.ies', '08')
        parse_items(c, 'item_EP12.ies', '09')
        parse_items(c, 'item_gem_relic.ies', '10')
        parse_items(c,'item_gem_bernice.ies', '11')
        parse_items(c,'item_GuildHousing.ies','12')
        parse_items(c,'item_PersonalHousing.ies','13')
        parse_items(c,'item_HiddenAbility.ies','14')
        parse_items(c,'item_event.ies', '15') 
    luautil.init(c)
    parse_equipment_grade_ratios(c)
    global equipment_grade_ratios 
    equipment_grade_ratios = c.data['equipment_grade_ratios']
    parse_equips(c, 'item_equip.ies')
    parse_equips(c, 'item_Equip_EP12.ies')
    parse_equips(c, 'item_event_equip.ies')
    parse_equipment_sets('setitem.ies', c)
    parse_links_equipment_sets('setitem.ies',c)

    parse_cards(c)
    parse_cards_battle(c)
    
    parse_links_cubes(c)
    
    parse_links_collections(c)
    
    parse_gems(c)
    
    parse_gems_bonus(c)
    
    parse_links_skills(c)

    parse_links_recipes(c)
    
    parse_books_dialog(c)
    
    

def parse_items(globals, file_name, id_prefix):
    
    
    log.info('Parsing %s...', file_name)
    file_name = file_name.lower()
    ies_path= globals.file_dict[file_name]['path']

    #ies_path = os.path.join(globals.PATH_INPUT_DATA, "ies.ipf", file_name)
    if(not exists(ies_path)):
        log.warning("file not found {}".format(file_name))
        return
   
    ies_file = io.open(ies_path, 'r', encoding="utf-8")
    ies_reader = csv.DictReader(ies_file, delimiter=',', quotechar='"')
    rows = []

    for row in ies_reader:
        
        rows.append(row)
        item_type = row['GroupName'].upper() if 'GroupName' in row else None 
        item_type = row['Category'].upper() if 'Category' in row and row['Category'] != '' else item_type
        item_type_equipment = row['ClassType'] if 'ClassType' in row else None
        item_type_equipment = row['ClassType2'] if 'ClassType' in row and row['ClassType'] == 'NO' and 'ClassType2' in row else item_type_equipment
    

        obj = {}

        obj['$ID'] = str(id_prefix) + str( row['ClassID'])
        obj['$ID_NAME'] = row['ClassName']
        obj['Description'] = globals.translate(row['Desc']) if 'Desc' in row else None
        obj['Icon'] = globals.parse_entity_icon(row['Icon'])
        obj['Name'] = globals.translate(row['Name']) if 'Name' in row else None
        obj['Grade'] = row['ItemGrade']  if 'ItemGrade' in row else 1
        if obj['Grade'] == "":
            obj['Grade'] = 1
        obj['Price'] = row['SellPrice']
        obj['TimeCoolDown'] = float(int(row['ItemCoolDown']) / 1000) if 'ItemCoolDown' in row else None
        obj['TimeLifeTime'] = float(int(row['LifeTime'])) if 'LifeTime' in row else None
        obj['Tradability'] = '%s%s%s%s' % (
            'T' if row['MarketTrade'] == 'YES' else 'F',    # Market
            'T' if row['UserTrade'] == 'YES' else 'F',      # Players
            'T' if row['ShopTrade'] == 'YES' else 'F',      # Shop
            'T' if row['TeamTrade'] == 'YES' else 'F',      # Team Storage
        )
        obj['Type'] = item_type
        if 'Weight' in row :
            obj['Weight'] = float(row['Weight']) 
        else:
            obj['Weight'] = ''
    
        obj['Link_Collections'] = []
        obj['Link_Cubes'] = []
        obj['Link_Maps'] = []
        obj['Link_Maps_Exploration'] = []
        obj['Link_Monsters'] = []
        obj['Link_RecipeTarget'] = []
        obj['Link_RecipeMaterial'] = []
        if item_type == 'CUBE':
            globals.cubes_by_stringarg[row['StringArg']] = obj
        globals.data['items'][obj['$ID']] = obj
        globals.data['items_by_name'] [obj['$ID_NAME']] = obj
    
    
    ies_file.close()
    return globals
   

def parse_equips(globals, filename):
    log = logging.getLogger("parser.equips")
    log.setLevel("INFO")
    log.info('Parsing equipment...')

    ies_path = os.path.join(globals.PATH_INPUT_DATA, 'ies.ipf', filename)
    if(not exists(ies_path)):
       return
    ies_file = io.open(ies_path, 'r', encoding = 'utf-8')
    ies_reader = csv.DictReader(ies_file, delimiter=',', quotechar='"')
    
    if not 'EQUIPMENT' in globals.data['item_type']:
        globals.data['item_type']['EQUIPMENT'] = []
    LUA_RUNTIME = luautil.LUA_RUNTIME
    LUA_SOURCE = luautil.LUA_SOURCE
    rows = []

    for row in ies_reader:
        rows.append(row)
        if str(row['ClassName']) not in globals.data['items_by_name'].keys():
            continue
        if int(row['ItemLv'])>0:
            rows.append(row)
        item_grade = equipment_grade_ratios[int(row['ItemGrade'])]
        item_type_equipment = row['ClassType']
        obj = globals.data['items_by_name'][str(row['ClassName'])]
        
        if obj['$ID_NAME'] not in globals.data['item_type']['EQUIPMENT']:
            globals.data['item_type']['EQUIPMENT'].append(obj['$ID_NAME'])
        obj['Type'] = 'Equipment'
        # Calculate all properties using in-game formulas
        tooltip_script = row['RefreshScp']
        if ('MarketCategory' in row):
            tooltip_script = 'SCR_REFRESH_ACC' if not tooltip_script and 'Accessory_' in row['MarketCategory'] else tooltip_script
            tooltip_script = 'SCR_REFRESH_ARMOR' if not tooltip_script and 'Armor_' in row['MarketCategory'] else tooltip_script
            tooltip_script = 'SCR_REFRESH_HAIRACC' if not tooltip_script and 'HairAcc_' in row['MarketCategory'] else tooltip_script
            tooltip_script = 'SCR_REFRESH_WEAPON' if not tooltip_script and ('Weapon_' in row['MarketCategory'] or 'ChangeEquip_' in row['MarketCategory']) else tooltip_script

        if tooltip_script:
            try:
                LUA_RUNTIME[tooltip_script](row)
            except :
                pass

        # Add additional fields
        obj['AnvilATK'] = []
        obj['AnvilDEF'] = []
        obj['AnvilPrice'] = []
        obj['Bonus'] = []
        obj['Durability'] = int(row['MaxDur']) / 100
        obj['Durability'] = -1 if obj['Durability'] <= 0 else obj['Durability']
        obj['Grade'] = int(row['ItemGrade'])
        if obj['Grade'] == "":
            obj['Grade'] = 1
        obj['Level'] = int(row['ItemLv']) if int(row['ItemLv']) > 0 else int(row['UseLv'])
        obj['Material'] = row['Material']
        obj['Potential'] = int(row['MaxPR'])
        obj['RequiredClass'] = '%s%s%s%s%s' % (
            'T' if any(j in row['UseJob'] for j in ['All', 'Char3']) else 'F',  # Archer
            'T' if any(j in row['UseJob'] for j in ['All', 'Char4']) else 'F',  # Cleric
            'T' if any(j in row['UseJob'] for j in ['All', 'Char5']) else 'F',  # Scout
            'T' if any(j in row['UseJob'] for j in ['All', 'Char1']) else 'F',  # Swordsman
            'T' if any(j in row['UseJob'] for j in ['All', 'Char2']) else 'F',  # Wizard
        )
        obj['RequiredLevel'] = int(row['UseLv'])
        obj['Sockets'] = int(row['BaseSocket'])
        obj['SocketsLimit'] = int(row['MaxSocket_COUNT'])
        obj['Stars'] = int(row['ItemStar'])
        try:
            obj['Stat_ATTACK_MAGICAL'] = int(row['MATK']) 
        except:
            obj['Stat_ATTACK_MAGICAL'] = 0
        try:
            obj['Stat_ATTACK_PHYSICAL_MIN'] = int(row['MINATK']) 
        except:
            obj['Stat_ATTACK_PHYSICAL_MIN'] = 0
        try:
            obj['Stat_ATTACK_PHYSICAL_MAX'] = int(row['MAXATK']) if 'MAXATK' in row and row['MAXATK'] !=None else 0
        except:
            obj['Stat_ATTACK_PHYSICAL_MAX'] = 0
        try:
            obj['Stat_DEFENSE_MAGICAL'] = int(row['MDEF']) if 'MDEF' in row and row['MDEF'] !=None else 0
        except:
            obj['Stat_DEFENSE_MAGICAL'] = 0
        try:
            obj['Stat_DEFENSE_PHYSICAL'] = int(row['DEF']) if 'DEF' in row and row['DEF'] !=None else 00
        except:
            obj['Stat_DEFENSE_PHYSICAL'] = 0
        obj['TranscendPrice'] = []
        obj['TypeAttack'] = row['AttackType']
        obj['TypeEquipment'] = item_type_equipment
        # hair acc 
        if ('ReqToolTip' in row):
            if (row['ReqToolTip'] == '헤어 코스튬1'):
                obj['TypeEquipment'] = 'Hair Acc 1'    
            if (row['ReqToolTip'] == '헤어 코스튬2'):
                obj['TypeEquipment'] = 'Hair Acc 2'    
            if (row['ReqToolTip'] == '헤어 코스튬3'):
                obj['TypeEquipment'] = 'Hair Acc 3'    
        obj['Unidentified'] = int(row['NeedAppraisal']) == 1
        obj['UnidentifiedRandom'] = int(row['NeedRandomOption']) == 1

        obj['Link_Set'] = None

        # HotFix: if it's a Rapier, use THRUST as the TypeAttack
        #if obj['TypeEquipment'] == TOSEquipmentType.RAPIER:
        #    obj['TypeAttack'] = TOSAttackType.MELEE_THRUST

        # HotFix: in case it doesn't give physical nor magical defense (e.g. agny necklace)
        if 'ADD_FIRE' in row['BasicTooltipProp'].split(','):
            lv = obj['Level']
            gradeRatio = (int(item_grade['BasicRatio']) / 100.0)

            row['ADD_FIRE'] = floor(lv * gradeRatio)

        # Anvil
        """
        ===================
        anvil price error
        ===================
        """
        reinf = 'GET_REINFORCE_PRICE'
        if ('GET_REINFORCE_PRICE' not in LUA_RUNTIME) and 'GET_REINFORCE_131014_PRICE' in LUA_RUNTIME:
            reinf = 'GET_REINFORCE_131014_PRICE'
        else:
            reinf = None
        if (obj['Grade'] != 6) and reinf!= None: #goddess!
            if any(prop in row['BasicTooltipProp'] for prop in ['ATK', 'DEF', 'MATK', 'MDEF']):
                for lv in range(40):
                    row['Reinforce_2'] = lv
                    
                    if any(prop in row['BasicTooltipProp'] for prop in ['DEF', 'MDEF']):
                        obj['AnvilDEF'].append(LUA_RUNTIME['GET_REINFORCE_ADD_VALUE'](None, row, 0, 1))
                        if (obj['Grade']<6):
                            obj['AnvilPrice'].append(LUA_RUNTIME[reinf](row, {}, None))
                    if any(prop in row['BasicTooltipProp'] for prop in ['ATK', 'MATK']):
                        obj['AnvilATK'].append(LUA_RUNTIME['GET_REINFORCE_ADD_VALUE_ATK'](row, 0, 1, None))
                        if (obj['Grade']<6):
                            obj['AnvilPrice'].append(LUA_RUNTIME[reinf](row, {}, None))
               
    
            obj['AnvilPrice'] = [value for value in obj['AnvilPrice'] if value > 0]
            obj['AnvilATK'] = [value for value in obj['AnvilATK'] if value > 0] if len(obj['AnvilPrice']) > 0 else None
            obj['AnvilDEF'] = [value for value in obj['AnvilDEF'] if value > 0] if len(obj['AnvilPrice']) > 0 else None
            for lv in range(10):
                row['Transcend'] = lv
                obj['TranscendPrice'].append(LUA_RUNTIME['GET_TRANSCEND_MATERIAL_COUNT'](row, None))

            obj['TranscendPrice'] = [value for value in obj['TranscendPrice'] if value > 0]
           
        # Bonus
        for stat in EQUIPMENT_STAT_COLUMNS:
            if stat in row:
                if row[stat] == None:
                    row[stat] = 0
                value = floor(float(row[stat]))

                if value != 0:
                    obj['Bonus'].append([
                        stat,    # Stat
                        value                               # Value
                    ])

        # More Bonus
        if 'OptDesc' in row and len(row['OptDesc']) > 0:
            for bonus in globals.translate(row['OptDesc']).split('{nl}'):
                bonus = bonus.strip()
                bonus = bonus[bonus.index('-'):] if '-' in bonus else bonus

                obj['Bonus'].append([
                    'UNKNOWN',           # Stat
                    bonus.replace('- ', '').strip()     # Value
                ])

        # Transcendence

        globals.data['items'][obj['$ID']] = obj
        globals.data['items_by_name'] [obj['$ID_NAME']] = obj
    return globals


def parse_equipment_grade_ratios(globals):
    log = logging.getLogger("parser.equips.grade")
    log.setLevel("INFO")
    log.info('Parsing equipment grade...')

    ies_path = os.path.join(globals.PATH_INPUT_DATA, 'ies.ipf', 'item_grade.ies')
    
    ies_file = io.open(ies_path, 'r', encoding = 'utf-8')
    ies_reader = csv.DictReader(ies_file, delimiter=',', quotechar='"')

    for row in ies_reader:
        equipment_grade_ratios[int(row['Grade'])] = row
    globals.data['equipment_grade_ratios'] = equipment_grade_ratios
    ies_file.close()


def parse_equipment_sets(file_name, globals):
    log = logging.getLogger("parser.equips.set")
    log.setLevel("INFO")
    log.info('Parsing equipment sets...')

    ies_path = os.path.join(globals.PATH_INPUT_DATA, 'ies.ipf', file_name)
    if(not exists(ies_path)):
       return
    ies_file = open(ies_path, 'r', encoding = 'utf-8')
    ies_reader = csv.DictReader(ies_file, delimiter=',', quotechar='"')

    for row in ies_reader:
        obj = {}
        obj['$ID'] = str(row['ClassID'])
        obj['$ID_NAME'] = row['ClassName']
        obj['Name'] = globals.translate(row['Name']) if 'Name' in row else None

        obj['Link_Items'] = []

        # Parse bonus
        obj['Bonus2'] = globals.translate(row['EffectDesc_2']) if row['EffectDesc_2'] != '' else None
        obj['Bonus3'] = globals.translate(row['EffectDesc_3']) if row['EffectDesc_3'] != '' else None
        obj['Bonus4'] = globals.translate(row['EffectDesc_4']) if row['EffectDesc_4'] != '' else None
        obj['Bonus5'] = globals.translate(row['EffectDesc_5']) if row['EffectDesc_5'] != '' else None
        obj['Bonus6'] = globals.translate(row['EffectDesc_6']) if row['EffectDesc_6'] != '' else None
        obj['Bonus7'] = globals.translate(row['EffectDesc_7']) if row['EffectDesc_7'] != '' else None

        globals.data['equipment_sets'][obj['$ID']] = obj
        globals.data['equipment_sets_by_name'][obj['$ID_NAME']] = obj
    return globals

def parse_links_equipment_sets(file_name, globals):
    log = logging.getLogger("parser.equips.set.link")
    log.setLevel("INFO")
    log.info('Parsing items for equipment sets: %s...', file_name)

    ies_path = os.path.join(globals.PATH_INPUT_DATA, 'ies.ipf', file_name)
    if(not exists(ies_path)):
       return
    ies_file = open(ies_path, 'r', encoding = 'utf-8')
    ies_reader = csv.DictReader(ies_file, delimiter=',', quotechar='"')

    for row in ies_reader:
        equipment_set = globals.data['equipment_sets_by_name'][row['ClassName']]

        # Parse items
        for i in range(1, 8):
            item_name = row['ItemName_' + str(i)]

            if item_name == '':
                continue
            if (item_name in globals.data['items_by_name'].keys()):
                item = globals.data['items_by_name'][item_name]
            else:
                continue

            
            equipment_set['Link_Items'].append(item['$ID_NAME'])

    ies_file.close()
    

def parse_cards(globals):
    log = logging.getLogger("parser.equips.card")
    log.setLevel("INFO")
    log.info('Parsing cards...')

    ies_path = os.path.join(globals.PATH_INPUT_DATA, 'ies.ipf', 'item.ies')
    if(not exists(ies_path)):
       return
    ies_file = open(ies_path, 'r', encoding = 'utf-8')
    ies_reader = csv.DictReader(ies_file, delimiter=',', quotechar='"')
    if 'CARD' not in globals.data['item_type']:
        globals.data['item_type']['CARD'] = []
    for row in ies_reader:
        if row['GroupName'] != 'Card':
            continue
        
        obj = globals.data['items_by_name'][row['ClassName']]
        globals.data['item_type']['CARD'].append(obj['$ID_NAME'])
        
        obj['Description'] = obj['Description']
        obj['IconTooltip'] = globals.parse_entity_icon(row['TooltipImage'])
        obj['TypeCard'] = row['CardGroupName']
        obj['Type']         = 'CARD'
        globals.data['items'] [obj['$ID']] = obj
        globals.data['items_by_name'] [obj['$ID_NAME']] = obj

    ies_file.close()
    return globals


def parse_cards_battle(globals):
    log = logging.getLogger("parser.equips.card.battle")
    log.setLevel("INFO")
    log.info('Parsing cards battle...')

    ies_path = os.path.join(globals.PATH_INPUT_DATA, 'ies.ipf', 'cardbattle.ies')
    if(not exists(ies_path)):
       return
    ies_file = open(ies_path, 'r', encoding = 'utf-8')
    ies_reader = csv.DictReader(ies_file, delimiter=',', quotechar='"')

    for row in ies_reader:
        obj = globals.data['items_by_name'][row['ClassName']]

        obj['Stat_Height'] = int(row['Height'])
        obj['Stat_Legs'] = int(row['LegCount'])
        obj['Stat_Weight'] = int(row['BodyWeight'])
        globals.data['items'] [obj['$ID']] = obj

    ies_file.close()
    return globals


def parse_links_cubes(globals):
    log = logging.getLogger("parser.cubes")
    log.setLevel("INFO")
    log.info('Parsing items for cubes...')

    ies_path = os.path.join(globals.PATH_INPUT_DATA, 'ies.ipf', 'reward_indun.ies')
    if(not exists(ies_path)):
       return
    ies_file = open(ies_path, 'r', encoding = 'utf-8')
    ies_reader = csv.DictReader(ies_file, delimiter=',', quotechar='"')
    if 'CUBES' not in globals.data['item_type']:
        globals.data['item_type']['CUBES'] = []
    a = []
    for row in ies_reader:
        if row['Group'] not in globals.data['items_by_name']:
            continue
        
        if row['Group'] not in globals.cubes_by_stringarg:
            continue
        a.append(row)
        cube = globals.cubes_by_stringarg[row['Group']]
        globals.data['item_type']['CUBES'].append(cube['$ID_NAME'])
        cube['Type']         = 'Cube'
        if not 'Link_Items' in cube.keys():
            cube['Link_Items'] = []
        try:
            cube['Link_Items'].append(globals.data['items_by_name'][row['ItemName']]['ID_NAME'])
            globals.data['items'] [cube['$ID']] = cube
            globals.data['items_by_name'] [cube['$ID_NAME']] = cube
        except:
            print("key error ... {} for {} cube".format(row['ItemName'], cube['Name']))
    
    ies_file.close()
    return globals


def parse_links_collections(globals):
    log = logging.getLogger("parser.collections")
    log.setLevel("INFO")
    log.info('Parsing items for collections...')
    if 'COLLECTION' not in globals.data['item_type']:
        globals.data['item_type']['COLLECTION'] = []
    ies_path = os.path.join(globals.PATH_INPUT_DATA, 'ies.ipf', 'collection.ies')
    if(not exists(ies_path)):
       return
    ies_file = open(ies_path, 'r', encoding = 'utf-8')
    ies_reader = csv.DictReader(ies_file, delimiter=',', quotechar='"')

    for row in ies_reader:
        if row['ClassName'] not in globals.data['items_by_name']:
            continue

        collection = globals.data['items_by_name'][row['ClassName']]
        globals.data['item_type']['COLLECTION'].append(collection['$ID_NAME'])
        collection['Type']         = 'COLLECTION'
        if not 'Link_Items' in collection.keys():
            collection['Link_Items'] = []
            collection['Bonus'] = []
        # Parse items
        for i in range(1, 10):
            item_name = row['ItemName_' + str(i)]

            if item_name == '':
                continue

            collection['Link_Items'].append(globals.data['items_by_name'][item_name]['$ID_NAME'])

        # Parse bonus
        bonus = row['PropList'].split('/') + row['AccPropList'].split('/')

        for i in bonus:
            if i == '':
                bonus.remove(i)
        if (len(bonus) != 1):
            for i in range(0, len(bonus), 2):
                collection['Bonus'].append([
                    parse_links_items_bonus_stat(bonus[i]),   # Property
                    int(bonus[i + 1])                         # Value
                ])
        globals.data['items'][collection['$ID']] = collection
        globals.data['items_by_name'][collection['$ID_NAME']] = collection
    ies_file.close()
    return globals

def parse_links_items_bonus_stat(stat):
    return {
        'CON_BM': 'CON',
        'DEX_BM': 'DEX',
        'INT_BM': 'INT',
        'MNA_BM': 'SPR',
        'STR_BM': 'STR',

        'CRTATK_BM': 'Critical Attack',
        'CRTMATK_BM': 'Critical Magic Attack',
        'CRTHR_BM': 'Critical Rate',
        'CRTDR_BM': 'Critical Defense',

        'MHP_BM': 'Maximum HP',
        'MSP_BM': 'Maximum SP',
        'RHP_BM': 'HP Recovery',
        'RSP_BM': 'SP Recovery',

        'DEF_BM': 'Defense',
        'MDEF_BM': 'Magic Defense',
        'MATK_BM': 'Magic Attack',
        'PATK_BM': 'Physical Attack',

        'DR_BM': 'Evasion',
        'HR_BM': 'Accuracy',
        'MHR_BM': 'Magic Amplification',  # ???

        'ResDark_BM': 'Dark Property Resistance',
        'ResEarth_BM': 'Earth Property Resistance',
        'ResHoly_BM': 'Holy Property Resistance',

        'MaxSta_BM': 'Stamina',
        'MaxAccountWarehouseCount': 'Team Storage Slots',
        'MaxWeight_Bonus': 'Weight Limit',
        'MaxWeight_BM': 'Weight Limit'
    }[stat]


def parse_gems(globals):
    log = logging.getLogger("parser.gems")
    log.setLevel("INFO")
    log.info('Parsing gems...')

    ies_path = os.path.join(globals.PATH_INPUT_DATA, 'ies.ipf', 'item_gem.ies')
    if(not exists(ies_path)):
       return
    ies_file = open(ies_path, 'r', encoding = 'utf-8')
    ies_reader = csv.DictReader(ies_file, delimiter=',', quotechar='"')
    if 'GEMS' not in globals.data['item_type']:
        globals.data['item_type']['GEMS'] = []
    for row in ies_reader:
        obj = globals.data['items_by_name'][row['ClassName']]
        globals.data['item_type']['GEMS'].append(obj['$ID_NAME'])
        obj['BonusBoots'] = []
        obj['BonusGloves'] = []
        obj['BonusSubWeapon'] = []
        obj['BonusTopAndBottom'] = []
        obj['BonusWeapon'] = []
        obj['TypeGem'] = row['EquipXpGroup']
        globals.data['items_by_name'][row['ClassName']] = obj
        globals.data['items'][obj['$ID']] = obj
    ies_file.close()
    return globals

def parse_gems_bonus(globals):
    log = logging.getLogger("parser.gems.bonus")
    log.setLevel("INFO")
    log.info('Parsing gems bonus...')

    xml_path = os.path.join(globals.PATH_INPUT_DATA, 'xml.ipf', 'socket_property.xml')
    if(not exists(xml_path)):
       return
    xml = ET.parse(xml_path).getroot()

    SLOTS = ['TopLeg', 'HandOrFoot', 'MainOrSubWeapon']

    # example: <Item Name="gem_circle_1">
    for item in xml:
        try:
            gem = globals.data['items_by_name'][item.get('Name')]
        except:
            logging.warning('gem not found {}'.format(item.get('Name')))
            continue

        for level in item:
            if level.get('Level') == '0':
                continue

            for slot in SLOTS:
                bonus = level.get('PropList_' + slot)
                penalty = level.get('PropList_' + slot + '_Penalty')

                for slot in (slot.split('Or') if 'Or' in slot else [slot]): # support for Re:Build 2-in-1 slots
                    for prop in [bonus, penalty]:
                        if prop is not None and prop != 'None':
                            if gem['TypeGem'] == 'Gem_Skill':
                                gem['Bonus' + parse_gems_slot(slot)].append({
                                    'Stat': globals.translate(prop).replace('OptDesc/', '')
                                })
                            elif gem['TypeGem'] == "Gem":
                                prop_slot = prop.split('/')

                                stat ='ADD_' + prop_slot[0]
                                stat = prop_slot[0] if stat is None else stat

                                gem['Bonus' + parse_gems_slot(slot)].append({
                                    'Stat': stat,
                                    'Value': int(prop_slot[1])
                                })
            globals.data['items'][gem['$ID']] = gem


def parse_gems_slot(key):
    return {
        'Foot': 'Boots',
        'Hand': 'Gloves',
        'Main': 'Weapon',
        'SubWeapon': 'SubWeapon',
        'TopLeg': 'TopAndBottom',
        'Weapon': 'Weapon',
    }[key]

def parse_links_skills(globals):
    log = logging.getLogger("parser.gem.link")
    log.setLevel("INFO")
    log.info('Parsing skills for gems...')

    for gem in globals.data['items'].values():
        if gem['Type'] != 'GEM':
            continue
        skill = gem['$ID_NAME'][len('Gem_'):]
        if (skill not in globals.data['skills_by_name']):
            logging.debug('skills missing : %s', skill)
            continue
        skill = globals.data['skills_by_name'][skill]['$ID']
        gem['Link_Skill'] = skill
        globals.data['items'][gem['$ID']] = gem
        


def parse_links_recipes(globals):
    log = logging.getLogger("parser.recipe.link")
    log.setLevel("INFO")
    log.info('Parsing items for recipes...')

    ies_path = os.path.join(globals.PATH_INPUT_DATA, 'ies.ipf', 'recipe.ies')
    if(not exists(ies_path)):
       return
    ies_file = open(ies_path, 'r', encoding = "utf-8")
    ies_reader = csv.DictReader(ies_file, delimiter=',', quotechar='"')
    if 'RECIPES' not in globals.data['item_type']:
         globals.data['item_type']['RECIPES'] = []
    for row in ies_reader:
        recipe = globals.data['items_by_name'][row['ClassName']]
        globals.data['item_type']['RECIPES'].append(recipe['$ID_NAME'])
        if row['TargetItem'] in globals.data['items_by_name'] :
            recipe['Link_Target'] = globals.data['items_by_name'][row['TargetItem']]['$ID_NAME']
        else:
            log.warning('recipe target not found {}'.format( row['TargetItem']))
            continue
        recipe['Name'] = 'Recipe - Unknown'
        recipe['Type'] = "RECIPES"
        if recipe['Link_Target'] is not None:
            recipe['Name'] = 'Recipe - ' + globals.data['items_by_name'][row['TargetItem']]['Name']

        # Parse ingredients
        for i in range(1, 6):
            if row['Item_' + str(i) + '_1'] == '':
                continue

            obj = {}
            if (row['Item_' + str(i) + '_1'] not in globals.data['items_by_name'].keys()):
                logging.warn("missing item {} for recipe {}".format(row['Item_' + str(i) + '_1'], recipe['Name']))
                continue
            
            obj['Item'] = globals.data['items_by_name'][row['Item_' + str(i) + '_1']]['$ID_NAME']
            obj['Quantity'] = int(row['Item_' + str(i) + '_1_Cnt'])
            
            if 'Link_Materials' not in recipe.keys():
                recipe['Link_Materials'] = []
                
            recipe['Link_Materials'].append(obj)
            
        globals.data['items'][recipe['$ID']] = recipe
    ies_file.close()

def parse_gem_bernice(globals):
    file = 'item_gem_relic.ies'
    logging.debug('Parsing bernice gems (ep13)...')
    
    ies_path = os.path.join(globals.PATH_INPUT_DATA, 'ies.ipf',file)
    ies_file = open(ies_path, 'r', encoding = 'utf-8')
    ies_reader = csv.DictReader(ies_file, delimiter=',', quotechar='"')
    rows = []
    for row in ies_reader:
        rows.append(row)
    ies_file.close()
    return globals


def parse_books_dialog(globals):
    logging.debug('Parsing books dialog...')

    ies_path = os.path.join(globals.PATH_INPUT_DATA, 'ies_client.ipf', 'dialogtext.ies')
    if(not exists(ies_path)):
       return
    ies_file = io.open(ies_path, 'r', encoding = 'utf-8')
    ies_reader = csv.DictReader(ies_file, delimiter=',', quotechar='"')
    b = []
    if 'BOOKS' not in globals.data['item_type']:
        globals.data['item_type']['BOOKS'] = []
    for row in ies_reader:
        if row['ClassName'] not in globals.data['items_by_name']:
            continue
        book = globals.data['items_by_name'][row['ClassName']]
        globals.data['item_type']['BOOKS'].append(book['$ID_NAME'])
        if 'Text' not in book:
            book['Text'] = None
        
        book['Text'] = globals.translate(row['Text'])
        b.append(book)
        globals.data['items'][book['$ID']] = book
        globals.data['items_by_name'][book['$ID_NAME']] = book
    
    ies_file.close()
