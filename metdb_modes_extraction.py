#!/usr/bin/env python3.7
# -*- coding: iso-8859-1 -*-
"""
metdb_modes_extracton.py

Script to extract observations data from the metdb database based on an example available at
http://www-mdb-apps/metdb-python/html/examples.html

This script is specifically for extracting Mode-S data and writing all unique values to file

"""

import metdb
from datetime import datetime, timedelta
import os
#------------------------------------------------------------------------------
# Write to file
#------------------------------------------------------------------------------
def write_obs_to_file(filename, obs):
    """
    Writes the mode-s data to a temporary file and then sort to only contain unique lines
    The data is a csv list with one line per measurement
    The columns are:
    longitude of measurement, lattitude of measurement, pressure at aircraft height
    """

    # Write to file
    with open(filename, 'w') as outfile:

        # Loop over each ascent
        for point in range(len(obs)):

            # Use one line per measurement.
            lon = obs[point]['LNGD']
            lat = obs[point]['LTTD']
            pressure = obs[point]['STTN_PESR']
#            pressure = obs[point]['BRMTC_PESR']

            # Write location to file
            out_str = '{0:16.12f}, {1:16.12f}, {2:8.2f}'.format(lon, lat, pressure)
            outfile.write('{0}\n'.format(out_str))

    return

#------------------------------------------------------------------------------
# Plots data using cartopy
#------------------------------------------------------------------------------
def main():
    """
    Main script
    """
    # Set study extraction period
#    first = 20210201
#    last = 20210731
    first = 20210801
    last = 20210807

    # Set metdb extraction fixed parameters
    contact = 'matthew.fry@metoffice.gov.uk'
    obstype = 'WOW'
    uk_area = 'AREA 61.0N 49.0N 12.0W 3.0E'

    # The following extracts lattitude, longitude and pressure for each mode-s entry
#    elements=['HOUR' ,'MINT', 'LTTD', 'LNGD', 'PESR_ALTD']
#    elements=['LTTD', 'LNGD', 'BRMTC_PESR']
    elements=['LTTD', 'LNGD', 'STTN_PESR']

    # Set root directory for output data and temp file to hold data temporarily
    datadir = '/scratch/mfry/modes/'
    tempfile = '{0}/modes_temp.txt'.format(datadir)

    # Create start and end day time objects and initialiser counter
    start = datetime.strptime(str(first) + "0000", "%Y%m%d%H%M")
    end = datetime.strptime(str(last) + "0000", "%Y%m%d%H%M")
    current = start

    # Loop over each previous day
    while current <= end:

        # Get date stamp for current day
        datestamp = datetime.strftime(current, "%Y%m%d")

        #(a) first 6 hours
        # Get the obs from MetDB/MOODS.
        for quarter in [("1", "00", "05"), ("2", "06", "11"), ("3", "12", "17"), ("4", "18", "23")]:
            print(datestamp, quarter[0])
            obs = metdb.obs(contact, obstype,
                            keywords=['START TIME {0}/{1}00Z'.format(datestamp, quarter[1]),
                                      'END TIME {0}/{1}59Z'.format(datestamp, quarter[2]),
                                      uk_area],
                            elements=elements)

            # Write data for this day to file
            write_obs_to_file(tempfile, obs)

            # Extract only the unique entries
            filename = '{0}/modes_{1}_{2}.txt'.format(datadir, datestamp, quarter[0])
            command = "sort -u {0} > {1}".format(tempfile, filename)
            os.system(command)

        # Move to next day in series
        current += timedelta(days=1)

if __name__ == '__main__':
    main()
