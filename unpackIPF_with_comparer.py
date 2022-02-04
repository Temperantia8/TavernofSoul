# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 22:42:59 2021

@author: Intel
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 22:41:30 2021

@author: Intel
"""

import subprocess 
import io
import csv
import os
from os.path import join, exists
import json
import logging

from shutil import copyfile

def importJSON(file):
    if not exists(file):
        return {}
    try:
        with open(file, "r") as f:
            data = json.load(f)
    except:
        logging.error("error in importing file {}".format(file))
        return {}
    return data



def printJSON(item, file):
    with open(file, "w") as f:
        json.dump(item,f)


def compare(oldfilename, newfilename):
    oldfile = []
    try:
        with io.open(oldfilename, 'r',  encoding="utf-8") as ies_file:
             for row in csv.DictReader(ies_file, delimiter=',', quotechar='"'):
                 oldfile.append(row)
    except:
        return {'status':"new file"}
    newfile = []
    try:
        with io.open(newfilename, 'r',  encoding="utf-8") as ies_file:
             for row in csv.DictReader(ies_file, delimiter=',', quotechar='"'):
                 newfile.append(row)
    except:
        return False
    dict_prev = {}
    dict_now = {}     
    if 'ClassID' in oldfile[0]:
        count = 1
        for item in oldfile:
            item['row'] = count
            dict_prev[item['ClassID']] = item
            count+=1
        count = 1
        for item in newfile:
            item['row'] = count
            dict_now [item['ClassID']] = item
            count+=1
    changes = {'changed' : [], 'changed_old': [], 'added' : [], 'deleted' : []}
    
    for item  in dict_now:
        if item not in dict_prev:
            changes['added'].append(dict_now[item])
        else:
            a = dict_now[item]['row']
            b = dict_prev[item]['row'] 
            dict_now[item]['row'] = 0
            dict_prev[item]['row'] = 0
            if (dict_now[item] != dict_prev[item]):
                dict_now[item]['row'] = a
                dict_prev[item]['row'] = b
                changes['changed'].append(dict_now[item])
                changes['changed_old'].append(dict_prev[item])
            dict_now[item]['row'] = a
            dict_prev[item]['row'] = b
    for item in dict_prev:
        if item not in dict_now:
            changes['removed'].append(dict_prev[item])
    return changes
            
def copyfiles(output):
    subprocess.run(['cp', '-r', join(output,'shared.ipf'), 'lua'])
    subprocess.run(['cp', '-r', join(output,'ies_ability.ipf'), 'lua'])
    subprocess.run(['cp', '-r', join(output,'ies_drop.ipf'), 'lua'])
    subprocess.run(['cp', '-r', join(output,'ies_mongen.ipf'), 'lua'])
    subprocess.run(['cp', '-r', join(output,'ui.ipf'), 'lua'])
    subprocess.run(['cp', '-r', join(output,'bg.ipf'), 'lua'])
    subprocess.run(['cp', '-r', join(output,'language.ipf'), 'lua'])
    subprocess.run(['cp', '-r', join(output,'ies.ipf'), 'lua'])
    

def compareAll(ipf_name, region):
    files_inp = os.listdir(join("{}_unpack_temp",'ies.ipf'))
    for i in files:
        changes = compare(join("{]_unpack".format(region),'ies.ipf',i), join("{}_unpack_temp",'ies.ipf', i))
        with open(join("{}_changes".format(region),'{}.csv'.format(i)), 'w') as f:  # You will need 'wb' mode in Python 2.x
            w = csv.DictWriter(f, changes.keys())
            w.writeheader()
            w.writerow(changes)
    
import sys
file        = 'version.txt'
IPF_PATH    = join("..", "ipf")
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
    file = 'unpacker_version_{}.txt'.format(region.lower())
    IPF_PATH    = "{}_patch".format(region)
    OUTPUT_PATH = "{}_unpack".format(region)
    #print(os.getcwd())
    
    logging.basicConfig(level=logging.DEBUG)
    unpacker    = join('IPFUnpacker', 'ipf_unpack')
    logging.warning("region : {}".format(region))
    patched     = importJSON(file)['patched']
    
    cwd = os.getcwd()
    search_dir = IPF_PATH
    os.chdir(search_dir)
    files = filter(os.path.isfile, os.listdir())
    files = [ f for f in files] # add path to each file
    files.sort(key=lambda x: os.path.getmtime(x))
    
    os.chdir(cwd)
    files.sort()
    extension_needed = ['ies', 'xml', 'lua','png', 'jpg', 'tga', 'json','tok', 'colmesh', 'tsv'   ]
    for f in files:
        if f not in patched:
            logging.info("patching {}".format(f))
            cur_file = join(IPF_PATH, f)
            copyfile(cur_file, join(OUTPUT_PATH,f))
            subprocess.run ([unpacker, f, 'decrypt'])
            subprocess.run([unpacker, f, 'extract']+ extension_needed)
            os.remove(cur_file, region) 
            patched.append(f)
            os.mkdir("{}_unpack_temp")
            copyfiles("{}_unpack_temp".format(region))
            subprocess.run(['rm', '-r', "{}_unpack_temp".format(region)])
            compareAll(f)
            copyfiles("{}_unpack".format(region))
            subprocess.run(['rm', '-r', 'extract'])
            subprocess.run(['rm', f])
    
    
    item        = {"patched" : patched}
    printJSON(item, file)
    
