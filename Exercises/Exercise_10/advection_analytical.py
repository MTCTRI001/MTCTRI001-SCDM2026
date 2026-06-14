#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 19:49:03 2020
Analytical solution of a 1D advection problem
@author: vichi
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# problem parameters
c=1         # Advection speed [m s-1]
dx=500      # X resolution [m]
dt=200      # time step [s]
t0=0.       # initial time
tmax=0.1    # duration of simulation [days]
xmax=10.0e3 # length of the basin [m]

# Grid definition
# time axis
NT = int(np.floor(tmax*86400/dt))+1  # number of steps (starts from 0)
# X axis (centred at 0)
x = np.arange(-xmax,xmax,dx)
IM = len(x)   # number of grid points
print('grid size : ',IM)
print('number of timesteps : ',NT)

#%% Spatial shape of the temperature disturbance
def Gaussian(x):
    # This is a Gaussian (peak) function with the following params
    T0 = 15         # baseline temperature [degC]
    sigma = 1000.   # width at half amplitude [m]
    A = 5.          # amplitude [degC]
    Gaussian = T0+A*np.exp(-(x/sigma)**2)
    return Gaussian


#%% plot an animation of the temperature disturbance 
fig, ax = plt.subplots()
# set the axis limits and turn off autoscaling
plt.axis([-xmax/1000, xmax/1000, 13, 22])
plt.autoscale(False)
line, = ax.plot(x/1000., Gaussian(x),'k')
ax.set_xlabel('X (km)')
ax.set_ylabel('T ($^o$C)')

def animate(i):
    t = t0 + i*dt
    line.set_ydata(Gaussian(x-c*t))  # update the data.
    return line,

# create the animation (interval is in ms)
ani = animation.FuncAnimation(
    fig, animate, interval=200, blit=True, frames=NT, repeat=True)

# To save the animation, use e.g.
# ani.save("movie.mp4")
# or
# writer = animation.FFMpegWriter(
#     fps=15, metadata=dict(artist='Me'), bitrate=1800)
# ani.save("movie.mp4", writer=writer)

plt.show()