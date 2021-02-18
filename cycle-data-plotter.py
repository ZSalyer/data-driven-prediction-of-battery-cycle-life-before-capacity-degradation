# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 20:32:47 2021

@author: Zach
"""

import pickle
import matplotlib.pyplot as plt

test_data = pickle.load(open(r'.\Data\batch1.pkl', 'rb'))

#Add moving average for discharge capacity
#test_data['summary']['QD_ma'] = 

#Plot capacity fade versus cycle number for all cells in a batch
fig1 = plt.figure()
for cell_id in test_data.keys():
    plt.plot(test_data[cell_id]['summary']['cycle'], test_data[cell_id]['summary']['QD'])

fig2 = plt.figure()
#Plot capacity fade versus cycle number for all cells in a batch
for cell_id in test_data.keys():
    plt.plot(test_data[cell_id]['summary']['cycle'], test_data[cell_id]['summary']['Tmax'])