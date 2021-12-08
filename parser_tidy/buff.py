# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 08:55:17 2021

@author: CPPG02619
"""

import csv
import logging
import os
import io
from os.path import exists
from DB import ToS_DB as constants


def parse(c = None):
    if c == None:
        c = constants()
        c.build()
        
    parse_buff('buff_hardskill.ies',c )
    parse_buff('buff.ies',c )
    

def parse_buff(filename, globals):
    logging.debug('Parsing skills...')


    #ies_path = os.path.join(globals.PATH_INPUT_DATA, 'ies.ipf', filename)
    ies_path = globals.file_dict[filename.lower()]['path']
    if(not exists(ies_path)):
       return
    rows = []
    buffs = {}
    with io.open(ies_path, 'r', encoding = 'utf-8') as ies_file:
        for row in csv.DictReader(ies_file, delimiter=',', quotechar='"'):
            # Ignore 'Common_' skills (e.g. Bokor's Summon abilities)
            if row['ClassName'].find('Common_') == 0:
                continue
            rows.append(row)
            obj = {}
            obj['$ID'] = row['ClassID']
            obj['$ID_NAME'] = row['ClassName']
            obj['Description'] = globals.translate(row['ToolTip'])
            obj['Icon'] = globals.parse_entity_icon(row['Icon'])
            obj['Name'] = globals.translate(row['Name'])
            obj['Keyword'] = row['Keyword']
            obj['ApplyTime'] = row['ApplyTime']
            obj['OverBuff'] = row['OverBuff']
            obj['UserRemove'] = 1 if row['UserRemove'] == "YES" else 0
            for i in range(1,4):
                if ('Group{}'.format(i) in row):
                    obj['Group{}'.format(i)] = row['Group{}'.format(i)]
                else:
                    obj['Group{}'.format(i)] = None
            obj['GroupIndex'] = row['GroupIndex']
            globals.data['buff'][row['ClassID']] = obj
          
