
# coding: utf-8

# Get a list of all stations:

# In[1]:

import json
import requests

url_stations = 'http://barcelonaapi.marcpous.com/bicing/stations.json'
res_stations = requests.get(url_stations)
stations = json.loads(res_stations.text)


# Arrange the data to be in lists:

# In[2]:

station_id = []
station_name = []
station_lat = []
station_lon = []

for idx,i in enumerate(stations['data']['bici']):
    station_id.append(int(stations['data']['bici'][idx]['id']))
    station_name.append(stations['data']['bici'][idx]['name'])
    station_lat.append(float(stations['data']['bici'][idx]['lat']))
    station_lon.append(float(stations['data']['bici'][idx]['lon']))


# Find out how many bikes are available at each of the selected stations:

# In[3]:

import datetime

bikes = []
slots = []
dates = []
bikes_ok = []
slots_ok = []

for i in station_id:
    url_availability = 'http://wservice.viabicing.cat/v2/stations/'+str(i)
    res_availability = requests.get(url_availability)
    json_availability = json.loads(res_availability.text)
    
    try:
        bikes_num = json_availability['stations'][0]['bikes']
        slots_num = json_availability['stations'][0]['slots']
        dates.append(datetime.datetime.fromtimestamp(json_availability['updateTime']).strftime('%Y-%m-%d %H:%M:%S'))
    except:
        bikes_num = 0
        slots_num = 0
        
        try: 
            dates.append(dates[len(dates)-1])
        except:
            dates.append(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            
    bikes.append(bikes_num)
    slots.append(slots_num)
    
    if int(bikes_num) >= 2:
        bikes_ok.append(True)
    else:
        bikes_ok.append(False)
        
    if int(slots_num) >= 2:
        slots_ok.append(True)
    else:
        slots_ok.append(False)


# Create a dataframe so that we can easily filter out the non-available stations:

# In[4]:

import pandas as pd
dataset = pd.DataFrame({'station_id':station_id,
                        'station_name':station_name,
                        'station_lat':station_lat,
                        'station_lon':station_lon,
                        'bikes':bikes,
                        'slots':slots,
                        'bikes_ok':bikes_ok,
                        'slots_ok':slots_ok,
                        'entry_date':dates
                       })
dataset


# Import the *new* dataset into a SQL table:

# In[5]:

import sqlite3
conn = sqlite3.connect("bicidb.db")
cursos = conn.cursor()


# In[7]:

dataset.to_sql('historical_availability', con=conn, if_exists='append')


# Load back the *full* dataset into a data frame:

# In[8]:

pd.read_sql("SELECT * FROM historical_availability;", con=conn)


# In[10]:




# In[ ]:



