# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 19:49:09 2021

@author: Intel
"""

import subprocess
from os.path import join
import os
def revision_txt_read(revision_txt):
    if os.path.isfile(revision_txt):
        with open(revision_txt, 'r') as file:
            return file.readline()
    else:
        return 0
if __name__ == "__main__":
    subprocess.run(['git', 'pull'])
    version = ""
    for region in ['itos', 'ktos', 'ktest', 'jtos']:
        
        version = "{} | {} : {}".format(version , region, revision_txt_read(join("downloader","revision_{}.txt".format(region))))
    subprocess.run(['git', 'add', '.'])
    subprocess.run(['git', 'commit', '-m', '"{}"'.format(version)])
    subprocess.run(['git', 'push'])
        
    
