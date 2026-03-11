# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 16:35:50 2026

@author: trist
"""

"""
P2 Part 2: Time series - The file SAA2_WC_2017_metocean_10min_avg.csv attached 
below contains the data log from the SA Agulhas II winter cruise in the Southern
Ocean in 2017
"""
# Import packages for .CSV flatfile 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Function to convert ddmm to decimal degrees.
def ddmm2dd(ddmm):     
    """     
    Converts a position input from degrees and minutes to degrees and decimals     
    Input is ddmm.cccc and output is dd.cccc     
    Note, it does not check if positive or negative     
    """     
    thedeg = np.floor(ddmm/100.)     
    themin = (ddmm-thedeg*100.)/60.     
    return thedeg+themin

# Load the CSV file in python, using the appropriate column for the time index.
df = pd.read_csv("SAA2_WC_2017_metocean_10min_avg.csv")

print(df.columns)

"""
Index(['id', 'TIME_SERVER', 'TIME_GPS', 'LATITUDE', 'N_S', 'LONGITUDE', 'E_W',
       'HUMIDITY', 'BAROMETER', 'AIR_TEMPERATURE', 'WIND_SPEED_REL',
       'WIND_SPEED_TRUE', 'WIND_DIR_REL', 'WIND_DIR_TRUE', 'PAR',
       'TSG_SALINITY', 'TSG_TEMP'],
      dtype='object')

From the output we need to use TIME_SERVER as the time index becasue it represents 
the date and time when the data was measured 
"""
df = pd.read_csv("SAA2_WC_2017_metocean_10min_avg.csv",
                 parse_dates=["TIME_SERVER"], # convert to a datetime object 
                 index_col="TIME_SERVER")

print(df.columns)
print(df.head())

# Check that the missing values are properly recognised.
"""
Console output shows 'NaN', meaning that pandas already converted the 'NULL' 
values automatically

                       id  TIME_GPS  LATITUDE  ...    PAR  TSG_SALINITY TSG_TEMP
TIME_SERVER                                    ...                              
2017-06-28 17:10:00  1256  17:09:58  3428.595  ...  16.26           NaN      NaN
2017-06-28 17:20:00  1257  17:19:58  3430.443  ...  16.26       34.3408  17.1690
2017-06-28 17:30:00  1258  17:29:59  3432.261  ...  16.26       34.3407  17.2606
2017-06-28 17:40:00  1259  17:40:02  3434.121  ...  16.26           NaN      NaN
2017-06-28 17:50:00  1260  17:49:58  3435.981  ...  16.26           NaN      NaN
"""

# Use the time indexing to select the data from departure to that date included.
df_subset = df["2017-06-28":"2017-07-04"]
print(df_subset.head())
print(df_subset.tail())

# Plot the time series of temperature. Save the figure using the 'grayscale' style.
plt.style.use("grayscale")

# Plot the temperature time series.
# "TSG_TEMP" ThermoSalinoGraph Temperature data, measurement of SST (in degC).
fig, ax = plt.subplots()
ax.plot(df_subset["TSG_TEMP"]) 
ax.set_xlabel("Date")
ax.set_ylabel("Sea Surface Temperature (degC)")
ax.set_title("Temperature time series")

# The dates on the x-axis where overlapping, so I rotated the labels by 45 degrees.
fig.tight_layout()
plt.xticks(rotation=45)

# Saving the temperature time series plot.
fig.savefig("Temperature_timeseries.png", dpi=300)

# Show the temperature time series plots.
plt.show()

# Plot a histogram of the salinity distribution using bins of 0.5 psu between 30 and 35.
fig, ax = plt.subplots()
ax.hist(df_subset["TSG_SALINITY"], bins= np.arange(30, 35.5, 0.5))
ax.set_xlabel("Salinity (psu)")
ax.set_ylabel("Frequency")
ax.set_title("Salinity distribution")

fig.savefig("Salinity_histogram.png", dpi=300)
plt.show()

# Print the mean, SD, interquartile range for T and S in a table.
# Calculate statistics for temperature and salinity.
stats = pd.DataFrame({
    "Mean": df_subset[["TSG_TEMP", "TSG_SALINITY"]].mean(),
    "Std Dev": df_subset[["TSG_TEMP", "TSG_SALINITY"]].std(),
    "IQR": df_subset[["TSG_TEMP", "TSG_SALINITY"]].quantile(0.75)
           - df_subset[["TSG_TEMP", "TSG_SALINITY"]].quantile(0.25)
})

stats.index = ["Temperature", "Salinity"]
print(stats)

stats.to_csv("Temp_Salinity_stats_table.csv")

# Convert latitude to decimal degrees.
df_subset["LAT_DEC"] = ddmm2dd(df_subset["LATITUDE"])
df_subset.loc[df_subset["N_S"] == "S", "LAT_DEC"] *= -1

# Create a Scatter plot of wind speed and air temperature.
fig, ax = plt.subplots()

sc = ax.scatter(
    df_subset["WIND_SPEED_TRUE"],
    df_subset["AIR_TEMPERATURE"],
    c=df_subset["LAT_DEC"],
    cmap="viridis"
)

ax.set_xlabel("Wind speed (m/s)")
ax.set_ylabel("Air temperature (degC)")
ax.set_title("Wind speed vs Air temperature")

cbar = plt.colorbar(sc)
cbar.set_label("Latitude (°)")

fig.savefig("Wind_speed_Air_Temp_scatter.png", dpi=300)

plt.show()