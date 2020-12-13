"""The main python module that integrate the whole projects can complete all its functions.
It generates data, draw animation graph and linear regression graph."""
from graph import draw_figure, get_color
from linear_regression import go_plot
from climate_sea_level_system import ClimateSeaLevelSystem
from generates import GenerateTemperature, GenerateStationAndSeaLevel

# When having trouble opening the graph, you can uncomment the following code and try again.
# import plotly.io as pio
# pio.renderers.default = "browser"


def graph_data_set_up() -> tuple:
    """Set up all the datq for drawing the animation graph.

    It set up the color, location, name, and dates of each station as well as the total number of stations."""
    dates = []
    x = []
    y = []
    color = []
    station_name = []
    num_station = len(system.get_station())

    date_list = sorted(system.get_dates())[-360:]
    starting_date = date_list[0]

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
                colour = get_color(starting_date, station_obj, station_obj.sea_level[date])
            x.append(la)
            y.append(lon)
            station_name.append(f'Name of station: {station}')
            inner_lst.append(colour)
        color.append(inner_lst)
    return (num_station, color, dates, x, y, station_name)


def see_regression() -> None:
    """A helper function for the main function.

    On its own, it shows the linear regression of all data collected at the input station."""
    all_station = system.get_station().keys()
    station = input('Please type in the station name that you want to see detailed report of. '
                    'Hover over it to see name.')
    while station not in all_station:
        print(f'The input station name {station} is invalid, please try again.')
        station = input('Please type in the station name that you want to see detailed report of. '
                        'Hover over it to see name.')
    go_plot(station, system)


def main() -> None:
    """The main function that integrates everything in this project and show the animation graph. It also calls
    see_regression function to show the linear regression."""
    GenerateTemperature().generate(system)
    GenerateStationAndSeaLevel().generate(system)
    draw_figure(graph_data_set_up())
    while True:
        see_regression()


if __name__ == '__main__':
    # Created instances for the next two functions.
    system = ClimateSeaLevelSystem()

    # Run the main function.
    main()
