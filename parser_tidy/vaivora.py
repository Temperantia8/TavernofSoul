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

vv_dict_job = {'conviction':'4019', 'ema' : '4018'}
vv_common = ['0511050094', '0511050097', '0511050119', '0511050164', '0511050147', '0511050130']
vv_common_name = ['concentrated defence', 'echo', 'coordination', 'bloody fight' ]


def translate(name):
    if name in vv_dict:
        return vv_dict[name]
    return name

def createdict(c):
    all_dic = {}
    exception = []
    for skills in c.data['skills']:
        skills = c.data['skills'][skills]
        job  = skills['Link_Job']
        job  = c.data['jobs'][job]['$ID']
        key= skills['Name'].lower().replace('\xa0', ' ')
        if key in all_dic:
            all_dic.pop(key)
            exception.append(key)
        elif key in exception :
            continue
        else:
            all_dic[key] =job
    """
    ambigous = []
    for i in all_dic.keys():
        for h in all_dic.keys():
            if h!= i and i in h:
                ambigous.append(i)
                break
    for item in ambigous:
        all_dic.pop(item)
    """
    all_dic_k = sorted(all_dic, key=lambda k: len(k))
    all_dic_sorted = {}
    for i in all_dic_k:
        all_dic_sorted[i] = all_dic[i]
    
    all_dic = all_dic_sorted
    global job_names
    job_names = []
    for jobs in c.data['jobs']:
        jobs = c.data['jobs'][jobs]
        all_dic[jobs['Name'].lower()] = jobs['$ID']    
        all_dic_k.append(jobs['Name'].lower())
        job_names.append(jobs['Name'].lower())
        
    global bow, bow_key, class_code
    bow = all_dic 
    bow_key = all_dic_k
    class_code = list(set(bow.values()))
    
    

def parse(c):
    logging.warning("parsing vaivoras")
    items = c.data['items']
    if len(c.data['items']) ==0:
        logging.warning("items are empty ?")
        return
    vvrs = []
    if c.region == 'jtos':
        vv_name = 'バイボラ秘伝'
    else:
        vv_name = "Vaivora Vision"
    c.data['vvrs'] = []
    for i in items:
        vv = {}
        if items[i]['Name']!=None and vv_name.lower()  in items[i]['Name'].lower():
            vv['name']          = items[i]['Name']
            vv['$ID_NAME']      = items[i]['$ID_NAME']
            vv['$ID']           = items[i]['$ID']
            vv['type']          = translate("-".join(items[i]['Name'].split("-")[1:]).strip()).lower().replace("\xa0", " ")
            vvrs.append(vv)
            c.data['vvrs'].append(vv)
            
    tl = c.data['dictionary']
    
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
        

def getclass_fromstring(c, string):
    
    
    bonus = string.lower().\
            replace('{nl}',' ').\
            replace("'s",' ').\
            replace('\xa0', ' ').\
            replace(',', '').\
            replace(':', '').\
            split(' ')
    rank = {i:0 for i in class_code}
    found = []
    for i in range(len(bonus)):
        if bonus[i] in job_names:
            rank[bow[bonus[i]]] +=5
            found.append(bonus[i])
        if ' '.join(bonus[i:i+2]) in job_names:
             rank[bow[' '.join(bonus[i:i+2])]] +=5
             found.append(bonus[i:1+2])
             

        if bonus[i] in bow_key:
            rank[bow[bonus[i]]] +=1
            found.append(bonus[i])
            
        if ' '.join(bonus[i:i+2]) in bow_key:
            rank[bow[' '.join(bonus[i:i+2])]] +=3
            found.append(bonus[i:i+2])
        if  ' '.join(bonus[i:i+3]) in bow_key:
            rank[bow[' '.join(bonus[i:i+3])]] +=5
            found.append(bonus[i:i+3])
    maks=-1
    maks_code = ''
    for i in rank:
        if maks < rank[i]:
            maks = rank[i]
            maks_code = i 
    if maks == 0:
        return ''
    return maks_code


def getclass_vv(c):
    createdict(c)
    vv4 = []
    for i in c.data['vvrs']:
        if i ['type'] in vv_common_name:
            continue
        if 'lv4' in i['name'].lower():
            vv4.append(i)
            
    vvs = []
    for i in vv4:
        vvs.append(c.data['items'][i['$ID']])
     
    
    for item in vvs:
       
        try:
            string = item['Bonus'][-1][1]
            item['job'] = getclass_fromstring(c, string)
        except:
            continue
        try:
           name = item['Name'].split('-')[1].strip().lower().replace("\xa0", " ")
           item['job'] = vv_dict_job[name]
        except:
           pass
    return vvs
    
def parse_lv4(c):
    vvs = getclass_vv(c)
    tl  = c.data['dictionary']
    key = '{nl}{@st66d}{s15}'
    
    
    meaningfull_phrase = []
    for phrase in tl.values() :
        if key in phrase.lower():
            meaningfull_phrase.append(phrase)
    
    mapped_lv4 = {}
    err = []
    for phrase in meaningfull_phrase:
        string = phrase
        job = getclass_fromstring(c, string)
        if job in mapped_lv4:
            err.append(phrase)
        mapped_lv4[job] = string.replace('{nl} {nl}{@st66d}{s15}', '')
    
    for bonus4 in mapped_lv4:
        for vv in vvs:
            try:
                if bonus4 == vv['job'] and bonus4!='':
                    vv['Bonus'].append(['lv4', mapped_lv4[bonus4]])
            except:
                continue
        
    vv_check = []
    err = []
    for i in vvs:
        if 'job' not in i:
            err.append(i)
            continue
        try:
            job = c.data['jobs'][i['job']]['Name']
        except:
            job = ''
        check = [i['Name'],job]
        vv_check.append(check)