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
import plotly.offline as pyo

json_path=os.getcwd()+"//Leo Location History.json"
with open(json_path, 'r') as fh:
    raw = json.loads(fh.read())

location_data = pd.DataFrame(raw['locations'])
del raw #free up some memory

# convert to typical units
location_data['latitudeE7'] = location_data['latitudeE7']/float(1e7)
location_data['longitudeE7'] = location_data['longitudeE7']/float(1e7)
location_data['timestampMs'] = location_data['timestampMs'].map(lambda x: float(x)/1000) #to seconds
location_data['datetime'] = location_data.timestampMs.map(datetime.datetime.fromtimestamp)
location_data['person'] = "Leo"
# Rename fielocation_datas based on the conversions we just did
location_data.rename(columns={'latitudeE7':'latitude', 'longitudeE7':'longitude', 'timestampMs':'timestamp'}, inplace=True)
location_data = location_data[location_data.accuracy < 1000] #Ignore locations with accuracy estimates over 1000m
location_data.reset_index(drop=True, inplace=True)

earliest_obs = min(location_data["datetime"]).strftime('%m-%d-%Y')
latest_obs = max(location_data["datetime"]).strftime('%m-%d-%Y')

print("earliest observed date: {}".format(earliest_obs))
print("latest observed date: {}".format(latest_obs))

degrees_to_radians = np.pi/180.0
location_data['phi'] = (90.0 - location_data.latitude) * degrees_to_radians
location_data['theta'] = location_data.longitude * degrees_to_radians
# Compute distance between two GPS points on a unit sphere
location_data['distance'] = np.arccos(
    np.sin(location_data.phi)*np.sin(location_data.phi.shift(-1)) * np.cos(location_data.theta - location_data.theta.shift(-1)) +
    np.cos(location_data.phi)*np.cos(location_data.phi.shift(-1))) * 6378.100 # radius of earth in km

location_data['speed'] = location_data.distance/(location_data.timestamp - location_data.timestamp.shift(-1))*3600 #km/hr

longitudes = location_data['longitude'].tolist()
latitudes = location_data['latitude'].tolist()

fig = go.Figure(go.Scattermapbox(
    mode = "markers",
    lon = longitudes,
    lat = latitudes,
    marker = {'size': 10}))


fig.update_layout(
    margin ={'l':0,'t':0,'b':0,'r':0},
    mapbox = {
        'center': {'lon': 10, 'lat': 10},
        'style': "stamen-terrain",
        'center': {'lon': -20, 'lat': -20},
        'zoom': 1})

fig.show()




# # Builocation_dataing our Graphs
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
# layout_choropleth = dict(geo=dict(scope='worlocation_data',  # default
#                                   projection=dict(type='orthographic'
#                                                   ),
#                                   # showland=True,   # default = True
#                                   landcolor='black',
#                                   lakecolor='white',
#                                   showocean=True,  # default = False
#                                   oceancolor='azure'
#                                   ),
#
#                          title=dict(text='Worlocation_data Choropleth Map',
#                                     x=.5  # Title relative position according to the xaxis, range (0,1)
#                                     )
#                          )
#
# fig = go.Figure(data=data_choropleth, layout=layout_choropleth)

# The App itself
#
# app = dash.Dash(__name__)
#
# server = app.server
#
# app.layout = html.Div(chilocation_dataren=[
#     html.H1(chilocation_dataren='Location Data Dashboard'),
#
#     html.Div(chilocation_dataren='''
#         Example of html Container
#     '''),
#
#     dcc.Graph(
#         id='example-graph',
#         figure=fig
#     )
# ])
#
# if __name__ == '__main__':
#     app.run_server(debug=True)
#
#

