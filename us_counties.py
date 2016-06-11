from __future__ import absolute_import

import csv
import xml.etree.cElementTree as et
from os.path import join

data_dir = '/var/www/FlaskApp/FlaskApp/static/data/community_health/'

nan = float('NaN')

data = {}
with open(join(data_dir, 'US_Counties.csv')) as f:
    next(f)
    reader = csv.reader(f, delimiter=',', quotechar='"')
    for row in reader:
        name, dummy, state, dummy, geometry, dummy, dummy, dummy, dummy, state_id, county_id, dummy, dummy = row
        xml = et.fromstring(geometry)
        lats = []
        lons = []
        for i, poly in enumerate(xml.findall('.//outerBoundaryIs/LinearRing/coordinates')):
            if i > 0:
                lats.append(nan)
                lons.append(nan)
            coords = (c.split(',')[:2] for c in poly.text.split())
            lat, lon = list(zip(*[(float(lat), float(lon)) for lon, lat in
                coords]))
            lats.extend(lat)
            lons.extend(lon)
        data[(int(state_id), int(county_id))] = {
            'name' : name,
            'state' : state,
            'lats' : lats,
            'lons' : lons,
        }
