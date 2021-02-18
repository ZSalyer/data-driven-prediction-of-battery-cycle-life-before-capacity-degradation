# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 20:32:47 2021

@author: Zach
"""

import matplotlib.pyplot as plt
import pickle

batch1 = pickle.load(open(r'.\Data\batch1.pkl', 'rb'))
#remove batteries that do not reach 80% capacity
# del batch1['b1c8']
# del batch1['b1c10']
# del batch1['b1c12']
# del batch1['b1c13']
# del batch1['b1c22']

numBat1 = len(batch1.keys())

batch2 = pickle.load(open(r'.\Data\batch2.pkl','rb'))
