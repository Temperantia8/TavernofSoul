# -*- coding: utf-8 -*-
"""
Created on Fri Nov 19 14:15:41 2021

@author: CPPG02619
"""

from DB import ToS_DB as DB
import maps
c = DB()
c.build('jtos')
c.importJSON("maps.json")

maps.parse_maps_images(c)
