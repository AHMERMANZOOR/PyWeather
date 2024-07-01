import openmeteo_requests
import geocoder
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image
from settigns import MARKER_COLOR, FILL_BETWEEN_COLOR
from datetime import date as dt
from datetime import datetime

# Getting the current coordinates using geocoder
def get_coordinates():
    g = geocoder.ip('me')
    if g.latlng is not None:
        return (g.latlng[0], g.latlng[1])
    else:
        raise ConnectionError

# Retrieving data from openmeteo API
def data(latitude, longitude, date):
    om = openmeteo_requests.Client()
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": ["temperature_2m", "relative_humidity_2m", "precipitation_probability", "wind_speed_10m", "weather_code"],
        "current": ["temperature_2m", "weather_code", "precipitation", "relative_humidity_2m", "wind_speed_10m"],
        "start_date": f"{date}",
	    "end_date": f"{date}"
    }

    responses = om.weather_api("https://api.open-meteo.com/v1/forecast", params=params)[0]
    
    # Getting the hourly data
    hourly = responses.Hourly()
    
    # Formatting the hourly data
    hourly_data = {}
    hourly_data['hour'] = np.arange(start=0, stop=24, step=1)
    hourly_data["temperature_2m"] = hourly.Variables(0).ValuesAsNumpy()
    hourly_data["relative_humidity_2m"] = hourly.Variables(1).ValuesAsNumpy()
    hourly_data["precipitation_probability"] = hourly.Variables(2).ValuesAsNumpy()
    hourly_data["wind_speed_10m"] = hourly.Variables(3).ValuesAsNumpy()
    hourly_data["weather_code"] = hourly.Variables(4).ValuesAsNumpy()
    
    # Creating a pandas dataframe of the data
    hourly_dataframe = pd.DataFrame(data = hourly_data)
    #print(hourly_dataframe)
    
    # Getting the data for the Graphs
    l = (np.arange(
        start=0, 
        stop=24, 
        step=2))
    x = []
    y_temp = []
    y_precipitation = []
    for i in l:
        y_temp.append(hourly_dataframe['temperature_2m'].loc[hourly_dataframe.index[i]])
        y_precipitation.append(hourly_dataframe['precipitation_probability'].loc[hourly_dataframe.index[i]])
        x.append(hourly_dataframe['hour'].loc[hourly_dataframe.index[i]])
        
    # Creating the Graph and saving it as png
    
        # Creating the temperature graph
    figure_temp = plt.figure(figsize=(10,3), dpi=100)
    sub_plot = figure_temp.add_subplot(111)
    sub_plot.plot(x, y_temp, marker='.', markersize=10, color=MARKER_COLOR)
    sub_plot.set_xticks(x)
    sub_plot.set_xlim(-1, 24)
    sub_plot.set_ylim(int(hourly_dataframe['temperature_2m'].min()-10), 
                      int(hourly_dataframe['temperature_2m'].max()+10))
    sub_plot.axis('off')
    sub_plot.fill_between(x, y_temp, color=FILL_BETWEEN_COLOR)
    for i in range(0, len(x)):
        sub_plot.text(x[i]-0.3, y_temp[i]+1, s=str(int(y_temp[i])))
        sub_plot.text(
            x[i]-0.3 if i!= len(x)-1 else x[i]-1, 
            y_temp[i]-2, 
            s=str(x[i]-12)+'pm' if x[i] >11 else str(x[i])+'am')
    figure_temp.savefig(fname='assets/out_temp.png', transparent=True)
    
        # Croping the Image
    
    #img = Image.open("assets/out_temp.png")
    #img_crop = img.crop(box=(147,0,846,266))
    #img_crop.save("assets/out_temp.png")
    
        # Creating the precipitation graph
        
    figure_prep = plt.figure(figsize=(10,3), dpi=100)
    sub_plot_prep = figure_prep.add_subplot(111)
    m = y_precipitation
    y_precipitation = []
    for i in range(0, len(m)):
        y_precipitation.append(m[i]/100+0.2)
    sub_plot_prep.bar(x,y_precipitation, width = 1.5, align='center', color='#42b2eb')
    sub_plot_prep.set_xticks(x)
    sub_plot_prep.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2])
    sub_plot_prep.set_yticklabels(['',0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    figure_prep.savefig('assets/out_prep', transparent=True)
    
            # Croping the Image
    
    img = Image.open("assets/out_prep.png")
    img_crop = img.crop(box=(94,0,901,288))
    img_crop.save("assets/out_prep.png")
    
    # Closing all the figures.
    plt.close('all')
    
    if date == dt.today():
    
        temperature = round(responses.Current().Variables(0).Value(), 1)
        weather_code = int(responses.Current().Variables(1).Value())
        precipitation = round(responses.Current().Variables(2).Value(), 1)
        humidity = responses.Current().Variables(3).Value()
        wind_speed = round(responses.Current().Variables(4).Value(), 1)
        
    else:
        
        row = hourly_dataframe.values[int(str(datetime.now()).split(' ')[1].split(':')[0])]
        
        temperature = round(row[1], 1)
        weather_code = int(row[5])
        precipitation = round(row[3], 1)
        humidity = round(row[2], 1)
        wind_speed = round(row[4], 1)
        
    # Returning the data
    return(temperature, 
        weather_code, 
        precipitation,
        humidity,
        wind_speed,
        "assets/out_temp.png",
        "assets/out_prep.png")
