from django.shortcuts import render
from os.path import join
from django.http import HttpResponse
from Buffs.models import Buffs
from Jobs.models import Jobs
from Skills.models import Skills
from django.http import Http404
# Create your views here.
APP_NAME = "Buffs"
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

    data['item']            = Buffs.objects.filter(query).order_by('ids')
    data['item_len']        = len(data['item'])
    data['item']            = data['item'] [(data['curpage']-1)*20:data['curpage']*20]

    pages = list(range(math.ceil(data['item_len']/20) +1))
    pages.remove(0) #there's no page 0
    makePagination(request, data, pages, 11 )

    data['query'] = getFromGet(request, 'q','')
    return render(request, join(APP_NAME,"search.html"), data)

def item_detail(request, id):

    try:
        item = Buffs.objects.get(ids = id)
    except:
        raise Http404
    data = {}
    data['item'] = item
    data['desc'] = data['item'].descriptions.replace('{#DD5500}{ol}','').replace('{/}','').split('{nl}')
    template = join(APP_NAME,"index.html")
    return render(request, template ,data)