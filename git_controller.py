# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 19:49:09 2021

@author: Intel
"""

import subprocess
from os.path import join
import os
import csv
def read_version(filename):
    rev = {}
    with open(filename, 'r') as f:
        w = csv.reader(f)
        for lines in w:
            if len(lines)<2:
                continue
            rev[lines[0]] = lines[1]
    return rev

if __name__ == "__main__":
    subprocess.run(['git', 'pull'])
    versions = read_version(join('downloader', 'revision.csv'))
    version = ""
    for region in ['itos', 'ktos', 'ktest', 'jtos','twtos']:
        version = "{} | {} : {}".format(version , region, versions[region])
    subprocess.run(['git', 'add', '.'])
    subprocess.run(['git', 'commit', '-m', '"{}"'.format(version)])
    subprocess.run(['git', 'push'])
        
    
