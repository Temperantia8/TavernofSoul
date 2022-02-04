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
import skill_bytool
import parse_xac
from item_static import add_item_static
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
    if(version == current_version) and ('-f' not in sys.argv):
        logging.warning("ipf up to date")
        quit()
        
    c.build(region)
    parse_xac.parse_xac(c)
    luautil.init(c)
    no_tl = ['ktos', 'ktest']
    asset.parse(c)
    if (region not in no_tl):
        translation.makeDictionary(c)
      
    jobs.parse(c)
    skill_bytool.parse(c)
    skills.parse(c)
    attributes.parse(c)
    attributes.parse_links(c)   
    attributes.parse_clean(c)
    skills.parse_clean(c)
    buff.parse(c)
    items.parse(c)
    if (region not in no_tl):
        vaivora.parse(c)
        vaivora.parse_lv4(c)
    add_item_static(c)
    
    items.parse_goddess_EQ(c)
    
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
    v = {'version' : "{}_001001.ipf".format(version)}
    with open(join(c.BASE_PATH_OUTPUT, 'version.json'), "w") as f:
        json.dump(v,f)
       
   
   
