from django.shortcuts import render
from os.path import join
from django.http import HttpResponse
from Attributes.models import Attributes
from Jobs.models import Jobs
from django.http import Http404
# Create your views here.
APP_NAME = "Attributes"
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
        query2.add(Q(skill__job__ids = job), Q.OR)
        query.add(query2, Q.AND)

    data['curpage']         = int(getFromGet(request, 'page',1))

    data['item']            = Attributes.objects.filter(query).order_by('ids')
    data['item_len']        = len(data['item'])
    data['item']            = data['item'] [(data['curpage']-1)*20:data['curpage']*20]
    data['jobs']            = Jobs.objects.all()


    for i in data['item']:
        i.descriptions = i.descriptions.split("{nl}")

    pages = list(range(math.ceil(data['item_len']/20) +1))
    pages.remove(0) #there's no page 0
    makePagination(request, data, pages, 11 )

    data['query'] = getFromGet(request, 'q','')
    return render(request, join(APP_NAME,"search.html"), data)

def item_detail(request, id):

    try:
        item = Attributes.objects.get(ids = id)
    except:
        raise Http404
    data = {}
    data['item'] = item

    data['refference'] = 0
    
    try:
        data['skills'] = item.skill.all()
    except:
        pass


    try:
        data['jobs'] = item.job.all()
    except:
        pass

    try:
        data['desc'] = item.descriptions.split('{nl}')
    except:
        pass

    data['item'].descriptions_required = data['item'].descriptions_required.replace('{nl}','').replace('{b}','') 

    return render(request, join(APP_NAME,"index.html"),data)