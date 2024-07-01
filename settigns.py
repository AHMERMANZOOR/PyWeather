from datetime import datetime
current_t = int(str(datetime.now()).split(' ')[1].split(':')[0])
clear_sky = None
cloudy = None
if (current_t > 6 and current_t < 18):
    clear_sky = "assets/sun.png"
    cloudy = "assets/sun_cloud.png"
else:
    clear_sky = "assets/moon.png"
    cloudy = "assets/cloud_moon.png"

WEATHER_CODES = {0:{'text':'Clear Sky', 'image':clear_sky},
                 1:{'text':'Mainly Clear', 'image':cloudy},
                 2:{'text':'Partly Cloudy', 'image':cloudy},
                 3:{'text':'OverCast', 'image':"assets/clouds.png"},
                 45:{'text':'Fog', 'image':"assets/fog.png"},
                 48:{'text':'Depositing rime Fog', 'image':"assets/clouds.png"},
                 51:{'text':'Drizzle(light)', 'image':"assets/drizzle.png"},
                 53:{'text':'Drizzle(moderate)', 'image':"assets/drizzle.png"},
                 55:{'text':'Drizzle(dense)', 'image':"assets/drizzle.png"},
                 56:{'text':'Freezing Drizzle(light)', 'image':"assets/freezing_drizzle.png"},
                 57:{'text':'Freezing Drizzle(dense)', 'image':"assets/freezing_drizzle.png"},
                 61:{'text':'Rain(light)', 'image':"assets/rain_cloud.png"},
                 63:{'text':'Rain(moderate)', 'image':"assets/rain_cloud.png"},
                 65:{'text':'Rain(dense)', 'image':"assets/heavy_rain.png"},
                 66:{'text':'Freezing Rain(light)', 'image':"assets/rain_thunder.png"},
                 67:{'text':'Freezing Rain(dense)', 'image':"assets/snow_rain.png"},
                 71:{'text':'Snowfall(slight)', 'image':"assets/snow.png"},
                 73:{'text':'Snowfall(moderate)', 'image':"assets/snow_flake_cloud.png"},
                 75:{'text':'Snowfall(heavy)', 'image':"assets/snow_cloud.png"},
                 77:{'text':'Snow Grains', 'image':"assets/snow.png"},
                 80:{'text':'Rain Showers(slight)', 'image':"assets/rain_cloud.png"},
                 81:{'text':'Rain Showers(moderate)', 'image':"assets/rain_cloud.png"},
                 82:{'text':'Rain Showers(intense)', 'image':"assets/heavy_rain.png"},
                 85:{'text':'Snow Showers(slight)', 'image':"assets/snow_flake_cloud.png"},
                 86:{'text':'Snow Showers(heavy)', 'image':"assets/snow_cloud.png"},
                 95:{'text':'Thunderstorm', 'image':"assets/cloud_thunder.png"},
                 96:{'text':'Thunderstorm and hail', 'image':"assets/thunder_and_hail.png"},
                 99:{'text':'Thunderstorm(intense)', 'image':"assets/cloud_thunder.png"}}

MAIN_BG_COLOR = "#0EA8FF"
MARKER_COLOR = "#f7f700"
FILL_BETWEEN_COLOR = "#0f76a6"
GRAPH_BACKGROUND = "#24eaed"