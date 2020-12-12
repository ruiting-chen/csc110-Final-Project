import plotly.graph_objects as go
import datetime
from generates import GenerateTemperature, GenerateStationAndSeaLevel
from climate_sea_level_system import ClimateSeaLevelSystem
from linear_regression import go_plot
from entities import Station

system = ClimateSeaLevelSystem()
generate_temp = GenerateTemperature()
generate_station = GenerateStationAndSeaLevel()

# import plotly.io as pio
# pio.renderers.default = "browser"

def generate_tempera():
    generate_temp.generate(system)


def generate_sea():
    generate_station.generate_all(system)


def get_color(station: Station, height: float) -> str:
    interval = (station.max_height - station.min_height) / 6
    colors = ['blue', 'green', 'yellow', 'orange', 'red', 'purple']
    for i in range(1, 7):
        if height <= station.min_height + interval * i:
            return colors[i - 1]


# def graph_data_set_up_old() -> tuple:
#     generate_sea()
#     dates = []
#     x = []
#     y = []
#     color = []
#     station_name = []
#     min_mon = []
#     max_mon = []
#     for station in system.get_station():
#         if len(system.get_station()[station].sea_level.keys()) < 240:
#             continue
#         min_mon.append(min(system.get_station()[station].sea_level.keys()))
#         max_mon.append(max(system.get_station()[station].sea_level.keys()))
#
#     max_month = min(max_mon)
#     min_month = max(min_mon)
#     num_station = len(system.get_station())
#
#     for month in range((max_month - min_month).days // 30):
#         dates.append(month)
#         inner_lst = []
#         for station in system.get_station():
#             station_obj = system.get_station()[station]
#             if len(station_obj.sea_level.keys()) < 120:
#                 continue
#             lon = station_obj.location[0]
#             la = station_obj.location[1]
#             new_date = min_month + datetime.timedelta(month * 30)
#             day = datetime.date(new_date.year, new_date.month, 6)
#             if day not in station_obj.sea_level:
#                 colour = 'white'
#             else:
#                 colour = get_color(station_obj, station_obj.sea_level[day])
#                 # print(colour)
#             x.append(la)
#             y.append(lon)
#             station_name.append(f'Name of station: {station}')
#             inner_lst.append(colour)
#         color.append(inner_lst)
#         # print(color)
#     return (num_station, color, dates, x, y, station_name)


def graph_data_set_up() -> tuple:
    generate_sea()
    dates = []
    x = []
    y = []
    color = []
    station_name = []

    max_date_station = ''
    max_date = datetime.date(1800, 1, 1)
    for station in system.get_station():
        if system.get_station()[station].max_date > max_date:
            max_date_station = system.get_station()[station]

    num_station = len(system.get_station())
    date_list = sorted(max_date_station.sea_level)[-360:]
    print(date_list)
    for date in date_list:
        dates.append(f'{date.year}-{date.month}')
        inner_lst = []
        for station in system.get_station():
            station_obj = system.get_station()[station]
            lon = station_obj.location[0]
            la = station_obj.location[1]
            if date not in station_obj.sea_level:
                colour = 'white'
            else:
                colour = get_color(station_obj, station_obj.sea_level[date])
                # print(colour)
            x.append(la)
            y.append(lon)
            station_name.append(f'Name of station: {station}')
            inner_lst.append(colour)
        color.append(inner_lst)
        # print(color)
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
            "prefix": "Year and Month:",
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
