# -*- coding: utf-8 -*-
"""
Created on Sun Oct  3 20:11:07 2021

@author: Intel

"""

import csv
import logging
import os
import glob
from os.path import exists
from DB import ToS_DB as constants
import luautil


log = logging.getLogger("parse.monsters")
log.setLevel("INFO")
class TOSMonsterRace():
    BEAST = 0
    DEMON = 1
    INSECT = 2
    ITEM = 3
    MUTANT = 4
    PLANT = 5
    VELNAIS = 6

    @staticmethod
    def value_of(string):
        try:
            return {
                'WIDLING': 'BEAST',
                'VELNIAS': 'DEMON',
                'KLAIDA': 'INSECT',
                'ITEM': 'ITEM',
                'PARAMUNE': 'MUTANT',
                'FORESTER': 'PLANT',
                'VELNAIS': 'VELNAIS',
                '': ''
            }[string.upper()]
        except:
            return string.upper()



statbase_monster = {}
statbase_monster_type = {}

statbase_monster_race = {}
monster_const={}


def parse(c = None):
    if (c==None):
        c= constants()
        c.build()
        luautil.init()
    parse_monsters_statbase('statbase_monster.ies', statbase_monster,c)
    parse_monsters_statbase('monster_const.ies', monster_const,c)
    parse_monsters_statbase('statbase_monster_type.ies', statbase_monster_type,c)
    parse_monsters_statbase('statbase_monster_race.ies', statbase_monster_race,c)

    parse_monsters('monster.ies', c)
    parse_monsters('monster_event.ies', c)
    parse_monsters('monster_npc.ies', c)
    parse_monsters('Monster_solo_dungeon.ies',c)
    parse_monsters('monster_pcsummon.ies',c)
    parse_monsters('monster_pet.ies',c)
    parse_monsters('Monster_BountyHunt.ies',c)
    parse_monsters('monster_guild.ies',c)
    parse_monsters('monster_mgame.ies',c)
    return c
    

def parse_monsters(file_name, constants):
    
    
    log.info('Parsing %s...', file_name)

    LUA_RUNTIME = luautil.LUA_RUNTIME
    LUA_SOURCE = luautil.LUA_SOURCE

    #ies_path = os.path.join(constants.PATH_INPUT_DATA, "ies.ipf", file_name)
    ies_path = constants.file_dict[file_name.lower()]['path']
    if not exists(ies_path):
        log.warning("file not found {}".format(ies_path))
        return 
    ies_file = open(ies_path, 'r', encoding="utf-8")
    ies_reader = csv.DictReader(ies_file, delimiter=',', quotechar='"')
    for row in ies_reader:
        #logging.debug('Parsing monster: %s :: %s', row['ClassID'], row['ClassName'])

        # HotFix: these properties need to be calculated before the remaining ones
        row['Lv'] = int(row['Level']) if int(row['Level']) > 1 else 1

        # injection constants
        for k, v in monster_const[1].items():
            if (k != "ClassID" and k != "Lv"):
                if v in LUA_RUNTIME and LUA_RUNTIME[v] is not None:
                    row[k] = LUA_RUNTIME[v](row)
                else:
                    if k not in row:
                        row[k] = v
        #2pass
        for k, v in monster_const[1].items():
            if (k!="ClassID"and k!="Lv") :
                if v in LUA_RUNTIME and LUA_RUNTIME[v] is not None:
                    row[k] = LUA_RUNTIME[v](row)
                else:
                    if  k not in row:
                        row[k]=v


        # row['CON'] = LUA_RUNTIME['SCR_Get_MON_CON'](row)
        # row['DEX'] = LUA_RUNTIME['SCR_Get_MON_DEX'](row)
        # row['INT'] = LUA_RUNTIME['SCR_Get_MON_INT'](row)
        # row['MNA'] = LUA_RUNTIME['SCR_Get_MON_MNA'](row)
        # row['STR'] = LUA_RUNTIME['SCR_Get_MON_STR'](row)

        obj = {}
        obj['$ID'] = int(row['ClassID'])
        obj['$ID_NAME'] = row['ClassName']
        obj['Description'] = constants.translate(row['Desc'])
        obj['Icon'] = constants.parse_entity_icon(row['Icon']) if row['Icon'] != 'ui_CreateMonster' else None
        obj['Name'] = constants.translate(row['Name'])
        obj['Type'] = row['GroupName']
        obj['SkillType'] = row['SkillType']
        if obj['Type'] == 'Monster':
            obj['Armor'] = row['ArmorMaterial'] if row['ArmorMaterial'] != 'Iron' else 'Plate'
            obj['Element'] = row['Attribute']
            obj['Level'] = int(row['Lv'])
            obj['Race'] = TOSMonsterRace.value_of(row['RaceType'])
            obj['Rank'] = row['MonRank']
            obj['Size'] = row['Size'] if row['Size'] else None
            obj['EXP'] = int(LUA_RUNTIME['SCR_GET_MON_EXP'](row)) if obj['Level'] < 999 else 0
            obj['EXPClass'] = int(LUA_RUNTIME['SCR_GET_MON_JOBEXP'](row)) if obj['Level'] < 999 else 0
            obj['Stat_CON'] = int(row['CON'])
            obj['Stat_DEX'] = int(row['DEX'])
            obj['Stat_INT'] = int(row['INT'])
            obj['Stat_SPR'] = int(row['MNA'])
            obj['Stat_STR'] = int(row['STR'])
            obj['Stat_HP'] = int(row['MHP'])
            obj['Stat_SP'] = int(row['MSP'])
            obj['Stat_ATTACK_MAGICAL_MAX'] =int(row['MAXMATK'])
            obj['Stat_ATTACK_MAGICAL_MIN'] =int(row['MINMATK'])
            obj['Stat_ATTACK_PHYSICAL_MAX'] = int(row['MAXPATK'])
            obj['Stat_ATTACK_PHYSICAL_MIN'] = int(row['MINPATK'])
            obj['Stat_DEFENSE_MAGICAL'] = int(row['MDEF'])
            obj['Stat_DEFENSE_PHYSICAL'] = int(row['DEF'])
            obj['Stat_Accuracy'] = int(LUA_RUNTIME['SCR_Get_MON_HR'](row))
            obj['Stat_Evasion'] = int(LUA_RUNTIME['SCR_Get_MON_DR'](row))
            obj['Stat_CriticalDamage'] = int(LUA_RUNTIME['SCR_Get_MON_CRTATK'](row))
            obj['Stat_CriticalDefense'] = int(LUA_RUNTIME['SCR_Get_MON_CRTDR'](row))
            obj['Stat_CriticalRate'] = int(LUA_RUNTIME['SCR_Get_MON_CRTHR'](row))
            obj['Stat_BlockRate'] = int(LUA_RUNTIME['SCR_Get_MON_BLK'](row))
            obj['Stat_BlockPenetration'] = int(LUA_RUNTIME['SCR_Get_MON_BLK_BREAK'](row))
            
            obj['Link_Items'] = []
            obj['Link_Maps'] = []
            constants.data['monsters'][obj['$ID']] = obj
            constants.data['monsters_by_name'][obj['$ID_NAME']] = obj
        elif obj['Type'] == 'NPC':
            obj['Icon'] = constants.parse_entity_icon(row['MinimapIcon']) if row['MinimapIcon'] else obj['Icon']

            constants.data['npcs'][obj['$ID']] = obj
            constants.data['npcs_by_name'][obj['$ID_NAME']] = obj
    ies_file.close()
    return constants


def parse_monsters_statbase(file_name, destination,constants):
    logging.debug('Parsing %s...', file_name)

    #ies_path = os.path.join(constants.PATH_INPUT_DATA, "ies.ipf", file_name)
    ies_path = constants.file_dict[file_name.lower()]['path']
    ies_file = open(ies_path, 'r', encoding = 'utf-8')
    ies_reader = csv.DictReader(ies_file, delimiter=',', quotechar='"')

    for row in ies_reader:
        destination[int(row['ClassID'])] = row

    ies_file.close()


def parse_links(c=None):
    if (c==None):
        c = constants()
        c.build()
    c.data['item_monster'] = []
    parse_links_items(c)


def parse_links_items(constants):
    logging.debug('Parsing Monsters <> Items...')

    for monster in constants.data['monsters'].values():
        #mongen_dir = os.listdir(os.path.join(constants.PATH_INPUT_DATA, 'ies_drop.ipf'))
        ies_drop = os.path.join("..", "itos_unpack", 'ies_drop.ipf')
        mongen_dir = os.listdir(ies_drop)
        path_insensitive= {}
        for item in mongen_dir:
            path_insensitive[item.lower()] = item
            
            
        ies_file = monster['$ID_NAME'] + '.ies'
        try:
            ies_file = path_insensitive[ies_file.lower()]
        except:
            #logging.warning("file not found {}".format(ies_file))
            pass
        
        ies_path = os.path.join(ies_drop, ies_file)

        try:
            with open(ies_path, 'r', encoding="utf-8") as ies_file:
                for row in csv.DictReader(ies_file, delimiter=',', quotechar='"'):
                    if not row['ItemClassName'] or row['ItemClassName'] not in constants.data['items_by_name']:
                        continue

                    item = constants.data['items_by_name'][row['ItemClassName']]
                    item_link = item['$ID']
                    monster_link = monster['$ID']
                    constants.data['item_monster'].append({
                        'Chance'        : int(row['DropRatio']) / 100.0,
                        'Item'          : item_link,
                        'Monster'       : monster_link,
                        'Quantity_MAX'  : int(row['Money_Max']),
                        'Quantity_MIN'  : int(row['Money_Min']),
                    })

        except IOError:
            continue


def parse_skill_mon(constants):
    xml_skills = constants.data['xml_skills']
    logging.debug('Parsing Monsters <> Skills...')
    ies_file = 'skill_mon.ies'
    #ies_path = os.path.join(constants.PATH_INPUT_DATA, 'ies.ipf', ies_file)
    ies_path = constants.file_dict[ies_file.lower()]['path']
    if (not exists(ies_path)):
        log.warning("file not found {}".format(ies_path))
        return False
    
    with open(ies_path, 'r', encoding="utf-8") as ies_file:
        rows = []
        skill_mon = {}
        for row in csv.DictReader(ies_file, delimiter=',', quotechar='"'):
            rows.append(row)
            skill               = {}
            skill['$ID']        = row['ClassID']
            skill['$ID_NAME']   = row['ClassName']
            skill['CD']         = row['BasicCoolDown'] if 'BasicCoolDown' in row else 0
            skill['Name']       = constants.translate(row['Name'])
            skill['SFR']        = row['SklFactor'] if 'SklFactor' in row else 0
            skill['Attribute']  = row['Attribute']
            skill['HitCount']   = row['SklHitCount']
            skill['AAR']        = row['SklSR']
            mon                 = row['ClassName'].split('_')
            mon_s               = ''
            skill['TargetBuffs']= []
            skill['SelfBuffs']  = []

            if len(mon)>=2 and (mon[-2].lower() == "skill" or mon[-2].lower() =='attack'):
                mon = mon[:-1]
            for i in mon[1:-1]:
                mon_s += i+"_"
            mon_s = mon_s[:-1]
        
            skill['Monster']    = constants.getMonbySkill(mon_s)
            
            
            
            if row['ClassName'] in xml_skills:
                data                    =xml_skills[row['ClassName']]
                skill['TargetBuffs']    = data['TargetBuffs']
            
            if (skill['Monster']  == []):
                logging.debug("monster {} (for skill) not found ({})".format(mon_s,row['ClassName'] ))
                continue
            skill_mon[row['ClassID']]  = skill


        constants.data['skill_mon'] = skill_mon         
        
