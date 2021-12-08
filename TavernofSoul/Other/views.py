from django.shortcuts import render
from os.path import join
from django.http import HttpResponse
from Other.models import Achievements
from django.http import Http404
# Create your views here.
APP_NAME = "Other"
import math
import os
from django.http import JsonResponse
from django.db.models import Q

from ipfparser.utils import *


def index(request):

    data = {}
    return render(request, join(APP_NAME,"index.html"), data)


def achieve(request):

    query                   = getFromGet(request, 'q','')
    data 					= {'item' : Achievements.objects.filter(name__icontains=query).all()}
    data['item_len']        = len(data['item'])
    data['curpage']         = int(getFromGet(request, 'page',1))
    data['query']           = query
    data['item']            = data['item'] [(data['curpage']-1)*20:data['curpage']*20]

    for i in data['item']:
        i.descriptions = i.descriptions.split('{nl}')
    pages = list(range(math.ceil(data['item_len']/20) +1))
    pages.remove(0) #there's no page 0
    makePagination(request, data, pages, 11 )
    return render(request, join(APP_NAME,"achieve.html"), data)
