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

import os
from os.path import join, exists
import json
import logging

from shutil import copyfile, move, rmtree

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

            
def copyfiles(output):
    files = ['shared.ipf', 
             'ies_ability.ipf',
             'ies_client.ipf',
             'ies_drop.ipf',
             'ies_mongen.ipf',
             'ui.ipf',
             'bg.ipf',
             'language.ipf',
             'ies.ipf',
             'xml.ipf',]
    for i in files:
        if os.path.exists (join('extract',i)):
            subprocess.run(['cp', '-r', join('extract',i), join(output, i)])
            logging.warning("copying {}".format(i))

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
        
        if f.split(".")[-1]!= "ipf":
            patched.append(f)
            logging.warning("ignoring {}..".format(f))
            continue
        if f not in patched:
            logging.info("patching {}".format(f))
            cur_file = join(IPF_PATH, f)
            copyfile(cur_file, f)
            subprocess.run ([unpacker, f, 'decrypt'])
            subprocess.run([unpacker, f, 'extract']+ extension_needed)
            os.remove(f) 
            #os.remove(cur_file) 
            patched.append(f)
            copyfiles("{}_unpack".format(region))
            rmtree('extract')
            
    
    
    item        = {"patched" : patched}
    printJSON(item, file)
    
