import plotly.offline as pyo
import plotly.graph_objs as go
import numpy as np

t=np.linspace(0,2*np.pi,100)
x = np.cos(t)
y = np.sin(t)

x2 = 2*np.cos(t)
y2 = 2*np.sin(t)

trace1 = go.Scatter(
    x = x,
    y = y,
    mode = 'markers',
    text = 'Sardines and Sharks',
    name='Ecosystem 1',
    marker = dict(size = 12,color = 'rgb(51,204,153)',symbol = 'pentagon',line = dict(width = 2,)))

trace2 = go.Scatter(
    x = x2,
    y = y2,
    mode = 'markers',
    text='Rabbits and Foxes',
    name='Ecosystem 2',
    marker = dict(size = 12,color = 'rgb(204,51,153)',symbol = 'pentagon',line = dict(width = 2,)))


data = [trace1, trace2]

layout = go.Layout(
    title = 'Predator and Prey', # Graph title
    xaxis = dict(title = 'Number of Predators'), # x-axis label
    yaxis = dict(title = 'Number of Preys') # y-axis label
)
fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename='lesson_1_example.html')


