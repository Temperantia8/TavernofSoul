from django.shortcuts import render
from os.path import join
from django.http import HttpResponse
from Items.models import Items, Equipment_Bonus, Item_Recipe_Material
from Items.models import Equipments
from Items.models import Item_Collection_Material, Item_Collection_Bonus
from Monsters.models import Monsters, Item_Monster
from Maps.models import Maps, Map_Item, Map_NPC, Map_Item_Spawn
from django.http import Http404
# Create your views here.
APP_NAME = "Items"
import math

import os
from django.http import JsonResponse
from django.db.models import Q
from Items.constants import bonus_stat_translator, goddess_anvil, goddess_scale, goddess_gabija, goddess_chance, getGoddess
from Items.getEnhancement import getAnvil
from ipfparser.utils import *

def index(request):

    data = {}
    data['types']               = []
    in_type                     = []
    types                       = Items.objects.values('type')
    for i in Items.objects.values('type').distinct() :
        data['types'].append({'type':i['type'], 'id' : i['type']})
    for i in Equipments.objects.values('type_equipment').distinct() :
        data['types'].append({'type':i['type_equipment'], 'id' : i['type_equipment']})
    # data['types'] = list(set(data['types']))

    if 'q' in request.GET:
        query                       = getFromGet(request, 'q','')
        grade                       = getFromGet(request,'grade', '')
        clas                        = getFromGet(request,'class', '')
        class_def                   = ['.','.','.','.','.']
        query                       = Q(name__icontains = query)
        type_n                      = getFromGet(request, 'type', '')
        minLV                       = getFromGet(request, 'lvmin', '')
        maxLV                       = getFromGet(request, 'lvmax', '')
        order                       = getFromGet(request, 'order', 'updated-dsc')



        if minLV != '':
            try:
                int(minLV)
                query.add(Q(equipments__level__gte =minLV), Q.AND)
            except:
                pass
        if maxLV != '':
            try:
                int(maxLV)
                query.add(Q(equipments__level__lte =maxLV), Q.AND)
            except:
                pass

        if (type_n != ''):
            if ('_eq' in type_n):
                query.add(Q(equipments__type_equipment =type_n), Q.AND)
            else:
                query.add(Q(type =type_n), Q.AND)

        data['type'] = getFromGet(request, 'type', '')


        if (grade != ''):
            query.add(Q(grade=grade), Q.AND)
        if clas!= '':
            class_def[int(clas)] = 'T'
            class_def = ''.join(class_def)
            query.add(Q(equipments__requiredClass__regex =class_def), Q.AND)

        orders = order.split("-")
        srt = '' if orders[-1] == 'asc' else '-'
        data['curpage']     = int(getFromGet(request, 'page',1))
        if ('eq' in order):
            data['item']            = Items.objects.filter(query).order_by('{}equipments__{}'.format(srt, orders[1]))
        else:
            data['item']            = Items.objects.filter(query).order_by('{}{}'.format(srt, orders[0]))

        data['item_len']        = len(data['item'])
        data['item']            = data['item'] [(data['curpage']-1)*10:data['curpage']*10]
        query                   = getFromGet(request, 'q','')
        data['query']           = query 
        data['class']           = clas
        data['grade']           = grade
        data['minLV']           = minLV
        data['maxLV']           = maxLV
        data['order']           = order
        #creating pages
        pages = list(range(math.ceil(data['item_len']/10) +1))
        pages.remove(0) #there's no page 0
        makePagination(request, data, pages, 11 )
        # data['item']            = []
        # return JsonResponse(data, safe=False)
        
        
    return render(request, join(APP_NAME,"search.html"), data)

def item_detail(request, id):

    try:
        item = Items.objects.get(ids__contains = id)
    except:
        raise Http404
    data = {}
    data['item'] = item
    trade = []
    if item.tradability[0] == 'T':
        trade.append("Market")
    if item.tradability[1] == 'T':
        trade.append("Personal")
    if item.tradability[2] == 'T':
        trade.append("Shop")
    if item.tradability[3] == 'T':
        trade.append("Team")
    item.tradability = ", ".join(trade)
    if len(trade) ==0:
        item.tradability = "None"


    try:
        classes = []
        if (item.equipments.requiredClass[0] == 'T'):
            classes.append('Archer')
        if (item.equipments.requiredClass[1] == 'T'):
            classes.append('Cleric')
        if (item.equipments.requiredClass[2] == 'T'):
            classes.append('Scout')
        if (item.equipments.requiredClass[3] == 'T'):
            classes.append('Swordman')
        if (item.equipments.requiredClass[4] == 'T'):
            classes.append('Wizard')
        if len(classes) >0:
            data['item'].equipments.requiredClass = ", ".join(classes)
        else:
            data['item'].equipments.requiredClass = "None"
    except:
        pass
    try:
        bonus_db = list(Equipment_Bonus.objects.filter(equipment = item.equipments))
        bonus_all = []
        for i in bonus_db:
            bonus = {}
            if i.bonus_stat in bonus_stat_translator:
                bonus['bonus_stat'] = bonus_stat_translator[i.bonus_stat]
            else:
                bonus['bonus_stat'] = i.bonus_stat
            bonus['bonus_val']  = i.bonus_val.replace('{img green_up_arrow 16 16}', '▲')\
                                        .replace('{img green_down_arrow 16 16}', '▼')
            bonus['bonus_val'] = bonus['bonus_val'].split('{nl}')
            bonus_all.append(bonus)
        data['equipment_bonus'] = bonus_all
    except:
        pass

    data['refference'] = 0
    try:
        data['materialRecipe'] = list(Item_Recipe_Material.objects.filter(material = item))
        if (len(data['materialRecipe']) != 0):
            data['refference'] = 1
    except:
        pass
    try:
        data['targetRecipe'] = list(Item_Recipe_Target.objects.filter(target = item))
        if (len(data['targetRecipe']) != 0):
            data['refference'] = 1
    except:
        pass
    try:
        data['item'].descriptions = data['item'].descriptions.replace("{img star_mark 20 20}", "★")
    except:
        pass

    try:
        data['materialRecipe'] = list(Item_Recipe_Material.objects.filter(recipe = item.recipes))
    except:
        pass

    try:
        data['target'] = Item_Recipe_Target.objects.filter(recipe = item.recipes)
    except:
        pass

    try:
        data['collectionMaterialFor'] = list(Item_Collection_Material.objects.filter(material = item))
        if (len(data['collectionMaterialFor']) != 0):
            data['refference'] = 1
    except:
        pass

    try:
        data['mapDrop'] = list(Map_Item.objects.filter(item = item))
        if (len(data['mapDrop']) != 0):
            data['refference'] = 1
    except:
        pass

    try:
        data['foundAt'] = list(Map_Item_Spawn.objects.filter(item = item))
        if (len(data['foundAt']) != 0):
            data['refference'] = 1
    except:
        pass


    try:
        data['collectionMaterial'] = list( Item_Collection_Material.objects.filter(collection = item.collections))
    except:
        pass

    try:
        data['collectionBonus'] = list( Item_Collection_Bonus.objects.filter(collection = item.collections))
    except:
        pass

    try:
        data['pages'] = []
        pages = item.books.text.split("{np}")
        for i in pages:
            i = i.replace('\\-', '')
            i = i.replace('\\', '')
            lines = i.split("{nl}") 

            data['pages'].append(lines)
    except:
        pass
    try:
        desc = data['item'].descriptions
        lines = desc.split('{nl}')
        data['desc'] = lines
    except:
        pass

    try:
        data['dropped'] = list(Item_Monster.objects.filter(item = item))
        if (len(data['dropped']) != 0):
            data['refference'] = 1
    except:
        pass

    try:
        if item.equipments:
            if item.grade == 6:
                data['mat'], data['reinf'], data['tc_cost'] = getAnvil(item)
            else:
                data['reinf'], data['reinf_price'], data['tc_cost'] = getAnvil(item)

    except:
        pass
    # if item.grade==6:
    # data['item']            = []
    # return JsonResponse(data, safe=False)
    return render(request, join(APP_NAME,"index.html"),data)
