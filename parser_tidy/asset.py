# -*- coding: utf-8 -*-
"""
Created on Wed Sep 22 13:47:05 2021

@author: CPPG02619
"""

import logging
#import multiprocessing
import os
from os.path import exists
import shutil
import xml.etree.ElementTree as ET
#from functools import partial
#from multiprocessing import Pool
from DB import ToS_DB as constants
import  imageutil

IMAGE_SIZE = {  # top, left, width, height
    'bosscard2': (330, 440),
    'sub_card3': (330, 440),
    'npccard': (330, 440),
    'goddesscard': (330, 440),
    'item_tooltip_icon': (256, 256),
    '256_equip_icons': (256, 256),
    '256_costume_icons': (256, 256),
    'acc_item': (256, 256),
    'hair_accesory': (256, 256),
    'item': (256, 256),
    'payment': (256, 256),
}


WHITELIST_BASESKINSET = [
    'bosscard2',
    'minimap_icons',
    'sub_card3',
    'wearing_weapon',
    'npccard',
    'goddesscard',
]

WHITELIST_RGB = [
    'bosscard2',
    'sub_card3',
    'npccard',
    'goddesscard',
]


def parse( c = None):
    if c == None:
        logging.warn("c is none")
        c = constants()
        c.build()
    logging.basicConfig(level=logging.DEBUG)
    
    logging.info('Parsing assets...')
    parse_icons('baseskinset.xml',c)
    parse_icons('classicon.xml',c)
    parse_icons('itemicon.xml',c)
    parse_icons('mongem.xml',c)
    parse_icons('monillust.xml',c)
    parse_icons('skillicon.xml',c)
    
    

def parse_icons(file_name,c):
    
    logging.info('Parsing file {}'.format(file_name))
    
    #data_path = os.path.join(globals.PATH_INPUT_DATA, 'ui.ipf', 'baseskinset', file_name)
    logging.warning(file_name)
    try:
        data_path = c.file_dict[file_name.lower()]['path']
    except:
        data_path = os.path.join(c.PATH_INPUT_DATA, 'ui.ipf', 'baseskinset', file_name)
        pass
    if (not exists(data_path)):
        logging.warn("{} not exists".format(data_path))
        return 
    data = ET.parse(data_path).getroot()
    data = [(image, imagelist) for imagelist in data for image in imagelist]

    for work in data:
        parse_icons_step(file_name, work,c)


def parse_icons_step(file_name, work,c):     
    image = work[0]
    image_category = work[1].get('category')
    if image.get('file') is None or image.get('name') is None:
        return
    if file_name == 'baseskinset.xml' and image_category not in WHITELIST_BASESKINSET:
        return
    file_name = c.file_dict[file_name.lower()]['name']
    image_extension = '.jpg' if image_category in WHITELIST_RGB else '.png'
    image_file = image.get('file').split('\\')[-1]
    try:
        image_file = c.file_dict[image_file.lower()]['name']
    except:
        pass
    image_name = image.get('name')
    image_rect = tuple(int(x) for x in image.get('imgrect').split()) if len(image.get('imgrect')) else None  # top, left, width, height

    # Copy icon to web assets folder
    copy_from = os.path.join(c.PATH_INPUT_DATA, 'ui.ipf', *image.get('file').lower().split('\\')[:-1])
    copy_from = os.path.join(copy_from, image_file)
    copy_to = os.path.join(c.PATH_BUILD_ASSETS_ICONS, (image_name + image_extension).lower())

    if not os.path.isfile(copy_from):
        #logging.warning("asset file not found {}".format(copy_from))
        # Note for future self:
        # if you find missing files due to wrong casing, go to the Hotfix at unpacker.py and force lowercase
        #logging.warning('Non-existing icon: %s', copy_from)
        c.data['assets_icons'][image_name.lower()] = image_name.lower()

        return


    #logging.warning("parsing {}".format(copy_to))
    if (not os.path.exists(c.PATH_BUILD_ASSETS_ICONS)):
        
        os.mkdir (c.PATH_BUILD_ASSETS_ICONS)
    shutil.copy(copy_from, copy_to)
    #os.remove(copy_from)
    # Crop, Resize, Optimize and convert to JPG/PNG
    image_mode = 'RGB' if image_extension == '.jpg' else 'RGBA'
    image_size = IMAGE_SIZE[image_category] if image_category in IMAGE_SIZE else (image_rect[2], image_rect[3])
    image_size = (256, 256) if file_name == 'classicon.xml' else image_size
    image_size = (256, 256) if file_name == 'skillicon.xml' else image_size

    imageutil.optimize(copy_to, image_mode, image_rect, image_size)

    # Store mapping for later use
    c.data['assets_icons'][image_name.lower()] = image_name.lower()

