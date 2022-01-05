# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 15:29:39 2021

@author: CPPG02619
"""

import translation
import logging

vv_dict={'Reinforced Bowstring' : 'Reinforce Bowstring', 
        'Lewa Advent': ' Lewa Advent ',
         'Cluster Bomb' : 'Cluster Shot', 
         'Triple Steps Single Shot': 'Triple Steps Single Shot',
         'Mass Heal: Freeze' : 'Mass Heal: Cooling', 
         'Doble Attaque' : 'Especial', 
         'クラスターボム' : 'クラスターショット',
         'アドベント・ロア': ' アドベント・ロア', 
         'レバー - アクション': "レバー・アクション", 
         'ドブレ・アタケ' : 'エスペシアル'
         }

def translate(name):
    if name in vv_dict:
        return vv_dict[name]
    return name

def parse(c):
    logging.warning("parsing vaivoras")
    items = c.data['items']
    if len(c.data) ==0:
        logging.warning("items are empty ?")
        return
    vvrs = []
    
    for i in items:
        vv = {}
        if items[i]['Name']!=None and  "Vaivora Vision" in items[i]['Name']:
            vv['name']          = items[i]['Name']
            vv['$ID_NAME']      = items[i]['$ID_NAME']
            vv['$ID']           = items[i]['$ID']
            vv['type']          = translate("-".join(items[i]['Name'].split("-")[1:]).strip()).lower().replace("\xa0", " ")
            vvrs.append(vv)
            
    tl = translation.parseTranslation(c)
    
    for v in vvrs:
        lookup = "{nl}"+v['type']+"{nl}"
        v['tl_crude'] = []
        for i in tl:
            if lookup in tl[i].lower():
                t = {'code':i, 'tl':tl[i]}
                v['tl_crude'].append(t)
        
    for v in vvrs:
        if len(v['tl_crude'])>0:
            v['tl'] = v['tl_crude'][-1]['tl']
        else:
            v['tl'] = ""
            
    for v in vvrs:
        if v['tl'] != "" and "Bonus" in c.data['items_by_name'][v['$ID_NAME']]:
            c.data['items_by_name'][v['$ID_NAME']]['Bonus'].append(['-', v['tl']])
            c.data['items'][v['$ID']]   = c.data['items_by_name'][v['$ID_NAME']]
