from django.shortcuts import render
from django.http import JsonResponse
from Jobs.models import Jobs, getJobsByName
from Skills.models import Skills
from Attributes.models import Attributes
from os.path import join
import json
import re
from django.views.decorators.cache import cache_page
# Create your views here.
from django.templatetags.static import static
from django.db.models import Q
APP_NAME = 'Planner'
def imcFormatRemover(string):
    string = string.split('{nl}')
    s2 = []
    for i in string:
        s2.append( re.sub(r'\{(.*?)\}', '', i) )
    return s2

# def parseToJSfriendly(string):
#     specialvar= [
#         '{CaptionRatio}', '{CaptionRatio2}', '{CaptionRatio3}',
#         '{SkillSR}', '{SpendItemCount}', '{SkillFactor}','{CaptionTime}',
#         '{SpendItemCount}', '{SpendPoison}', '{SpendSP}' 
#         ]
#     new_string = ''
#     new_words = ''
#     words = string.split('#')
#     for word in words:
#         if word in specialvar:
#             word = word.replace('{','').replace('}','')
#             word = " <span class='{}'> </span> ".format(word)
#         new_words+= word
#     new_string+=new_words

#     return imcFormatRemover(new_string)



def parseEffect(effect, obj):
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
        # new_lines = []
        # for word in lines:
        #     if word in specialvar:
        #         if (obj[specialvar[word]] == None):
        #             continue
        #         word = obj[specialvar[word]][0]
        #     new_lines.append(word)
        ef.append(lines)
    return ef

#@cache_page(60 * 60)
def index(request):
    FUNCT_NAME = 'index'
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
                new_attrib.append(n_attr)
            k['attributes_set'] = new_attrib

            k['counter']            = count 
            k['effect']             = parseEffect(l.effect, k) 
            count+=1
            a['skills'].append(k)

        data['skills'].append(a)
    return render(request, join(APP_NAME,"index.html"), data)

def getTree(request):
    try:
        ids = request.GET['ids']
        tree = Jobs.objects.get(ids = ids).job_tree
        ret = {'tree' : tree}
        return JsonResponse(ret)
    except:
        ret = {} 
        ret = json.dumps(ret)
        return JsonResponse(ret)

def getTreeData(request):
    try:
        tree = request.GET['tree']
        tree = Jobs.objects.filter(job_tree = tree)
 
        ret = [{'name' : i.name, 'ids' : i.ids, 'icon':i.icon } for i in tree]
        return JsonResponse(ret)
    except:
        ret = {} 
        ret = json.dumps(ret)
        return JsonResponse(ret)
import pandas as pd

def getLast(item):
    if item!=None:
        return item[-1]
    return None

def getJob(request):
    jobs = Jobs.objects.all()
    data = {'skills' : []}
    for i in jobs:
        a = {}
        a['job'] = i.name
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
            k['sfr']                = getLast(l.sfr)
            k['descriptions']       = l.descriptions 
            
            k['max_lv']             = l.max_lv 
            k['overheat']           = l.overheat 
            k['captionratio1']      = getLast(l.captionratio1)
            k['captionratio2']      = getLast(l.captionratio2)
            k['captionratio3']      = getLast(l.captionratio3)
            k['captiontime']        = getLast(l.captiontime)
            k['skillsr']            = getLast(l.skillsr)
            k['spenditemcount']     = getLast(l.spenditemcount )
            k['spendsp']            = getLast(l.spendsp)
            k['spendpoison']        = getLast(l.spendpoison)
            k['other']              = getLast(l.other)
            k['stance']             = l.stance 

            k['counter']            = count 
            k['effect']             = l.effect
            count+=1
            a['skills'].append(k)

        data['skills'].append(a)
    return JsonResponse(data,safe=False)
    pass
    #try:
    # job = request.GET['ids']
    # job = Jobs.objects.get(ids = job)
    # skill = Skills.objects.filter(job = job)
    # jobs = {}
    # jobs['ids']     = job.ids 
    # jobs['name']    = job.name 
    # jobs['is_starter'] = job.is_starter 
    # skills = []
    # for s in skills:
    #     k = {} 
    #     k['ids']    = s.ids 
    #     k['name']   = k.name 
    #     k['max_lv'] = k.max_lv 
    #     k['descriptions'] = k.descriptions
    #     k['overheat']           = l.overheat 
    #     k['captionratio1']      = l.captionratio1
    #     k['captionratio2']      = l.captionratio2
    #     k['captionratio3']      = l.captionratio3
    #     k['captiontime']        = l.captiontime
    #     k['skillsr']            = l.skillsr
    #     k['spenditemcount']     = l.spenditemcount 
    #     k['spendsp']            = l.spendsp
    #     k['spendpoison']        = l.spendpoison
    #     k['other']              = l.other
    #     k['job']                = l.job 
    #     k['stance']             = l.stance 
    #     k['sfr']                = l.sfr[-1]
    #     skills.append(k)

    # ret = {'job' : jobs, 'skills' : skills }
    # return JsonResponse(ret, safe = False)
 
    #except:
    #    ret = {} 
    #    ret = json.dumps(ret)
    #    return JsonResponse(ret)