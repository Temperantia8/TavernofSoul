from django.shortcuts import render
from os.path import join
from django.http import HttpResponse
from Attributes.models import Attributes
from Items.models import Equipment_Bonus
from Jobs.models import Jobs
from Skills.models import Skills
# Create your views here.
APP_NAME = "Jobs"
import math
import os
from django.http import JsonResponse
from django.db.models import Q
from ipfparser.utils import *
from Items.constants import bonus_stat_translator
from django.http import Http404
def index(request):

    data = {}

    query                   = getFromGet(request, 'q','')
    query                   = Q(name__icontains = query)
    job                     = getFromGet(request, 'job', '')
    data['jobq']            = job


    if (job != ''):
        job_start           = Jobs.objects.get(ids = job)
        query.add(Q(job_tree = job_start.job_tree), Q.AND)

    data['curpage']         = int(getFromGet(request, 'page',1))

    data['item']            = Jobs.objects.filter(query).order_by('ids')
    data['item_len']        = len(data['item'])
    data['item']            = data['item'] [(data['curpage']-1)*20:data['curpage']*20]
    data['jobs']            = Jobs.objects.filter(is_starter = True)


    for i in data['item']:
        i.descriptions = i.descriptions.split("{nl}")

    pages = list(range(math.ceil(data['item_len']/20) +1))
    pages.remove(0) #there's no page 0
    makePagination(request, data, pages, 11 )

    data['query'] = getFromGet(request, 'q','')
    return render(request, join(APP_NAME,"search.html"), data)

specialvar= {
        'CaptionRatio'  : 'captionratio1', 
        'CaptionRatio2' : 'captionratio2', 
        'CaptionRatio3' : 'captionratio3',
        'SkillSR'       : 'skillsr', 
        'SpendItemCount': 'spenditemcount' , 
        'SkillFactor'   : 'sfr',
        'CaptionTime'   : 'captiontime',
        'SpendItemCount': 'spenditemcount', 
        'SpendPoison'   : 'spendpoison',   
        'SpendSP'       : 'spendsp'
    }
def parseEffect(effect):
    
    effect = effect.replace('{#339999}{ol}','').split('{nl}')
    ef = []
    for lines in effect:
        lines = lines.replace('{','').replace('}','').replace('//','').split('#')
        ef.append(lines)
    return ef

def item_detail(request, id):
    try:
        item = Jobs.objects.get(ids = id)
    except:
        raise Http404
    data = {}
    data['item'] = item

    data['refference'] = 0
    
    skill = Skills.objects.filter(job = item)
    data['skills'] = []
    for i in skill:
        i.descriptions = i.descriptions.replace('{#DD5500}{ol}','').replace('{#993399}{ol}','').replace('{/}','').split('{nl}')
        i.effect = parseEffect(i.effect)
        data['skills'].append(i)


    attributes = Attributes.objects.filter(job__ids = data['item'].ids)

    # try:
    bonus_db = list(Equipment_Bonus.objects.filter(equipment = item.vaivora))
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
    # except:
        # pass

    
    data['attributes'] = []
    for i in attributes:
        i.descriptions = i.descriptions.replace('{#DD5500}{ol}','').replace('{#993399}{ol}','').replace('{/}','').split('{nl}')
        data['attributes'].append(i)
    try:
        data['desc'] = item.descriptions.split('{nl}')
    except:
        pass
    data['specialvar'] = specialvar

    return render(request, join(APP_NAME,"index.html"),data)