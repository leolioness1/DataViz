


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




import plotly.io as pio





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

longitudes = location_data['longitude'].tolist()
latitudes = location_data['latitude'].tolist()





len(longitudes)



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

#        html.Div([

#            html.Div([
#
#                html.Div([html.Label(id='gas_1')], className='mini pretty'),
#                html.Div([html.Label(id='gas_2')], className='mini pretty'),
#                html.Div([html.Label(id='gas_3')], className='mini pretty'),
#                html.Div([html.Label(id='gas_4')], className='mini pretty'),
#                html.Div([html.Label(id='gas_5')], className='mini pretty'),
#
#            ], className='5 containers row'),
#
#            html.Div([dcc.Graph(id='bar_graph')], className='bar_plot pretty')
#
 #       ], className='column2'),

    ], className='row'),

    html.Div([

        html.Div([dcc.Graph(id='choropleth')], className='column2 pretty'),

        html.Div([dcc.Graph(id='aggregate_graph')], className='column3 pretty')

    ], className='row'),

])

@app.callback(
    [
        Output("choropleth", "figure"),
        Output("aggregate_graph","figure")
    ],
    [
        Input("person_drop","value"),
        Input("year_drop","value"),
        Input("month_drop","value"),
    ]
)
def plots(person, year, month):
    import plotly.graph_objects as go
    longitudes
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


if __name__ == '__main__':
    app.run_server(debug=True)

# ## HEATMAP

# In[10]:



    #country_info = json.load(open('portugal_municipios.geojson', encoding='utf-8'))






