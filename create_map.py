# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 18:52:38 2015

@author: Dudz
"""
import numpy as np

from collections import OrderedDict

import us_counties
import chi_demographics

from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import HoverTool
from bokeh.embed import components
from bokeh.palettes import Spectral11

def create_map(state, attribute):
        
    county_xs = []
    county_ys = []
    county_colors = []
    county_names = []
    county_attribute = []
    
    for county_id in us_counties.data:
        if state == 'All':
            county_xs.append(us_counties.data[county_id]['lons'])
            county_ys.append(us_counties.data[county_id]['lats'])
            try:
                attr = chi_demographics.data[county_id][attribute]
            except KeyError:
                pass
        elif us_counties.data[county_id]['state'] != state:
            continue
        else:
            county_xs.append(us_counties.data[county_id]['lons'])
            county_ys.append(us_counties.data[county_id]['lats'])
            try:
                attr = chi_demographics.data[county_id][attribute]
            except KeyError:
                pass
        county_names.append(us_counties.data[county_id]['name'])
        county_attribute.append(attr)
    
    colors = Spectral11    
    
    if np.min(county_attribute) < 0:
        min_attr = 0
    else:
        min_attr = np.min(county_attribute)
    
    max_attr = np.max(county_attribute)
    
    for i in county_attribute:
        freq, bins = np.histogram(i, bins=11, range=[min_attr, max_attr])
        freq = list(freq)
        idx = freq.index(1)
        county_colors.append(colors[idx])
    
    source = ColumnDataSource(
        data = dict(
            x=county_xs,
            y=county_ys,
            color=county_colors,
            name=county_names,
            attr=county_attribute,
        )
    )
    
    
    TOOLS="pan,wheel_zoom,box_zoom,reset,hover,save"
    
    p = figure(title="Poverty Levels in Texas", 
               plot_width=1400, plot_height=800,
               tools=TOOLS)
    
    p.patches('x', 'y',
        fill_color='color', fill_alpha=0.9,
        line_color="white", line_width=0.5,
        source=source)
    
    hover = p.select(dict(type=HoverTool))
    hover.point_policy = "follow_mouse"
    hover.tooltips = OrderedDict([
        ("Name", "@name"),
        ("Poverty", "@attr%"),
    ])
    
    script, div = components(p)
    
    return script, div