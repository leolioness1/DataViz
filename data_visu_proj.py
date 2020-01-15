


import json
import time
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
#from ipython.display import Image
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import plotly.express as px
import plotly




#import plotly.io as pio





import warnings
import warnings,os
warnings.filterwarnings('ignore')
import simplejson as json

location_data=pd.read_pickle(os.getcwd()+"\\merged_location_data.pkl")

location_data['datetime'] =pd.to_datetime(location_data['datetime'])
location_data['year'] = location_data['datetime'].dt.year
location_data['month'] =location_data['datetime'].dt.month

name_options = [dict(label=name, value=name) for name in location_data['person'].unique()]
year_options = [dict(label=year, value=year) for year in location_data['year'].unique()]
initial_year = list(range(min(location_data['year']),max(location_data['year'])))
month_options = [dict(label = month, value = month) for month in location_data['month'].unique()]
initial_month = list(location_data['month'].unique())

location_data.head()


"""

location_data['latitude'] = list(map(round,location_data['latitude']))
location_data['longitude'] = list(map(round,location_data['longitude']))
point_list = []
for i in range(0,len(location_data)):
    point_list.append([location_data.loc[i,'latitude'],location_data.loc[i,'longitude'],location_data.loc[i,'person']])
point_list_unique, counts = np.unique(point_list,axis=0,return_counts=True)
latitudes = pd.DataFrame()
longitudes = pd.DataFrame()
persons = pd.DataFrame()
for i,value in enumerate(point_list_unique):
    latitudes.append(point_list_unique.loc[i,'latitude'])
    longitudes.append(point_list_unique.loc[i,'longitude'])
    persons.append(point_list_unique.loc[i,'person'])

"""

app = dash.Dash(__name__)

app.layout = html.Div([

    html.Div([
        html.H1('Google Location History')
    ], className='Title'),

    html.Div([

        html.Div([
            html.Label('Person'),
            dcc.Dropdown(
                id='person_drop',
                options=name_options,
                value=['Ben','Carolina','Leo','Pedro'],
                multi=True
            ),

            html.Br(),

            html.Label('Year Choice'),
            dcc.Dropdown(
                id='year_drop',
                options=year_options,
                value=initial_year,
                multi=True
            ),

            html.Br(),

            html.Label('Month Choice'),
            dcc.Dropdown(
                id='month_drop',
                options=month_options,
                value=initial_month,
                multi=True
            ),

            html.Br(),



            html.Label('Projection'),
            dcc.RadioItems(
                id='projection',
                options=[dict(label='Equirectangular', value=0), dict(label='Orthographic', value=1)],
                value=0
            )
        ], className='column1 pretty'),

        html.Div([dcc.Graph(id='scattermapbox')], className='column2 pretty'),

    ], className='row'),

    html.Div([

        html.Div([dcc.Graph(id='bar_graph')], className='column1 pretty'),

        html.Div([dcc.Graph(id='heatmap')], className='column3 pretty')

    ], className='row'),

])

@app.callback(
    [
        Output("scattermapbox", "figure"),
        Output("heatmap","figure"),
        Output("bar_graph","figure")
    ],
    [
        Input("person_drop","value"),
        Input("year_drop","value"),
        Input("month_drop","value"),
    ]
)
def plots(person, year, month):


    location_data_useful = location_data.loc[location_data['person'].isin(person)]
    location_data_useful = location_data_useful.loc[location_data_useful['year'].isin(year)]
    location_data_useful = location_data_useful.loc[location_data_useful['month'].isin(month)]
    point_list = []
    for i in range(0, len(location_data_useful)):
        point_list.append(
            [location_data.loc[i, 'latitude'], location_data.loc[i, 'longitude'], location_data.loc[i, 'person']])
    point_list_unique, counts = np.unique(point_list, axis=0, return_counts=True)
    latitudes = []
    longitudes = []
    persons = []
    for i, value in enumerate(point_list_unique):
        latitudes.append(point_list_unique.loc[i, 'latitude'])
        longitudes.append(point_list_unique.loc[i, 'longitude'])
        persons.append(point_list_unique.loc[i, 'person'])


        colors = []
    for i,names in enumerate(persons):
        if names == 'Ben':
            colors.append('red')
        if names == 'Carolina':
            colors.append('yellow')
        if names == 'Leo':
            colors == 'blue'
        if names == 'Pedro':
            colors.append('green')


    data_scattermap=dict(type='scattermapbox',
                         mode="markers",
                         lon = longitudes,
                         lat = latitudes,
                         marker = dict({'size' : 10},color=colors),alpha=0.3)



    layout_scatter = dict(margin ={'l':0,'t':0,'b':0,'r':0},
                        mapbox = {
                        'center': {'lon': 10, 'lat': 10},
                        'style': "stamen-terrain",
                        'center': {'lon': -20, 'lat': -20},
                        'zoom': 1})
    from math import log

    data_circle = dict(type='scattermapbox',
                         mode="markers",
                         lon = longitudes,
                         lat = latitudes,
                         marker = dict({'size' : list(map(lambda x: 2.5*x,list(map(log,counts))))},
                                       color=colors,
                                       alpha=0.1))

    data_bar=dict(type='bar', x=x_bar, y=counts)

    layout_bar = dict(title=dict(text='Most Popular Countries'),
                      yaxis=dict(title='# of People'),
                      paper_bgcolor='#f9f9f9')

    return [go.Figure(data=data_scattermap,layout=layout_scatter),
    go.Figure(data = data_circle, layout = layout_scatter),
    go.Figure(data=data_bar, layout=layout_bar)]


if __name__ == '__main__':
    app.run_server(debug=True)

# ## HEATMAP

# In[10]:



    #country_info = json.load(open('portugal_municipios.geojson', encoding='utf-8'))






