#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 05:30:07 2020

@author: sandeep
"""

#import dependencies
import bs4
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas as pd

r = Request('https://www.investing.com/indices/major-indices',headers={"User-Agent": "Mozilla/5.0"})#fool them to be website.
c = urlopen(r).read()
soup = BeautifulSoup(c, "html.parser")
#to scrape the required list
s = ''
s = soup.find('div',{'class':'js-ga-on-sort'}).find('tbody').find_all('tr')[0].text
s = s.replace('\n','*')
s = s.replace('\xa0','')
s = s[2:-2]
s = s.split('*')

# to create dataframe
z = pd.DataFrame(data = [s],columns =['INSTRUMENT NAME','LAST TRADED PRICE','PREV_PRICE','DEATH_PRICE','CHANGE','CHANGE%','TIME'])

#loop for the subsequent additions
for i in range(1,5):
    s = soup.find('div',{'class':'js-ga-on-sort'}).find('tbody').find_all('tr')[i].text
    s = s.replace('\n','*')
    s = s.replace('\xa0','')
    s = s[2:-2]
    s = s.split('*')
    df_length = len(z)
    z.loc[df_length] = s

print(z.head())
