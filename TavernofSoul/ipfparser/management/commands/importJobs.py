# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 14:08:20 2021

@author: Temperantia
"""

"""
#run this first if from spyder (dev purpose)

import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TavernofSoul.settings")
django.setup()

"""

from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
import logging
import json
from os.path import join, exists
from Items.models import Items
from Jobs.models import Jobs
from Skills.models import Skills, Stance
from Attributes.models import Attributes

class Command(BaseCommand):
    
    base_path               = settings.JSON_ROOT
    jobs_path               = join(base_path, "job.json")
    jobs_by_name_path       = join(base_path, "job_by_name.json")
    attributes_by_name_path = join (base_path, "attributes_by_name.json")
    attributes_path         = join (base_path, "attributes.json")
    skills_path             = join(base_path, "skills.json")
    skills_by_name_path     = join(base_path, "skills_by_name.json")
        
    def importJSON(self,file):
        if not exists(file):
            return {}
        try:
            with open(file, "r") as f:
                data = json.load(f)
        except:
            logging.error("error in importing file {}".format(file))
            return {}
        return data
    

    def add_arguments(self, parser):
        parser.add_argument('-u', '--update', type=int, help='Indicate wether ignore any \
                            existing data or update them')
        parser.add_argument('-all', '--all_item', type=bool, help='update all item')
       
    
    def escaper(self,string):
        string = str(string)
        escaped = string.translate(str.maketrans({"-":  r"\-",
                                              "]":  r"\]",
                                              "\\": r"\\",
                                              "^":  r"\^",
                                              "$":  r"\$",
                                              "*":  r"\*",
                                              ".":  r"\.",
                                              "'" : r"\'",
                                              '"' : r'\"',
                                              ',' :r''
                                              
                                              }))
        return escaped
        
    def handle(self,  *args, **kwargs):
        logging.basicConfig(level=logging.DEBUG)
        update = kwargs['update']
        if update == None:
            update = 1

        jobs           = self.importJSON(self.jobs_path)
        
        attrib         = self.importJSON(self.attributes_path)
        
        skills         = self.importJSON(self.skills_path)
        
        
        if kwargs['all_item']:
           self.importJobs(jobs, update)
           self.importSkills(skills, update)
           self.importAttrib(attrib, update)
    
    
    def importJobs(self,jobs, update ):
        logging.debug("migrating monsters")
        count = 0
        count_all = len(jobs.values())
        
        for i in jobs.values() :
            flag_u = False
            try :
                handler = Jobs.objects.get(ids= i['$ID'])
                flag_u = True
                if update == 0:
                    logging.info("skipping ({}/{})  {}".format(count,count_all,i['Name']))
                    
                else:
                    logging.info("updating ({}/{})  {}".format(count,count_all,i['Name']))
            except:
                handler = Jobs()
                logging.info("inserting ({}/{})  {}".format(count,count_all,i['Name']))
            
            if flag_u and update == 0:
                count+=1
                continue
            
            handler.ids             = i['$ID']
            handler.id_name         = i['$ID_NAME']            
            handler.name            = i['Name']
            handler.is_starter      = i['IsStarter']
            handler.job_tree        = i['JobTree']
            handler.icon            = i['Icon']
            handler.descriptions    = i['Description']
            handler.save()
            count+=1
        
    def importSkills(self,skills, update ):
        logging.debug("migrating monsters")
        count = 0
        count_all = len(skills)
        stances_db = list(Skills.objects.all())
        stances  = {}
        for s in stances_db:
            stances[s.name] = s
        for i in skills.values() :
            flag_u = False
            try :
                handler = Skills.objects.get(ids= i['$ID'])
                flag_u = True
                if update == 0:
                    logging.info("skipping ({}/{})  {}".format(count,count_all,i['Name']))
                    
                else:
                    logging.info("updating ({}/{})  {}".format(count,count_all,i['Name']))
            except:
                handler = Skills()
                logging.info("inserting ({}/{})  {}".format(count,count_all,i['Name']))
            
            if flag_u and update == 0:
                count+=1
                continue
            if i['Link_Job'] == None:
                continue
            
            handler.ids             = i['$ID']
            handler.id_name         = i['$ID_NAME']            
            handler.name            = i['Name']
            handler.icon            = i['Icon']
            handler.descriptions    = i['Description']
            if 'BasicCoolDown' in i:
                handler.cooldown        = i['BasicCoolDown']
            else:
                handler.cooldown        = 0
            handler.sp              = i['BasicSP']
            
            handler.effect          = i['Effect']
            handler.element         = i['Element']
            handler.max_lv          = i['MaxLevel']
            handler.unlock          = i['UnlockClassLevel']
            handler.overheat        = i['OverHeat']
            
            if 'sfr' in i:
                handler.sfr             = i['sfr']
            if 'CaptionRatio' in i:
                try:
                    for h in i['CaptionRatio']:
                        h = int(h)
                except:
                    i['CaptionRatio'] = None
                handler.captionratio1   = i['CaptionRatio']
            if 'CaptionRatio2' in i:
                try:
                    for h in i['CaptionRatio2']:
                        h = int(h)
                except:
                    i['CaptionRatio2'] = None
                handler.captionratio2   = i['CaptionRatio2']
            if 'CaptionRatio3' in i:
                try:
                    for h in i['CaptionRatio3']:
                        h = int(h)
                except:
                    i['CaptionRatio3'] = None
                handler.captionratio3   = i['CaptionRatio3']
            if 'CaptionTime' in i:
                try:
                    for h in i['CaptionTime']:
                        h = int(h)
                except:
                    i['CaptionTime'] = None
                handler.captiontime     = i['CaptionTime']
            if 'SkillSR' in i:
                try:
                    for h in i['SkillSR']:
                        h = int(h)
                except:
                    i['SkillSR'] = None
                handler.skillsr     = i['SkillSR'] 
            if 'SpendItemCount' in i:
                try:
                    for h in i['SpendItemCount']:
                        h = int(h)
                except:
                    i['SpendItemCount'] = None
                handler.spenditemcount  = i['SpendItemCount'] 
            if 'SpendPoison' in i:
                try:
                    for h in i['SpendPoison']:
                        h = int(h)
                except:
                    i['SpendPoison'] = None
                handler.spendpoison     = i['SpendPoison'] 
            if 'SpendSP' in i:
                try:
                    for h in i['SpendSP']:
                        h = int(h)
                except:
                    i['SpendSP'] = None
                handler.spendsp     = i['SpendSP'] 
            handler.save()
            for h in i['RequiredStance']:
                if h['Name'] not in stances:
                    stance = Stance()
                    stance.icon = h['Icon']
                    stance.name = h['Name']
                    stance.save()
                    stances[stance.name] = stance
                else:
                    stance = stances[h['Name']]
                handler.stance.add(stance)
            handler.job = Jobs.objects.get(ids = i['Link_Job'])
            handler.save()
            count+=1
    

    def importAttrib (self,attrib, update ):
        logging.debug("migrating monsters")
        count = 0
        count_all = len(attrib.values())
        
        for i in attrib.values() :
            flag_u = False
            try :
                handler = Attributes.objects.get(ids= i['$ID'])
                flag_u = True
                if update == 0:
                    logging.info("skipping ({}/{})  {}".format(count,count_all,i['Name']))
                    
                else:
                    logging.info("updating ({}/{})  {}".format(count,count_all,i['Name']))
            except:
                handler = Attributes()
                logging.info("inserting ({}/{})  {}".format(count,count_all,i['Name']))
            
            if flag_u and update == 0:
                count+=1
                continue
            if (handler.max_lv == -1):
                continue
            handler.ids             = i['$ID']
            handler.id_name         = i['$ID_NAME']            
            handler.descriptions    = i['Description']
            handler.icon            = i['Icon']
            handler.name            = i['Name']
            handler.descriptions_required = i['DescriptionRequired']
            handler.is_toggleable   = i['IsToggleable']
            handler.max_lv          = i['LevelMax']
            handler.save()
            for h in i['Link_Skills']:
                try:
                    skill = Skills.objects.get(id_name = h)
                    handler.skill.add(skill)
                except:
                    logging.warning("skill not found {}".format(h))
            for h in i['Link_Jobs']:
                try:
                    job = Jobs.objects.get(ids = h)
                    handler.job.add(job)
                except:
                    logging.warning("skill not found {}".format(h))
            handler.save()
            count+=1