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

#==============================================================================
# Function Definitions / Reference Variable Declaration
#==============================================================================


#==============================================================================
# Working Code
#==============================================================================

# Set the project working directory
os.chdir(r'/home/ejreidelbach/projects/SBIR/Data/Awards_API/Phase 2/')

# Read in all Files
files = [f for f in os.listdir('.') if f.endswith(('.json'))]
files = sorted(files)

# Set the project working directory
os.chdir(r'/home/ejreidelbach/projects/SBIR/Data/')
for f in files:
    print("Reading in "+f)

    # Get the links for every file in a specific year
    with open('Awards_API/Phase 2/'+f) as json_data:
        data = json.load(json_data)
    if data == []:
        print('No Phase 2 proposals in: ' + f)
        continue
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
        
        # Grab Award Information (Agency, Branch, Contract, Agency Tracking Number, 
        #       Amount, PHase, Program, Award Year, Solicitation Year, Solicitation
        #       Topic Code, Solicitation Number)
        awardHTML = soup.find('div', {'class':'container-fluid'})
        for div in awardHTML.find_all('div', {'class':'col-md-6'}):
            for row in div.find_all('span', {'class':'open-description'}):
                tempAwardInfo.append(row.text.encode('ascii','ignore').strip())
                
        for div in awardHTML.find_all('div', {'class':'col-md-3'}):
            for row in div.find_all('span', {'class':'open-description'}):
                tempAwardInfo.append(row.text.encode('ascii','ignore').strip())
                
        tempAwardInfo[6] = float(tempAwardInfo[6].strip('$').replace(',',''))
            
        # Grab Business Information (Business Name, Business URL, Address, DUNS, 
        #       Hubzone Owned, Woman Owned, Socially Disadvantaged, PI, 
        #       Business Contact)
        busHTML = soup.find('div', {'class':'small-business-info-wrapper'})
        tempAwardInfo.append(busHTML.find(
                'div', {'class':'sbc-name-wrapper'}).text.encode(
                'ascii','ignore').strip())
        # Attempt to grab business URL
        try:
            tempAwardInfo.append('https://www.sbir.gov'+busHTML.find(
                    'a')['href'].encode('ascii','ignore').strip())
        except:
            tempAwardInfo.append('')
        tempAwardInfo.append(busHTML.find('div', {'class':
            'sbc-address-wrapper'}).text.strip().encode('ascii','ignore'))
        for row in busHTML.find_all('span', {'class':'open-description'}):
            tempAwardInfo.append(row.text.encode('ascii','ignore').strip())
        
        # Business Contact Info (PI, Business Contact...ignore Research Institution)
        busContactHTML = soup.find('div', {'class':'row award-sub-wrapper'})
        for row in busContactHTML.find_all('div', {'class':'award-sub-description'})[:2]:
            if (row.text.strip() != 'N/A'):
                    temp = row.text.encode('ascii','replace').replace(
                            '?',' ').strip().replace('&nbsp','').replace(';','')
                    # Name
                    try:
                        tempAwardInfo.append(temp.split(
                                'Name:')[1].strip().split('Phone: ')[0])
                    except:
                        tempAwardInfo.append('')
                    # Phone
                    try:
                        tempAwardInfo.append(temp.split(
                                'Phone: ')[1].strip().split('Email:')[0])
                    except:
                        tempAwardInfo.append('')
                    # Email
                    try:
                        tempAwardInfo.append(temp.split(
                                'Email:')[1].strip())
                    except:
                        tempAwardInfo.append('')
            else:
                tempAwardInfo.append('N/A') #Name
                tempAwardInfo.append('N/A') #Phone
                tempAwardInfo.append('N/A') #Email
        
        # Grab Abstract
        abstractHTML = soup.find('div',{'class':'abstract-wrapper'})
        abstract = abstractHTML.text.encode(
                'ascii','ignore').strip().replace('\n',' ')
        if abstract == 'Abstract         N/A':
            tempAwardInfo.append('N/A')
        else:
            tempAwardInfo.append(abstract)
        
        awardDict = {}
        
        awardDict['title'] = tempAwardInfo[0]
        awardDict['url'] = tempAwardInfo[1]
        awardDict['agency'] = tempAwardInfo[2]
        awardDict['branch'] = tempAwardInfo[3]
        awardDict['contract_num'] = tempAwardInfo[4]
        awardDict['agency_tracking_num'] = tempAwardInfo[5]
        awardDict['award_amount'] = tempAwardInfo[6]
        awardDict['phase'] = tempAwardInfo[7]
        awardDict['program'] = tempAwardInfo[8]
        awardDict['award_year'] = tempAwardInfo[9]
        awardDict['solicit_year'] = tempAwardInfo[10]
        awardDict['solicit_topic_code'] = tempAwardInfo[11]
        awardDict['solicit_num'] = tempAwardInfo[12]
        awardDict['comp_name'] = tempAwardInfo[13]
        awardDict['comp_url'] = tempAwardInfo[14]
        awardDict['comp_address'] = tempAwardInfo[15]
        awardDict['comp_duns'] = tempAwardInfo[16]
        awardDict['comp_hubzone'] = tempAwardInfo[17]
        awardDict['comp_wom_owned'] = tempAwardInfo[18]
        awardDict['comp_social'] = tempAwardInfo[19]
        awardDict['comp_pi_name'] = tempAwardInfo[20]
        awardDict['comp_pi_phone'] = tempAwardInfo[21]
        awardDict['comp_pi_email'] = tempAwardInfo[22]
        awardDict['comp_bus_name'] = tempAwardInfo[23]
        awardDict['comp_bus_phone'] = tempAwardInfo[24]
        awardDict['comp_bus_email'] = tempAwardInfo[25]
        awardDict['abstract'] = tempAwardInfo[26]  
        
        awardInfo.append(awardDict)
    
        print(awardCount)
        awardCount+=1
        
        #time.sleep(5)
    
    # Export the data set
    filename = 'Awards_Scraped/Phase 2/Phase2_' + f
    with open(filename, 'wt') as out:
        json.dump(awardInfo, out, sort_keys=True, indent=4, separators=(',', ': ')) 