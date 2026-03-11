# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 16:34:36 2026

@author: trist
"""

"""
P2_Part1: Create a two-panels plot showing temperature and salinity profiles
"""
# Import flatfiles using Pandas 
import pandas as pd 
import matplotlib.pyplot as plt 

# Loading the CTD profile data from the previous assignment- P1 
profile = pd.read_csv("ctd_profile_T_S_depth.dat", sep="\t") 

# Check the names of the rows and columns in the CTD file. 
print(profile.head())
print(profile.columns)

"""
These are the column names from the CTD profile data 
Index(['date', 'time', 'depth_m', 'temperature_degC', 'salinity_psu'], dtype='object')
"""

# Make sure the two-panels plot share the y-axis range.  
fig, ax = plt.subplots(1, 2, sharey=True)

# Creating the temperature profile.
ax[0].plot(profile["temperature_degC"],   
           profile["depth_m"],    
           color='r') # making the line colour red 

#label the x & y axis (inverted), and add a title. 
ax[0].set_xlabel("Temperature (degC)")
ax[0].set_ylabel("Depth (m)")
ax[0].invert_yaxis() # Inverting the depth axis
ax[0].set_title("Temperature profile")

# Creating the salinity profile.
ax[1].plot(profile["salinity_psu"],   
           profile["depth_m"],    
           color='b') # making the line colour blue 

#label the x axis and add a title.
ax[1].set_xlabel("Salinity (psu)")
ax[1].set_title("Salinity profile")


# Saving the profiles plot.
fig.savefig("Part1_T_S_profiles.png", dpi=300)

# Show the T-S plots.
plt.show()