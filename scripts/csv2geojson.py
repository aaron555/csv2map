#!/usr/bin/env python3

# Convert CSV file to GeoJSON feature collection for overlaying on LeafletJS map

# Syntax: csv2geojson.py <input CSV file/path> [<Output GeoJSON file/path>]

# <input CSV file/path> - File/path of CSV - CSV must have at least 3 columns - 'latitude, longitude, label[, ...]'  - note header of column 3-> will be used as names for respective data
# NOTE the first column MUST be the decimal latitude and the second column MUST be the decimal longitude.  This will be assumed and headers ignored.
# There must be exactly one header row, and it must contain at least as many columns as all the subsequent data
# If <Output GeoJSON file/path> is not specified default "points-geojson.js" will be used - note if this file exists it will be over-written

# Example calls:
# csv2geojson.py "input_file.csv"
# csv2geojson.py "/tmp/input_file.csv" "/var/www/html/mygeojsonfile.js"

# Each popup on the map will contain the latitude and longitude in bold, and then contain an additional line for each additional column in the CSV
# Each subsequent line will be in form "Header: data"

# Changelog
# 02/12/2020 - First Version
# 12/04/2021 - Improved error handling and user feedback

# Copyright (C) 2020,2021 Aaron Lockton

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from geojson import Feature, FeatureCollection, Point, dump
import csv
import sys
import os
from time import gmtime, strftime

print(strftime("%Y-%m-%d_%H:%M:%S: Starting conversion of data from CSV to GeoJSON", gmtime()))

# Process arguments and set defaults
if len(sys.argv) < 2:
  print("ERROR: You must specify a valid CSV file of input data as first argument")
  sys.exit(1)
elif os.path.isfile(sys.argv[1]) != 1:
  print("ERROR: You must specify a valid CSV file of input data as first argument - cannot find file: "+sys.argv[1])
  sys.exit(1)
else:
  # Input file is first argument
  csv_input = sys.argv[1]

if len(sys.argv) > 2:
  # Output file is second argument, if specified
  json_output = sys.argv[2]
  output_dir = os.path.dirname(json_output)
  if os.path.isdir(output_dir) != 1 and output_dir != "":
    # Empty directory is valid, this will use current working directory
    print("ERROR: Specified output directory '%s' does not exist" % output_dir)
    sys.exit(1)
else:
  print("WARNING: No output file specified, using default 'points-geojson.js' in current working directory")
  json_output = "points-geojson.js"
if os.path.isfile(json_output) == 1:
  print("WARNING: specified output file '%s' already exists, and will be overwritten" % json_output)


# Set up output arrays
labels = []
lats = []
lons = []
output_array = []

# Read in values from CSV
print("Opening CSV file %s and importing data..." % csv_input)
try:
  with open(csv_input, 'r') as csv_data:
    csv_reader = csv.reader(csv_data, delimiter=',')
    line_count = 0
    for row in csv_reader:
      # First row must be header
      if line_count == 0:
        # Assume first and second row are lat,lon, ignore headers
        for ii, label in enumerate(row):
          if ii > 1:
            labels.append(label)
        line_count += 1
      else:
        if len(row) <= len(labels)+2 and len(row) >= 3:
          try:
            rowlat = float(row[0])
            rowlon = float(row[1])
            lats.append(rowlat)
            lons.append(rowlon)
            output_array.append(row[2:])
            line_count += 1
          except:
            # Missing Lat, Lon will through exception - this data is useless
            print("WARNING: Ignoring invalid line: "+", ".join(row))
        else:
          # More columns than header not accepted - however missing data or columns is OK (of course if completely missing not empty will be incorrectly labelled)
          print("WARNING: Ignoring invalid line (number of elements exceeds header, or contains only coordinates with no label): "+", ".join(row))
except IOError:
  print("ERROR: Cannot read from file (check permissions?): "+csv_input)
  sys.exit(1)

# Check input data
if line_count < 2:
  print("ERROR: Input CSV must contain at least 1 header line AND one data line")
  sys.exit(1)
else:
  print("Read "+str(line_count)+" lines from input CSV (inc header)")

# Create GeoJSON features
print("Creating GeoJSON features and writing to file "+json_output)
feature_collection = {"type": "FeatureCollection", "features": []}

location_counter = 0
for  lon, lat, data in zip(lons, lats, output_array):
  popupstr="<b>"+str(lat)+", "+str(lon)
  for ii,element in enumerate(data):
    popupstr+="</b><br />"+labels[ii]+": "+element
  feature_element = Feature(geometry=Point(([lon, lat])), properties={"name": labels[0]+": "+data[0], "popupContent": popupstr})
  feature_collection["features"].append(feature_element)
  location_counter+=1

try:
  with open(json_output, 'w') as out:
    out.write("var locations=")
except IOError:
  print("ERROR: Cannot write to file (check permissions?): "+json_output)
  sys.exit(1)

with open(json_output, 'a') as out:
  dump(feature_collection, out)

print(strftime("%Y-%m-%d_%H:%M:%S: Completed conversion of data from CSV to GeoJSON", gmtime())+", wrote "+str(location_counter)+" location(s) to file")
