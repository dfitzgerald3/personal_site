from __future__ import absolute_import

import csv
from os.path import join


data_dir = '/var/www/FlaskApp/FlaskApp/static/data/community_health/'

data = {}
with open(join(data_dir, 'DEMOGRAPHICS.csv')) as f:
    reader = csv.reader(f, delimiter=',', quotechar='"')
    for row in reader:
        state_id, county_id, population_size, population_density, poverty, age_19_under, age_19_64, age_65_84, age_85_older, white, black, native_american, asian, hispanic = row
        data[(int(state_id), int(county_id))] = {
            'population_size': int(population_size),
            'population_density': int(population_density),
            'poverty': float(poverty),
            'age_19_under': float(age_19_under),
            'age_19_64': float(age_19_64),
            'age_65_84': float(age_65_84),
            'age_85_older': float(age_85_older),
            'white': float(white),
            'black': float(black),
            'native_american': float(native_american),
            'asian': float(asian),
            'hispanic': float(hispanic)           
        }
        
