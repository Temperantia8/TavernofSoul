# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 08:55:17 2021

@author: CPPG02619
"""

import csv
import logging
import math
import os
import re
import io
from os.path import exists
from DB import ToS_DB as constants
from DB import TOSElement, TOSAttackType
import luautil

EFFECT_DEPRECATE = {
    'SkillAtkAdd': 'SkillFactor'
}

EFFECTS = []
class TOSRequiredStanceCompanion():
    BOTH = 0
    NO = 1
    SELF = 2
    YES = 3

    @staticmethod
    def value_of(string):
        return {
            'BOTH': TOSRequiredStanceCompanion.BOTH,
            '': TOSRequiredStanceCompanion.NO,
            'SELF': TOSRequiredStanceCompanion.SELF,
            'YES': TOSRequiredStanceCompanion.YES,
        }[string.upper()]


def parse(c = None):
    
    is_rebuild = True
    if c == None:
        c = constants()
        c.build('ktest')
        luautil.init(c)
    c.skills={}
    c.skills_by_name={}
    parse_skills(is_rebuild,c)
    parse_skills_overheats(c)
    parse_skills_simony(c)
    # parse_skills_stances(c)
    parse_links_jobs(c)
    parse_skills_script(c)
    


def parse_skills(is_rebuild, globals):
    logging.debug('Parsing skills...')

    LUA_RUNTIME = luautil.LUA_RUNTIME
    LUA_SOURCE = luautil.LUA_SOURCE

    ies_path = os.path.join(globals.PATH_INPUT_DATA, 'ies.ipf', 'skill.ies')
    ies_path = globals.file_dict['skill.ies']['path']
    if(not exists(ies_path)):
       return
    rows = []
    with io.open(ies_path, 'r', encoding = 'utf-8') as ies_file:
        for row in csv.DictReader(ies_file, delimiter=',', quotechar='"'):
            # Ignore 'Common_' skills (e.g. Bokor's Summon abilities)
            if row['ClassName'].find('Common_') == 0:
                continue
            rows.append(row)
            obj = {}
            obj['$ID'] = row['ClassID']
            obj['$ID_NAME'] = row['ClassName']
            obj['Description'] = globals.translate(row['Caption'])
            obj['Icon'] = globals.parse_entity_icon(row['Icon'])
            obj['Name'] = globals.translate(row['Name'])

            obj['Effect'] = globals.translate(row['Caption2'])
            obj['Element'] = TOSElement.value_of(row['Attribute'])
            obj['IsShinobi'] = row['CoolDown'] == 'SCR_GET_SKL_COOLDOWN_BUNSIN' or (row['CoolDown'] and 'Bunshin_Debuff' in LUA_SOURCE[row['CoolDown']])
            obj['OverHeat'] = {
                'Value': int(row['SklUseOverHeat']),
                'Group': row['OverHeatGroup']
            } if not is_rebuild else int(row['SklUseOverHeat'])  # Re:Build overheat is now simpler to calculate
            obj['BasicCoolDown'] = int(row['BasicCoolDown'])
            obj['BasicPoison'] = int(row['BasicPoison'])
            obj['BasicSP'] = int(math.floor(float(row['BasicSP'])))
            obj['LvUpSpendPoison'] = int(row['LvUpSpendPoison'])
            obj['LvUpSpendSp'] = float(row['LvUpSpendSp'])
            obj['SklAtkAdd'] = float(row['SklAtkAdd'])
            obj['SklAtkAddByLevel'] = float(row['SklAtkAddByLevel'])
            obj['SklFactor'] = float(row['SklFactor'])
            obj['SklFactorByLevel'] = float(row['SklFactorByLevel'])
            obj['SklSR'] = float(row['SklSR'])
            obj['SpendItemBaseCount'] = int(row['SpendItemBaseCount'])
            obj['RequiredStance'] = row['ReqStance']
            obj['RequiredStanceCompanion'] = row['EnableCompanion']

            obj['CoolDown'] = row['CoolDown']
            obj['IsEnchanter'] = False
            obj['IsPardoner'] = False
            obj['IsRunecaster'] = False
            obj['MaxLevel'] = -1
            obj['UnlockClassLevel'] = -1
            obj['SP'] = None
            obj['TypeAttack'] = []
            obj['Link_Attributes'] = []
            obj['Link_Gem'] = None
            obj['Link_Job'] = None
            obj['other'] = []
            # Parse TypeAttack
            if row['ValueType'] == 'Buff':
                obj['TypeAttack'].append(TOSAttackType.BUFF)
            if row['ClassType'] is not None:
                obj['TypeAttack'].append(TOSAttackType.value_of(row['ClassType']))
            if row['AttackType'] is not None:
                obj['TypeAttack'].append(TOSAttackType.value_of(row['AttackType']))

            obj['TypeAttack'] = list(set(obj['TypeAttack']))
            obj['TypeAttack'] = [attack for attack in obj['TypeAttack'] if attack is not None and attack != TOSAttackType.UNKNOWN]

            # Add missing Description header
            if not re.match(r'{#.+}{ol}(\[.+?\]){\/}{\/}{nl}', obj['Description']):
                header = ['[' + TOSAttackType.to_string(attack) + ']' for attack in obj['TypeAttack']]

                if obj['Element'] != TOSElement.MELEE:
                    header.append('[' + TOSElement.to_string(obj['Element']) + ']')


            # Parse effects
            for effect in re.findall(r'{(.*?)}', obj['Effect']):
                if effect in EFFECT_DEPRECATE:
                    # Hotfix: sometimes IMC changes which effects are used, however they forgot to properly communicate to the translation team.
                    # This code is responsible for fixing that and warning so the in-game translations can be fixed
                    logging.warning('[%32s] Deprecated effect [%s] in Effect', obj['$ID_NAME'], effect)

                    effect_deprecate = effect
                    effect = EFFECT_DEPRECATE[effect]

                    obj['Effect'] = re.sub(r'\b' + re.escape(effect_deprecate) + r'\b', effect, obj['Effect'])

                if effect in row:
                    key = 'Effect_' + effect

                    # HotFix: make sure all skills have the same Effect columns (1/2)
                    if key not in EFFECTS:
                        EFFECTS.append('Effect_' + effect)

                    if row[effect] != 'ZERO':
                        obj[key] = row[effect]

                    else:
                        # Hotfix: similar to the hotfix above
                        logging.warning('[%32s] Deprecated effect [%s] in Effect', obj['$ID_NAME'], effect)
                        obj[key] = None
                else:
                    continue

            # Parse formulas
            if row['CoolDown']:
                obj['CoolDown'] = row['CoolDown']
                #obj['CoolDown'] = parse_skills_lua_source(row['CoolDown'])
                #obj['CoolDown'] = parse_skills_lua_source_to_javascript(row, obj['CoolDown'])
            if row['SpendSP']:
                obj['SP'] = row['SpendSP']
                #obj['SP'] = parse_skills_lua_source(row['SpendSP'])
                #obj['SP'] = parse_skills_lua_source_to_javascript(row, obj['SP'])

            globals.data['skills'][obj['$ID']] = obj
            globals.data['skills_by_name'][obj['$ID_NAME']] = obj

    # HotFix: make sure all skills have the same Effect columns (2/2)
    for skill in globals.data['skills'].values():
        for effect in EFFECTS:
            if effect not in skill:
                skill[effect] = None



def parse_skills_overheats( globals):
    logging.debug('Parsing skills overheats...')
    ies_path = os.path.join(globals.PATH_INPUT_DATA, 'ies.ipf', 'cooldown.ies')
    ies_path = globals.file_dict['cooldown.ies']['path']
    if(not exists(ies_path)):
       return
    with io.open(ies_path, 'r', encoding = 'utf-8') as ies_file:
        for row in csv.DictReader(ies_file, delimiter=',', quotechar='"'):
            # We're only interested in overheats
            if row['IsOverHeat'] != 'YES':
                continue
            skill = None
            for obj in globals.data['skills'].values():
                if isinstance(obj['OverHeat'], (dict,)) and row['ClassName'] == obj['OverHeat']['Group']:
                    skill = obj
                    break
            # If skill isn't available, ignore
            if skill is None:
                continue
            skill['OverHeat'] = int(row['MaxOverTime']) / skill['OverHeat']['Value'] if skill['OverHeat']['Value'] > 0 else 0
    # Clear skills with no OverHeat information
    for skill in globals.data['skills'].values():
        if isinstance(skill['OverHeat'], (dict,)):
            skill['OverHeat'] = 0


def parse_skills_simony(globals):
    logging.debug('Parsing skills simony...')

    ies_path = os.path.join(globals.PATH_INPUT_DATA, 'ies.ipf', 'skill_simony.ies')
    if(not exists(ies_path)):
       return
    with io.open(ies_path, 'r', encoding = 'utf-8') as ies_file:
        for row in csv.DictReader(ies_file, delimiter=',', quotechar='"'):
            if row['ClassID'] not in globals.data['skills']:
                logging.error('Unknown skill: {}'.format( row['ClassID']))
                continue

            skill = globals.data['skills'][row['ClassID']]
            skill['IsEnchanter'] = True
            skill['IsPardoner'] = True
            skill['IsRunecaster'] = True


def parse_skills_stances(globals):
    logging.debug('Parsing skills stances...')

    stance_list = []
    ies_path = os.path.join(globals.PATH_INPUT_DATA, 'ies.ipf', 'stance.ies')
    ies_path = globals.file_dict[ 'stance.ies']['path']
    if(not exists(ies_path)):
       return
    # Parse stances
    with io.open(ies_path, 'r', encoding = 'utf-8') as ies_file:
        for row in csv.DictReader(ies_file, delimiter=',', quotechar='"'):
            stance_list.append(row)

    # Add stances to skills
    # from addon.ipf\skilltree\skilltree.lua :: MAKE_STANCE_ICON
    for skill in globals.data['skills'].values():
        stances_main_weapon = []
        stances_sub_weapon = []

        if skill['RequiredStance']:
            for stance in stance_list:
             

               
                if skill['RequiredStance'] == 'TwoHandBow' and stance['ClassName'] == 'Bow':
                    continue
                if 'Artefact' in stance['Name']:
                    continue

                if stance['UseSubWeapon'] == 'NO':
                    stances_main_weapon.append({
                        'Icon': globals.parse_entity_icon(stance['Icon']),
                        'Name': stance['ClassName']
                    })
                else:
                    found = False
                    for stance_sub in stances_sub_weapon:
                        if stance_sub['Icon'] == globals.parse_entity_icon(stance['Icon']):
                            found = True
                            break

                    if not found:
                        stances_sub_weapon.append({
                            'Icon': globals.parse_entity_icon(stance['Icon']),
                            'Name': stance['ClassName']
                        })
        else:
            stances_main_weapon.append({
                'Icon': globals.parse_entity_icon('weapon_All'),
                'Name': 'All'
            })

        if skill['RequiredStanceCompanion'] in [TOSRequiredStanceCompanion.BOTH, TOSRequiredStanceCompanion.YES]:
            stances_main_weapon.append({
                'Icon': globals.parse_entity_icon('weapon_companion'),
                'Name': 'Companion'
            })

        skill['RequiredStance'] = [
            stance for stance in (stances_main_weapon + stances_sub_weapon)
            if stance['Icon'] is not None
        ]

def parse_skills_script(globals):
    """
    parse skills skill factor caption ratio etc which use lua script
    """
    
    LUA_RUNTIME = luautil.LUA_RUNTIME
    LUA_SOURCE = luautil.LUA_SOURCE

    for g in globals.data['skills'].values():
        sfrs = []
        g['other'] = []
        CaptionRatios = []
        if (g['Effect_SkillFactor']):
            for lv in range(0,g['MaxLevel']+10,1):
                g['Level'] = lv
                sfr = LUA_RUNTIME[g['Effect_SkillFactor']](g) 
                if sfr == -1:
                    sfr = 0
                sfrs.append(sfr)
            g['sfr'] = sfrs
            
        if g['Effect_CaptionRatio']:
            if ( g['Effect_CaptionRatio'] == 'SCR_GET_SwellHands_Ratio'):
                g['other'].append("Effect_CaptionRatio ((maxpatk + minpatk)/2) * (0.02 + skill.Level * 0.002)")
                continue
            if ( g['Effect_CaptionRatio'] == 'SCR_GET_OverReinforce_Ratio'):
                g['other'].append("Effect_CaptionRatio ((maxpatk + minpatk)/2) * (0.015 + skill.Level * 0.004)")
                continue
            for lv in range(0,g['MaxLevel']+10,1):
                g['Level'] = lv
                CaptionRatio = LUA_RUNTIME[g['Effect_CaptionRatio']](g) 
                if CaptionRatio == -1:
                    CaptionRatio = 0
                CaptionRatios.append(CaptionRatio)
            g['CaptionRatio'] = CaptionRatios
        
        CaptionRatios = []
        if g['Effect_CaptionRatio2']:
            if ( g['Effect_CaptionRatio2'] == 'SCR_GET_Sanctuary_Ratio2'):
                g['other'].append("Effect_CaptionRatio2 mdefRate = MDEF * (0.1 * skill.Level)")
                continue
            if ( g['Effect_CaptionRatio2'] == 'SCR_GET_Ayin_sof_Ratio2'):
                g['other'].append("Effect_CaptionRatio2 Hp recovery")
                continue
            for lv in range(0,g['MaxLevel']+10,1):
                g['Level'] = lv
                CaptionRatio = LUA_RUNTIME[g['Effect_CaptionRatio2']](g) 
                if CaptionRatio == -1:
                    CaptionRatio = 0
                CaptionRatios.append(CaptionRatio)
            g['CaptionRatio2'] = CaptionRatios
            
        CaptionRatios = []
        if g['Effect_CaptionRatio3']:
            for lv in range(0,g['MaxLevel']+10,1):
                g['Level'] = lv
                CaptionRatio = LUA_RUNTIME[g['Effect_CaptionRatio3']](g) 
                if CaptionRatio == -1:
                    CaptionRatio = 0
                CaptionRatios.append(CaptionRatio)
            g['CaptionRatio3'] = CaptionRatios

        CaptionRatios = []
        if g['Effect_CaptionTime']:
            for lv in range(0,g['MaxLevel']+10,1):
                g['Level'] = lv
                CaptionRatio = LUA_RUNTIME[g['Effect_CaptionTime']](g) 
                if CaptionRatio == -1:
                    CaptionRatio = 0
                CaptionRatios.append(CaptionRatio)
            g['CaptionTime'] = CaptionRatios
        
        CaptionRatios = []
        if g['Effect_SkillSR']:
            for lv in range(0,g['MaxLevel']+10,1):
                g['Level'] = lv
                CaptionRatio = LUA_RUNTIME[g['Effect_SkillSR']](g) 
                if CaptionRatio == -1:
                    CaptionRatio = 0
                CaptionRatios.append(CaptionRatio)
            g['SkillSR'] = CaptionRatios
        
        CaptionRatios = []
        if g['Effect_SpendItemCount']:
            for lv in range(0,g['MaxLevel']+10,1):
                g['Level'] = lv
                CaptionRatio = LUA_RUNTIME[g['Effect_SpendItemCount']](g) 
                if CaptionRatio == -1:
                    CaptionRatio = 0
                CaptionRatios.append(CaptionRatio)
            g['SpendItemCount'] = CaptionRatios
        
        CaptionRatios = []
        if g['Effect_SpendPoison']:
            for lv in range(0,g['MaxLevel']+10,1):
                g['Level'] = lv
                CaptionRatio = LUA_RUNTIME[g['Effect_SpendPoison']](g) 
                if CaptionRatio == -1:
                    CaptionRatio = 0
                CaptionRatios.append(CaptionRatio)
            g['SpendPoison'] = CaptionRatios
            
        CaptionRatios = []
        if g['Effect_SpendSP']:
            for lv in range(0,g['MaxLevel']+10,1):
                g['Level'] = lv
                CaptionRatio = LUA_RUNTIME[g['Effect_SpendSP']](g) 
                if CaptionRatio == -1:
                    CaptionRatio = 0
                CaptionRatios.append(CaptionRatio)
            g['SpendSP'] = CaptionRatios
        Cooldown = []
        #blacklist_cd = ['SCR_GET_SKL_COOLDOWN_WIZARD', 'SCR_GET_SKL_COOLDOWN','SCR_GET_SKL_COOLDOWN_ADD_LEVEL_BYGEM' ]
        if g['CoolDown']:
            for lv in range(0,g['MaxLevel']+10,1):
                #if (g['CoolDown'].upper() in blacklist_cd):
                #    Cooldown.append(g['BasicCoolDown'])
                #    continue
                g['Level'] = lv
                cd = LUA_RUNTIME[g['CoolDown']](g) 
                if cd < 0:
                    cd = 0
                Cooldown.append(cd)
            g['CoolDown'] = Cooldown
        globals.data['skills_by_name'][g['$ID']] = g
            

def parse_links(c = None):
    if c == None:
        c = constants()
        c.build(constants.iTOS)
    parse_links_gems(c)
    c = parse_links_jobs(True,c)

def parse_links_gems(globals):
    logging.debug('Parsing gems for skills...')
    
    ies_path = os.path.join(globals.PATH_INPUT_DATA, 'ies.ipf', 'item_gem.ies')
    ies_path = globals.file_dict[ 'item_gem.ies']['path']
    with io.open(ies_path, 'r', encoding = 'utf-8') as ies_file:
        for row in csv.DictReader(ies_file, delimiter=',', quotechar='"'):
            skill = row['ClassName'][len('Gem_'):]

            if skill not in globals.data['skills_by_name']:
                continue

            skill = globals.data['skills_by_name'][skill]
            skill['Link_Gem'] = globals.get_gem_link(row['ClassName'])


def parse_links_jobs(globals):
    logging.debug('Parsing jobs for skills...')
    ies_path = os.path.join(globals.PATH_INPUT_DATA, 'ies.ipf', 'skilltree.ies')
    ies_path = globals.file_dict[ 'skilltree.ies']['path']

    z = []
    with io.open(ies_path, 'r', encoding = 'utf-8') as ies_file:
        for row in csv.DictReader(ies_file, delimiter=',', quotechar='"'):
            z.append(row)
            # Ignore discarded skills
            if row['SkillName'] not in globals.data['skills_by_name']:
                continue

            skill = globals.data['skills_by_name'][row['SkillName']]
            skill['MaxLevel'] = int(row['MaxLevel'])
            skill['LevelPerGrade'] = int(row['LevelPerGrade']) if 'LevelPerGrade' in row else 0
            skill['UnlockClassLevel'] = int(row['UnlockClassLevel']) if 'UnlockClassLevel' in row else 0
            skill['UnlockGrade'] = int(row['UnlockGrade']) if 'UnlockGrade' in row else 0

            job = '_'.join(row['ClassName'].split('_')[:2])       
            skill['Link_Job'] = globals.data['jobs_by_name'][job]['$ID']
            globals.data['skills_by_name'][row['SkillName']] = skill
            globals.data['skills'][skill['$ID']] = skill
    return globals


def parse_clean(globals):
    skills_to_remove = []
    # Find which skills are no longer active
    for skill in globals.data['skills'].values():
        if skill['Link_Job'] is None:
            skills_to_remove.append(skill)

    # Remove all inactive skills
    for skill in skills_to_remove:
        del globals.data['skills'][str(skill['$ID'])]
        del globals.data['skills_by_name'][skill['$ID_NAME']]

        skill_id = skill['$ID']

        for attribute in globals.data['attributes'].values():
            attr = globals.data['attributes_by_name'][attribute['$ID_NAME']]
            attribute['Link_Skills'] = [link for link in attribute['Link_Skills'] if link != skill_id]
            attr['Link_Skills'] = [link for link in attr['Link_Skills'] if link != skill_id]
        for job in globals.data['jobs'].values():
            job2= globals.data['jobs_by_name'][job['$ID_NAME']]
            job['Link_Skills'] = [link for link in job['Link_Skills'] if link != skill_id]
            job2['Link_Skills'] = [link for link in job2['Link_Skills'] if link != skill_id]
    
  