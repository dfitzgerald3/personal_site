from __future__ import absolute_import

import csv
from os.path import join


data_dir = '/var/www/FlaskApp/FlaskApp/static/data/community_health/'

data = {}
with open(join(data_dir, 'MEASURESOFBIRTHANDDEATH_filt.csv')) as f:
    next(f)
    reader = csv.reader(f, delimiter=',', quotechar='"')
    for row in reader:
        state_id, county_id, lbw, lbw_ind, vlbw, vlbw_ind, premature, premature_ind, under_18, under_18_ind, over_40, over_40_ind, unmarried, unmarried_ind, late_care, late_care_ind, im, im_ind, im_wh, im_wh_ind, im_bl, im_bl_ind, im_h, im_h_ind, im_neonatal, im_neonatal_ind, im_postneonatal, im_postneonatal_ind, breast_cancer, breast_cancer_ind, col_cancer, col_cancer_ind, chd, chd_ind, homicide, homicide_ind, lung_cancer, lung_cancer_ind, mva, mva_ind, stroke, stroke_ind, suicide, suicide_ind, injury, injury_ind, total_birth, total_death = row
        data[(int(state_id), int(county_id))] = {
            'lbw': float(lbw),
            'lbw_ind': float(lbw_ind),
            'vlbw': float(vlbw),
            'vlbw_ind': float(vlbw_ind),
            'premature': float(premature),
            'premature_ind': float(premature_ind),
            'under_18': float(under_18),
            'under_18_ind': float(under_18_ind),
            'over_40': float(over_40),
            'over_40_ind': float(over_40_ind),
            'unmarried': float(unmarried),
            'unmarried_ind': float(unmarried_ind),       
            'late_care': float(late_care),
            'late_care_ind': float(late_care_ind),
            'im': float(im),
            'im_ind': float(im_ind),
            'im_wh': float(im_wh),
            'im_wh_ind': float(im_wh_ind),
            'im_bl': float(im_bl),
            'im_bl_ind': float(im_bl_ind),
            'im_h': float(im_h),
            'im_h_ind': float(im_h_ind),
            'im_neonatal': float(im_neonatal),
            'im_neonatal_ind': float(im_neonatal_ind),
            'im_postneonatal': float(im_postneonatal),
            'im_postneonatal_ind': float(im_postneonatal_ind),
            'breast_cancer': float(breast_cancer),
            'breast_cancer_ind': float(breast_cancer_ind),
            'col_cancer': float(col_cancer),
            'col_cancer_ind': float(col_cancer_ind),
            'chd': float(chd),
            'chd_ind': float(chd_ind),
            'homicide': float(homicide),
            'homicide_ind': float(homicide_ind),
            'lung_cancer': float(lung_cancer),
            'lung_cancer_ind': float(lung_cancer_ind),
            'mva': float(mva),
            'mva_ind': float(mva_ind),
            'stroke': float(stroke),
            'stroke_ind': float(stroke_ind),
            'suicide': float(suicide),
            'suicide_ind': float(suicide_ind),
            'injury': float(injury),
            'injury_ind': float(injury_ind),
            'total_birth': float(total_birth),
            'total_death': float(total_death)
        }