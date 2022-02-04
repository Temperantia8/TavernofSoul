import json

import subprocess 
import sys
import logging
from unpackIPF import importJSON
from os.path import join
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
    
    path = join('TavernofSoul', 'JSON_{}'.format(region), 'jobs.json')
    with open(path, 'r') as f:
        jobs = list(json.load(f).keys())
    
    for job in jobs:
        subprocess.run (['curl', '{}.tavernofsoul.com/planner/getJob?ids={}'.format(region,job)],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    