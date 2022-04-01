from django.shortcuts import render
from os.path import join
from django.http import HttpResponse
from Monsters.models import Monsters, Item_Monster
from Maps.models import Maps,  Map_NPC
from django.http import Http404
# Create your views here.
APP_NAME = "Monsters"
import math
import os
from django.http import JsonResponse
from django.db.models import Q
from ipfparser.utils import *

def eva (hr):
    c = 0
    eva = hr
    if hr == 0:
        hr = 1
    while c <0.5: 
        eva+=1
        c = min(pow(eva/hr,0.65)-1, 0.5)
    return eva

def accuracy (eva):
    c = 0
    hr = 1
    while c >=0.: 
        hr+=1
        c = min(pow(eva/hr,0.65)-1, 0.5)
    return hr


def critrate(cdef):
    cr = cdef
    c = 0
    if cdef == 0:
        cdef = 1
    while c<0.5:
        cr+=1
        c = min (pow(cr/cdef,0.6)-1, 0.5)
    return cr

def critdef(cr):
    cdef = 1
    c = 0
    while c>=0:
        cdef+=1
        c = min (pow(cr/cdef,0.6)-1, 0.5)
    return cdef


def block(bp):
    br = bp
    c = 0
    if bp ==0:
        bp = 1
    while c<0.5:
        br+=1
        c = min (pow(br/bp,0.7)-1, 0.5)
    return br


def blockpen(br):
    bp = 1
    c = 0
    while c>=0:
        bp+=1
        c = min (pow(br/bp,0.7)-1, 0.5)
    return bp


def unpack(item):
    unpacked = [] 
    for i in item:
        if i[0] == "":
            continue

        unpacked.append(i[0])
    return unpacked

def index(request):

    data = {}
    data['Race']                   = unpack(Monsters.objects.values_list("race").distinct())
    data['Armor']                   = unpack(Monsters.objects.values_list("armor").distinct())
    data['Attribute']               = unpack(Monsters.objects.values_list("element").distinct())
    data['race']            = getFromGet(request, 'race',False)
    data['armor']            = getFromGet(request, 'armor',False)
    data['attribute']            = getFromGet(request, 'attribute',False)

    order                   = getFromGet(request, 'order', 'updated-dsc')
    data['order']           = getFromGet(request, 'order', 'updated-dsc')
    orders                  = order.split("-")
    srt                     = '' if orders[-1] == 'asc' else '-'
    clsname                 = getFromGet(request, 'byClass',False)
    query                   = getFromGet(request, 'q','')
    if (clsname):
        query                   = Q(id_name__icontains = query)    
    else:
        query                   = Q(name__icontains = query)
    data['curpage']         = int(getFromGet(request, 'page',1))

    query.add(Q(race__icontains =getFromGet(request, 'race',"")), Q.AND)
    query.add(Q(armor__icontains =getFromGet(request, 'armor',"")), Q.AND)
    query.add(Q(element__icontains =getFromGet(request, 'attribute',"")), Q.AND)


    data['item']            = Monsters.objects.filter(query).order_by('ids').order_by('{}{}'.format(srt, orders[0]))
    data['item_len']        = len(data['item'])
    data['item']            = data['item'] [(data['curpage']-1)*20:data['curpage']*20]
    data['cls']             = clsname


    pages = list(range(math.ceil(data['item_len']/20) +1))
    pages.remove(0) #there's no page 0
    makePagination(request, data, pages, 11 )

    data['query'] = getFromGet(request, 'q','')
    return render(request, join(APP_NAME,"search.html"), data)

def item_detail(request, id):

    try:
        item = Monsters.objects.get(ids = id)
    except:
        raise Http404
    data = {}
    data['item'] = item

    data['refference'] = 0
    
    try:
        data['drop'] = list(Item_Monster.objects.filter(monster = item))
        if (len(data['dropped']) != 0):
            data['refference'] = 1
    except:
        pass

    try:
        desc = data['item'].descriptions
        lines = desc.split('{nl}')
        data['desc'] = lines
    except:
        pass

    try:
        data['spotted']  = list(Map_NPC.objects.filter(monster = item))
    except:
        pass

    data['eva'] = eva(data['item'].accuracy)
    data['iblock'] = block(data['item'].blockpen )
    data['critrate'] = critrate(data['item'].critdef)
    data['accuracy'] = accuracy(data['item'].eva)
    data['blockpen'] = blockpen(data['item'].block)
    data['critdef'] = critdef(data['item'].critrate)
    try:
        
        data['skills'] = item.skill_monster_set.all()
    except:
        pass


    return render(request, join(APP_NAME,"index.html"),data)
