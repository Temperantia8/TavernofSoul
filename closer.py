# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 11:11:42 2021

@author: CPPG02619
"""
import json

import subprocess 
import sys
import logging
from unpackIPF import importJSON
if __name__ == "__main__":
    #last_patched = importJSON('version.txt')['patched'][-1]
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

    subprocess.run (['cp', '-r', '{}_unpack/ui.ipf/baseskinset'.format(region), '.'])
    subprocess.run(['rm', '-r', '{}_unpack//ui.ipf'.format(region)])
    subprocess.run(['rm', '-r', '{}_unpack//bg.ipf/'.format(region)])
    subprocess.run(['mkdir', '{}_unpack//ui.ipf'.format(region)])
    subprocess.run (['mv', 'baseskinset', '{}_unpack//ui.ipf'.format(region)])
    #subprocess.run(['git', 'add', '.'])
    #subprocess.run(['git', 'commit', '-m', '"{}"'.format(last_patched)])
    #subprocess.run(['git', 'push'])