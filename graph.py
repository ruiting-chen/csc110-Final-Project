import plotly.graph_objects as go
import numpy as np
import random
from generates import GenerateStationAndSeaLevel


import datetime
from generates import GenerateTemperature, GenerateStationAndSeaLevel
from climate_sea_level_system import ClimateSeaLevelSystem
from linear_regression import go_plot

system = ClimateSeaLevelSystem()
generate_temp = GenerateTemperature()
generate_station = GenerateStationAndSeaLevel()
base_height = 900


def generate_tempera():
    generate_temp.generate(system)


def generate_sea():
    generate_station.generate_all(system)

generate_sea()
x = []
y = []
color = []
for station in system.get_station():
    month = list(system.get_station()[station].sea_level.keys())[0]
    lon = system.get_station()[station].location[0]
    la = system.get_station()[station].location[1]
    if system.get_station()[station].sea_level[month] < base_height:
        colour = 'blue'
    else:
        colour = 'red'
    x.append(la)
    y.append(lon)
    color.append(colour)











fig = go.Figure(go.Scattergeo(lat=x, lon=y, mode='markers', marker={'color': color},
                              hovertemplate='call the see_detail function and pass in "Wellington" to see detail',
                              showlegend=False))
fig.update_layout(height=1000, margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
fig.update_geos(showland=True, landcolor='Green',
                showocean=True, oceancolor='LightBlue',
                showrivers=True, rivercolor='DarkBlue',
                showlakes=True, lakecolor='DarkBlue',
               showcountries=True, countrycolor='White')
fig.update_geos(lataxis_showgrid=True, lonaxis_showgrid=True)
# fig.update_layout(height=1000)
fig.show()


def see_detail(station: str):
    go_plot(station)
