from django.shortcuts import render
from os.path import join
from django.http import HttpResponse
from Attributes.models import Attributes
from Jobs.models import Jobs
from Skills.models import Skills
from django.http import Http404
# Create your views here.
APP_NAME = "Skills"
import math
import os
from django.http import JsonResponse
from django.db.models import Q
from ipfparser.utils import *

def index(request):

    data = {}

    query                   = getFromGet(request, 'q','')
    query                   = Q(name__icontains = query)
    job                     = getFromGet(request, 'job', '')
    data['jobq']            = job


    if (job != ''):
        query2                  = Q(job__ids = job)
        query.add(query2, Q.AND)

    data['curpage']         = int(getFromGet(request, 'page',1))

    data['item']            = Skills.objects.filter(query).order_by('ids')
    data['item_len']        = len(data['item'])
    data['item']            = data['item'] [(data['curpage']-1)*20:data['curpage']*20]
    data['jobs']            = Jobs.objects.all()

    pages = list(range(math.ceil(data['item_len']/20) +1))
    pages.remove(0) #there's no page 0
    makePagination(request, data, pages, 11 )

    data['query'] = getFromGet(request, 'q','')
    return render(request, join(APP_NAME,"search.html"), data)

def item_detail(request, id):

    try:
        item = Skills.objects.get(ids = id)
    except:
        raise Http404
    data = {}
    data['item'] = item

    data['refference'] = 0
    
    try:
        data['attributes'] = item.attributes.all()
    except:
        pass

    data['specialvar']= [
        'CaptionRatio', 'CaptionRatio2', 'CaptionRatio3',
        'SkillSR', 'SpendItemCount', 'SkillFactor','CaptionTime',
        'SpendItemCount', 'SpendPoison', 'SpendSP' 
    ]
    data['desc'] = data['item'].descriptions.replace('{#DD5500}{ol}','').replace('{/}','').split('{nl}')
    data['effect'] = data['item'].effect.replace('{#339999}{ol}','').split('{nl}')
    ef = []
    for lines in data['effect']:
        lines = lines.replace('{','').replace('}','').replace('//','').split('#')
        ef.append(lines)
    data['effect'] = ef
    data['item'].cooldown = data['item'].cooldown/ 1000
    data['item'].stance = " ".join(data['item'].stance.split(';'))
    if data['item'].stance == "":
        data['item'].stance = "All"
    return render(request, join(APP_NAME,"index.html"),data)