from django.shortcuts import render
from os.path import join
from django.http import HttpResponse
from Attributes.models import Attributes
from Jobs.models import Jobs
from Skills.models import Skills
# Create your views here.
APP_NAME = "Jobs"
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

def item_detail(request, id):

    item = Jobs.objects.get(ids = id)
    data = {}
    data['item'] = item

    data['refference'] = 0
    
    skill = Skills.objects.filter(job = item)
    data['skills'] = []
    for i in skill:
        i.descriptions = i.descriptions.replace('{#DD5500}{ol}','').replace('{#993399}{ol}','').replace('{/}','').split('{nl}')
        data['skills'].append(i)


    attributes = Attributes.objects.filter(job__ids = data['item'].ids)
    
    data['attributes'] = []
    for i in attributes:
        i.descriptions = i.descriptions.replace('{#DD5500}{ol}','').replace('{#993399}{ol}','').replace('{/}','').split('{nl}')
        data['attributes'].append(i)
    try:
        data['desc'] = item.descriptions.split('{nl}')
    except:
        pass

    return render(request, join(APP_NAME,"index.html"),data)