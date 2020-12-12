"""TODO: Write docstring"""
import plotly.graph_objects as go
from entities import Station
import plotly.io as pio
pio.renderers.default = "browser"


def get_color(station: Station, height: float) -> str:
    """TODO: Write docstring"""
    interval = (station.max_height - station.min_height) / 6
    colors = ['blue', 'green', 'yellow', 'orange', 'red', 'purple']
    for i in range(1, 7):
        if height <= station.min_height + interval * i:
            return colors[i - 1]


def draw_figure(tup: tuple) -> None:
    """TODO: Write docstring"""
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
