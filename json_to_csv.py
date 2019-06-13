#!/usr/bin/env python

import argparse
import json
from csv import DictWriter
from typing import TextIO

from pyproj import Proj, transform


def json2csv(jsonfile: TextIO, csvfile: TextIO) -> None:
    inProj = Proj(init='epsg:4326')
    outProj = Proj(init='epsg:3857')
    data = json.load(jsonfile)
    fieldnames = ['age', 'date_of_death', 'latitude', 'longitude', 'x', 'y', 'person', 'place', 'sex', 'detail', 'timestamp']
    writer = DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for record in data:
        (x, y) = transform(inProj, outProj, record['longitude'], record['latitude'])
        record['x'] = x
        record['y'] = y
        writer.writerow(record)
    csvfile.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert data in JSON to CSV format')
    parser.add_argument('jsonfile', type=argparse.FileType())
    parser.add_argument('csvfile', type=argparse.FileType('w'))
    args = parser.parse_args()

    json2csv(args.jsonfile, args.csvfile)
