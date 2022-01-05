# -*- coding: utf-8 -*-

import csv
import logging
import os
import io
from os.path import exists
from DB import ToS_DB as constants


def parse(c = None):
    if (c==None):
        c = constants()
        c.build()
    parse_jobs(c)
    parse_jobs_stats(c)



def parse_jobs(constants):
    logging.info('Parsing Jobs...')
    ies_path = os.path.join(constants.PATH_INPUT_DATA, 'ies.ipf', 'job.ies')
    if(not exists(ies_path)):
       return
    with io.open(ies_path, 'r',  encoding="utf-8") as ies_file:
        for row in csv.DictReader(ies_file, delimiter=',', quotechar='"'):
            obj = {}
            obj['$ID'] = str(row['ClassID'])
            obj['$ID_NAME'] = row['ClassName']
            obj['Description'] = constants.translate(row['Caption1'])
            obj['Icon'] = constants.parse_entity_icon(row['Icon'])
            obj['Name'] = constants.translate(row['Name'])
            obj['JobTree'] = row['CtrlType']
            obj['IsHidden'] = row['HiddenJob'] == 'YES'
            obj['IsStarter'] = int(row['Rank']) == 1
            obj['Rank'] = int(row['Rank'])
            obj['Stat_CON'] = int(row['CON'])
            obj['Stat_DEX'] = int(row['DEX'])
            obj['Stat_INT'] = int(row['INT'])
            obj['Stat_SPR'] = int(row['MNA'])
            obj['Stat_STR'] = int(row['STR'])
            obj['Link_Attributes'] = []
            obj['Link_Skills'] = []

            constants.data['jobs'][obj['$ID']] = obj
            constants.data['jobs_by_name'][obj['$ID_NAME']] = obj

def parse_jobs_stats(constants):
    logging.debug('Parsing Jobs base stats...')

    ies_path = os.path.join(constants.PATH_INPUT_DATA, 'ies.ipf', 'statbase_pc.ies')
    if(not exists(ies_path)):
       return
    with io.open(ies_path, 'r', encoding="utf-8") as ies_file:
        for row in csv.DictReader(ies_file, delimiter=',', quotechar='"'):
            if not len(row['ClassName']):
                continue

            job_tree = row['ClassName']

            for job in constants.data['jobs'].values():
                if job['JobTree'] == job_tree:
                    job['StatBase_CON'] = int(row['CON'])
                    job['StatBase_DEX'] = int(row['DEX'])
                    job['StatBase_INT'] = int(row['INT'])
                    job['StatBase_SPR'] = int(row['MNA'])
                    job['StatBase_STR'] = int(row['STR'])
