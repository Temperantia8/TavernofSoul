from django.shortcuts import render
from os.path import join
from django.http import HttpResponse
from Items.models import Items, Equipment_Bonus, Item_Recipe_Material
from Items.models import Item_Recipe_Target,Item_Type
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

goddess_anvil     = [219,219,219,219,219,
                                     238,238,238,238,238,
                                     256,256,256,256,256,
                                     275,275,275,275,275,
                                     294,294,294,294,294,
                                     294,294,294,294,294,]
goddess_scale     = [3,3,3,3,3,
                     5,5,5,5,5,
                     7,7,7,7,7,
                     8,8,8,8,8,
                     10,11,12,13,14,
                     15,16,17,18,19                    
                     ]
goddess_gabija    = [263,263,263,263,450,
                     450,450,450,450,673,
                     673,673,673,673,927,
                     927,1212,1523,1861,2224,
                     2586,2948,3311,3673,4036,
                     4398,4760,5123,5485,5848]

goddess_chance      = [100,100,100,100,100,
                                          80, 72, 64, 58, 52,
                                          42, 33, 27, 21, 18,
                                          12,  8,  6,  4,  3, 
                                           2, 1,  1,  1,  1 ,
                                           1, 1,  1,  1,  1]

bonus_stat_translator={
    'ADD_CLOTH'     : 'Attack against Cloth Armored Targets',
    'ADD_LEATHER'   : 'Attack against Leather Armored Targets',
    'ADD_CHAIN'     : 'Attack against Chain Armored Targets',
    'ADD_IRON'      : 'Attack against Plate Armored Targets',
    'ADD_GHOST'     : 'Attack against Ghost Armored Targets',
    'ADD_SMALLSIZE' : 'Attack against Small-sized Targets',
    'ADD_MIDDLESIZE': 'Attack against Medium-sized Targets',
    'ADD_LARGESIZE' : 'Attack against Large-sized Targets',
    'ADD_FORESTER'  : 'Attack against Plant-type Targets',
    'ADD_WIDLING'   : 'Attack against Beast-type Targets',
    'ADD_VELIAS'    : 'Attack against Devil-type Targets',
    'ADD_PARAMUNE'  : 'Attack against Mutant-type Targets',
    'ADD_KLAIDA'    : 'Attack against Insect-type Targets',
    'Aries'         : 'Piercing',
    'AriesDEF'      : 'Piercing Defense',
    'SlashDEF'      : 'Slash Defense',
    'StrikeDEF'     : 'Strike Defense',
    'ADD_FIRE'      : 'Add. Fire Property Damage',
    'ADD_ICE'       : 'Add. Ice Property Damage',
    'ADD_POISON'    : 'Add. Poison Property Damage',
    'ADD_LIGHTNING' : 'Add. Lightning Property Damage',
    'ADD_SOUL'      : 'Add. Soul Property Damage',
    'ADD_EARTH'     : 'Add. Earth Property Damage',
    'ADD_HOLY'      : 'Add. Holy Property Damage',
    'ADD_DARK'      : 'Add. Dark Property Damage',
    'RES_FIRE'      : 'Fire Property Resistance',
    'RES_ICE'       : 'Ice Property Resistance',
    'RES_POISON'    : 'Poison Property Resistance',
    'RES_LIGHTNING' : 'Lightning Property Resistance',
    'RES_SOUL'      : 'Soul Property Resistance',
    'RES_EARTH'     : 'Earth Property Resistance',
    'RES_HOLY'      : 'Holy Property Resistance',
    'RES_DARK'      : 'Dark Property Resistance',
    'LootingChance' : 'Looting Chance',
    'UNKNOWN'       : '-'
}

from ipfparser.utils import *

def index(request):

    data = {}
    data['types']       = []
    types                       = Item_Type.objects.all()
    for i in types:
        if (i.is_equipment):
            data['types'].append({'type':i.name.lower(), 'id' : str(i.id)+"_eq"})
        else:
            data['types'].append({'type':i.name.lower(), 'id' : str(i.id)})

    if 'q' in request.GET:
        query                           = getFromGet(request, 'q','')
        grade                       = getFromGet(request,'grade', '')
        clas                            = getFromGet(request,'class', '')
        class_def             = ['.','.','.','.','.']
        query                           = Q(name__icontains = query)
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
                type_n = type_n.replace('_eq','')
                t = Item_Type.objects.get(id = type_n)
                query.add(Q(equipments__type_equipment =t.name), Q.AND)
            else:
                t = Item_Type.objects.get(id = type_n)
                query.add(Q(type =t.name), Q.AND)

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
            data['item']            = list(Items.objects.filter(query).order_by('{}equipments__{}'.format(srt, orders[1])))
        else:
            data['item']            = list(Items.objects.filter(query).order_by('{}{}'.format(srt, orders[0])))

        data['item_len']    = len(data['item'])
        data['item']            = data['item'] [(data['curpage']-1)*10:data['curpage']*10]
        query                           = getFromGet(request, 'q','')
        data['query']       = query 
        data['class']           = clas
        data['grade']           = grade
        data['minLV']           = minLV
        data['maxLV']           = maxLV
        data['order']           = order
        #creating pages
        pages = list(range(math.ceil(data['item_len']/10) +1))
        pages.remove(0) #there's no page 0
        makePagination(request, data, pages, 11 )

        
        
    return render(request, join(APP_NAME,"search.html"), data)

def item_detail(request, id):

    try:
        item = Items.objects.get(ids = id)
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

    if item.grade == 6:
        data['scale']   = goddess_scale
        data['anvil']   = goddess_anvil
        data['chance']  = goddess_chance
        data['gabija']  = goddess_gabija

    return render(request, join(APP_NAME,"index.html"),data)
