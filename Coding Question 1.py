#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 05:22:42 2020

@author: sandeep
"""
#import dependencies
import pandas as pd
trade_data = pd.read_csv("niftyjan2019_minute.txt",sep=',')
#remove unwanted columns
trade_data.drop(['OPEN INTEREST', 'VOLUME'], axis = 1,inplace = True)
trade_data['TIME_INDEX'] = trade_data['TIME']
v1 = lambda x: float(x[1])+float(x[3:])/100
trade_data.TIME_INDEX = trade_data.TIME_INDEX.apply(v1)
trade_data = trade_data[(trade_data['TIME_INDEX']>9.16)&(trade_data['TIME_INDEX']<15.30)]
index1 = list(range(1,trade_data.shape[0]+1))
trade_data['index1'] = index1
trade_data = trade_data.set_index('index1')
#2 Calculate a simple moving average of the CLOSE prices with period set as 14 
#minutes (aka. sma_14).
trade_data['sma_14'] = trade_data['CLOSE'].rolling(window = 14).mean()
#3 Calculate a simple moving average of the CLOSE prices with period set as 30 
#minutes (aka. sma_30)
trade_data['sma_30'] = trade_data['CLOSE'].rolling(window = 30).mean()
#4 Print DATE TIME “BUY” if sma_14 crosses above sma_30 Print DATE TIME “SELL” 
#if sma_14 crosses below sma_30
trade_data['sma_14'].fillna(trade_data['CLOSE'],inplace=True)
trade_data['sma_30'].fillna(trade_data['CLOSE'],inplace=True)
trade_data['Decision'] = trade_data['sma_14'].astype(int)-trade_data['sma_30'].astype(int)
l = []
for i in trade_data['Decision']:
    if i>0:
        l.append('BUY')
    elif i<0:
        l.append('SELL')
    else:
        l.append('0')
trade_data['Decision'] = l
index = list(range(1,trade_data.shape[0]+1))
trade_data['index']= index
trade_data = trade_data.set_index('index')
res = pd.DataFrame({'DATE':20190101,'TIME':'00:00','Decision':'0'}, index =[0])
prev = ''
for i in range(30,trade_data.shape[0]) :
    if trade_data['Decision'][i] != '0':
        if trade_data['Decision'][i] == 'SELL' and prev != 'SELL':
            res = res.append(trade_data.loc[i, ['DATE', 'TIME','Decision']],ignore_index = True)
            prev = 'SELL'
        elif trade_data['Decision'][i] == 'BUY' and prev!= 'BUY':
            res = res.append(trade_data.loc[i, ['DATE', 'TIME','Decision']],ignore_index = True)
            prev = 'BUY'
        else:
            continue
res = res.iloc[1:]
print(res.head())