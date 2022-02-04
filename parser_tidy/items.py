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
import parse_xac
# from shared.ipf/item_calculate.lua
EQUIPMENT_STAT_COLUMNS = []

equipment_grade_ratios = {}
goddess_atk_list       = {}

log = logging.getLogger("parse.items")
log.setLevel("INFO")

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
        c.build("jtos")
        luautil.init(c)
    if (from_scratch):
        c.data['items'] = {}
        c.data['items_by_name'] = {}
        c.cubes_by_stringarg = {}
        c.equipment_sets = {}
        item_ies = c.ITEM_IES
        for i in item_ies:
            parse_items(c, i )
    
    luautil.init(c)
    equipment_ies = c.EQUIPMENT_IES
    global EQUIPMENT_STAT_COLUMNS
    a = luautil.LUA_RUNTIME['GET_COMMON_PROP_LIST']()
    EQUIPMENT_STAT_COLUMNS =[a[i] for i in a]
    
    parse_equipment_grade_ratios(c)
    global equipment_grade_ratios        
    equipment_grade_ratios = c.data['equipment_grade_ratios']
    
    
    parse_goddess_reinf(c)
    
    
    for i in equipment_ies:    
        parse_equips(c, i)
    
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
    
    

def parse_items(constants, file_name):
    
    
    log.info('Parsing %s...', file_name)
    file_name = file_name.lower()
    try:
        ies_path= constants.file_dict[file_name]['path']
    except:
        return

    #ies_path = os.path.join(constants.PATH_INPUT_DATA, "ies.ipf", file_name)
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

        obj['$ID'] = str( row['ClassID'])
        obj['$ID_NAME'] = row['ClassName']
        obj['Description'] = constants.translate(row['Desc']) if 'Desc' in row else None
        obj['Icon'] = constants.parse_entity_icon(row['Icon'])
        obj['Name'] = constants.translate(row['Name']) if 'Name' in row else None
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
            constants.cubes_by_stringarg[row['StringArg']] = obj
        constants.data['items'][obj['$ID']] = obj
        constants.data['items_by_name'] [obj['$ID_NAME']] = obj
    
    
    ies_file.close()
    return constants
   

def parse_equips(constants, filename):
    log = logging.getLogger("parser.equips")
    log.setLevel("INFO")
    log.info('Parsing equipment %s ...'%(filename))
    try:
        ies_path =  constants.file_dict[filename.lower()]['path']
    except:
        logging.warning("file not found {}".format(filename))
        return
    
    #ies_path = os.path.join(constants.PATH_INPUT_DATA, 'ies.ipf', filename)
    #if(not exists(ies_path)):
    #   return
    ies_file = io.open(ies_path, 'r', encoding = 'utf-8')
    ies_reader = csv.DictReader(ies_file, delimiter=',', quotechar='"')
    
    if not 'EQUIPMENT' in constants.data['item_type']:
        constants.data['item_type']['EQUIPMENT'] = []
    LUA_RUNTIME = luautil.LUA_RUNTIME
    LUA_SOURCE = luautil.LUA_SOURCE
    rows = []
    objs = []
    types = []
    for row in ies_reader:
      
        if str(row['ClassName']) not in constants.data['items_by_name'].keys():
            continue
            
        item_grade = equipment_grade_ratios[int(row['ItemGrade'])]
        item_type_equipment = row['ClassType']
        types.append(row['ClassType'])
        rows.append(row)
        #continue
        obj = constants.data['items_by_name'][str(row['ClassName'])]
        
        if obj['$ID_NAME'] not in constants.data['item_type']['EQUIPMENT']:
            constants.data['item_type']['EQUIPMENT'].append(obj['$ID_NAME'])
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
        
        
        matk = ['staff', 'rod']
       
        if obj['Grade'] == 6:
            if int(row['UseLv']) in goddess_atk_list:
                
                if tooltip_script == 'SCR_REFRESH_ACC' :
                    atk = goddess_atk_list[int(row['UseLv'])]['BasicAccAtk']
                    obj['Stat_ATTACK_MAGICAL']      = atk
                    obj['Stat_ATTACK_PHYSICAL_MIN'] = atk
                    obj['Stat_ATTACK_PHYSICAL_MAX'] = atk
                        
                        
                #if tooltip_script == 'SCR_REFRESH_ARMOR':
                #    pass
                    
                #if tooltip_script == 'SCR_REFRESH_WEAPON':
                #    

            
        
        
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
        reinf = 'GET_REINFORCE_PRICE'
        if ('GET_REINFORCE_PRICE' not in LUA_RUNTIME) and 'GET_REINFORCE_131014_PRICE' in LUA_RUNTIME:
            reinf = 'GET_REINFORCE_131014_PRICE'
        if (obj['Grade'] != 6) and reinf!= None: #goddess!
            if any(prop in row['BasicTooltipProp'] for prop in ['ATK', 'DEF', 'MATK', 'MDEF']):
                for lv in range(40):
                    row['Reinforce_2'] = lv
                    if any(prop in row['BasicTooltipProp'] for prop in ['DEF', 'MDEF']):
                        obj['AnvilDEF'].append(LUA_RUNTIME['GET_REINFORCE_ADD_VALUE'](None, row, 0, 1))
                        obj['AnvilPrice'].append(LUA_RUNTIME[reinf](row, {}, None))
                    if any(prop in row['BasicTooltipProp'] for prop in ['ATK', 'MATK']):
                        obj['AnvilATK'].append(LUA_RUNTIME['GET_REINFORCE_ADD_VALUE_ATK'](row, 0, 1, None))
                        obj['AnvilPrice'].append(LUA_RUNTIME[reinf](row, {}, None))
               
    
            obj['AnvilPrice'] = [int(value) for value in obj['AnvilPrice'] if value > 0]
            obj['AnvilATK'] = [int(value) for value in obj['AnvilATK'] if value > 0] if len(obj['AnvilPrice']) > 0 else None
            obj['AnvilDEF'] = [int(value) for value in obj['AnvilDEF'] if value > 0] if len(obj['AnvilPrice']) > 0 else None
        # try:
        lua = luautil.lua
        obj['TranscendPrice'] = []
        for lv in range(10):
            row['Transcend'] = 0
            obj['TranscendPrice'].append(LUA_RUNTIME['GET_TRANSCEND_MATERIAL_COUNT'](row, lv))
        #somehow it wont contain tc 10 =w=
        if (obj['Grade'] == 6):
            obj['TranscendPrice'].append(lua.execute('return get_TC_goddess')(int(row['UseLv']), row['ClassType'], 0,10))
        
        
        try:
            obj['TranscendPrice'] = [floor(value) for value in obj['TranscendPrice'] if value > 0]
        except:
            #goddess
            a = [dict(table)['Premium_item_transcendence_Stone'] for table in 
                 obj['TranscendPrice'][1:] ]
            obj['TranscendPrice'] = [0] + a + [20]
        
           
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
            for bonus in constants.translate(row['OptDesc']).split('{nl}'):
                bonus = bonus.strip()
                bonus = bonus[bonus.index('-'):] if '-' in bonus else bonus

                obj['Bonus'].append([
                    'UNKNOWN',           # Stat
                    bonus.replace('- ', '').strip()     # Value
                ])

        # Transcendence
        """
        try:
            obj['FileName'] = row['FileName']
            obj['row'] = row
        except:
            obj['FileName'] = ''
        """
        obj['model'] = parse_xac.eq_model_name(row,constants)
        constants.data['items'][obj['$ID']] = obj
        constants.data['items_by_name'] [obj['$ID_NAME']] = obj
        rows.append(row)
        objs.append(obj)
    return constants


def parse_goddess_reinf(constants):
    files = constants.EQUIPMENT_REINFORCE_IES
    global goddess_atk_list
    for i in files:
        
        if i not in constants.file_dict:
            continue
        ies_path = constants.file_dict[i]['path']
        ies_file = io.open(ies_path, 'r', encoding = 'utf-8')
        ies_reader = csv.DictReader(ies_file, delimiter=',', quotechar='"')
        rows = []
        for row in ies_reader:
            rows.append(row)
        row = rows[0]
        goddess_atk_list[files[i]] = row
        
        

def parse_equipment_grade_ratios(constants):
    log = logging.getLogger("parser.equips.grade")
    log.setLevel("INFO")
    log.info('Parsing equipment grade...')

    ies_path = os.path.join(constants.PATH_INPUT_DATA, 'ies.ipf', 'item_grade.ies')
    
    ies_file = io.open(ies_path, 'r', encoding = 'utf-8')
    ies_reader = csv.DictReader(ies_file, delimiter=',', quotechar='"')

    for row in ies_reader:
        equipment_grade_ratios[int(row['Grade'])] = row
    constants.data['equipment_grade_ratios'] = equipment_grade_ratios
    ies_file.close()


def parse_equipment_sets(file_name, constants):
    log = logging.getLogger("parser.equips.set")
    log.setLevel("INFO")
    log.info('Parsing equipment sets...')

    ies_path = os.path.join(constants.PATH_INPUT_DATA, 'ies.ipf', file_name)
    if(not exists(ies_path)):
       return
    ies_file = open(ies_path, 'r', encoding = 'utf-8')
    ies_reader = csv.DictReader(ies_file, delimiter=',', quotechar='"')

    for row in ies_reader:
        obj = {}
        obj['$ID'] = str(row['ClassID'])
        obj['$ID_NAME'] = row['ClassName']
        obj['Name'] = constants.translate(row['Name']) if 'Name' in row else None

        obj['Link_Items'] = []

        # Parse bonus
        obj['Bonus2'] = constants.translate(row['EffectDesc_2']) if row['EffectDesc_2'] != '' else None
        obj['Bonus3'] = constants.translate(row['EffectDesc_3']) if row['EffectDesc_3'] != '' else None
        obj['Bonus4'] = constants.translate(row['EffectDesc_4']) if row['EffectDesc_4'] != '' else None
        obj['Bonus5'] = constants.translate(row['EffectDesc_5']) if row['EffectDesc_5'] != '' else None
        obj['Bonus6'] = constants.translate(row['EffectDesc_6']) if row['EffectDesc_6'] != '' else None
        obj['Bonus7'] = constants.translate(row['EffectDesc_7']) if row['EffectDesc_7'] != '' else None

        constants.data['equipment_sets'][obj['$ID']] = obj
        constants.data['equipment_sets_by_name'][obj['$ID_NAME']] = obj
    return constants

def parse_links_equipment_sets(file_name, constants):
    log = logging.getLogger("parser.equips.set.link")
    log.setLevel("INFO")
    log.info('Parsing items for equipment sets: %s...', file_name)

    ies_path = os.path.join(constants.PATH_INPUT_DATA, 'ies.ipf', file_name)
    if(not exists(ies_path)):
       return
    ies_file = open(ies_path, 'r', encoding = 'utf-8')
    ies_reader = csv.DictReader(ies_file, delimiter=',', quotechar='"')

    for row in ies_reader:
        equipment_set = constants.data['equipment_sets_by_name'][row['ClassName']]

        # Parse items
        for i in range(1, 8):
            item_name = row['ItemName_' + str(i)]

            if item_name == '':
                continue
            if (item_name in constants.data['items_by_name'].keys()):
                item = constants.data['items_by_name'][item_name]
            else:
                continue

            
            equipment_set['Link_Items'].append(item['$ID_NAME'])

    ies_file.close()
    

def parse_cards(constants):
    log = logging.getLogger("parser.equips.card")
    log.setLevel("INFO")
    log.info('Parsing cards...')

    ies_path = os.path.join(constants.PATH_INPUT_DATA, 'ies.ipf', 'item.ies')
    if(not exists(ies_path)):
       return
    ies_file = open(ies_path, 'r', encoding = 'utf-8')
    ies_reader = csv.DictReader(ies_file, delimiter=',', quotechar='"')
    if 'CARD' not in constants.data['item_type']:
        constants.data['item_type']['CARD'] = []
    for row in ies_reader:
        if row['GroupName'] != 'Card':
            continue
        
        obj = constants.data['items_by_name'][row['ClassName']]
        constants.data['item_type']['CARD'].append(obj['$ID_NAME'])
        
        obj['Description'] = obj['Description']
        obj['IconTooltip'] = constants.parse_entity_icon(row['TooltipImage'])
        obj['TypeCard'] = row['CardGroupName']
        obj['Type']         = 'CARD'
        constants.data['items'] [obj['$ID']] = obj
        constants.data['items_by_name'] [obj['$ID_NAME']] = obj

    ies_file.close()
    return constants


def parse_cards_battle(constants):
    log = logging.getLogger("parser.equips.card.battle")
    log.setLevel("INFO")
    log.info('Parsing cards battle...')

    ies_path = os.path.join(constants.PATH_INPUT_DATA, 'ies.ipf', 'cardbattle.ies')
    if(not exists(ies_path)):
       return
    ies_file = open(ies_path, 'r', encoding = 'utf-8')
    ies_reader = csv.DictReader(ies_file, delimiter=',', quotechar='"')

    for row in ies_reader:
        obj = constants.data['items_by_name'][row['ClassName']]

        obj['Stat_Height'] = int(row['Height'])
        obj['Stat_Legs'] = int(row['LegCount'])
        obj['Stat_Weight'] = int(row['BodyWeight'])
        constants.data['items'] [obj['$ID']] = obj

    ies_file.close()
    return constants


def parse_links_cubes(constants):
    log = logging.getLogger("parser.cubes")
    log.setLevel("INFO")
    log.info('Parsing items for cubes...')

    ies_path = os.path.join(constants.PATH_INPUT_DATA, 'ies.ipf', 'reward_indun.ies')
    if(not exists(ies_path)):
       return
    ies_file = open(ies_path, 'r', encoding = 'utf-8')
    ies_reader = csv.DictReader(ies_file, delimiter=',', quotechar='"')
    if 'CUBES' not in constants.data['item_type']:
        constants.data['item_type']['CUBES'] = []
    a = []
    for row in ies_reader:
        if row['Group'] not in constants.data['items_by_name']:
            continue
        
        if row['Group'] not in constants.cubes_by_stringarg:
            continue
        a.append(row)
        cube = constants.cubes_by_stringarg[row['Group']]
        constants.data['item_type']['CUBES'].append(cube['$ID_NAME'])
        cube['Type']         = 'Cube'
        if not 'Link_Items' in cube.keys():
            cube['Link_Items'] = []
        try:
            cube['Link_Items'].append(constants.data['items_by_name'][row['ItemName']]['ID_NAME'])
            constants.data['items'] [cube['$ID']] = cube
            constants.data['items_by_name'] [cube['$ID_NAME']] = cube
        except:
            print("key error ... {} for {} cube".format(row['ItemName'], cube['Name']))
    
    ies_file.close()
    return constants


def parse_links_collections(constants):
    log = logging.getLogger("parser.collections")
    log.setLevel("INFO")
    log.info('Parsing items for collections...')
    if 'COLLECTION' not in constants.data['item_type']:
        constants.data['item_type']['COLLECTION'] = []
    ies_path = os.path.join(constants.PATH_INPUT_DATA, 'ies.ipf', 'collection.ies')
    if(not exists(ies_path)):
       return
    ies_file = open(ies_path, 'r', encoding = 'utf-8')
    ies_reader = csv.DictReader(ies_file, delimiter=',', quotechar='"')

    for row in ies_reader:
        if row['ClassName'] not in constants.data['items_by_name']:
            continue

        collection = constants.data['items_by_name'][row['ClassName']]
        constants.data['item_type']['COLLECTION'].append(collection['$ID_NAME'])
        collection['Type']         = 'COLLECTION'
        if not 'Link_Items' in collection.keys():
            collection['Link_Items'] = []
            collection['Bonus'] = []
        # Parse items
        for i in range(1, 10):
            item_name = row['ItemName_' + str(i)]

            if item_name == '':
                continue

            collection['Link_Items'].append(constants.data['items_by_name'][item_name]['$ID_NAME'])

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
        constants.data['items'][collection['$ID']] = collection
        constants.data['items_by_name'][collection['$ID_NAME']] = collection
    ies_file.close()
    return constants

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


def parse_gems(constants):
    log = logging.getLogger("parser.gems")
    log.setLevel("INFO")
    log.info('Parsing gems...')

    ies_path = os.path.join(constants.PATH_INPUT_DATA, 'ies.ipf', 'item_gem.ies')
    if(not exists(ies_path)):
       return
    ies_file = open(ies_path, 'r', encoding = 'utf-8')
    ies_reader = csv.DictReader(ies_file, delimiter=',', quotechar='"')
    if 'GEMS' not in constants.data['item_type']:
        constants.data['item_type']['GEMS'] = []
    for row in ies_reader:
        obj = constants.data['items_by_name'][row['ClassName']]
        constants.data['item_type']['GEMS'].append(obj['$ID_NAME'])
        obj['BonusBoots'] = []
        obj['BonusGloves'] = []
        obj['BonusSubWeapon'] = []
        obj['BonusTopAndBottom'] = []
        obj['BonusWeapon'] = []
        obj['TypeGem'] = row['EquipXpGroup']
        constants.data['items_by_name'][row['ClassName']] = obj
        constants.data['items'][obj['$ID']] = obj
    ies_file.close()
    return constants

def parse_gems_bonus(constants):
    log = logging.getLogger("parser.gems.bonus")
    log.setLevel("INFO")
    log.info('Parsing gems bonus...')

    xml_path = os.path.join(constants.PATH_INPUT_DATA, 'xml.ipf', 'socket_property.xml')
    if(not exists(xml_path)):
       return
    xml = ET.parse(xml_path).getroot()

    SLOTS = ['TopLeg', 'HandOrFoot', 'MainOrSubWeapon']

    # example: <Item Name="gem_circle_1">
    for item in xml:
        try:
            gem = constants.data['items_by_name'][item.get('Name')]
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
                                    'Stat': constants.translate(prop).replace('OptDesc/', '')
                                })
                            elif gem['TypeGem'] == "Gem":
                                prop_slot = prop.split('/')

                                stat ='ADD_' + prop_slot[0]
                                stat = prop_slot[0] if stat is None else stat

                                gem['Bonus' + parse_gems_slot(slot)].append({
                                    'Stat': stat,
                                    'Value': int(prop_slot[1])
                                })
            constants.data['items'][gem['$ID']] = gem


def parse_gems_slot(key):
    return {
        'Foot': 'Boots',
        'Hand': 'Gloves',
        'Main': 'Weapon',
        'SubWeapon': 'SubWeapon',
        'TopLeg': 'TopAndBottom',
        'Weapon': 'Weapon',
    }[key]

def parse_links_skills(constants):
    log = logging.getLogger("parser.gem.link")
    log.setLevel("INFO")
    log.info('Parsing skills for gems...')

    for gem in constants.data['items'].values():
        if gem['Type'] != 'GEM':
            continue
        skill = gem['$ID_NAME'][len('Gem_'):]
        if (skill not in constants.data['skills_by_name']):
            logging.debug('skills missing : %s', skill)
            continue
        skill = constants.data['skills_by_name'][skill]['$ID']
        gem['Link_Skill'] = skill
        constants.data['items'][gem['$ID']] = gem
        


def parse_links_recipes(constants):
    log = logging.getLogger("parser.recipe.link")
    log.setLevel("INFO")
    log.info('Parsing items for recipes...')

    ies_path = os.path.join(constants.PATH_INPUT_DATA, 'ies.ipf', 'recipe.ies')
    if(not exists(ies_path)):
       return
    ies_file = open(ies_path, 'r', encoding = "utf-8")
    ies_reader = csv.DictReader(ies_file, delimiter=',', quotechar='"')
    if 'RECIPES' not in constants.data['item_type']:
         constants.data['item_type']['RECIPES'] = []
    for row in ies_reader:
        recipe = constants.data['items_by_name'][row['ClassName']]
        constants.data['item_type']['RECIPES'].append(recipe['$ID_NAME'])
        if row['TargetItem'] in constants.data['items_by_name'] :
            recipe['Link_Target'] = constants.data['items_by_name'][row['TargetItem']]['$ID_NAME']
        else:
            log.warning('recipe target not found {}'.format( row['TargetItem']))
            continue
        recipe['Name'] = 'Recipe - Unknown'
        recipe['Type'] = "RECIPES"
        if recipe['Link_Target'] is not None:
            recipe['Name'] = 'Recipe - ' + constants.data['items_by_name'][row['TargetItem']]['Name']

        # Parse ingredients
        for i in range(1, 6):
            if row['Item_' + str(i) + '_1'] == '':
                continue

            obj = {}
            if (row['Item_' + str(i) + '_1'] not in constants.data['items_by_name'].keys()):
                logging.warn("missing item {} for recipe {}".format(row['Item_' + str(i) + '_1'], recipe['Name']))
                continue
            
            obj['Item'] = constants.data['items_by_name'][row['Item_' + str(i) + '_1']]['$ID_NAME']
            obj['Quantity'] = int(row['Item_' + str(i) + '_1_Cnt'])
            
            if 'Link_Materials' not in recipe.keys():
                recipe['Link_Materials'] = []
                
            recipe['Link_Materials'].append(obj)
            
        constants.data['items'][recipe['$ID']] = recipe
    ies_file.close()

def parse_gem_bernice(constants):
    file = 'item_gem_relic.ies'
    logging.debug('Parsing bernice gems (ep13)...')
    
    ies_path = os.path.join(constants.PATH_INPUT_DATA, 'ies.ipf',file)
    ies_file = open(ies_path, 'r', encoding = 'utf-8')
    ies_reader = csv.DictReader(ies_file, delimiter=',', quotechar='"')
    rows = []
    for row in ies_reader:
        rows.append(row)
    ies_file.close()
    return constants


def parse_books_dialog(constants):
    logging.debug('Parsing books dialog...')

    ies_path = os.path.join(constants.PATH_INPUT_DATA, 'ies_client.ipf', 'dialogtext.ies')
    if(not exists(ies_path)):
       return
    ies_file = io.open(ies_path, 'r', encoding = 'utf-8')
    ies_reader = csv.DictReader(ies_file, delimiter=',', quotechar='"')
    b = []
    if 'BOOKS' not in constants.data['item_type']:
        constants.data['item_type']['BOOKS'] = []
    for row in ies_reader:
        if row['ClassName'] not in constants.data['items_by_name']:
            continue
        book = constants.data['items_by_name'][row['ClassName']]
        constants.data['item_type']['BOOKS'].append(book['$ID_NAME'])
        if 'Text' not in book:
            book['Text'] = None
        
        book['Text'] = constants.translate(row['Text'])
        b.append(book)
        constants.data['items'][book['$ID']] = book
        constants.data['items_by_name'][book['$ID_NAME']] = book
    
    ies_file.close()

def parse_goddess_EQ(c):
    LUA_RUNTIME = luautil.LUA_RUNTIME
    LUA_SOURCE = luautil.LUA_SOURCE
    func_list = {'setting_lv470_material_acc' : 470 ,
                 'setting_lv470_material_armor' : 470,
                 'setting_lv460_material' : 460,
                 }
    #mat_list_by_lv[460][1][seasonCoin]
    #mat_list_by_lv[lv]['armor'][1][seasonCoin] = 263
    mat  = {
            460: { i : {} for i in range(1, 31) },
            470: {
                'acc' : {i : {} for i in range(1, 31) },
                'armor': {i : {} for i in range(1, 31) }
                }
        }
    for func in func_list:
        lv = func_list[func]
        if func not in LUA_RUNTIME:
            continue
        LUA_RUNTIME[func](mat)
    a = mat[460] 
    mat[460]  = {'armor' : a}
    c.data['goddess_reinf_mat'] = mat
    
    ies_list = {'item_goddess_reinforce.ies' : 460, 
                'item_goddess_reinforce_470.ies' : 470}
    objs = {}
    for ies in ies_list:
        file_name = ies.lower()
        try:
            ies_path= c.file_dict[file_name]['path']
        except:
            continue
        ies_file = io.open(ies_path, 'r', encoding="utf-8")
        ies_reader = csv.DictReader(ies_file, delimiter=',', quotechar='"')
        obj  = []
        for row in ies_reader:
            obj.append(row)
        objs[ies_list[ies]] = obj
        c.data['goddess_reinf'][ies_list[ies]] = obj
    
    
    
