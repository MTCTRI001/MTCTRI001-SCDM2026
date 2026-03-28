# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 15:57:10 2026

@author: trist
"""

"""
P4 - Final Assignment
Student Number: MTCTRI001 
Student Name: Tristan Mitchell 
Coastal region I chose: Lüderitz   
"""

# Import all needed sub-modules and packages:
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.colors import LogNorm
import xarray as xr

"""
Plot 1: A large figure with the map of the region bathymetry, using an
adequate colormap
"""

# Defining the Lüderitz region, 200-300 km wide
west = 10.5
east = 16.0
south = -29.5
north = -25.5
extent = [west, east, south, north]

# Loading in the bathymetry dataset from GMRT
bathy = xr.open_dataset("luderitz_bathymetry.nc")
print(bathy)
"""
Dimensions:   (lat: 1028, lon: 1253)
Coordinates:
  * lat       (lat) float64 8kB -29.5 -29.5 -29.49 -29.49 ... -25.5 -25.5 -25.49
  * lon       (lon) float64 10kB 10.49 10.5 10.5 10.51 ... 15.99 15.99 16.0 16.0
Data variables:
    altitude  (lat, lon) float64 10MB ...
Attributes:
    title:        GMRT Grid
    history:      Projection: Cylindrical Equidistant\nExtracted from the Glo...
    Conventions:  COARDS,CF-1.6
    GMT_version:  4.5.7
"""

# Subset the bathymetry dataset to the Lüderitz coastal region
bathy = bathy.sel(lon = slice(west, east), lat = slice(south, north))

# Creating variables from the bathymetry dataset
lon = bathy["lon"]
lat = bathy["lat"]
depth = bathy["altitude"]
print(depth)
"""
<xarray.DataArray 'altitude' (lat: 1025, lon: 1250)> Size: 10MB
[1281250 values with dtype=float64]
Coordinates:
  * lat      (lat) float64 8kB -29.5 -29.49 -29.49 ... -25.51 -25.51 -25.5
  * lon      (lon) float64 10kB 10.5 10.51 10.51 10.52 ... 15.99 15.99 16.0
Attributes:
    long_name:      altitude
    standard_name:  altitude
    units:          m
    actual_range:   [-4872.95536548  1699.05238899]
"""

# Plotting the bathymetry map for Lüderitz coastal region
# Need to create a figure and axis object first 
fig = plt.figure(figsize = (10, 7))
ax = plt.axes(projection=ccrs.PlateCarree())

# Plotting the bathymetry data on the map axis
bathymetry_plot = depth.plot(ax=ax,
                             transform=ccrs.PlateCarree(), 
                             cmap = "terrain", # using the terrain colour map 
                             vmin = -5000,
                             vmax = 1000,
                             cbar_kwargs = {"label": "Elevation / Depth (m)"})

# Adjusting the colour bar appearance 
cbar = bathymetry_plot.colorbar
cbar.set_label("Elevation / Depth (m)", fontsize = 14)
cbar.ax.tick_params(labelsize = 12)

# Adding bathymetric contours to the Lüderitz coastal region plot 
ax.contour(lon, lat, depth,
           levels = np.arange(-4500, 1, 500),
           colors = "black",
           linewidths = 0.5,
           transform = ccrs.PlateCarree()) # Tells Cartopy the plotted data is in long and lat coordinates

# Adding main bathymetric contours to stand out on the plot
contours2 = ax.contour(lon, lat, depth,
                       levels = [-4000, -3000, -2000, -1000],
                       colors = "black",
                       linewidths = 1.0,
                       transform = ccrs.PlateCarree())

# Add depth labels to the main contour lines
ax.clabel(contours2,
          fmt = "%d m", # depth labels are whole numbers followed by the unit (m)
          fontsize = 10,
          inline = True) # Places the contour labels directly along the contour lines

ax.set_extent(extent, crs=ccrs.PlateCarree())
ax.coastlines(resolution="10m") # 1:10 million scale resolution 

# Adding in a marker and label to show the location of Lüderitz: 26.6420° S,15.1639° E from google
ax.plot(15.16, -26.65,
        marker = "o", # circle
        markersize = 5,
        color = "r",
        transform=ccrs.PlateCarree())

ax.text(15.20, -26.66, "Lüderitz",
        fontsize = 13,
        color = "black",
        transform=ccrs.PlateCarree())

# Add gridlines showing latitude and longitude
gl = ax.gridlines(
    draw_labels = True, # display the coordinate labels on the map
    linewidth = 0.5, # making the gridlines thinner 
    color ='gray', # grey colouring for the gridlines 
    alpha = 0.7, # making the gridlines slightly transparent 
    linestyle = '--') # dashed-line style  

# Removing labels for the top and right sides to make reading the plot easier
gl.top_labels = False
gl.right_labels = False

# Adding axis labels for longitude and latitude 
# Can't use the ax.set_xlabel & ax.set_ylabel commands because it's a cartopy map axis
fig.supxlabel("Longitude (°E)", fontsize = 14, x = 0.45, y = 0.09)
fig.supylabel("Latitude (°S)", fontsize = 14, x = 0.02)
fig.subplots_adjust(bottom = 0.12, left = 0.10) # need to also adjust the figure margins

# Adding a title
ax.set_title("Bathymetry of the Lüderitz Coastal Region", fontsize = 18)

# Saving the plot 
plt.savefig("Plot1_bathymetry_luderitz.png", dpi = 300, bbox_inches = "tight")

# Showing the plot
plt.show()






"""
Plot 2: 
A map of the mean annual chlorophyll. Choose carefully the range of values and 
the colormap, to display the different regions (Note: chlorophyll is usually 
plotted in logarithmic scale, but this is not a requirement)
"""

# Loading the satellite-derived chlorophyll concentration for the world ocean
chloro = xr.open_dataset("ESACCI-OC-MAPPED-CLIMATOLOGY-1M_MONTHLY_4km_PML_CHL-fv5.0.nc")
print(chloro) # Checking the variables in the dataset 
"""
<xarray.Dataset> Size: 2GB
Dimensions:  (time: 12, lat: 4320, lon: 8640)
Coordinates:
  * time     (time) datetime64[ns] 96B 1998-01-01 1998-02-01 ... 1997-12-01
  * lat      (lat) float64 35kB 89.98 89.94 89.9 89.85 ... -89.9 -89.94 -89.98
  * lon      (lon) float64 69kB -180.0 -179.9 -179.9 ... 179.9 179.9 180.0
Data variables:
    crs      int32 4B ...
    chlor_a  (time, lat, lon) float32 2GB ...
Attributes: (12/53)
    CDI:                               Climate Data Interface version ?? (htt...
    history:                           Tue Apr 27 20:27:21 2021: cdo selvar,c...
    source:                            NASA SeaWiFS  L1A and L2 R2018.0 LAC a...
    institution:                       Plymouth Marine Laboratory
    Conventions:                       CF-1.7
    Metadata_Conventions:              Unidata Dataset Discovery v1.0
                               ...
    time_coverage_start:               199801010000Z
    time_coverage_end:                 202001312359Z
    id:                                ESACCI-OC-MAPPED-CLIMATOLOGY-1M_MONTHL...
    NCO:                               4.7.2
    nco_openmp_thread_number:          1
    CDO:                               Climate Data Operators version 1.9.3 (...
"""

# Need to subset the chlorophyll data for the Lüderitz coastal region
chloro_subset = chloro.sel(lon = slice(west, east), lat = slice(north, south))
print(chloro_subset) 
"""
<xarray.Dataset> Size: 610kB
Dimensions:  (time: 12, lat: 96, lon: 132)
Coordinates:
  * time     (time) datetime64[ns] 96B 1998-01-01 1998-02-01 ... 1997-12-01
  * lat      (lat) float64 768B -25.52 -25.56 -25.6 ... -29.4 -29.44 -29.48
  * lon      (lon) float64 1kB 10.52 10.56 10.6 10.65 ... 15.85 15.9 15.94 15.98
Data variables:
    crs      int32 4B ...
    chlor_a  (time, lat, lon) float32 608kB ...
Attributes: (12/53)
    CDI:                               Climate Data Interface version ?? (htt...
    history:                           Tue Apr 27 20:27:21 2021: cdo selvar,c...
    source:                            NASA SeaWiFS  L1A and L2 R2018.0 LAC a...
    institution:                       Plymouth Marine Laboratory
    Conventions:                       CF-1.7
    Metadata_Conventions:              Unidata Dataset Discovery v1.0
                               ...
    time_coverage_start:               199801010000Z
    time_coverage_end:                 202001312359Z
    id:                                ESACCI-OC-MAPPED-CLIMATOLOGY-1M_MONTHL...
    NCO:                               4.7.2
    nco_openmp_thread_number:          1
    CDO:                               Climate Data Operators version 1.9.3 (...
"""

# Extracting only the chlorophyll concentration variable
chloro = chloro_subset["chlor_a"] 

# Calculating the mean annual chlorophyll concentration
chloro_annual = chloro.mean(dim = "time")

# Need to remove all zero or negative values before applying a logarithmic scale
chloro_annual = chloro_annual.where(chloro_annual > 0)
print(chloro_annual) 

# Check the mean values for the Lüderitz region
print("Min:", chloro_annual.min().values)
print("Max:", chloro_annual.max().values)
print("Mean:", chloro_annual.mean().values)
"""
Min: 0.19713683
Max: 8.921852
Mean: 0.7014003
"""

# Need to create a figure and axis object
fig = plt.figure(figsize=(10, 7))
ax = plt.axes(projection=ccrs.PlateCarree())

# Plotting the mean annual chlorophyll map using a logarithmic colour scale
chlorophyll_plot = chloro_annual.plot(ax=ax, 
                                     transform=ccrs.PlateCarree(),
                                     cmap = "viridis", # Using the viridis colour mapping
                                     norm = LogNorm(vmin=0.1, vmax=10),
                                     cbar_kwargs = {"label": "Chlorophyll-a (mg m$^{-3}$)"})

# Improving the colour bar and setting the ticks for the plot 
cbar = chlorophyll_plot.colorbar
cbar.set_label("Chlorophyll-a (mg m$^{-3}$)", fontsize = 14)
cbar.set_ticks([0.1, 0.2, 0.5, 1, 2, 5, 10])
cbar.set_ticklabels(["0.1", "0.2", "0.5", "1", "2", "5", "10"])

# Adding chlorophyll contour lines
chlorophyll_contours = ax.contour(chloro_subset["lon"], chloro_subset["lat"], chloro_annual,
                                  levels = [0.1, 0.2, 0.3, 0.5, 1, 2, 5, 10],
                                  colors = "black",
                                  linewidths = 0.8,
                                  alpha = 0.9,
                                  transform=ccrs.PlateCarree())

# Adding labels to the chlorophyll contour lines
ax.clabel(chlorophyll_contours,
          fmt = "%g", # removes the decimal notation after the chlorophyll contour values 
          fontsize = 12,
          inline = True) # Places the contour labels directly along the contour lines


# Adding a coastline and land background colour to the plot 
ax.set_extent(extent, crs=ccrs.PlateCarree())
# 'zorder' control the drawing order on the plot 
ax.add_feature(cfeature.LAND, facecolor = "lightgray", edgecolor = "black", zorder = 1)  
ax.coastlines(resolution="10m", zorder = 2) # 1:10 million scale resolution 

# Adding in a marker and label to show the location of Lüderitz: 26.6420° S,15.1639° E
ax.plot(15.16, -26.64,
        marker = "o",
        markersize = 5,
        color = "r",
        transform=ccrs.PlateCarree(),   
        zorder = 3)

ax.text(15.20, -26.66, "Lüderitz",
        fontsize = 13,
        color = "black",
        transform=ccrs.PlateCarree(),   
        zorder = 4)

# Add gridlines showing latitude and longitude
gl = ax.gridlines(
    draw_labels = True, # display the coordinate labels on the map
    linewidth = 0.5, # making the gridlines thinner 
    color = 'gray', # grey colouring for the gridlines 
    alpha = 0.7, # making the gridlines slightly transparent 
    linestyle = '--') # dashed-line style  

# Removing labels for the top and right sides to make reading the plot easier
gl.top_labels = False
gl.right_labels = False

# Adding axis labels for longitude and latitude, and adjusting the position 
fig.supxlabel("Longitude (°E)", fontsize = 14, x = 0.45, y = 0.09)
fig.supylabel("Latitude (°S)", fontsize = 14, x = 0.02)
fig.subplots_adjust(bottom = 0.12, left = 0.10) # need to adjust the figure margins as well

# Adding a title
ax.set_title("Mean Annual Chlorophyll for the Lüderitz Coastal Region", fontsize = 16)

# Saving the plot
plt.savefig("Plot2_mean_annual_chloro_luderitz.png", dpi = 300, bbox_inches = "tight")

# Showing the plot
plt.show()






"""
Plot 3: 
A faceted figure, showing 12 maps, one for each month. The colorbar range can
be different from the annual mean map, because it should show the seasonal 
variation.
"""
# Creating a faceted figure, showing 12 maps, one for each month
fig, axes = plt.subplots(3, 4, figsize=(16, 10),
                         subplot_kw={"projection": ccrs.PlateCarree()})

# Creating a list of month names to use as titles for each subplot
month_names = ["January", "February", "March", "April", "May", "June", "July",  
               "August", "September", "October", "November", "December"]

# Check the mean values for the Lüderitz coastal region
print("Minimum:", chloro.min().values)
print("Maximum:", chloro.max().values)
print("Mean:", chloro.mean().values)
"""
Minimum: 0.09138316
Maximum: 20.208591
Mean: 0.68698055

I chose vmax=10 because it captures more of the upper range without allowing 
extreme values to dominate the entire colour scale.
"""
# creating a 'for loop' to cycle through each plot
for monthly_index, ax in enumerate(axes.flat):  
    monthly_chl_plot = ax.pcolormesh(chloro_subset["lon"], chloro_subset["lat"],
                                     chloro.isel(time = monthly_index),
                                     cmap = "viridis", # Using the viridis colour mapping
                                     norm = LogNorm(vmin = 0.1, vmax = 10),
                                     transform=ccrs.PlateCarree())  
    
    # Adding a coastline and land background colour to each plot
    ax.set_extent(extent, crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.LAND, facecolor = "lightgray", edgecolor = "black", zorder = 1)
    ax.coastlines(resolution = "10m", zorder = 2) # 1:10 million scale resolution
    
    
    # Adding a marker and label to show the location of Lüderitz on the 12 plots 
    ax.plot(15.12, -26.64,
        marker = "o",
        markersize = 8,
        color = "r",
        transform=ccrs.PlateCarree(),
        zorder = 3)

    ax.text(15.25, -26.66, "L",
        fontsize = 15,
        color = "black",
        transform=ccrs.PlateCarree(),
        zorder = 4)
    
    # Add gridlines showing latitude and longitude
    gl = ax.gridlines(
        draw_labels = True, # display the coordinate labels on the map
        linewidth = 0.5, # making the gridlines thinner 
        color = 'grey', # grey colouring for the gridlines 
        alpha = 0.7, # making the gridlines slightly transparent 
        linestyle = '--') # dashed-line style  

    # Removing labels for the top and right sides to make reading the plot easier
    gl.top_labels = False
    gl.right_labels = False

    # This line of code only keeps labels on the outer panels for a cleaner plot 
    if monthly_index % 4 != 0: # If the subplot is not in the first column, turn off the latitude labels.
        gl.left_labels = False

    # setting the months name to the correct subplot
    ax.set_title(month_names[monthly_index], fontsize = 14)

# Adding a separate axis for the colour bar so that it doesn't overlap with the other plots
cbar_axis = fig.add_axes([0.90, 0.16, 0.025, 0.68])

# Improving the colour bar values to that it's easier to read on the plot  
cbar = fig.colorbar(monthly_chl_plot, cax=cbar_axis)
cbar.set_label("Chlorophyll-a (mg m$^{-3}$)", fontsize = 18)
cbar.ax.tick_params(labelsize = 10)

# Setting the tick values for the logarithmic colour bar
cbar.set_ticks([0.1, 0.2, 0.5, 1, 2, 5, 10])
cbar.set_ticklabels(["0.1", "0.2", "0.5", "1", "2", "5", "10"])

# Adding axis labels for longitude and latitude, and adjusting their position 
fig.supxlabel("Longitude (°E)", fontsize = 18, x = 0.50, y = 0.02)
fig.supylabel("Latitude (°S)", fontsize = 18, x = 0.02)

# Adding a title
fig.suptitle("Monthly Mean Chlorophyll for the Lüderitz Coastal Region", fontsize=24)

# Adjusting the plot spacing between panels and the colour bar
fig.subplots_adjust(right = 0.87, left = 0.08, wspace = 0.08,   
                    hspace = 0.25, top = 0.90, bottom = 0.08)

# Saving the plot
plt.savefig("Plot3_monthly_chlorophyll_luderitz.png", dpi = 300, bbox_inches = "tight")

# Showing the plot 
plt.show()






"""
Plot 4: 
A timeseries plot showing two lines: the mean seasonal cycle of the whole region 
compared with the timeseries from a single grid point of your choice, preferably 
close to an area of high chlorophyll (use the keyword method='nearest' to select 
the point)
"""

# Calculating the mean seasonal cycle for the Lüderitz coastal region
regional_cycle = chloro.mean(dim=["lat", "lon"])

# Selecting a single grid close to an area of high chlorophyll
point_lon = 15.8
point_lat = -28.5
selected_point_cycle = chloro.sel(lon=point_lon, lat=point_lat, method="nearest")

# Creating a variable for the nearest grid-point coordinates, as real numbers i.e a floats 
nearest_lon = float(selected_point_cycle.lon.values)
nearest_lat = float(selected_point_cycle.lat.values)

# Checking what the point coordinates are 
print(f"Selected point: lon={nearest_lon:.2f}, lat={nearest_lat:.2f}")
"""
Selected point: lon=15.81, lat=-28.52
"""

# Defining the month labels for the x-axis 
month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",   
               "Oct", "Nov", "Dec"]

# Numeric positions for the 12 months
x = np.arange(len(month_names))

# Need to create a figure and axis object
fig, ax = plt.subplots(figsize = (10, 6))

# Leaving room on the right for the selected grid point map
fig.subplots_adjust(right = 0.70)

# Plotting the two seasonal cycles 
ax.plot(x, regional_cycle.values,
        marker = "o", # circle markers 
        linewidth = 2.5,
        color = "b",
        label = "Regional mean")

ax.plot(x, selected_point_cycle.values,
        marker = "v", # triangle markers
        linewidth = 2.5,
        color = "orange",
        label = "Single grid point")

# Adding in the months labels to the y-axis 
ax.set_xticks(x)
ax.set_xticklabels(month_names, rotation = 40)

# Adding in the axis labels and plot title
ax.set_xlabel("Months", fontsize = 14)
ax.set_ylabel("Chlorophyll-a (mg m$^{-3}$)", fontsize = 14)
ax.set_title("Seasonal Cycle of Chlorophyll for the Lüderitz Coastal Region", fontsize = 16,    
             pad = 15) # Creating more space between the title and plot 

# Adding in the gridlines and axis ticks
ax.tick_params(axis="both", labelsize = 12)

ax.grid(True,   
        linestyle="--", # dashed-line style 
        linewidth = 0.7, # making the gridlines thinner   
        alpha = 0.7) # making the gridlines slightly transparent 

# Adding in a legend at the upper left corner 
ax.legend(loc="upper left", fontsize = 12)

# Creating the single grid point map to the side of the plot 
inset_ax = fig.add_axes([0.76, 0.605, 0.22, 0.28], projection=ccrs.PlateCarree())
inset_ax.set_extent(extent, crs=ccrs.PlateCarree())
inset_ax.add_feature(cfeature.LAND, facecolor = "lightgray", edgecolor = "black", zorder = 1)
inset_ax.coastlines(resolution="10m", zorder = 2)

# Plot the selected point on the inset map
inset_ax.plot(nearest_lon, nearest_lat,
              marker = "o", # circle 
              markersize=  7,
              color = "orange",
              transform=ccrs.PlateCarree(),
              zorder = 3)

# Add the label beside the red dot
inset_ax.text(nearest_lon -3.8, nearest_lat +0.06,
              "Single grid point",
              fontsize = 12,
              transform=ccrs.PlateCarree())

# Gridlines on the map
gl = inset_ax.gridlines(draw_labels = True, # display the coordinate labels on the map
                        linewidth = 0.5, # making the gridlines thinner 
                        color = 'grey', # grey colouring for the gridlines 
                        alpha = 0.7, # making the gridlines slightly transparent 
                        linestyle = '--') # dashed-line style  


# Removing labels for the top and right sides to make reading the plot easier
gl.top_labels = False
gl.right_labels = False

# Changing the font size of the gridline labels on the map 
gl.xlabel_style = {"size": 8}
gl.ylabel_style = {"size": 8}

# Saving the plot
plt.savefig("Plot4_seasonal_cycle_luderitz.png", dpi = 300, bbox_inches = "tight")

# Showing the plot
plt.show()
