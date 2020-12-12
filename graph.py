import plotly.graph_objects as go
import datetime
from generates import GenerateTemperature, GenerateStationAndSeaLevel
from climate_sea_level_system import ClimateSeaLevelSystem
from linear_regression import go_plot
from entities import Station

system = ClimateSeaLevelSystem()
generate_temp = GenerateTemperature()
generate_station = GenerateStationAndSeaLevel()
base_height = 900

import plotly.io as pio
pio.renderers.default = "browser"

def generate_tempera():
    generate_temp.generate(system)


def generate_sea():
    generate_station.generate_all(system)


def get_color(height: float) -> str:
    stations = system.get_station()
    global_min_height = min(stations[x].min_height for x in stations)
    global_max_height = max(stations[x].max_height for x in stations)
    interval = (global_max_height - global_min_height) / 4
    colors = ['blue', 'green', 'yellow', 'red']
    for i in range(1, 5):
        if height <= global_min_height + interval * i:
            return colors[i - 1]


def graph_data_set_up() -> tuple:
    dates = []
    generate_sea()
    x = []
    y = []
    color = []
    station_name = []
    min_mon = []
    max_mon = []
    for station in system.get_station():
        if len(system.get_station()[station].sea_level.keys()) < 240:
            continue
        min_mon.append(min(system.get_station()[station].sea_level.keys()))
        max_mon.append(max(system.get_station()[station].sea_level.keys()))

    max_month = min(max_mon)
    min_month = max(min_mon)
    num_station = len(system.get_station())

    for month in range((max_month - min_month).days // 30):
        dates.append(month)
        inner_lst = []
        for station in system.get_station():
            if len(system.get_station()[station].sea_level.keys()) < 120:
                continue
            lon = system.get_station()[station].location[0]
            la = system.get_station()[station].location[1]
            new_date = min_month + datetime.timedelta(month * 30)
            day = datetime.date(new_date.year, new_date.month, 6)
            if day not in system.get_station()[station].sea_level:
                colour = 'black'
            else:
                colour = get_color(system.get_station()[station].sea_level[day])
                print(colour)
            x.append(la)
            y.append(lon)
            station_name.append(f'Name of station: {station}')
            inner_lst.append(colour)
        color.append(inner_lst)
        print(color)
    return (num_station, color, dates, x, y, station_name)


def draw_figure(tup: tuple) -> None:
    num_station, color, dates, x, y, station_name = tup
    fig_dict = {
        "data": [],
        "layout": {},
        "frames": []
    }

    sliders_dict = {
        "active": 0,
        "yanchor": "top",
        "xanchor": "left",
        "currentvalue": {
            "font": {"size": 20},
            "prefix": "Months Since Recorded:",
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

    fig = go.Scattergeo(lat=x[0:num_station], lon=y[0:num_station], mode='markers', marker={'color': color[0]},
                        hovertext=station_name)

    fig_dict["data"].append(fig)

    # make frames
    for i in range(len(dates)):

        fig = go.Scattergeo(lat=x[num_station * i: num_station * i + num_station],
                            lon=y[num_station * i: num_station * i + num_station],
                            mode='markers', marker={'color': color[i]},
                            hovertext=station_name)
        frame = {"data": fig, 'name': dates[i]}

        fig_dict["frames"].append(frame)

        slider_step = {"args": [[dates[i]],
                                {"frame": {"duration": 300, "redraw": True},
                                "mode": "immediate",
                                    "transition": {"duration": 300}}],
                       "label": dates[i],
                       "method": "animate"}
        sliders_dict["steps"].append(slider_step)

    fig_dict["layout"]["sliders"] = [sliders_dict]

    fig = go.Figure(fig_dict)
    # fig = go.Figure(fig)
    fig.show()


def see_detail(station: str):
    go_plot(station)


draw_figure(graph_data_set_up())
name = input('Please type in the station name that you want to see detailed report of. Hover over it to see name.')
see_detail(name)
