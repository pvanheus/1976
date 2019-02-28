#!/usr/bin/env python
import datetime
import json
import os.path
import random
import re
from io import StringIO
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderTimedOut

nom = Nominatim()
google = GoogleV3()
random.seed(1551374432)

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
# data = pd.read_csv(input_filename, skiprows=1, names=['Name', 'Gender', 'Age', 'Details', 'Street', 'Location', 'Date of death', 'Comments'])
data = pd.read_csv(input_filename)
clean_data_list = []
data = data.fillna('Unknown')
for i, row in data.iterrows():
    if row['PLACE of death'].strip() == 'Unknown':
        continue
    detail = ''
    for line in StringIO(row['CAUSE OF DEATH']):
        line = line.strip()
        if line == '' or 'mortem' in line.lower() or 'Inquest number' in line or 'Inquiry number' in line or 'arson' in line or 'public violence' in line:
            continue
        detail += line + ' '
    detail = detail.strip()
    date = ''
    look_for_died = False
    for line in StringIO(str(row['DATE of death'])):
        line = line.strip()
        if line == '':
            continue
        elif 'Shot' in line:
            look_for_died = True
            continue
        elif look_for_died and 'Died' in line:
            date += line.split()[1]
            look_for_died = False
        else:
            date += line
        # print(row['Age'])
        row.at['DATE of death'] = date
        row.at['CAUSE OF DEATH'] = detail
        row.at['PLACE of death'] = row['PLACE of death'].strip()
        # print(row['CAUSE OF DEATH'])
    clean_data_list.append(row)
    # print(row.name)
clean_data = pd.DataFrame.from_dict(dict([(s.name, s) for s in clean_data_list]), orient='index')
location_set = set(clean_data['PLACE of death'])
# for location in sorted(location_set):
#     print(location)
# data = data.dropna(how='all')  # remove blank lines
# for detail in data['Details']:
#     print(filter_detail(detail))
# for gender in data['Gender']:
#     print(gender.strip())
# for index, row in data.iterrows():
#     print(row['Gender'])
# place_set = set()
# for location in data['Location']:
#     place_set.add(location.strip())
# locations = []
cache_filename = 'locations.json'
try:
    locations = json.load(open(cache_filename))
except (IOError, json.decoder.JSONDecodeError):
    locations = dict()
    for place in sorted(location_set):
        if place == 'Nyanga East':
            # location lookup of Nyanga East gets it wrong, so substitute Nyanga latitude
            latitude = -33.9869444
            longitude = 18.5847222
        elif place == 'Nyanga':
            # looked-up location for Nyanga
            latitude = -33.98798
            longitude = 18.57589
        elif place == 'Caledon Square':
            # lookup does Caledon Square incorrectly
            latitude = -33.92759
            longitude = 18.42230
        else:
            location = lookup(place)
            latitude = location.latitude
            longitude = location.longitude
        print(place, location, location.longitude, location.latitude)
        locations[place] = dict(latitude=latitude, longitude=longitude)
    json.dump(locations, open(cache_filename, 'w'), indent=2, sort_keys=True)

date_re = re.compile('^\d+/\d+/\d+$')
relaxed_date_re = re.compile('\d+/\d+/\d+$')
searchable_dates = []
longitudes = []
latitudes = []
deaths_by_place = dict()
for i, row in clean_data.iterrows():
    place = row['PLACE of death']
    deaths_by_place[place] = deaths_by_place.get(place, 0) + 1
    longitudes.append(locations[place]['longitude'])
    latitudes.append(locations[place]['latitude'])
    date = row['DATE of death'].strip()
    if not date_re.match(date) and date != 'Unknown':
        # deal with problematic dates where the searchable date is
        # not the same as the display date
        # print(row['NAME'], date)
        date_match = relaxed_date_re.search(date)
        if date_match is None:
            print('PROBLEM DATE:', row['NAME'], date)
            exit(1)
        else:
            date = date_match.group(0)
    try:
        if date == 'Unknown':
            searchable_dates.append(-1)
        else:
            searchable_dates.append(int(datetime.datetime.strptime(date,'%d/%m/%Y').timestamp()))
    except ValueError as e:
        print("failed to parse", date, row['NAME'], str(e))

print("Places and number of deaths")
for place in sorted(deaths_by_place.keys()):
    print(place, deaths_by_place[place])
clean_data['longitude'] = longitudes
clean_data['latitude'] = latitudes
clean_data['searchable_date'] = searchable_dates
# print(clean_data)
output_data = []
for i, row in clean_data.iterrows():
    place = row['PLACE of death']
    if deaths_by_place[place] > 1:
        fudge_lat = (random.random() - 0.5) / 50
        fudge_long = (random.random() - 0.5) / 50
    else:
        fudge_lat = 0
        fudge_long = 0
    row.index = pd.Index(['person', 'sex', 'age', 'detail', 'place', 'date_of_death', 'longitude', 'latitude', 'timestamp'])
    row.at['latitude'] += fudge_lat
    row.at['longitude'] += fudge_long
    output_data.append(row.to_dict())

places_output = {}
for place in deaths_by_place:
    places_output[place] = {
                            'name': place,
                            'longitude': locations[place]['longitude'],
                            'latitude': locations[place]['latitude'],
                            'number_of_deaths': deaths_by_place[place]
                           }

json.dump(places_output, open('1976_cape_death_places.json', 'w'), indent=4, sort_keys=True)
json.dump(output_data, open('1976_cape_deaths.json', 'w'), indent=4, sort_keys=True)
# json.dump(clean_data.to_dict(orient='index'), open('1976_cape_deaths.json', 'w'))