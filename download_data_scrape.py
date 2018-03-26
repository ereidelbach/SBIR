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
from selenium import webdriver
from bs4 import BeautifulSoup

'''
    NOTE 1: For the Selenium driver to function properly on Ubuntu, I had to 
            download the most up-to-date geckodriver found at:
            https://github.com/mozilla/geckodriver/releases
                
            Once that is complete, extract the driver and place it in the
            /us/local/bin folder
           
    NOTE 2: An effective selenium guide can be found here:
            https://automatetheboringstuff.com/chapter11/
            
            The relevant contents begin roughly 3/4 down the page.
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

#  Use the instructions found here to install PhantomJS on Ubuntu: 
#       https://www.vultr.com/docs/how-to-install-phantomjs-on-ubuntu-16-04

# Phase 1 - SBIR
#https://www.sbir.gov/sbirsearch/award/all?f[0]=im_field_program:105791&f[1]=im_field_phase:105788

# Phase 2 - SBIR
url = 'https://www.sbir.gov/sbirsearch/award/all/?f%5B0%5D=im_field_phase%3A105789&f%5B1%5D=im_field_program%3A105791'

# Open a PhantomJS web browser and direct it to the DEA's dropbox search page
browser = webdriver.PhantomJS()   
browser.get(url)
browser.implicitly_wait(100)

#==============================================================================
# Working Code
#==============================================================================

# Set the project working directory
os.chdir(r'/home/ejreidelbach/projects/SBIR/Data/Awards_Scraped')

# Use beautifulSoup to extract the download file links for XLS and JSON formats
html = browser.page_source
soup = BeautifulSoup(html, 'lxml')
xlsList = []
jsonList = []
for ultag in soup.find_all('ul', {'class': 'dropdown-menu'}):
    for row in ultag.find_all('div', {'class': 'col-md-5'}):
        for a in row.select("a[href*=solr_print]"):
            xlsList.append(a['href'])
        for a in row.select("a[href*=json_print]"):
            jsonList.append(a['href'])       
            
# Try downloading a file via the headless browser
dl_url = 'https://www.sbir.gov' + jsonList[0]
headers = {"User-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"}
r = requests.get(dl_url, headers=headers)
soup = BeautifulSoup(r.content,'html.parser')               