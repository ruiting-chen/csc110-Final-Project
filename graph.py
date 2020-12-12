"""This python module contains all functions needed to draw the animation graph."""
import plotly.graph_objects as go
from generates import GenerateTemperature, GenerateStationAndSeaLevel
from climate_sea_level_system import ClimateSeaLevelSystem
from entities import Station
import datetime

system = ClimateSeaLevelSystem()
generate_temp = GenerateTemperature()
generate_station = GenerateStationAndSeaLevel()

# When having trouble opening the graph, you can uncomment the following code and try again.
# import plotly.io as pio
# pio.renderers.default = "browser"


def get_color(start_date: datetime.date, station: Station, height: float) -> str:
    """Return the colour representing the level of increasing/decreasing of the measured sea level at a station."""
    starting_height = station.sea_level[start_date]
    colors = ['blue', 'red']
    if height <= starting_height:
        return colors[0]
    else:
        return colors[1]


def draw_figure(tup: tuple) -> None:
    """The function to draw the animation graph."""
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
    fig.show()
