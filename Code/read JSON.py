#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 08:35:02 2018

@author: ejreidelbach

description

:REQUIRES:
   
:TODO:
"""

#==============================================================================
# Package Import
#==============================================================================
import gzip
import json
import pandas as pd

#==============================================================================
# Function Definitions / Reference Variable Declaration
#==============================================================================

#==============================================================================
# Working Code
#==============================================================================

# Set the project working directory
os.chdir(r'/home/ejreidelbach/')

# Read in one JSON file
f = "/home/ejreidelbach/Data-Sets/SBIR Data/merged_dataset.json.gz"

print("Reading in "+f)

#Opening the Gziped File
stream = gzip.open(f)

# Read in every line of the JSON; each line corresponds to a one minute pull of the Waze API
for line in stream:
    report = json.loads(line)
    
    report.head

