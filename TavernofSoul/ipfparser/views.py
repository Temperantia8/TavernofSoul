from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
import logging
import json
APP_NAME = "parser"
import os
from os.path import join
from django.conf import settings
from datetime import datetime
def index(request):
    FUNCT_NAME = "index"
    di = settings.CHANGES_DIR
    patches = os.listdir(di)
    data = []
    for i in patches:
        date = os.path.getmtime(join(di,i))
        date = datetime.fromtimestamp(date)
        date = date.strftime("%d-%m-%Y")
        dic = {'name' : i, 'date': date}
        data.append(dic)
        
        
    data = {'patches' : data}
    
    return render(request, join(APP_NAME,FUNCT_NAME,"search.html"), data)

def item_detail(request, id):
    logging.warning('parsing')
    FUNCT_NAME = "index"
    di = settings.CHANGES_DIR
    path = join(di, id)
    items = os.listdir(path)    
    json_tables = []
    for i in items:
        with open(join(path,i),'r', encoding="utf-8") as f:
            h = json.load(f)
        h['filename'] = i
        json_tables.append(h)
    
    true_tables = []
    for i in json_tables:
        
        filename = i['filename'].replace(".json", "")
        logging.warning('parsing {}'.format(filename))
        keys = []
        changes = {'changed':{},'changed_old':{},'removed':{},'added':{}}
        rows = []
        if 'status' in i:
            true_tables.append({"flag":True, 'status' :'new file..'  ,'filename':filename})
            continue
        for h in i:
            if h == 'filename':
                continue
            for k in i[h]:
                k['stat'] = h
                changes[h][k['ClassID']] = k
                rows.append(k['ClassID'])
                if len(k)>0:
                    
                    keys = list(k.keys())
        if len(keys)>200:
            true_tables.append({"flag":True, 'status': 'too long..' , 'filename':filename})
            continue
        table_row=[]
        for status in changes:
            for item in changes[status]:
                if status == 'changed':
                    table_row.append({'stat'    :status, 
                                      'data'    :changes[status][item], 
                                      'data_old':changes['changed_old'][item]})
                elif status=='changed_old':
                    continue
                else:
                    table_row.append({'stat'    :status, 
                                      'data'    :changes[status][item], 
                                      'data_old':""})
        table_row.sort(key=lambda x:x['data']['ClassID'])
        true_tables.append({'filename':filename, 'header':keys, 'rows':table_row})
    del(json_tables)
    # return JsonResponse({'data':true_tables})
    data = {'json' :true_tables}
    # logging.warning('parsing views')
    return render(request, join(APP_NAME,FUNCT_NAME,"index.html"), data)