
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

# Dataset Processing

df_emissions = pd.read_csv('emission_full.csv')

df_emission_0 = df_emissions.loc[df_emissions['year'] == 2000]

# Building our Graphs

data_choropleth = dict(type='choropleth',
                       locations=df_emission_0['country_name'],
                       # There are three ways to 'merge' your data with the data pre embedded in the map
                       locationmode='country names',
                       z=np.log(df_emission_0['CO2_emissions']),
                       text=df_emission_0['country_name'],
                       colorscale='inferno',
                       colorbar=dict(title='CO2 Emissions log scaled')
                       )

layout_choropleth = dict(geo=dict(scope='world',  # default
                                  projection=dict(type='orthographic'
                                                  ),
                                  # showland=True,   # default = True
                                  landcolor='black',
                                  lakecolor='white',
                                  showocean=True,  # default = False
                                  oceancolor='azure'
                                  ),

                         title=dict(text='World Choropleth Map',
                                    x=.5  # Title relative position according to the xaxis, range (0,1)
                                    )
                         )

fig_choropleth = go.Figure(data=data_choropleth, layout=layout_choropleth)

#######################################Another Figure#########################################################
data_scatter = [go.Scatter(dict(
    y=df_emission_0.loc[df_emission_0['continent'] == i]['CO2_emissions'],
    x=df_emission_0.loc[df_emission_0['continent'] == i]['CH4_emissions'],
    text=df_emission_0.loc[df_emissions['continent'] == i]['country_name'],
    mode='markers',
    opacity=.75,
    marker=dict(size=15, line=dict(width=.5, color='white')),
    name=i
)) for i in df_emission_0['continent'].unique()]

layout_scatter = dict(title=dict(text='Continent Emissions', x=.5),
              yaxis=dict(type='log', title='CO2 Emissions'),
              xaxis=dict(type='log', title='CH4 Emissions'),
              margin=dict(l=40, b=40, t=50, r=40),
              legend=dict(x=1, y=0)
              )

fig_scatter = go.Figure(data=data_scatter, layout=layout_scatter)

# The App itself

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([
    html.H1(children='My First DashBoard'),

    html.Div('''
        Example of html Container
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig_scatter
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
