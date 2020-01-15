# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 11:53:28 2020

@author: benoi
"""


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



from datetime import datetime

import warnings
import warnings,os
warnings.filterwarnings('ignore')
import simplejson as json

location_data=pd.read_pickle(os.getcwd()+"\\merged_location_data.pkl")


def select_person (name_person):
    
    if name_person == 'Ben':
        
        location = location_data.loc[location_data['person'] == 'Ben']
        
    elif name_person == 'Leo':
        
        location = location_data.loc[location_data['person'] == 'Leo']
    
    elif name_person == 'Carolina':
        
        location = location_data.loc[location_data['person'] == 'Carolina']
   
    elif name_person == 'Pedro':
        
        location = location_data.loc[location_data['person'] == 'Pedro']

    return location
    

def select_year (person, year,month):
    
    day = str(1)
    year = str(year)
    month = str(month)
    
    #increase to make a range 
    if month == 2:
        day2 = str(28)
    else:
        day2 = str(30)
    
    month2 = month
    #if month == 12:
     #   month2 = 1
    #else:
        
     #   month2 = int(month) + 1 
      #  month2 = str(month2)
    
    
    my_string = day + ',' +month + ',' + year
    my_string2 = day2 + ',' +month2 + ',' + year
    
    my_date = datetime.strptime(my_string, "%d,%m,%Y")
    my_date2 = datetime.strptime(my_string2, "%d,%m,%Y")
      
    
    if person == 'Ben':
        
        location_person = select_person(name_person = person)
        
        location_person_year = location_person.loc[location_person['datetime'].between(my_date,my_date2, inclusive=True)]
        
        location_person_year_sample = location_person_year.loc[:, ['latitude', 'longitude','datetime']]
    
    elif person == 'Leo':
        
        location_person = select_person(name_person = person)
        
        location_person_year = location_person.loc[location_person['datetime'].between(my_date,my_date2, inclusive=True)]
        
        location_person_year_sample = location_person_year.loc[:, ['latitude', 'longitude','datetime']]
                    
    elif person == 'Carolina':
        
        location_person = select_person(name_person = person)
        
        location_person_year = location_person.loc[location_person['datetime'].between(my_date,my_date2, inclusive=True)]
        
        location_person_year_sample = location_person_year.loc[:, ['latitude', 'longitude','datetime']]
    
    elif person == 'Pedro':
        
        location_person = select_person(name_person = person)
        
        location_person_year = location_person.loc[location_person['datetime'].between(my_date,my_date2, inclusive=True)]
        
        location_person_year_sample = location_person_year.loc[:, ['latitude', 'longitude','datetime']]
        
                   
    
    return location_person, location_person_year_sample 
    
    
my_dataframe, sample_my_dataframe = select_year('Leo',2018,9)    
    
print("earliest observed date: {}".format(min(sample_my_dataframe["datetime"]).strftime('%m-%d-%Y')))
print("latest observed date: {}".format(max(sample_my_dataframe["datetime"]).strftime('%m-%d-%Y')))

print("earliest observed date: {}".format(min(my_dataframe["datetime"]).strftime('%m-%d-%Y')))
print("latest observed date: {}".format(max(my_dataframe["datetime"]).strftime('%m-%d-%Y')))


