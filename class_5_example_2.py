import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import socket

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Input(id='input', value='initial value', type='text'),
    html.Div(id='div')
])


@app.callback(
    Output(component_id='div', component_property='children'),
    [Input(component_id='input', component_property='value')]
)
def update_output_div(input_value):
    return 'You\'ve entered "{}"'.format(input_value)

host = socket.gethostbyname(socket.gethostname())

if __name__ == '__main__':
    app.run_server(debug=True, host=host)