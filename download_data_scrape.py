#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 11:02:23 2018

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
from bs4 import BeautifulSoup
import time

'''

'''

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
awardInfoNames = ['title','url','agency','branch','contract_num','agency_tracking_num',
             'award_amount','phase','program','award_year','solicit_year',
             'solicit_topic_code','solicit_num','comp_name','comp_url',
             'comp_address','comp_duns','comp_hubzone','comp_wom_owned',
             'comp_social','comp_pi_name','comp_pi_phone','comp_pi_email',
             'comp_bus_name','comp_bus_phone','comp_bus_email','abstract']

#==============================================================================
# Working Code
#==============================================================================

# Set the project working directory
os.chdir(r'/home/ejreidelbach/projects/SBIR/Data/')

# Get the links for every file in a specific year
with open('Awards/Combined/awards_2018.json') as json_data:
    data = json.load(json_data)
df = pd.DataFrame(data)
addressList = df['link']

# Scrape all the pages in the year
headers = {"User-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"}

awardInfo = []
awardCount = 0
for url in addressList:
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content,'html.parser')   
    
    # Create container for Award Information
    tempAwardInfo = []
    
    # Grab the Award Title
    header = soup.find('h1', {'class':'page-header'})
    tempAwardInfo.append(header.text.encode('ascii','ignore').strip())
    
    # Insert the Award URL
    tempAwardInfo.append(url.encode('ascii','ignore'))
    
    # Grab Award Information
    awardHTML = soup.find('div', {'class':'container-fluid'})
    for div in awardHTML.find_all('div', {'class':'col-md-6'}):
        for row in div.find_all('span', {'class':'open-description'}):
            tempAwardInfo.append(row.text.encode('ascii','ignore').strip())
            
    for div in awardHTML.find_all('div', {'class':'col-md-3'}):
        for row in div.find_all('span', {'class':'open-description'}):
            tempAwardInfo.append(row.text.encode('ascii','ignore').strip())
            
    tempAwardInfo[6] = float(tempAwardInfo[6].strip('$').replace(',',''))
        
    # Grab Business Information
    busHTML = soup.find('div', {'class':'small-business-info-wrapper'})
    tempAwardInfo.append(busHTML.find('div', {'class':'sbc-name-wrapper'}).text.encode(
            'ascii','ignore').strip())
    tempAwardInfo.append('https://www.sbir.gov'+busHTML.find(
            'a')['href'].encode('ascii','ignore').strip())
    tempAwardInfo.append(busHTML.find('div', {'class':
        'sbc-address-wrapper'}).text.strip().encode('ascii','ignore'))
    for row in busHTML.find_all('span', {'class':'open-description'}):
        tempAwardInfo.append(row.text.encode('ascii','ignore').strip())
    
    busContactHTML = soup.find('div', {'class':'row award-sub-wrapper'})
    for row in busContactHTML.find_all('div', {'class':'award-sub-description'}):
        if (row.text.strip() != 'N/A'):
            try:
                temp = row.text.encode('ascii','replace').replace(
                        '?',' ').strip().replace('&nbsp','').replace(';','')
                # Name
                tempAwardInfo.append(temp.split('Name:')[1].strip().split('Phone: ')[0])
                # Phone
                tempAwardInfo.append(temp.split('Phone: ')[1].strip().split('Email:')[0])
                # Email
                tempAwardInfo.append(temp.split('Email:')[1].strip())
            except:
                pass
    
    # Grab Abstract
    abstractHTML = soup.find('div',{'class':'abstract-wrapper'})
    tempAwardInfo.append(abstractHTML.text.encode(
            'ascii','ignore').strip().replace('\n',' '))
    awardInfo.append(tempAwardInfo)

    print(awardCount)
    awardCount+=1
    
    time.sleep(5)
    
# Convert List to DataFrame
df2 = pd.DataFrame(awardInfo)
df2.columns = awardInfoNames
df2_json = df2.to_json()

# Export the data set
year = '2018'
filename = 'Awards_Scraped/awards_' + year + '.json'
with open(filename, 'wt') as out:
    out.write(df2_json)
    
with open(filename, 'wt') as out:
    json.dump(awardInfo, out, sort_keys=True, indent=4, separators=(',', ': ')) 

#with open(filename) as json_data:
#    data = json.load(json_data)
#with open(filename, 'wt') as out:
#    json.dump(data, out, sort_keys=True, indent=4, separators=(',', ': ')) 

