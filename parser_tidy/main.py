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
import csv


def print_version(filename, data):
    out = [ [key, data[key]] for key in data]
    with open(filename, 'w') as f:  # You will need 'wb' mode in Python 2.x
        w = csv.writer(f)
        w.writerows(out)

def read_version(filename):
    rev = {}
    with open(filename, 'r') as f:
        w = csv.reader(f)
        for lines in w:
            if len(lines)<2:
                continue
            rev[lines[0]] = lines[1]
    return rev

            
    return rev
if __name__ == "__main__":
    try:
        region = sys.argv[1]
        region = region.lower()
        accepted = ['itos','ktos','ktest', 'jtos', 'twtos']
        if region not in accepted:
            logging.warning("region unsupported")
            quit()
    except:
        logging.warning("need 1 positional argument; region")
        quit()
    
    c= constants()
    current_version = read_version('parser_version.csv')
    #version = c.importJSON(join("..", 'unpacker_version_{}.txt'.format(region.lower())))['patched'][-1]
    version = read_version(join("..", 'downloader', 'revision.csv'))
    if(version[region] == current_version[region]) and ('-f' not in sys.argv):
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
    
    current_version[region] = version[region]
    print_version('parser_version.csv', current_version)
    v = {'version' : "{}_001001.ipf".format(version[region])}
    with open(join(c.BASE_PATH_OUTPUT, 'version.json'), "w") as f:
        json.dump(v,f)
       
   
   
