# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 11:19:50 2019

@author: Dell
"""

import yfinance as yf
import numpy as np
import pandas as pd

Download=yf.download('GOOG',start='2014-01-01',end='2018-01-01')

Google=Download.tail(620)

goog_data_signal = pd.DataFrame(index=Google.index)
goog_data_signal['price'] = Google['Adj Close']

#function to define parameters to determine signals for support and resistance
#define variables and create a series of seros with numpy
def trading_support_resistance(data, bin_width=20):
    data['sup_tolerance'] = pd.Series(np.zeros(len(data)))
    data['res_tolerance'] = pd.Series(np.zeros(len(data)))
    data['sup_count'] = pd.Series(np.zeros(len(data)))
    data['res_count'] = pd.Series(np.zeros(len(data)))
    data['sup'] = pd.Series(np.zeros(len(data)))
    data['res'] = pd.Series(np.zeros(len(data)))
    data['positions'] = pd.Series(np.zeros(len(data)))
    data['signal'] = pd.Series(np.zeros(len(data)))
    in_support=0
    in_resistance=0
    
    #defining parameter's formulas
    for x in range((bin_width - 1) + bin_width, len(data)):
         data_section = data[x - bin_width:x + 1]
         supportLevel=min(data_section['price'])
         resistanceLevel=max(data_section['price'])
         rangeLevel=resistanceLevel-supportLevel
         data['res'][x]=resistanceLevel
         data['sup'][x]=supportLevel
         data['sup_tolerance'][x]=supportLevel+(0.2*rangeLevel)
         data['res_tolerance'][x]=resistanceLevel-(0.2*rangeLevel)
         
         if data['price'][x]>=data['res_tolerance'][x] and\
                              data['price'][x] <= data['res'][x]:
            in_resistance+=1
            data['res_count'][x]=in_resistance
         elif data['price'][x] <= data['sup_tolerance'][x] and \
                                  data['price'][x] >= data['sup'][x]:
            in_support += 1
            data['sup_count'][x] = in_support
         else:
            in_support=0
            in_resistance=0
         if in_resistance>2:
             data['signal']=1
         elif in_support>2:
             data['signal']=0
         else:
             data['signal'][x]=data['signal'][x-1]
             
trading_support_resistance(goog_data_signal)

#visualizinng trading support resistance
import matplotlib.pyplot as plt

fig=plt.figure
ax1=fig.add_subplot(111,ylabel='Google Price in $')
goog_data_signal['sup'].plot(ax=ax1,color='g',lw=2)
goog_data_signal['res'].plot(ax=ax1,color='r',lw=2)

#plotting arrow directions
ax1.plot(goog_data_signal.loc[goog_data_signal['positions']==1].index\
,goog_data_signal['price'][goog_data_signal['positions']==1],'^',markersize=7,colorsize='k'\
,label='buy')

ax1.plot(goog_data_signal.loc[goog_data_signal['positions']==-1].index\
,goog_data_signal['price'][goog_data_signal['positions']==-1],'v',markersize=7,colorsize='k'\
,label='sell')

plt.legend()
plt.show()
             
         
             
         
         

         
         