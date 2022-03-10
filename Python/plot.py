# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 10:20:56 2022

@author: baret
"""
def f(x,y,z):
        return 0.22*x*y+0.1*x*y*z

import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 100, 100)
y =  np.linspace(0, 100, 100)
z =  np.linspace(0, 100, 100)

X,Y, Z= np.meshgrid(x,y,z)
A = f(X,Y,Z)
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot_surface( Y,Z,A ,rstride=1, cstride=1,cmap='jet', edgecolor='none')