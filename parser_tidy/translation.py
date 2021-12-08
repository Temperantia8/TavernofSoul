# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 09:12:11 2021

@author: Temperantia
modified from rjgtav 
 https://github.com/rjgtav/tos-database/blob/master/tos-parser/src/parserr/parser_translations.py

create dictionary csv for future translation of game aspects
"""

import csv
from os.path import join, exists
import xml.etree.ElementTree as ET
from DB import ToS_DB
import os
import logging


TRANSLATION_PREFIX = '@dicID_^*$'
TRANSLATION_SUFFIX = '$*^'

def parseDict(translations,c):
    #parsing the dictionary in language.ipf, translate it to dictionary from
    #language.tsv 
    
    translations_all = {}
    dictionary_path = join(c.PATH_INPUT_DATA,"language.ipf", "wholeDicID.xml")
    ies_path = c.file_dict[ "wholeDicID.xml".lower()]['path']
    if (not exists (dictionary_path)):
        return {}
    dictionary = ET.parse(dictionary_path).getroot()
 
    # example: <file name="xml\item_Equip.xml">
    for file in dictionary:
        # <data original="없음_helmet" dicid="@dicID_^*$ITEM_20150317_000001$*^"/>
        for data in file:
            key = data.get('original').replace('"', '')
            value = data.get('dicid')
            value_translated = '%s' % data.get('dicid')
    
            for dicid in value.split(TRANSLATION_SUFFIX):  # Sometimes there are multiple ids in a single entry (as translations are re-used)
                if TRANSLATION_PREFIX in dicid:
                    dicid = dicid[dicid.index(TRANSLATION_PREFIX) + len(TRANSLATION_PREFIX):]
                    if dicid not in translations:
                        logging.warn('Missing translation for dicid: (%s)', dicid)
    
                    translation = translations[dicid] if dicid in translations else dicid
                    value_translated = value_translated.replace(TRANSLATION_PREFIX + dicid + TRANSLATION_SUFFIX, translation)
    
            translations_all[key] = value_translated
    return translations_all

def parseTranslation(c):
    # opening the language csv ( there's various language, currently only using english)
    
    result = {}
    translation_path = c.transaltion_path
    for translation in os.listdir(translation_path):
        if(translation == '.git'):
            continue
        cur_path = os.path.join(translation_path, translation)

        if '.tsv' not in translation:
            continue

        with open(cur_path, 'r', encoding='utf-8') as translation_file:
            for row in csv.reader(translation_file, delimiter='\t', quoting=csv.QUOTE_NONE):
                if len(row) > 1:
                    result[row[0]] =row[1]
    return result

def makeDictionary(c = None):
    if (c == None):
        c = ToS_DB()
        c.build()
    
    translation = parseTranslation(c)
    dictionary = parseDict(translation,c)
    if dictionary!= {}:    
        c.data['dictionary'] = dictionary

    
