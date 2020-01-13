import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import plotly.graph_objs as go


app = dash.Dash(__name__)

df = pd.read_csv('emission_full.csv')
available_indicators = df.columns

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='CO2_emissions'
            ),
            dcc.RadioItems(
                id='xaxis-type',
                options=[{'label': i, 'value': i} for i in ['linear', 'log']],
                value='linear'
            )
        ],
        style=dict(width='50%', display='inline-block')
        ),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='CH4_emissions'
            ),
            dcc.RadioItems(
                id='yaxis-type',
                options=[{'label': i, 'value': i} for i in ['linear', 'log']],
                value='linear'
            )
        ],style=dict(width='50%', display='inline-block'))
    ]),

    dcc.Graph(id='indicator-graphic'),

    html.Br(),

    dcc.Slider(
        id='year--slider',
        min=df['year'].min(),
        max=df['year'].max(),
        value=df['year'].max(),
        marks={str(year): str(year) for year in df['year'].unique()},
        step=None
    )
])



@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('xaxis-column', 'value'),
     Input('yaxis-column', 'value'),
     Input('xaxis-type', 'value'),
     Input('yaxis-type', 'value'),
     Input('year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    filtered_df = df[df['year'] == year_value]

    data = [go.Scatter(dict(
        y=filtered_df.loc[filtered_df['continent'] == i][yaxis_column_name],
        x=filtered_df.loc[filtered_df['continent'] == i][xaxis_column_name],
        text=filtered_df.loc[df['continent'] == i]['country_name'],
        mode='markers',
        marker=dict(size=15, opacity=0.5, line=dict(width=0.5, color='white')),
        name=i
    )) for i in filtered_df['continent'].unique()]

    layout = dict(title=dict(text='Continent Emissions', x=.5),
                  xaxis=dict(title=xaxis_column_name,
                             type=xaxis_type),
                  yaxis=dict(title=yaxis_column_name,
                             type=yaxis_type),
                  margin=dict(l=40, b=40, t=50, r=40),
                  legend=dict(x=1, y=0)
                  )

    fig = go.Figure(data=data, layout=layout)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)