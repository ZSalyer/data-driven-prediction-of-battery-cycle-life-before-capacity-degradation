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
cell_data = test_data[random_cell_selection]

#Plot I,V,T for randomly selected cell at cycles 1 and 100
def plot_IVT(cell_data, cycle_number):
    fig, axs = plt.subplots(3, 1)
    axs[0].title.set_text('Cycle Number: {}'.format(str(cycle_number)))
    axs[0].plot(cell_data['cycles'][str(cycle_number)]['t'], cell_data['cycles'][str(cycle_number)]['I'])
    axs[0].set_ylabel('Current [A]')
    axs[1].plot(cell_data['cycles'][str(cycle_number)]['t'], cell_data['cycles'][str(cycle_number)]['V'])
    axs[1].set_ylabel('Voltage [V]')
    axs[2].plot(cell_data['cycles'][str(cycle_number)]['t'], cell_data['cycles'][str(cycle_number)]['T'])
    axs[2].set_ylabel('Temp [°C]')
    axs[2].set_xlabel('Time [s]')

plot_IVT(cell_data, 1)
plot_IVT(cell_data, 100)

#%% Recreate Fig. 2 from Paper
from tqdm import tqdm
from scipy import interpolate
import numpy as np

def extract_discharge_voltage_info(test_data):
    #Add dictionary key that contains info from only discharge portion of the cycle
    for cell_id in tqdm(test_data.keys()):     #For each cell
        cell_data = test_data[cell_id]   #Extract cell data
        for cycle_num in range(len(cell_data['cycles'])):
            test_data[cell_id]['cycles'][str(cycle_num)]['Qd_discharge'] = [Qd for idx, Qd in 
                                                                     enumerate(test_data[cell_id]['cycles'][str(cycle_num)]['Qd'])
                                                                     if test_data[cell_id]['cycles'][str(cycle_num)]['Qd'][idx] > 1e-3]
            test_data[cell_id]['cycles'][str(cycle_num)]['V_discharge'] = [V for idx, V in 
                                                                     enumerate(test_data[cell_id]['cycles'][str(cycle_num)]['V'])
                                                                     if test_data[cell_id]['cycles'][str(cycle_num)]['Qd'][idx] > 1e-3]
            
            #Normalize data by setting length to be 400 datapoints
            def normalize_data(new_size, data):
                f = interpolate.interp1d(range(len(data)),data)
                return f(np.linspace(0, new_size, new_size+1))
            
            try:
                test_data[cell_id]['cycles'][str(cycle_num)]['Qd_discharge'] = normalize_data(400, test_data[cell_id]['cycles'][str(cycle_num)]['Qd_discharge'])
                test_data[cell_id]['cycles'][str(cycle_num)]['V_discharge'] = normalize_data(400, test_data[cell_id]['cycles'][str(cycle_num)]['V_discharge'])
            catch
                if cycle_num != 0:
                    print('Normalization failed for cycle number: {}'.format(str(cycle_num)))
            
def create_Fig2(cell_data, all_cell_data):
    #Initialize Figure
    fig, axs = plt.subplots(1, 3)
    
    #Create Fig2a (discharge capacity curves for 100th and 10th cycles for random cell)
    axs[0].plot(cell_data['cycles']['10']['Qd_discharge'], cell_data['cycles']['10']['V_discharge'], label='Cycle 10')
    axs[0].plot(cell_data['cycles']['100']['Qd_discharge'], cell_data['cycles']['100']['V_discharge'], label='Cycle 100')
    axs[0].legend()
    axs[0].set_ylabel('Voltage [V]')
    axs[0].set_xlabel('Discharge Capacity [Ah]')
    
    #Create Fig2b
    
    #Create Fig2c
    
extract_discharge_voltage_info(test_data)  
create_Fig2(cell_data, test_data)

random_cell_selection = random.choice(list(test_data.keys()))
cell_data_update = test_data[random_cell_selection]