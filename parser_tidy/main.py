# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 11:17:20 2021

@author: Temperantia
"""

from DB import ToS_DB as constants
from os.path import join
import os

import logging
import translation
import jobs
import skills
import attributes
import luautil
import asset
import json
import items
import monsters
import maps
import buff
import vaivora
import sys
import misc

def revision_txt_write(revision_txt, revision):
    revision = str(revision)
    with open(revision_txt, 'w') as file:
        file.write(revision)

def revision_txt_read(revision_txt):
    if os.path.isfile(revision_txt):
        with open(revision_txt, 'r') as file:
            return file.readline()
    else:
        return 0

if __name__ == "__main__":
    try:
        region = sys.argv[1]
        region = region.lower()
        accepted = ['itos','ktos','ktest', 'jtos']
        if region not in accepted:
            logging.warning("region unsupported")
            quit()
    except:
        logging.warning("need 1 positional argument; region")
        quit()
    
    c= constants()
    
    current_version = revision_txt_read('parser_version_{}.txt'.format(region.lower()))
    #version = c.importJSON(join("..", 'unpacker_version_{}.txt'.format(region.lower())))['patched'][-1]
    version = revision_txt_read(join("..", 'downloader', 'revision_{}.txt'.format(region)))
    if(version == current_version):
        logging.warning("ipf up to date")
        quit()
    
    c.build(region)
    
    luautil.init(c)
    no_tl = ['ktos', 'ktest']
    asset.parse(c)
    if (region not in no_tl):
        translation.makeDictionary(c)
      
    jobs.parse(c)
   
    skills.parse(c)
    attributes.parse(c)
    attributes.parse_links(c)   
    attributes.parse_clean(c)
    skills.parse_clean(c)
    buff.parse(c)
    items.parse(c)
    if (region not in no_tl):
        vaivora.parse(c)
    
    
    c.data['items']['00000000'] = c.data['items']['089028'].copy()
    c.data['items']['00000000'] ['$ID'] =  '00000000'
    c.data['items']['00000000']['$ID_NAME'] = 'ViboraArcane_Random_Lv1'
    c.data['items']['00000000']['Name'] = 'Random Vaivora Vision lv 1'
    c.data['items']['00000000']['Icon'] = 'icon_item_vibora_vision'
    c.data['items']['00000000']['Link_Materials'] = []
    c.data['items']['00000000']['Link_Target'] = []
    c.data['items']['00000000']['Type'] = 'Arcane'
    c.data['items']['00000000']['Description'] = 'dummy for random vv vision drop'
    c.data['items_by_name'] ['ViboraArcane_Random_Lv1'] = c.data['items']['00000000']
    
    c.data['items']['00000001'] = c.data['items']['00000000'].copy()
    c.data['items']['00000001'] ['$ID'] =  '00000001'
    c.data['items']['00000001']['$ID_NAME'] = 'Moneybag1'
    c.data['items']['00000001']['Name'] = 'Silver'
    c.data['items']['00000001']['Icon'] = 'icon_item_silver'
    c.data['items']['00000001']['Link_Materials'] = []
    c.data['items']['00000001']['Link_Target'] = []
    c.data['items']['00000001']['Type'] = ''
    c.data['items']['00000001']['Description'] = 'is a silver coin'
    c.data['items_by_name'] ['Moneybag1'] = c.data['items']['00000001']
    
    monsters.parse(c)
    monsters.parse_links(c)
    monsters.parse_skill_mon(c)
    
    maps.parse(c)
    maps.parse_maps_images(c) #run map_image.py with py2.7 before running this
    maps.parse_links(c)
    misc.parse_achievements(c)
    #c.export_one("achievements")    
    
    c.export()

    revision_txt_write('parser_version_{}.txt'.format(region.lower()), version)
    v = {'version' : "{}_001001.ipf"version}
    with open(join(c.BASE_PATH_OUTPUT, 'version.json'), "w") as f:
        json.dump(v,f)
       
   
   
