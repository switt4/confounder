#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 14 11:30:54 2020

@author: switt
"""

import os
import yaml
from yaml import Loader, Dumper
import json
import pandas as pd
import numpy as np

def read_tsv(inTSV):
	dataTSV = pd.read_table(inTSV)
	dataTSV.head()
	#confoundsHeaders = list(confounds)
	return dataTSV

def read_json(inJSON):
	with open(inJSON,'rt') as cj:
		dataJSON = json.load(cj)
	return dataJSON

test = '/Users/switt/Documents/ComputationalCore/CONFOUNDER/confounder_0.0.1d/config.yaml'
stream = open(test,'r')
config = yaml.load(stream,Loader=Loader)

confounds_dict_var = config['CONFOUNDS']
confound_names = list(confounds_dict_var.keys())

confounds_dict_file = "/Users/switt/Documents/ComputationalCore/CONFOUNDER/confounder_0.0.1d/temp-files/confounds_dict.json"
with open(confounds_dict_file, 'w') as fp:
	json.dump(confounds_dict_var, fp, indent=4, separators=(',', ': '))

confounds_tsv = "/Users/switt/Documents/ComputationalCore/NoleControl/fmriprep_1.3.2/fmriprep/sub-CT03/func/sub-CT03_task-rest_run-01_desc-confounds_regressors.tsv"

confounds = read_tsv(confounds_tsv)
confounds_dict = read_json(confounds_dict_file)

filename_stem = os.path.split(confounds_tsv)[1]

for conf in confounds_dict.items():
    confounds_temp = confounds[conf[1]]
    confounds_name_temp = conf[0]
    confounds_temp = np.nan_to_num(np.array(confounds_temp))
    out_filename = filename_stem.replace("desc-confounds_regressors.tsv","confound-%s"%confounds_name_temp)
    out_file_path = os.path.join("/Users/switt/Documents/ComputationalCore/CONFOUNDER/confounder_0.0.1d/temp-files",out_filename)
    np.savetxt(out_file_path, confounds_temp, delimiter='\t')
        