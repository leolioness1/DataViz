import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# from mpl_toolkits.basemap import Basemap
# from shapely.geometry import Point, Polygon, MultiPoint, MultiPolygon
# from shapely.prepared import prep
#import fiona
# from matplotlib.collections import PatchCollection
# from descartes import PolygonPatch
import json, os
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go

json_path=os.getcwd()+"//Leo Location History.json"
with open(json_path, 'r') as fh:
    raw = json.loads(fh.read())

ld = pd.DataFrame(raw['locations'])
del raw #free up some memory

# convert to typical units
ld['latitudeE7'] = ld['latitudeE7']/float(1e7)
ld['longitudeE7'] = ld['longitudeE7']/float(1e7)
ld['timestampMs'] = ld['timestampMs'].map(lambda x: float(x)/1000) #to seconds
ld['datetime'] = ld.timestampMs.map(datetime.datetime.fromtimestamp)
ld['person'] = "Leo"
# Rename fields based on the conversions we just did
ld.rename(columns={'latitudeE7':'latitude', 'longitudeE7':'longitude', 'timestampMs':'timestamp'}, inplace=True)
ld = ld[ld.accuracy < 1000] #Ignore locations with accuracy estimates over 1000m
ld.reset_index(drop=True, inplace=True)

earliest_obs = min(ld["datetime"]).strftime('%m-%d-%Y')
latest_obs = max(ld["datetime"]).strftime('%m-%d-%Y')

print("earliest observed date: {}".format(earliest_obs))
print("latest observed date: {}".format(latest_obs))


import json

import dash
import dash_core_components as dcc
import dash_html_components as html
# import geopandas as gpd
import matplotlib
import matplotlib.cm as cm

mapbox_key = None
if not mapbox_key:
    raise RuntimeError("Mapbox key not specified! Edit this file and add it.")

# # Example shapefile from:
# lep_shp = 'data/lep/Limited_English_Proficiency.shp'
# lep_df = gpd.read_file(lep_shp)
#
# # Generate centroids for each polygon to use as marker locations
# lep_df['lon_lat'] = lep_df['geometry'].apply(lambda row: row.centroid)
# lep_df['LON'] = lep_df['lon_lat'].apply(lambda row: row.x)
# lep_df['LAT'] = lep_df['lon_lat'].apply(lambda row: row.y)
# lep_df = lep_df.drop('lon_lat', axis=1)
#
# lon = lep_df['LON'][0]
# lat = lep_df['LAT'][0]
#
# # Get list of languages given in the shapefile
# langs = [lng for lng in lep_df.columns
#          if lng.istitle() and
#          lng not in ['Id', 'Id2', 'Total_Pop_', 'Geography'] and
#          'Shape' not in lng]
#
# # Generate stats for example
# lep_df['NUM_LEP'] = lep_df[langs].sum(axis=1)
#
# # Create hover info text
# lep_df['HOVER'] = 'Geography: ' + lep_df.Geography + \
#     '<br /> Num. LEP:' + lep_df.NUM_LEP.astype(str)
#
# mcolors = matplotlib.colors


def set_overlay_colors(dataset):
    """Create overlay colors based on values
    :param dataset: gpd.Series, array of values to map colors to
    :returns: dict, hex color value for each language or index value
    """
    minima = dataset.min()
    maxima = dataset.max()
    norm = mcolors.Normalize(vmin=minima, vmax=maxima, clip=True)
    mapper = cm.ScalarMappable(norm=norm, cmap=cm.inferno)
    colors = [mcolors.to_hex(mapper.to_rgba(v)) for v in dataset]

    overlay_color = {
        idx: shade
        for idx, shade in zip(dataset.index, colors)
    }

    return overlay_color
# End set_overlay_colors()


# Create layer options that get displayed to the user in the dropdown
all_opt = {'label': 'All', 'value': 'All'}
opts = [{'label': lng.title(), 'value': lng} for lng in langs]
opts.append(all_opt)

# template for map
map_layout = {
    'title': 'our map',
    'data': [{
        'lon': ld['longitude'],
        'lat': ld['latitude'],
        'mode': 'markers',
        'marker': {
            'opacity': 0.0,
        },
        'type': 'scattermapbox',
        'name': 'Portland LEP',
        'text': lep_df['HOVER'],
        'hoverinfo': 'text',
        'showlegend': True,
    }],
    'layout': {
        'autosize': True,
        'hovermode': 'closest',
        'margin': {'l': 0, 'r': 0, 'b': 0, 't': 0},
        'mapbox': {
            'accesstoken': mapbox_key,
            'center': {
                'lat': lat,
                'lon': lon
            },
            'zoom': 8.0,
            'bearing': 0.0,
            'pitch': 0.0,
        },
    }
}

app = dash.Dash()

app.layout = html.Div([
    html.H1(children='Portland - Limited English Proficiency (Choropleth Example)'),
    dcc.Dropdown(
        id='overlay-choice',
        options=opts,
        value='All'
    ),
    html.Div([
        dcc.Graph(id='map-display'),
    ])
])


@app.callback(
    dash.dependencies.Output('map-display', 'figure'),
    [dash.dependencies.Input('overlay-choice', 'value')])
def update_map(overlay_choice):

    tmp = map_layout.copy()
    if overlay_choice == 'All':
        dataset = lep_df
        colors = set_overlay_colors(lep_df.NUM_LEP)
        tmp['data'][0]['text'] = lep_df['HOVER']
    else:
        dataset = lep_df.loc[lep_df[overlay_choice] > 0, :]

        colors = set_overlay_colors(dataset[overlay_choice])

        # Update hovertext display
        hovertext = lep_df['Geography'].str.cat(
                        lep_df[overlay_choice].astype(str), sep=': ')
        tmp['data'][0]['text'] = hovertext
    # End if

    # Create a layer for each region colored by LEP value
    layers = [{
        'name': overlay_choice,
        'source': json.loads(dataset.loc[dataset.index == i, :].to_json()),
        'sourcetype': 'geojson',
        'type': 'fill',
        'opacity': 1.0,
        'color': colors[i]
    } for i in dataset.index]

    tmp['layout']['mapbox']['layers'] = layers

    return tmp
# End update_map()


if __name__ == '__main__':
    app.run_server(debug=True, port=8051)

# # Building our Graphs
#
# data_choropleth = dict(type='choropleth',
#                        locations=df_emission_0['country_name'],
#                        # There are three ways to 'merge' your data with the data pre embedded in the map
#                        locationmode='country names',
#                        z=np.log(df_emission_0['CO2_emissions']),
#                        text=df_emission_0['country_name'],
#                        colorscale='inferno',
#                        colorbar=dict(title='CO2 Emissions log scaled')
#                        )
#
# layout_choropleth = dict(geo=dict(scope='world',  # default
#                                   projection=dict(type='orthographic'
#                                                   ),
#                                   # showland=True,   # default = True
#                                   landcolor='black',
#                                   lakecolor='white',
#                                   showocean=True,  # default = False
#                                   oceancolor='azure'
#                                   ),
#
#                          title=dict(text='World Choropleth Map',
#                                     x=.5  # Title relative position according to the xaxis, range (0,1)
#                                     )
#                          )
#
# fig = go.Figure(data=data_choropleth, layout=layout_choropleth)

# The App itself

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div(children=[
    html.H1(children='Location Data Dashboard'),

    html.Div(children='''
        Example of html Container
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)



