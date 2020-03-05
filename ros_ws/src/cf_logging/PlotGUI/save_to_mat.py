# -*- coding: utf-8 -*-
"""
Created on Fri Aug  2 07:32:22 2019

@author: diewa
"""

import CF_functions as cff
from scipy.io import savemat
import os
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Converting log data to Matlab file.')
parser.add_argument('-i', dest='input', help='Directory of log files')
parser.add_argument('-o', dest='output', help='Output directory for .mat files')

args = parser.parse_args()

if not os.path.exists(args.output):
    os.makedirs(args.output)
    
files = []
for (dirpath, dirnames, filenames) in os.walk(args.input):
    for file in filenames:
        files.append(dirpath+"/"+file)
    break

print(files)

for file in files:
    if os.path.isfile(file):
        # decode binary log data
        data = cff.decode(file)
        mat_data = {}
        temp_dict = {}
        last_key = ""
        keys_sorted = sorted(data.keys())
        for key in keys_sorted:
            if key.count(".") > 0:
                key_split = key.split(".")
                if key_split[0] == last_key:
                    temp_dict[key_split[1]] = data[key]
                else:
                    if last_key != "":
                        mat_data[last_key] = temp_dict
                    temp_dict = {}
                    last_key = key_split[0]
                    temp_dict[key_split[1]] = data[key]
            else:
                mat_data[key] = data[key]
        if temp_dict:
            mat_data[last_key] = temp_dict
#        for key,value in zip(data.keys(),data.values()):
#            new_key = key.replace(".", "_")
#            mat_data[new_key] = data[key]
        savemat(args.output + "/" + os.path.basename(file) + ".mat",mat_data)