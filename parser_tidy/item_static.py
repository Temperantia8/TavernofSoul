# -*- coding: utf-8 -*-
"""
Created on Wed Dec 22 09:14:45 2021
@author: CPPG02619
"""

def add_item_static(c):
    
    c.data['items']['00000000'] = c.data['items']['9028'].copy()
    c.data['items']['00000000'] ['$ID'] =  '00000000'
    c.data['items']['00000000']['$ID_NAME'] = 'ViboraArcane_Random_Lv1'
    c.data['items']['00000000']['Name'] = 'Random Vaivora Vision lv 1'
    c.data['items']['00000000']['Icon'] = 'icon_item_vibora_vision'
    c.data['items']['00000000']['Link_Materials'] = []
    c.data['items']['00000000']['Link_Target'] = []
    c.data['items']['00000000']['Type'] = ''

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
    
    c.data['items']['00000002'] = c.data['items']['00000000'].copy()
    c.data['items']['00000002'] ['$ID'] =  '00000002'
    c.data['items']['00000002']['$ID_NAME'] = 'GabijaCertificate'
    c.data['items']['00000002']['Name'] = 'Gabija Coin'
    c.data['items']['00000002']['Icon'] = 'icon_item_gabijacertificatecoin_1p'
    c.data['items']['00000002']['Link_Materials'] = []
    c.data['items']['00000002']['Link_Target'] = []
    c.data['items']['00000002']['Type'] = ''
    c.data['items']['00000002']['Description'] = 'dummy for gabija coin'
    c.data['items_by_name'] ['GabijaCertificate'] = c.data['items']['00000002']