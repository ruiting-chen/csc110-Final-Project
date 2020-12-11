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
station_name = []
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
    station_name.append(f'Name of station: {station}')










fig = go.Figure(go.Scattergeo(lat=x, lon=y, mode='markers', marker={'color': color},
                              hovertext=station_name))
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

name = input('Please type in the station name that you want to see detailed report of. Hover over it to see name.')
see_detail(name)






# import plotly.graph_objects as go

# import pandas as pd

# url = "https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv"
# dataset = pd.read_csv(url)

dates = ['2000', '2001', '2002', '2003', '2004']

# # make list of continents
# continents = []
# for continent in dataset["continent"]:
#     if continent not in continents:
#         continents.append(continent)
# make figure
fig_dict = {
    "data": [],
    "layout": {},
    "frames": []
}

x = np.random.randint(-90, 90, 100)
y = np.random.randint(-180, 180, 100)

# print(x)
# print(y)

color = [['red'], ['green'], ['yellow'], ['blue'], ['black']]

# fig.update_layout(height=1000, margin={'r':0, 't':0, 'l':0, 'b':0})


# fill in most of layout
# fig_dict["layout"]["xaxis"] = {"range": [30, 85], "title": "Life Expectancy"}
# fig_dict["layout"]["yaxis"] = {"title": "GDP per Capita", "type": "log"}
# fig_dict["layout"]["hovermode"] = "closest"
# fig_dict["layout"]["updatemenus"] = [
#     {
#         "buttons": [
#             {
#                 "args": [None, {"frame": {"duration": 500, "redraw": False},
#                                 "fromcurrent": True, "transition": {"duration": 300,
#                                                                     "easing": "quadratic-in-out"}}],
#                 "label": "Play",
#                 "method": "animate"
#             },
#             {
#                 "args": [[None], {"frame": {"duration": 0, "redraw": False},
#                                   "mode": "immediate",
#                                   "transition": {"duration": 0}}],
#                 "label": "Pause",
#                 "method": "animate"
#             }
#         ],
#         "direction": "left",
#         "pad": {"r": 10, "t": 87},
#         "showactive": False,
#         "type": "buttons",
#         "x": 0.1,
#         "xanchor": "right",
#         "y": 0,
#         "yanchor": "top"
#     }
# ]

sliders_dict = {
    "active": 0,
    "yanchor": "top",
    "xanchor": "left",
    "currentvalue": {
        "font": {"size": 20},
        "prefix": "Year:",
        "visible": True,
        "xanchor": "right"
    },
    "transition": {"duration": 300, "easing": "cubic-in-out"},
    "pad": {"b": 10, "t": 50},
    "len": 0.9,
    "x": 0.1,
    "y": 0,
    "steps": []
}

# make data
# date = 2000
# for continent in continents:
#     dataset_by_year = dataset[dataset["year"] == year]
#     dataset_by_year_and_cont = dataset_by_year[dataset_by_year["continent"] == continent]

#     data_dict = {
#         "x": list(dataset_by_year_and_cont["lifeExp"]),
#         "y": list(dataset_by_year_and_cont["gdpPercap"]),
#         "mode": "markers",
#         "text": list(dataset_by_year_and_cont["country"]),
#         "marker": {
#             "sizemode": "area",
#             "sizeref": 200000,
#             "size": list(dataset_by_year_and_cont["pop"])
#         },
#         "name": continent
#     }
fig = go.Scattergeo(lat=x, lon=y, marker={'color': color[0]})
fig_dict["data"].append(fig)

# make frames
frame = {"data": []}
for i in range(len(dates)):
    #     for i in range(len(x)):
    #         dataset_by_year = dataset[dataset["year"] == int(year)]
    #         dataset_by_year_and_cont = dataset_by_year[dataset_by_year["continent"] == continent]

    #         data_dict = {
    #             "x": list(dataset_by_year_and_cont["lifeExp"]),
    #             "y": list(dataset_by_year_and_cont["gdpPercap"]),
    #             "mode": "markers",
    #             "text": list(dataset_by_year_and_cont["country"]),
    #             "marker": {
    #                 "sizemode": "area",
    #                 "sizeref": 200000,
    #                 "size": list(dataset_by_year_and_cont["pop"])
    #             },
    #             "name": continent
    #         }

    fig = go.Scattergeo(lat=x, lon=y, marker={'color': color[i]})
    frame["data"].append(fig)

    fig_dict["frames"].append(frame)
    slider_step = {"args": [[dates[i]],
                            {"frame": {"duration": 300, "redraw": True},
                             "mode": "immediate",
                             "transition": {"duration": 300}}],
                   "label": date,
                   "method": "animate"}
    sliders_dict["steps"].append(slider_step)

fig_dict["layout"]["sliders"] = [sliders_dict]

fig = go.Figure(fig_dict)

fig.show()

