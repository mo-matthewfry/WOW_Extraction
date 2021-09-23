#!/usr/bin/env python3.7
# -*- coding: iso-8859-1 -*-

import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import os

def max_gust_per_site(filename,output):
	
	#Reading in WOW data, creating dataframe
	df = pd.read_csv(filename)
	
	#Adding column headings to dataframe
	df.columns = ['ID','LNGD','LTTD','SRFC_GUST_SPED']

	#Simultaneously grouping by site and sorting by max gust value
	g = df.groupby(by=["ID"])['SRFC_GUST_SPED'].transform('max')

	#Removing non-maximal gusts and null data. Converts data to float
	df = df.drop_duplicates('ID', keep='last')
	df = df[df.SRFC_GUST_SPED != ' --'].astype({"SRFC_GUST_SPED": float})

	#Plotting max gusts on UK map and saving a file of maximum gusts
	max_gust_map(df)
	df.to_csv(output, header=None, index=None)	


def max_gust_map(df):
	
	#Settting up background for CartoPy
	os.environ["CARTOPY_USER_BACKGROUNDS"] = "/home/h06/mfry/Pictures/cartopy_bg"

	ax = plt.axes(projection=ccrs.PlateCarree())
	plt.scatter(df['LNGD'], df['LTTD'], marker='x', c=df['SRFC_GUST_SPED'], cmap='coolwarm', 	             transform=ccrs.PlateCarree())
	ax.background_img(name='BM', resolution='med-high')
	#ax.stock_img()
	ax.set_extent([-12.0, 3.0, 49.0, 61.0], ccrs.PlateCarree())
	
	#Colorbar settings
	cbar = plt.colorbar(shrink=0.85)
	cbar.set_label(r'Max. Gust Speed ms$^{-1}$')
	
	plt.title("Max. Wind Gust from WOW 20210730 0000Z to 2359Z")	

	plt.show()

	return

def main():
	
	#Input data file
	filename = '/scratch/mfry/wow/wow_20210730.txt'

	#Output data file
	output = '/scratch/mfry/wow/wow_maxgust_20210730_full.txt'
	
	max_gust_per_site(filename,output)


if __name__ == '__main__':
    main()
