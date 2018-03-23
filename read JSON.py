#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 09:35:02 2018

@author: ejreidelbach
"""

import gzip
import json
import pandas as pd

# Read in one JSON file
f = "/home/ejreidelbach/Data-Sets/SBIR Data/merged_dataset.json.gz"

print("Reading in "+f)

#Opening the Gziped File
stream = gzip.open(f)

# Read in every line of the JSON; each line corresponds to a one minute pull of the Waze API
for line in stream:
    report = json.loads(line)
    
    report.head