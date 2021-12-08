from django.shortcuts import render
from os.path import join
from django.http import HttpResponse
from Maps.models import Maps, Map_Item, Map_NPC, Map_Item_Spawn
# Create your views here.
APP_NAME = "Maps"
import math
import os
from django.http import Http404
from django.http import JsonResponse
from django.db.models import Q
from ipfparser.utils import *
def index(request):

    data = {}
    clsname                 = getFromGet(request, 'byClass',False)
    query                   = getFromGet(request, 'q','')
    order                   = getFromGet(request, 'order', 'updated-dsc')
    orders                  = order.split("-")
    type_n                  = getFromGet(request, 'type', '')
    srt                     = '' if orders[-1] == 'asc' else '-'
    types                   = Maps.objects.values_list('type').distinct()
    if (clsname):
        query                   = Q(id_name__icontains = query)    
    else:
        query                   = Q(name__icontains = query)



    data['curpage']         = int(getFromGet(request, 'page',1))
    data['item']            = Maps.objects.filter(query & Q(type__icontains = type_n)).order_by('{}{}'.format(srt, orders[0]))
    data['item_len']        = len(data['item'])
    data['item']            = data['item'] [(data['curpage']-1)*20:data['curpage']*20]
    data['type_n']          = type_n
    data['cls']             = clsname
    data['types']           = []
    data['order']           = order
    for i in types:
        if (i[0] == ''):
            continue
        data['types'].append(i[0])
    pages = list(range(math.ceil(data['item_len']/20) +1))
    pages.remove(0) #there's no page 0
    makePagination(request, data, pages, 11 )

    data['query'] = getFromGet(request, 'q','')
    return render(request, join(APP_NAME,"search.html"), data)

def item_detail(request, id):

    try:
        item = Maps.objects.get(ids = id)
    except:
        raise Http404
    data = {}
    data['item'] = item
    try:
        data['drop'] = list(Map_Item.objects.filter(map = item))
    except:
        pass

    try:
        data['npc'] = list(Map_NPC.objects.filter(map = item))
    except:
        pass

    try:
        data['itemSpawn'] = list(Map_Item_Spawn.objects.filter(map = item))
    except:
        pass




    return render(request, join(APP_NAME,"index.html"),data)