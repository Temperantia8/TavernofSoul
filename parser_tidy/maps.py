# -*- coding: utf-8 -*-
"""
Created on Sun Oct  3 21:18:15 2021

@author: Intel
"""

import csv
import logging
import os
import re
from os.path import exists
from PIL import Image, ImageDraw, ImageColor, ImageFilter, ImageOps, ImageChops

from DB import ToS_DB as constants
import luautil

import  imageutil

MAP_SCALE = 0.5

def trim(image):    
    # remove alpha channel
    invert_im = image.convert("RGB") 
    
    # invert image (so that white is 0)
    im  = image
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    invert_im = ImageOps.invert(invert_im)
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    cropped=image.crop(bbox)
    return bbox,cropped




def parse(c = None):
    if (c==None):
        c = constants()
        c.build(c.iTOS)
    try:
        os.mkdir(constants.PATH_BUILD_ASSETS_IMAGES_MAPS)
    except:
        pass
    parse_maps(c)
    

def parse_maps(constants):
    logging.debug('Parsing Maps...')

    #ies_path = os.path.join(constants.PATH_INPUT_DATA, 'ies.ipf', 'map.ies')
    ies_path = constants.file_dict['map.ies']['path']
    rows = []
    with open(ies_path, 'r', encoding = 'utf-8') as ies_file:
        for row in csv.DictReader(ies_file, delimiter=',', quotechar='"'):
            rows.append(row)
            obj = {}
            if str(row['ClassID']) in constants.data['maps']:
                #continue
                obj = constants.data['maps'][row['ClassID']]
            obj['$ID'] = str(row['ClassID'])
            obj['$ID_NAME'] = row['ClassName']
            obj['Icon'] = None
            obj['Name'] = constants.translate(row['Name'])

            obj['HasChallengeMode'] = row['ChallengeMode'] == 'YES'
            obj['HasWarp'] = int(row['WarpCost']) > 0
            obj['Level'] = int(row['QuestLevel'])
            obj['Prop_EliteMonsterCapacity'] = int(row['EliteMonsterCapacity'])
            obj['Prop_MaxHateCount'] = int(row['MaxHateCount'])
            obj['Prop_RewardEXPBM'] = float(row['MaxHateCount'])
            obj['Stars'] = int(row['MapRank'])
            obj['Type'] = row['MapType']
            obj['Warp'] = int(row['WarpCost'])
            obj['WorldMap'] = [int(coord) for coord in row['WorldMap'].split('/')] if row['WorldMap'] else None

            obj['Link_Items'] = []
            obj['Link_Items_Exploration'] = []
            obj['Link_Maps'] = []
            obj['Link_Maps_Floors'] = []
            obj['Link_NPCs'] = []
            if ("bbox" not in obj):
                obj['bbox']     = [0,0,0,0]
            constants.data['maps'][obj['$ID']] = obj
            constants.data['maps_by_name'][obj['$ID_NAME']] = obj
            constants.data['maps_by_position']['-'.join(row['WorldMap'].split('/')) if obj['WorldMap'] else ''] = obj


def parse_maps_images(constants):

    logging.debug('Parsing Maps images...')
    log = logging.getLogger("parse.items")
    log.setLevel("INFO")

    ies_path = os.path.join(constants.PATH_INPUT_DATA, 'ies.ipf', 'map.ies')
    ies_path = constants.file_dict['map.ies']['path']
    rows = []
    with open(ies_path, 'r', encoding = 'utf-8') as ies_file:
        for row in csv.DictReader(ies_file, delimiter=',', quotechar='"'):
            rows.append(row)
            image_path = os.path.join(constants.PATH_BUILD_ASSETS_IMAGES_MAPS, row['ClassName'].lower() + '.png')
            map = constants.data['maps_by_name'][row['ClassName']]
            if (exists(image_path) and map['bbox'] != [0,0,0,0]):
                continue
            polygons = constants.importJSON(os.path.join('maps_poly',row['ClassName'].lower()+'poly.json'))
            if polygons == {}:
                continue
            # Scale map to save some space
            image_height = int(round(int(row['Height']) * MAP_SCALE))
            image_width = int(round(int(row['Width']) * MAP_SCALE))

            offset_x = image_width / 2.0
            offset_y = image_height / 2.0

            # Render map to image
            image = Image.new("RGBA", (image_width, image_height), (0, 0, 0, 0))
            image_draw = ImageDraw.Draw(image)

            for points in polygons:
                # Make sure coordinates are centered
                points = [(int(offset_x + coords[0] * MAP_SCALE), int(offset_y + coords[1] * MAP_SCALE)) for coords in points]

                image_draw.polygon(points, fill=ImageColor.getrgb('#67768a'))

            # Add a shadow
            image_shadow = imageutil.replace_color(image, ImageColor.getcolor('#F2BC65', 'RGBA'), ImageColor.getcolor('#000000', 'RGBA'))
            image_shadow = image_shadow.filter(ImageFilter.GaussianBlur(2))
            image = Image.composite(image, image_shadow, image_shadow)
            bbox,image= trim(image)
            log.info("map : {} bbox : {}".format(row['ClassName'], bbox))
            # Save image to disk
            try:
                os.mkdir(constants.PATH_BUILD_ASSETS_IMAGES_MAPS)
            except:
                pass
            image.save(image_path, optimize=True)
            image.close()
            image_shadow.close()
            
            map['bbox'] = bbox
            constants.data['maps'][map['$ID']] = map


def parse_links(c = None):
    if (c==None):
        c = constants()
        c.build(c.iTOS)
    c.data['map_item'] = []
    parse_links_items(c)
    parse_links_items_rewards(c)

    parse_links_maps(c)

    c.data['map_npc'] = []
    parse_links_npcs(c)



def parse_links_items(constants):
    logging.debug('Parsing Maps <> Items...')

    for map in constants.data['maps'].values():
        if map == None:
            continue
        ies_drop_p = os.path.join("..", 'itos_unpack', 'ies_drop.ipf')
        ies_drop =  os.listdir(os.path.join(ies_drop_p,  'zonedrop'))
        path_insensitive= {}
        for item in ies_drop:
            path_insensitive[item.lower()] = item
            
            
        ies_file = 'ZoneDropItemList_' + map['$ID_NAME'] + '.ies'
        try:
            ies_file = path_insensitive[ies_file.lower()]
        except:
            logging.debug("maps not found {}".format(ies_file))
            pass
        
        ies_path = os.path.join(ies_drop_p, 'zonedrop', ies_file)
        
        # For some reason IMC uses these 2 types of name formats...
        if not os.path.isfile(ies_path):
            ies_file = 'zonedropitemlist_f_' + map['$ID_NAME'] + '.ies'
            ies_path = os.path.join(constants.PATH_INPUT_DATA, 'ies_drop.ipf', 'zonedrop', ies_file)

        try:
            drops = []

            with open(ies_path, 'r', encoding = 'utf-8') as ies_file:
                for zone_drop in csv.DictReader(ies_file, delimiter=',', quotechar='"'):
                    chance = 100.0
                    if 'id_Unknownsanctuary'.lower() in ies_path.lower():
                        chance = 10000.0
                    if len(zone_drop['ItemClassName']) > 0:
                        drops.append({
                            'ItemClassName': zone_drop['ItemClassName'],
                            'DropRatio': int(zone_drop['DropRatio']) / chance,
                            'Money_Max': int(zone_drop['Money_Max']),
                            'Money_Min': int(zone_drop['Money_Min']),
                        })

                    # Note: drop groups work like a loot table
                    # Therefore we need to sum the DropRatio of the entire group before calculating the actual one
                    if len(zone_drop['DropGroup']) > 0:
                        ies_file = zone_drop['DropGroup'] + '.ies'
                        ies_path = os.path.join(constants.PATH_INPUT_DATA, 'ies_drop.ipf', 'dropgroup', ies_file)

                        group_drop_ratio = 0
                        group_drops = []

                        with open(ies_path, 'r', encoding = 'utf-8') as ies_file:
                            for group_drop in csv.DictReader(ies_file, delimiter=',', quotechar='"'):
                                group_drop_ratio += int(group_drop['DropRatio'])
                                group_drops.append({
                                    'ItemClassName': group_drop['ItemClassName'],
                                    'DropRatio': int(group_drop['DropRatio']),
                                    'Money_Max': 0,
                                    'Money_Min': 0,
                                })

                        for group_drop in group_drops:
                            group_drop['DropRatio'] = int(zone_drop['DropRatio']) / 100.0 * group_drop['DropRatio'] / group_drop_ratio

                            drops.append(group_drop)

                for drop in drops:
                    try:
                        map_item = {
                            'Chance': drop['DropRatio'],
                            'Item': constants.data['items_by_name'][drop['ItemClassName']]['$ID'],
                            'Map': constants.data['maps_by_name'][map['$ID_NAME']]['$ID'],
                            'Quantity_MAX': drop['Money_Max'],
                            'Quantity_MIN': drop['Money_Min'],
                        }
                        constants.data['map_item'].append(map_item)                    
                    except:
                        logging.warn('Map {} or item {} not found'
                                     .format(map['$ID_NAME'], drop['ItemClassName'],))

        except IOError:
            continue


def parse_links_items_rewards(constants):
    logging.debug('Parsing Maps <> Items (Rewards)...')

    ies_path = os.path.join(constants.PATH_INPUT_DATA, 'ies.ipf', 'map.ies')

    with open(ies_path, 'r', encoding = 'utf-8') as ies_file:
        for row in csv.DictReader(ies_file, delimiter=',', quotechar='"'):
            if int(row['MapRatingRewardCount1']) == 0 or len(row['MapRatingRewardItem1']) == 0:
                continue

            item_link = constants.data['items_by_name'][row['MapRatingRewardItem1']]
            map = constants.data['maps_by_name'][row['ClassName']]
            map_item = map['$ID']
            map_item = {
                'Chance': 100,
                'Map': map_item,
                'Item': item_link['$ID'],
                'Quantity_MAX': int(row['MapRatingRewardCount1']),
                'Quantity_MIN': int(row['MapRatingRewardCount1']),
            }

            constants.data['map_item'].append(map_item)


def parse_links_maps(constants):
    logging.debug('Parsing Maps <> Maps...')

    #ies_path = os.path.join(constants.PATH_INPUT_DATA, 'ies.ipf', 'map.ies')
    ies_path = constants.file_dict['map.ies']['path']
    name = ''
    with open(ies_path, 'r', encoding='utf8') as ies_file:
        try:
            for row in csv.DictReader(ies_file, delimiter=',', quotechar='"'):
                if len(row['PhysicalLinkZone']) == 0:
                    continue
    
                map = constants.data['maps_by_name'][row['ClassName']]
                
                map['Link_Maps'] = [constants.data['maps_by_name'][name]['$ID'] for name in row['PhysicalLinkZone'].split('/')]
    
                map_item = constants.data['maps_by_name'][map['$ID_NAME']]
    
                # Floors
                if map['WorldMap'] is not None and map['WorldMap'][2] > 0:
                    map_ground_floor = constants.data['maps_by_position']['-'.join([str(i) for i in (map['WorldMap'][0:2] + [1])])]
                    map_ground_floor['Link_Maps_Floors'].append(map_item['$ID'])
                constants.data['maps'][map['$ID']] = map
        except:
            pass


def parse_links_npcs(constants):
    logging.debug('Parsing Maps <> NPCs...')

    #ies_path = os.path.join(constants.PATH_INPUT_DATA, 'ies.ipf', 'map.ies')
    ies_path = constants.file_dict['map.ies']['path']
    with open(ies_path, 'r', encoding = 'utf8') as ies_file:
        for row in csv.DictReader(ies_file, delimiter=',', quotechar='"'):
            map = constants.data['maps_by_name'][row['ClassName']]
            map = constants.data['maps'][str(map['$ID'])]
            map_offset_x = int(round(int(row['Width']) / 2.0))
            map_offset_y = int(round(int(row['Height']) / 2.0))

            anchors = {}

            # Spawn Positions (aka Anchors)
            mongen_dir = os.listdir(os.path.join(constants.PATH_INPUT_DATA, 'ies_mongen.ipf'))
            path_insensitive= {}
            for item in mongen_dir:
                path_insensitive[item.lower()] = item
                
            ies_file = 'anchor_' + map['$ID_NAME'] + '.ies'
            try:
                ies_file = path_insensitive[ies_file.lower()]
            except:
                logging.warning("maps not found {}".format(ies_file))
                pass
            
            ies_path = os.path.join(constants.PATH_INPUT_DATA, 'ies_mongen.ipf', ies_file)
            
            try:
                with open(ies_path, 'r', encoding='utf8') as ies_file:
                    for row in csv.DictReader(ies_file, delimiter=',', quotechar='"'):
                        obj = anchors[row['GenType']] if row['GenType'] in anchors else { 'Anchors': [], 'GenType': {} }
                        obj['Anchors'].append([
                            int((map_offset_x + float(row['PosX'])) * MAP_SCALE),
                            int((map_offset_y - float(row['PosZ'])) * MAP_SCALE),
                        ])

                        anchors[row['GenType']] = obj
            except IOError:
                logging.debug("file not found {}".format(ies_path))
                continue

            # Spawn NPCs
            
            ies_file = 'gentype_' + map['$ID_NAME'] + '.ies'
            try:
                ies_file = path_insensitive[ies_file.lower()]
            except:
                logging.warning("gentype not found {}".format(ies_file))
                pass
            ies_path = os.path.join(constants.PATH_INPUT_DATA, 'ies_mongen.ipf', ies_file)

            try:
                with open(ies_path, 'r', encoding='utf8') as ies_file:
                    for row in csv.DictReader(ies_file, delimiter=',', quotechar='"'):
                        if constants.getNPCbyName(row['ClassType']) is None:
                            continue
                        if row['GenType'] not in anchors:
                            continue

                        obj = anchors[row['GenType']]
                        obj['GenType'] = row
            except IOError:
                continue

            # Group by Item/NPC and join anchors
            anchors_by_npc = {}

            for anchor in anchors.values():
                if len(anchor['GenType'].keys()) == 0:
                    continue

                item_name = re.search('\w+:(\w+):\w+', anchor['GenType']['ArgStr2'])
                npc_name = item_name.group(1) if item_name else anchor['GenType']['ClassType']

                if npc_name in anchors_by_npc:
                    anchors_by_npc[npc_name]['Anchors'] += anchor['Anchors']
                    anchors_by_npc[npc_name]['GenType']['MaxPop'] = int(anchors_by_npc[npc_name]['GenType']['MaxPop']) + int(anchor['GenType']['MaxPop'])
                else:
                    anchors_by_npc[npc_name] = anchor
                
            # Link everyone
            for anchor_name in anchors_by_npc.keys():
                anchor = anchors_by_npc[anchor_name]

                if anchor_name in constants.data['items_by_name']:
                    item = constants.data['items_by_name'][anchor_name]
                    item_link = item['$ID']
                    position = []
                    new_pos = []
                    for i in anchor['Anchors']:
                        pos = [i[0]-map['bbox'][0],i[1]-map['bbox'][1]]
                        new_pos.append(pos)
                        
                    item_link = {
                        'Item': item_link,
                        'Map' : map['$ID'],
                        'Population': int(anchor['GenType']['MaxPop']),
                        'Positions': new_pos,
                        'TimeRespawn': int(anchor['GenType']['RespawnTime']) / 1000.0,
                    }
                    constants.data['map_item_spawn'].append(item_link)
                    

                elif anchor_name in constants.data['npcs_by_name'] or anchor_name in constants.data['monsters_by_name']:
                    npc, types = constants.getNPCbyName(anchor_name)
                    npc_link = npc['$ID']
                    position = []
                    #logging.warning("loc bef {}".format(anchor['Anchors']))
                    #logging.warning("bbox : {}".format(map['bbox']))
                    new_pos = []
                    for i in anchor['Anchors']:
                        pos = [i[0]-map['bbox'][0],i[1]-map['bbox'][1]]
                        new_pos.append(pos)
                    #logging.warning("loc aft {}".format(new_pos))
                    npc_link = {
                        'NPC': npc_link,
                        'Map': map['$ID'],
                        'Type' : types,
                        'Population': int(anchor['GenType']['MaxPop']),
                        'Positions': new_pos,
                        'TimeRespawn': int(anchor['GenType']['RespawnTime']) / 1000.0,
                    }
                    constants.data['map_npc'].append(npc_link)
