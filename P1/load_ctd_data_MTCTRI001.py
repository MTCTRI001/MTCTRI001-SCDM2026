# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 09:54:26 2026

@author: trist
"""

import pandas as pd

# import the CTD file in the python workspace
df = pd.read_csv("ctd_profile_T_S_depth.dat", sep="\t") # columns in the file are separated by tabs

# printing out the DataFrame
print(df)