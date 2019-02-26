#!/usr/bin/env python
import pandas as pd
import geopandas as gpd
from geopy.geocoders import Nominatim
from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderTimedOut
nom = Nominatim()
google = GoogleV3()

def lookup(place, coder=nom, timeout=60):
    place = place + ', South Africa'
    try:
        location = coder.geocode(place, timeout=timeout)
    except GeocoderTimedOut:
        location = 'UNKNOWN'
    return location

# The list in lynn_consolidated_list needs to be converted into a "clean" list with information:
# Name
# Gender
# Age
# Detail of death (description of death, not the post mortem number etc)
# Street
# Location
# Date of death - in format day/month/year - simple date, not "Died on", etc
# Comments
#
# Then Location needs to be converted into a geographic coordinate

# dates missing from file
# Naomi van Kerk - 7/9/1976
# Owen Leukes - 11/9/1976
# Moses Prince - 12/9/1976
# Batwa Sogibag (Sobyiba) - 12/10/1976
def filter_detail(detail):
    if str(detail) == 'nan':
        detail = ''
    elif '"' in str(detail):
        detail = ''
    else:
        lines = str(detail).strip().split('\n')
        detail = lines[-1]
        if 'Inquest number' in detail:
            detail = ''
    return detail

input_filename = 'lynn_consolidated_list.csv'
string_data = open(input_filename).read()
data = pd.read_csv(input_filename, skiprows=1, names=['Name', 'Gender', 'Age', 'Details', 'Street', 'Location', 'Date of death', 'Comments'])
data = data.dropna(how='all')  # remove blank lines
for detail in data['Details']:
    print(filter_detail(detail))
for gender in data['Gender']:
    print(gender.strip())
for index, row in data.iterrows():
    print(row['Gender'])
# place_set = set()
# for location in data['Location']:
#     place_set.add(location.strip())
# locations = []
# for place in sorted(place_set):
#     location = lookup(place)
#     print(place, location)
#     locations.append((place, location))
