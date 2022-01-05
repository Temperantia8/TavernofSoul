# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 11:54:34 2021

@author: CPPG02619
"""


import csv
import logging
import os

from os.path import exists
from DB import ToS_DB as constants
import json

import tokutil

MAP_SCALE = 0.2

def parse_maps_images(c):
    """
    TOK!
    """
    logging.debug('Parsing Maps images...')

    #ies_path = os.path.join(constants.PATH_INPUT_DATA, 'ies.ipf', 'map.ies')
    ies_path = c.file_dict['map.ies']['path']

    with open(ies_path, 'rb') as ies_file:
        for row in csv.DictReader(ies_file, delimiter=',', quotechar='"'):
            if exists (os.path.join('maps_poly',row['ClassName'].lower()+'poly.json')):
                continue
            image_path = os.path.join(c.PATH_BUILD_ASSETS_IMAGES_MAPS, row['ClassName'].lower() + '.png')
            tok_path = os.path.join(c.PATH_INPUT_DATA, 'bg.ipf', row['ClassName'].lower() + '.tok')

            if not os.path.exists(tok_path):
                continue

            # Parse .tok mesh file
            tok_file = open(tok_path, 'rb')
            tok_xml = tokutil.tok2xml(tok_file)

            mesh3D = [elem for elem in tok_xml.getchildren() if elem.tag == 'mesh3D'][0]
            mesh3DVerts = [elem for elem in mesh3D.getchildren() if elem.tag == 'verts'][0]
            mappingTo2D = [elem for elem in tok_xml.getchildren() if elem.tag == 'mappingTo2D'][0]

            polygons = []

            for polygon in mappingTo2D.getchildren():
                points = []

                for edge in polygon.getchildren():
                    vertex = mesh3DVerts.getchildren()[int(edge.attrib['startVert'])]
                    points.append((int(vertex.attrib['x']), -int(vertex.attrib['y'])))

                polygons.append(points)

            # Free some memory before continuing
            tok_file.close()
            tok_xml.clear()

            del mesh3D
            del mesh3DVerts
            del mappingTo2D
            del tok_xml
            with open(os.path.join('maps_poly',row['ClassName'].lower()+'poly.json'), 'w') as f:
                json.dump(polygons,f)

import sys
if __name__ == "__main__":
    try:
        region = sys.argv[1]
    except:
        logging.warning("need 1 positional argument; region")
        quit()
    c= constants()
    c.build(region)
    parse_maps_images(c)