
# coding: utf-8

# In[2]:


'''
This is a project dedicated to analyzing a dataset of parking 
citations by the Parklink administartion in Raleigh, NC. The 
information was provided under the Freedom of Information Act 
as an Excel Spreadsheet. 

As a student and a resident of Boylan Heights, I find myself
always at odds with the parking enforcement. this is my attempt 
to outsmart them by vizualizitng their walking routes and 
attempting a time series analysis on the data to predict their 
paths of destruction.
'''


get_ipython().run_line_magic('matplotlib', 'inline')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#IMPORT DATA FROM PUBLIC RECORD REQUEST
df = pd.read_csv('/home/adam/tickets.csv')

#CONVERT TO DATATYPES
df['ISSUEDATE'] = pd.to_datetime(df['ISSUEDATE']).dt.date
df['ISSUETIME'] = pd.to_datetime(df['ISSUETIME']).dt.time
df['ISSUED'] = df.apply(lambda r : pd.datetime.combine(r['ISSUEDATE'],r['ISSUETIME']),1)
df = df.set_index(pd.DatetimeIndex(df['ISSUED']))
del df['ISSUETIME']
del df['ISSUEDATE']
del df['ISSUED']


# In[9]:


import geopandas as gpd
from geopy.geocoders import GoogleV3

API_KEY = 

geolocator = GoogleV3(api_key = API_KEY)   

def getLocation(row):
    address = row['LOCATIONDESC1'] + ", Raleigh, NC, USA"
    try:
        location = geolocator.geocode(address)
        print("SUCCESS   " + str(location))
        return (location.latitude, location.longitude)
    except:
        print("FAILURE    " + address)
        return (0.0, 0.0)
    
df['LOCATIONDESC2'] = df.apply(lambda row: getLocation(row), axis=1)


# In[10]:


df.to_csv('TicketsLatLong.csv')

