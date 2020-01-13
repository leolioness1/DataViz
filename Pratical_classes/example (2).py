import plotly.offline as pyo
import pandas as pd
import plotly.graph_objs as go

df = pd.read_csv('Data/mpg.csv')

trace=go.Scatter3d(x=df['displacement'], y=df['mpg'],z=df['model_year'],
                   mode='markers', name='Car Specs', text=df['name'],
                   marker=dict(color=df['acceleration'],size=df['weight']/200,colorscale='Jet', showscale=True,
                             colorbar=dict(title=dict(text='Acceleration m/s*2'))))
data=[trace]
layout = go.Layout(title='Cars Plot', scene=dict(
                   xaxis=dict(title='Displacement'),
                   yaxis=dict(title='1.6km per 3.8L'),
                   zaxis=dict(title='Model Year')),
                   template='plotly_dark'
                   )
fig = go.Figure(data=data, layout=layout)
pyo.plot(fig)







