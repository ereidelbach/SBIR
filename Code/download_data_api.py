#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 09:07:18 2018

@author: ejreidelbach

:SUMMARY:

:REQUIRES:
   
:TODO:
"""

#==============================================================================
# Package Import
#==============================================================================
import json
import requests
import os  
import pandas as pd
import time

#==============================================================================
# Function Definitions / Reference Variable Declaration
#==============================================================================
agencyAbbrev = ['DOD','HHS','NASA','NSF','DOE','USDA','EPA','DOC','ED','DOT','DHS']
agencyNames = ['Dept. of Defense','Dept. of Health and Human Services',
               'National Aeronautics and Space Administration',
               'National Science Foundation', 'Dept. of Energy',
               'United States Dept. of Agriculture', 
               'Environmental Protection Agency',
               'Dept. of Commerce','Dept. of Education','Dept. of Transportation',
               'Dept. of Homeland Security']

years = ['1983','1984','1985','1986','1987','1988','1989',
         '1990','1991','1992','1993','1994','1995','1996','1997','1998','1999',
         '2000','2001','2002','2003','2004','2005','2006','2007','2008','2009',
         '2010','2011','2012','2013','2014','2015','2016','2017','2018']


# Acquire all the closed SBIR Topics from the API
# Dump the contents of the JSON, add in the new elements, then overwrite the
#     old JSON
def getClosedTopics():
    os.chdir(r'/home/ejreidelbach/projects/SBIR/Data/Closed_Topics/Combined')
    for abbrev in agencyAbbrev:
        topicsList = []
        url = 'https://sbir.gov/api/solicitations.json?&agency=' + abbrev + '&closed=1'
        response = requests.get(url)
        data = json.loads(response.content)
        if (isinstance(data,list)):
            for row in data:
                topicsList.append(row)
                
        # Export the data set
        filename = 'awards_' + abbrev + '.json'
        with open(filename, 'wt') as out:
            json.dump(topicsList, out, sort_keys=True, indent=4, separators=(',', ': '))
            
        print('Done with: ' + abbrev)

# The Award database is continually updated throughout the year. As a result, data for the given year is not complete until April of the following year. Annual Reports data is a snapshot of agency reported information for that year and hence might look different from the live data in the Awards Information charts.  
def getAwardsAll():
    for year in years:
        os.chdir(r'/home/ejreidelbach/projects/SBIR/Data/Awards/Combined')
        url = 'https://www.sbir.gov/api/awards.json?year=' + year
        response = requests.get(url)
        data = json.loads(response.content)
                
        # Remove all STTR awards
        filtered_data = [award for award in data if award['program'] == 'SBIR']

        # Export the data set
        filename = 'awards_' + year + '.json'
        with open(filename, 'wt') as out:
            json.dump(filtered_data, out, sort_keys=True, indent=4, separators=(',', ': ')) 
            
        print(year)

def getAwardsPhaseI():
    for year in years:
        os.chdir(r'/home/ejreidelbach/projects/SBIR/Data/Awards/Phase 1')
        url = 'https://www.sbir.gov/api/awards.json?year=' + year
        response = requests.get(url)
        data = json.loads(response.content)
                
        # Remove all STTR awards
        filtered_data = [award for award in data if award['program'] == 'SBIR']
        
        # Remove all Phase II awards
        filtered_data2 = [award for award in filtered_data if award['phase'] == 'Phase I']

        # Export the data set
        filename = 'awards_' + year + '.json'
        with open(filename, 'wt') as out:
            json.dump(filtered_data2, out, sort_keys=True, indent=4, separators=(',', ': ')) 
            
        print(year)
        
def getAwardsPhaseII():
    for year in years:
        os.chdir(r'/home/ejreidelbach/projects/SBIR/Data/Awards/Phase 2')
        url = 'https://www.sbir.gov/api/awards.json?year=' + year
        response = requests.get(url)
        data = json.loads(response.content)
                
        # Remove all STTR awards
        filtered_data = [award for award in data if award['program'] == 'SBIR']
        
        # Remove all Phase II awards
        filtered_data2 = [award for award in filtered_data if award['phase'] == 'Phase II']

        # Export the data set
        filename = 'awards_' + year + '.json'
        with open(filename, 'wt') as out:
            json.dump(filtered_data2, out, sort_keys=True, indent=4, separators=(',', ': ')) 
            
        print(year)


#==============================================================================
# Working Code
#==============================================================================

# Acquire Closed Topics
getClosedTopics()

# Acquire Awards
getAwardsAll()
getAwardsPhaseI()
getAwardsPhaseII()

# Read in data
#with open('awards_2018.json') as json_data:
#    data = json.load(json_data)
#df = pd.DataFrame(data)