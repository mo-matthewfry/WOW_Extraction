#!/usr/bin/env python3.7
# -*- coding: iso-8859-1 -*-
"""
metdb_wow_extracton.py

Adapted from metdb_modes_extraction.py, by Sharon Jewell

Script to extract observations data from the metdb database based on an example available at
http://www-mdb-apps/metdb-python/html/examples.html

This script is specifically for extracting WOW data and writing all unique values to file

"""

import metdb
from datetime import datetime,timedelta
import os

OBS_TYPE = 'SRFC_GUST_SPED'
doPlot = False

#------------------------------------------------------------------------------
# Write to file
#------------------------------------------------------------------------------

def write_obs_to_file(filename, obs):

	"""
	Writes the WOW data to a temporary file and then sort to only contain unique lines
	The data is a csv list with one line per measurement
	The columns are:
	longitude of measurement, lattitude of measurement, pressure at station height
	"""

	# Write to file
	with open(filename, 'w') as outfile:

		# Loop over each ascent
		for point in range(len(obs)):

			# Use one line per measurement.
			sttn_id = obs[point]['SITE_KEY']
			lon = obs[point]['LNGD']
			lat = obs[point]['LTTD']
			pressure = obs[point][OBS_TYPE]

			# Write location to file
			out_str = '{},{:16.12f}, {:16.12f}, {:8.2f}'.format(sttn_id,lon, lat, 		 			  pressure)
			outfile.write('{0}\n'.format(out_str))

		

	return


def main():
	"""
	Main Script
	"""

	# Set study extraction date
	obs_date = 20210730

	contact = 'matthew.fry@metoffice.gov.uk'
	obstype = 'WOW'
	uk_area = 'AREA 61.0N 49.0N 12.0W 3.0E'

	elements = ['SITE_KEY','LTTD', 'LNGD', OBS_TYPE]

	datadir = '/scratch/mfry/wow/'
	tempfile = '{0}/wow_temp.txt'.format(datadir)
	
	start_time = datetime.strptime(str(obs_date) + "0000", "%Y%m%d%H%M")
	end_time = start_time + timedelta(hours = 24)
	
	obs = metdb.obs(contact, obstype,
      		keywords=['START TIME {0:%Y%m%d/%H%MZ}'.format(start_time),
                	  'END TIME {0:%Y%m%d/%H%MZ}'.format(end_time),
			  uk_area],
                elements=elements)

	write_obs_to_file(tempfile, obs)

	# Extract only the unique entries
	filename = '{0}/wow_{1}.txt'.format(datadir, obs_date)
	command = "sort -u {0} > {1}".format(tempfile, filename)
	os.system(command)


	if doPlot:
		import matplotlib.pyplot as plt
		import cartopy.crs as ccrs

		ax = plt.axes(projection=ccrs.PlateCarree())
		plt.scatter(obs['LNGD'], obs['LTTD'], c=obs['SRFC_GUST_SPED'], cmap='coolwarm', 	            	    transform=ccrs.PlateCarree())
		ax.stock_img()
		ax.set_extent([-12.0, 3.0, 49.0, 61.0], ccrs.PlateCarree())

		plt.title('{date:%Y%m%d} WOW observations in the period between {start_time:%H:%MZ}'
			  'and {end_time:%H:%MZ}'.format(date=start_time, start_time=start_time,
				                     end_time=end_time))
		plt.colorbar()
		plt.show()
	

if __name__ == '__main__':
    main()

