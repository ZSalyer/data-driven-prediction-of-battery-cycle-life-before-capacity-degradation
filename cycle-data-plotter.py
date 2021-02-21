# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 20:32:47 2021

@author: Zach

Plot various candidate features for capacity fade ML estimation.
Examples of different plot configurations with matplotlib.
"""

import pickle
import matplotlib.pyplot as plt
plt.style.use(['ggplot'])

test_data = pickle.load(open(r'.\Data\batch1.pkl', 'rb'))

#Generic plotter (just for future reference)
def generic_xy_plotter(ax, x_data, y_data, param_dict):
    out = ax.plot(x_data, y_data, **param_dict)
    return out

#Plot capacity fade versus cycle number for all cells in a batch
fig1, ax = plt.subplots()
for cell_id in test_data.keys():
    ax.plot(test_data[cell_id]['summary']['cycle'], test_data[cell_id]['summary']['QD'],
            'o', markersize=4)
    ax.set_xlabel('Cycle Number [-]')
    ax.set_ylabel('Discharge Capacity [Ah]')
    
#Plot max, avg, min temperature while cycling v. cycle number
fig2, axs = plt.subplots(3, 1)
for cell_id in test_data.keys():
    axs[0].plot(test_data[cell_id]['summary']['cycle'], test_data[cell_id]['summary']['Tmax'])
    axs[1].plot(test_data[cell_id]['summary']['cycle'], test_data[cell_id]['summary']['Tavg'])
    axs[2].plot(test_data[cell_id]['summary']['cycle'], test_data[cell_id]['summary']['Tmin'])
axs[0].set_ylabel('Max Temp. [°C]')
axs[1].set_ylabel('Avg. Temp.[°C]')
axs[2].set_ylabel('Min. Temp.[°C]')
axs[2].set_xlabel('Cycle Number [-]')

#%% dQdV and Discharge Voltage Analysis 
""" 
The discharge voltage curve contains many features that are indicative of capacity fade.
These can serve as useful features for cycle life prediction alongside QD.
Make a plot of Voltage v. Q_100 - Q_10 for a random selection of cells.
"""
import random

random_cell_selection = random.choice(list(test_data.keys()))
