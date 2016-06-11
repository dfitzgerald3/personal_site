from flask import Flask, render_template, request, jsonify
import numpy as np
import wikipedia

import us_counties
import chi_demographics
from state_list import state_dict
from demographics_list import demographics_dict
import operator
#import create_map as create_map
import json

from collections import OrderedDict

from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import HoverTool
from bokeh.embed import components
from bokeh.palettes import Spectral11


app = Flask(__name__)


#Navbar links
@app.route('/')
def homepage():
    return render_template('main.html')
    
@app.route('/aboutme/')
def aboutme():
    return render_template('aboutme.html')
    
@app.route('/webapps/')
def webapps():
    return render_template('/webapps.html')
    


#Function that faciliates WikiLocation
def wiki_geosearch(lat, lon, rad):
    loc_name = wikipedia.geosearch(lat, lon, radius=rad, results=30)    
    latLon = np.zeros(len(loc_name) * 2)
    summary = list()
    urls = list()
    x = 0
    y = 0
    while y < len(loc_name):
        page = wikipedia.page(str(loc_name[y]))
        sum_des = page.summary.encode('utf-8')
        summary.append(sum_des)
        url = page.url.encode('utf-8')
        urls.append(url)
        coord = page.coordinates        
        loc_name[y] = str(loc_name[y])          
        latLon[x] = float(coord[0])
        latLon[x+1] = float(coord[1])        
        x += 2
        y += 1
    latLon = latLon.reshape(len(loc_name), 2)
    latLon = latLon.tolist()
    return latLon, loc_name, summary, urls
    

@app.route('/get_markers', methods=['GET', 'POST'])
def get_markers():
    get = request.json
    lat = get['lat']
    lon = get['lng']
    latLon, loc_name, summary, urls = wiki_geosearch(lat, lon, 5000)
    
    return jsonify(result=[latLon, loc_name, summary, urls])
    


#Function to create maps
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
    
    
    TOOLS="hover"
    
    if state == 'All':
        chart_title = demographics_dict()[attribute] + ' in United States'
    else:
        chart_title = demographics_dict()[attribute] + ' in ' + state
    
    p = figure(title=chart_title,
               x_axis_label='Latitude',
               y_axis_label='Longitude',
               plot_width=1400, 
               plot_height=800,
               tools=TOOLS)
    
    p.patches('x', 'y',
        fill_color='color', fill_alpha=0.9,
        line_color="white", line_width=0.5,
        source=source)
    
    hover = p.select(dict(type=HoverTool))
    hover.point_policy = "follow_mouse"
    hover.tooltips = OrderedDict([
        ("Name", "@name"),
        (attribute, "@attr%"),
    ])
    
    script, div = components(p)
    
    return script, div



@app.route('/dataanalysis/')
def dataanalysis():
    state_list = state_dict()
    state_list = sorted(state_list.items(), key=operator.itemgetter(1))
    
    demographics_list = demographics_dict()
    demographics_list = sorted(demographics_list.items(), key=operator.itemgetter(1))

    state = 'wy'
    attribute = 'poverty'    
    
    script, div = create_map(state, attribute)
        
    return render_template('dataanalysis.html', 
                           script=script, 
                           div=div, 
                           state_list=state_list,
                           demographics_list=demographics_list)
                           


@app.route('/update_map', methods=['GET', 'POST'])
def map_update():
    get = request.json
    state = get['state']
    if state == 'All':
        state = 'All'
    else:
        state = state_dict()[state]
    attr = get['attribute']
    for key, value in demographics_dict().items():
        if value == str(attr):
            attr = key
    script, div = create_map(state, attr)
#    return json.dumps({'script': script, 'div': div})
    return jsonify(result=[script, div])
    #return jsonify(result=[state, attr])



if __name__ == "__main__":
    app.debug = True
    app.run()

