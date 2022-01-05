# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 08:38:06 2021

@author: CPPG02619
"""

import csv
import logging
import io
from DB import ToS_DB as constants
import xml.etree.ElementTree as ET

def parse(c = None):
    if c == None:
        c = constants()
        c.build("itos")
        
def parseChar(c):
    logging.warning('Parsing char exp...')
    ies_path = c.file_dict["xp.ies"]['path']
    rows    = []
    exp     = []
    with io.open(ies_path, 'r', encoding = 'utf-8') as ies_file:
        for row in csv.DictReader(ies_file, delimiter=',', quotechar='"'):
            rows.append(row)
            xp = {
                'Lv'        : int(row['Lv']),
                'TotalXp'   : float(row['TotalXp'] ),                
            }
            exp.append(xp)
    c.data['charxp'] = exp

def parsePetAssister(c):
    logging.warning('Parsing char exp...')
    ies_path    = c.file_dict["pet_exp.xml"]['path']
    data        = ET.parse(ies_path).getroot()
    pet         = [i.attrib for i in data[0]]
    assister    = [i.attrib for i in data[2]]
    
    c.data['petxp']       = pet
    c.data['assisterxp']  = assister
    