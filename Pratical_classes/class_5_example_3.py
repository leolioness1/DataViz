import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import plotly.graph_objs as go

# Dataset Processing

df_emissions = pd.read_csv('emission_full.csv')

df_emission_0 = df_emissions.loc[df_emissions['year'] == 2000]

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

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='year-slider',
        min=df_emissions['year'].min(),
        max=df_emissions['year'].max(),
        value=df_emissions['year'].min(),
        marks={str(Year): str(Year) for Year in df_emissions['year'].unique()},
        step=None
    )
])


@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value')])
def update_figure(selected_year):
    filtered_df = df_emissions.loc[df_emissions['year'] == selected_year]

    data_scatter_f = [go.Scatter(dict(
        y=filtered_df.loc[filtered_df['continent'] == i]['CO2_emissions'],
        x=filtered_df.loc[filtered_df['continent'] == i]['CH4_emissions'],
        text=filtered_df.loc[filtered_df['continent'] == i]['country_name'],
        mode='markers',
        opacity=.75,
        marker=dict(size=15, line=dict(width=.5, color='white')),
        name=i
    )) for i in filtered_df['continent'].unique()]

    return go.Figure(data=data_scatter_f, layout=layout_scatter)


if __name__ == '__main__':
    app.run_server(debug=True)