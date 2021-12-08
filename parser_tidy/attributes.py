# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 08:05:03 2021

@author: CPPG02619
"""

import csv
import logging
import os
import io
from os.path import exists
from DB import ToS_DB as constants
import luautil


def parse(c = None):
    if (c == None):
        c = constants()
        c.build(c.iTOS)
    parse_attributes(c)
    


def parse_attributes( globals):
    logging.debug('Parsing attributes...')
    
    ies_path = os.path.join(globals.PATH_INPUT_DATA, 'ies_ability.ipf', 'ability.ies')
    #ies_path = globals.file_dict['ies_ability.ipf']['path']
    if (not exists(ies_path)):
            return 
    with io.open(ies_path, 'r', encoding="utf-8") as ies_file:
        for row in csv.DictReader(ies_file, delimiter=',', quotechar='"'):
            obj = {}
            obj['$ID'] = str(row['ClassID'])
            obj['$ID_NAME'] = row['ClassName']
            obj['Description'] = globals.translate(row['Desc']).strip() + '{nl}'
            obj['Icon'] = globals.parse_entity_icon(row['Icon'])
            obj['Name'] = globals.translate(row['Name'])

            obj['IsToggleable'] = row['AlwaysActive'] == 'NO'

            obj['DescriptionRequired'] = None
            obj['LevelMax'] = -1
            obj['Unlock'] = None
            obj['UnlockArgs'] = {}
            obj['UpgradePrice'] = []
            obj['Link_Jobs'] = []
            obj['Link_Skills'] = [skill for skill in row['SkillCategory'].split(';') if len(skill)]

            globals.data['attributes'][obj['$ID']] = obj
            globals.data['attributes_by_name'][obj['$ID_NAME']] = obj


def parse_links(c = None):
    if c == None:
        c = constants()
        c.build(constants.iTOS)
        luautil.init()
        
    parse_links_jobs(c)
    #parse_clean(c)
def parse_links_jobs(globals):
    logging.debug("Parsing attributes <> jobs...")
    
    LUA_RUNTIME = luautil.LUA_RUNTIME
    LUA_SOURCE = luautil.LUA_SOURCE

    # Parse level, unlock and formula
    #ies_path = os.path.join(globals.PATH_INPUT_DATA, 'ies.ipf', 'job.ies')
    ies_path = globals.file_dict['job.ies']['path']
    if (not exists(ies_path)):
            return 
    with io.open(ies_path, 'r', encoding="utf-8") as ies_file:
        for row in csv.DictReader(ies_file, delimiter=',', quotechar='"'):
            job = globals.data['jobs_by_name'][row['ClassName']]
            mongen_dir = os.listdir(os.path.join(globals.PATH_INPUT_DATA, 'ies_ability.ipf'))
            path_insensitive= {}
            for item in mongen_dir:
                path_insensitive[item.lower()] = item
            ies_file = 'ability_' + row['EngName'] + '.ies'
            
            try:
                ies_file = path_insensitive[ies_file.lower()]
            except:
                logging.warning("class not found {}".format(ies_file))
                
            ies_path = os.path.join(globals.PATH_INPUT_DATA, 'ies_ability.ipf', ies_file)

            # If this job is still under development, skip
            if not os.path.isfile(ies_path):
                continue

            with io.open(ies_path, 'r', encoding = 'utf-8') as ies_file:
                for row2 in csv.DictReader(ies_file, delimiter=',', quotechar='"'):
                    
                    if row2['ClassName'] not in globals.data['attributes_by_name']:
                        logging.warn('Missing attribute in ability.ies: %s', row2['ClassName'])
                        continue

                    attribute = globals.data['attributes_by_name'][row2['ClassName']]
                    attribute['DescriptionRequired'] = attribute['DescriptionRequired'] if attribute['DescriptionRequired'] else ''
                    attribute['DescriptionRequired'] = attribute['DescriptionRequired'] + '{nl}{b}' + globals.translate(row2['UnlockDesc']) + '{b}'
                    attribute['LevelMax'] = int(row2['MaxLevel'])
                    
                   
                    # Parse attribute skill (in case it is missing in the ability.ies)
                    if not attribute['Link_Skills'] and row2['UnlockArgStr'] in globals.data['skills_by_name']:
                        logging.debug('adding missing skill %s', row2['UnlockArgStr'])
                        skill = globals.data['skills_by_name'][row2['UnlockArgStr']]
                        skill['Link_Attributes'].append( attribute['$ID'])
                        attribute['Link_Skills'].append(skill['$ID'])
                        globals.data['skills'][str(skill['$ID'])]['Link_Attributes'] = skill['Link_Attributes']
                        globals.data['attributes'][str(attribute['$ID'])]['Link_Skills'] = attribute['Link_Skills']


                    # Parse attribute job
                    if not attribute['Link_Skills'] or 'All' in attribute['Link_Skills']:
                        attribute['Link_Jobs'].append(job['$ID'])
                        job['Link_Attributes'].append(attribute['$ID'])
                        globals.data['jobs'][str(job['$ID'])]['Link_Attributes'] = job['Link_Attributes']
                        globals.data['attributes'][str(attribute['$ID'])] = attribute

                    # Parse attribute unlock
                    #attribute['Unlock'] = luautil.lua_function_source_to_javascript(
                    #    luautil.lua_function_source(LUA_SOURCE[row2['UnlockScr']])[1:-1]  # remove 'function' and 'end'
                    #) if not attribute['Unlock'] and row2['UnlockScr'] else attribute['Unlock']

                    attribute['UnlockArgs'][job['$ID']] = {
                        'UnlockArgStr': row2['UnlockArgStr'],
                        'UnlockArgNum': row2['UnlockArgNum'],
                    }


def parse_clean(globals):
    attributes_to_remove = []
    # Find which attributes are no longer active
    for attribute in globals.data['attributes_by_name'].values():
        if not attribute['Link_Jobs'] and not attribute['Link_Skills']:
            attributes_to_remove.append(attribute)
        elif attribute['LevelMax'] == -1:
            attributes_to_remove.append(attribute)

    # Remove all inactive attributes
    for attribute in attributes_to_remove:
        globals.data['attributes'].pop (str(attribute['$ID']))
        globals.data['attributes_by_name'].pop(str(attribute['$ID_NAME']))

        attribute_id = attribute['$ID']

        for job in globals.data['jobs'].values():
            job['Link_Attributes'] = [link for link in job['Link_Attributes'] if link != attribute_id]
            globals.data['jobs_by_name'][str(job['$ID_NAME'])]['Link_Attributes']  = [link for link in globals.data['jobs_by_name'][str(job['$ID_NAME'])]['Link_Attributes'] if link != attribute_id]
        for skill in globals.data['skills'].values():
            skill['Link_Attributes'] = [link for link in skill['Link_Attributes'] if link != attribute_id]
            globals.data['skills_by_name'] [str(skill['$ID_NAME'])]['Link_Attributes']  =  [link for link in globals.data['skills_by_name'] [str(skill['$ID_NAME'])]['Link_Attributes'] if link != attribute_id]
            
            