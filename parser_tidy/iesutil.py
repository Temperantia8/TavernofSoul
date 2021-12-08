# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 08:07:28 2021

@author: Temperantia
"""

import csv
import logging
import os
import io
from DB import ToS_DB as constants


def load(ies_name,c):
    ies_data = []
    #ies_path = os.path.join(globals.PATH_INPUT_DATA, "ies.ipf", ies_name)
    ies_path = c.file_dict[ies_name.lower()]['path']

    if not os.path.exists(ies_path):
        logging.warn('Missing ies file: %s', ies_path)
        return []

    with io.open(ies_path, 'r', encoding = "utf-8") as ies_file:
        ies_reader = csv.DictReader(ies_file, delimiter=',', quotechar='"')

        for row in ies_reader:
            # auto cast to int/float if possible
            for key in row.keys():
                try:
                    row[key] = int(row[key])
                except :
                    try:
                        row[key] = float(row[key])
                    except :
                        row[key] = row[key]

            ies_data.append(row)

    return ies_data