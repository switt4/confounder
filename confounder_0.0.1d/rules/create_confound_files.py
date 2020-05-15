import os
import argparse
import json
import pandas as pd
import numpy as np

def read_tsv(inTSV):
	dataTSV = pd.read_table(inTSV)
	dataTSV.head()
	return dataTSV

def read_json(inJSON):
	with open(inJSON,'rt') as cj:
		dataJSON = json.load(cj)
	return dataJSON

parser = argparse.ArgumentParser(description='Create confound text files for FEAT design.')
parser.add_argument('confounds_tsv', help='Input events.tsv to parse.')
parser.add_argument('confounds_dictionary', help='Filename for confounds dictionary file.')
parser.add_argument('confound_file', help='Output confound text file.')
args = parser.parse_args()

confounds = read_tsv(args.confounds_tsv)
confounds_dict = read_json(args.confounds_dictionary)

for conf in confounds_dict.items():
    confounds_temp = confounds[conf[1]]
    confounds_name_temp = conf[0]
    confounds_temp = np.nan_to_num(np.array(confounds_temp))
    np.savetxt(args.confound_file, confounds_temp, delimiter='\t')

