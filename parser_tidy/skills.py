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
    


def parse_skills(is_rebuild, constants):
    logging.debug('Parsing skills...')

    LUA_RUNTIME = luautil.LUA_RUNTIME
    LUA_SOURCE = luautil.LUA_SOURCE

    ies_path = os.path.join(constants.PATH_INPUT_DATA, 'ies.ipf', 'skill.ies')
    ies_path = constants.file_dict['skill.ies']['path']
    if(not exists(ies_path)):
       return
    rows = []
    with io.open(ies_path, 'r', encoding = 'utf-8') as ies_file:
        for row in csv.DictReader(ies_file, delimiter=',', quotechar='"'):
            # Ignore 'Common_' skills (e.g. Bokor's Summon abilities)
            if row['ClassName'].find('Common_') == 0:
                continue
            rows.append(row)
            obj                 = {}
            obj['$ID']          = row['ClassID']
            obj['$ID_NAME']     = row['ClassName']
            obj['Description']  = constants.translate(row['Caption'])
            obj['Icon']         = constants.parse_entity_icon(row['Icon'])
            obj['Name']         = constants.translate(row['Name'])

            obj['Effect']       = constants.translate(row['Caption2'])
            obj['Element']      = TOSElement.value_of(row['Attribute'])
            obj['IsShinobi']    = row['CoolDown'] == 'SCR_GET_SKL_COOLDOWN_BUNSIN' or (row['CoolDown'] and 'Bunshin_Debuff' in LUA_SOURCE[row['CoolDown']])
            obj['OverHeat']     = {
                'Value': int(row['SklUseOverHeat']),
                'Group': row['OverHeatGroup']
            } if not is_rebuild else int(row['SklUseOverHeat'])  # Re:Build overheat is now simpler to calculate
            obj['BasicCoolDown'] = int(row['BasicCoolDown'])
            obj['BasicPoison']  = int(row['BasicPoison'])
            obj['BasicSP']      = int(math.floor(float(row['BasicSP'])))
            obj['LvUpSpendPoison'] = int(row['LvUpSpendPoison'])
            obj['LvUpSpendSp']  = float(row['LvUpSpendSp'])
            obj['SklAtkAdd']    = float(row['SklAtkAdd'])
            obj['SklAtkAddByLevel'] = float(row['SklAtkAddByLevel'])
            obj['SklFactor']    = float(row['SklFactor'])
            obj['SklFactorByLevel'] = float(row['SklFactorByLevel'])
            obj['SklSR']        = float(row['SklSR'])
            obj['SpendItemBaseCount'] = int(row['SpendItemBaseCount'])
            obj['RequiredStance'] = row['ReqStance']
            obj['RequiredStanceCompanion'] = row['EnableCompanion']
            obj['Keyword']      = row['Keyword']
            obj['CoolDown']     = row['CoolDown']
            obj['IsEnchanter']  = False
            obj['IsPardoner']   = False
            obj['IsRunecaster'] = False
            obj['MaxLevel']     = -1
            obj['UnlockClassLevel'] = -1
            obj['SP']           = None
            obj['TypeAttack']   = []
            obj['Link_Attributes'] = []
            obj['Link_Gem']     = None
            obj['Link_Job']     = None
            obj['other']        = []
            obj['TargetBuffs']  = []
            if row['ClassName'] in constants.data['xml_skills']:
                data                    = constants.data['xml_skills'][row['ClassName']]
                obj['TargetBuffs']      = data['TargetBuffs']


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
            if row['SpendSP']:
                obj['SP'] = row['SpendSP']

            constants.data['skills'][obj['$ID']] = obj
            constants.data['skills_by_name'][obj['$ID_NAME']] = obj

    # HotFix: make sure all skills have the same Effect columns (2/2)
    for skill in constants.data['skills'].values():
        for effect in EFFECTS:
            if effect not in skill:
                skill[effect] = None



def parse_skills_overheats( constants):
    logging.debug('Parsing skills overheats...')
    ies_path = os.path.join(constants.PATH_INPUT_DATA, 'ies.ipf', 'cooldown.ies')
    ies_path = constants.file_dict['cooldown.ies']['path']
    if(not exists(ies_path)):
       return
    with io.open(ies_path, 'r', encoding = 'utf-8') as ies_file:
        for row in csv.DictReader(ies_file, delimiter=',', quotechar='"'):
            # We're only interested in overheats
            if row['IsOverHeat'] != 'YES':
                continue
            skill = None
            for obj in constants.data['skills'].values():
                if isinstance(obj['OverHeat'], (dict,)) and row['ClassName'] == obj['OverHeat']['Group']:
                    skill = obj
                    break
            # If skill isn't available, ignore
            if skill is None:
                continue
            skill['OverHeat'] = int(row['MaxOverTime']) / skill['OverHeat']['Value'] if skill['OverHeat']['Value'] > 0 else 0
    # Clear skills with no OverHeat information
    for skill in constants.data['skills'].values():
        if isinstance(skill['OverHeat'], (dict,)):
            skill['OverHeat'] = 0


def parse_skills_simony(constants):
    logging.debug('Parsing skills simony...')

    ies_path = os.path.join(constants.PATH_INPUT_DATA, 'ies.ipf', 'skill_simony.ies')
    if(not exists(ies_path)):
       return
    with io.open(ies_path, 'r', encoding = 'utf-8') as ies_file:
        for row in csv.DictReader(ies_file, delimiter=',', quotechar='"'):
            if row['ClassID'] not in constants.data['skills']:
                logging.error('Unknown skill: {}'.format( row['ClassID']))
                continue

            skill = constants.data['skills'][row['ClassID']]
            skill['IsEnchanter'] = True
            skill['IsPardoner'] = True
            skill['IsRunecaster'] = True


def parse_skills_stances(constants):
    logging.debug('Parsing skills stances...')

    stance_list = []
    ies_path = os.path.join(constants.PATH_INPUT_DATA, 'ies.ipf', 'stance.ies')
    ies_path = constants.file_dict[ 'stance.ies']['path']
    if(not exists(ies_path)):
       return
    # Parse stances
    with io.open(ies_path, 'r', encoding = 'utf-8') as ies_file:
        for row in csv.DictReader(ies_file, delimiter=',', quotechar='"'):
            stance_list.append(row)

    # Add stances to skills
    # from addon.ipf\skilltree\skilltree.lua :: MAKE_STANCE_ICON
    for skill in constants.data['skills'].values():
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
                        'Icon': constants.parse_entity_icon(stance['Icon']),
                        'Name': stance['ClassName']
                    })
                else:
                    found = False
                    for stance_sub in stances_sub_weapon:
                        if stance_sub['Icon'] == constants.parse_entity_icon(stance['Icon']):
                            found = True
                            break

                    if not found:
                        stances_sub_weapon.append({
                            'Icon': constants.parse_entity_icon(stance['Icon']),
                            'Name': stance['ClassName']
                        })
        else:
            stances_main_weapon.append({
                'Icon': constants.parse_entity_icon('weapon_All'),
                'Name': 'All'
            })

        if skill['RequiredStanceCompanion'] in [TOSRequiredStanceCompanion.BOTH, TOSRequiredStanceCompanion.YES]:
            stances_main_weapon.append({
                'Icon': constants.parse_entity_icon('weapon_companion'),
                'Name': 'Companion'
            })

        skill['RequiredStance'] = [
            stance for stance in (stances_main_weapon + stances_sub_weapon)
            if stance['Icon'] is not None
        ]

def run_lua(skill, key_special, key_dict):
    LUA_RUNTIME = luautil.LUA_RUNTIME
    LUA_SOURCE = luautil.LUA_SOURCE
    var = []
    if (skill[key_special]):
        if (skill['MaxLevel']==-1):
            skill[key_dict] = []
            return
        try:
            for lv in range(0,skill['MaxLevel']+10,1):
                skill['Level'] = lv
                row = LUA_RUNTIME[skill[key_special]](skill) 
                if row == -1:
                    row = 0
                elif (math.isnan(row) ):
                    row = 0
                var.append(row)
            skill[key_dict] = var
        except:
            skill[key_dict] = []


def parse_skills_script(constants):
    """
    parse skills skill factor caption ratio etc which use lua script
    """
    key_dict = [
        'sfr', 'CaptionRatio', 'CaptionRatio2', 'CaptionRatio3',
        'CaptionTime', 'SkillSR', 'SpendItemCount' ,
        'SpendPoison', 'SpendSP' , 'CoolDown'
    ]
    key_special = [
        'Effect_SkillFactor', 'Effect_CaptionRatio','Effect_CaptionRatio2', 'Effect_CaptionRatio3',
        'Effect_CaptionTime', 'Effect_SkillSR', 'Effect_SpendItemCount', 'Effect_SpendPoison',
        'Effect_SpendSP', 'CoolDown'
    ]

    for g in constants.data['skills'].values():
        for i in range(len(key_dict)):
            try:
                run_lua(g,key_special[i], key_dict[i])
            except:
               pass

            

def parse_links(c = None):
    if c == None:
        c = constants()
        c.build(constants.iTOS)
    parse_links_gems(c)
    c = parse_links_jobs(True,c)

def parse_links_gems(constants):
    logging.debug('Parsing gems for skills...')
    
    ies_path = os.path.join(constants.PATH_INPUT_DATA, 'ies.ipf', 'item_gem.ies')
    ies_path = constants.file_dict[ 'item_gem.ies']['path']
    with io.open(ies_path, 'r', encoding = 'utf-8') as ies_file:
        for row in csv.DictReader(ies_file, delimiter=',', quotechar='"'):
            skill = row['ClassName'][len('Gem_'):]

            if skill not in constants.data['skills_by_name']:
                continue

            skill = constants.data['skills_by_name'][skill]
            skill['Link_Gem'] = constants.get_gem_link(row['ClassName'])


def parse_links_jobs(constants):
    logging.debug('Parsing jobs for skills...')
    ies_path = os.path.join(constants.PATH_INPUT_DATA, 'ies.ipf', 'skilltree.ies')
    ies_path = constants.file_dict[ 'skilltree.ies']['path']

    z = []
    with io.open(ies_path, 'r', encoding = 'utf-8') as ies_file:
        for row in csv.DictReader(ies_file, delimiter=',', quotechar='"'):
            z.append(row)
            # Ignore discarded skills
            if row['SkillName'] not in constants.data['skills_by_name']:
                continue

            skill = constants.data['skills_by_name'][row['SkillName']]
            skill['MaxLevel'] = int(row['MaxLevel'])
            skill['LevelPerGrade'] = int(row['LevelPerGrade']) if 'LevelPerGrade' in row else 0
            skill['UnlockClassLevel'] = int(row['UnlockClassLevel']) if 'UnlockClassLevel' in row else 0
            skill['UnlockGrade'] = int(row['UnlockGrade']) if 'UnlockGrade' in row else 0

            job = '_'.join(row['ClassName'].split('_')[:2])       
            skill['Link_Job'] = constants.data['jobs_by_name'][job]['$ID']
            constants.data['skills_by_name'][row['SkillName']] = skill
            constants.data['skills'][skill['$ID']] = skill
    return constants


def parse_clean(constants):
    skills_to_remove = []
    # Find which skills are no longer active
    for skill in constants.data['skills'].values():
        if skill['Link_Job'] is None:
            skills_to_remove.append(skill)

    # Remove all inactive skills
    for skill in skills_to_remove:
        del constants.data['skills'][str(skill['$ID'])]
        del constants.data['skills_by_name'][skill['$ID_NAME']]

        skill_id = skill['$ID']

        for attribute in constants.data['attributes'].values():
            attr = constants.data['attributes_by_name'][attribute['$ID_NAME']]
            attribute['Link_Skills'] = [link for link in attribute['Link_Skills'] if link != skill_id]
            attr['Link_Skills'] = [link for link in attr['Link_Skills'] if link != skill_id]
        for job in constants.data['jobs'].values():
            job2= constants.data['jobs_by_name'][job['$ID_NAME']]
            job['Link_Skills'] = [link for link in job['Link_Skills'] if link != skill_id]
            job2['Link_Skills'] = [link for link in job2['Link_Skills'] if link != skill_id]
    