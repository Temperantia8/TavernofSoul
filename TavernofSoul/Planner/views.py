from django.shortcuts import render
from django.http import JsonResponse
from Jobs.models import Jobs, getJobsByName
from Planner.models import Builds
from Skills.models import Skills
from Attributes.models import Attributes
from os.path import join
import json
import re
from django.views.decorators.cache import cache_page
# Create your views here.
from django.templatetags.static import static
from django.db.models import Q
from ipfparser.utils import *
from django.core.cache import cache

APP_NAME = 'Planner'
def imcFormatRemover(string):
    string = string.split('{nl}')
    s2 = []
    for i in string:
        s2.append( re.sub(r'\{(.*?)\}', '', i) )
    return s2


def parseEffect(effect):
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
    effect = effect.replace('{#339999}{ol}','').split('{nl}')
    ef = []
    for lines in effect:
        lines = lines.replace('{','').replace('}','').replace('//','').split('#')
        ef.append(lines)
    return ef

def countRank(request):
    if 'd' in request.GET:
        data = getFromGet(request, 'd', '').replace("%7B", "{").replace("%7D", "}")
        if data == '':
            return
        try:
            handler = Builds.objects.get(url = data)
        except:
            handler = Builds(url = data)
        handler.count   += 1
        handler.save()

        perclass        = data.split("{")[1:]
        count           = 0
        for i in perclass:
            oneclass = i.split("}")
            handler.classes.add(Jobs.objects.get(ids = oneclass[0]))


def rankview(request):
    pass

def index2(request):
    FUNCT_NAME = 'index3.html'
    deprecatedClass = [1005, #centurion
                        2012, #mimic
                        9001, #gm
                        4013, #shepperd
                        ]
    data = {}
    data['jobs'] = Jobs.objects.filter().exclude(ids__in = deprecatedClass)
    
    data['specialvar']= [
        'CaptionRatio', 'CaptionRatio2', 'CaptionRatio3',
        'SkillSR', 'SpendItemCount', 'SkillFactor','CaptionTime',
        'SpendItemCount', 'SpendPoison', 'SpendSP' 
        ]
    data['job_ids'] = [i.ids for i in data['jobs']]
    return render(request, join(APP_NAME,FUNCT_NAME), data)

@cache_page(60 * 70)
def getJob(request):
    ids = getFromGet(request, 'ids', False)
    if not ids :
        return JsonResponse({}, safe=False)
    
    job = cache.get('job-{}'.format(ids))
    if not job:
        job         = Jobs.objects.filter(ids = ids).values()[0]
        skills      = list(Skills.objects.filter(job = job['id']).values())
        count       = 0
        for k in skills:
            k['cooldown']           = k['cooldown'] /1000
            k['descriptions']       = imcFormatRemover(k['descriptions'] )
            k['counter']            = count 
            k['effect']             = parseEffect(k['effect']) 
            count+=1
            k['attributes_set']     = list(Attributes.objects.filter(skill__ids = k['ids']).values('name', 'descriptions','ids','max_lv','icon'))
            for attr in k['attributes_set']:
                attr['descriptions'] = attr['descriptions'].split('{nl}')
        job['skills'] = skills 
        cache.set('job-{}'.format(ids), job, timeout = 60*70)

    return JsonResponse(job, safe=False)



@cache_page(35 * 60)
def index(request):
    try:
        countRank(request)
    except:
        pass
    FUNCT_NAME = 'index'
    data = {}

    data = cache.get('planner')
    if not data:
        data = {}
        deprecatedClass = [1005, #centurion
                            2012, #mimic
                            9001, #gm
                            4013, #shepperd
                            ]
        data['jobs'] = Jobs.objects.filter().exclude(ids__in = deprecatedClass)
        data['skills'] = []
        data['specialvar']= [
            'CaptionRatio', 'CaptionRatio2', 'CaptionRatio3',
            'SkillSR', 'SpendItemCount', 'SkillFactor','CaptionTime',
            'SpendItemCount', 'SpendPoison', 'SpendSP' 
        ]


        jobs = Jobs.objects.all()
        for i in jobs:
            a = {}
            a['job'] = i
            a['skills'] = []
            s = Skills.objects.filter(job = i)
            count = 0
            
            for l in s:
                k = {}
                k['ids']                = l.ids 
                k['icon']               = l.icon 
                k['name']               = l.name
                k['cooldown']           = l.cooldown /1000
                k['sp']                 = l.sp 
                k['sfr']                = l.sfr 
                k['descriptions']       = imcFormatRemover(l.descriptions )  

                k['cooldown_lv']        = l.cooldown_lv
                k['max_lv']             = l.max_lv 
                k['overheat']           = l.overheat 
                k['captionratio1']      = l.captionratio1
                k['captionratio2']      = l.captionratio2
                k['captionratio3']      = l.captionratio3
                k['captiontime']        = l.captiontime
                k['skillsr']            = l.skillsr
                k['spenditemcount']     = l.spenditemcount 
                k['spendsp']            = l.spendsp
                k['spendpoison']        = l.spendpoison
                k['other']              = l.other
                k['job']                = l.job 
                k['stance']             = l.stance 
                k['attributes_set']     = l.attributes_set

                new_attrib = []
                for attr in k['attributes_set'].all():
                    n_attr = {}
                    n_attr['name'] = attr.name 
                    n_attr['descriptions'] = attr.descriptions.split("{nl}")
                    n_attr['ids'] = attr.ids
                    n_attr['icon'] = attr.icon
                    n_attr['max_lv'] = attr.max_lv
                    new_attrib.append(n_attr)
                k['attributes_set'] = new_attrib

                k['counter']            = count 
                k['effect']             = parseEffect(l.effect) 
                count+=1
                a['skills'].append(k)

            data['skills'].append(a)

        cache.set('planner', data, timeout=35*60)

    return render(request, join(APP_NAME,"index.html"), data)
