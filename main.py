"""TODO: Write docstring"""
from graph import draw_figure, get_color
from linear_regression import go_plot
from climate_sea_level_system import ClimateSeaLevelSystem
from generates import GenerateTemperature, GenerateStationAndSeaLevel

system = ClimateSeaLevelSystem()
generate_temp = GenerateTemperature()
generate_station = GenerateStationAndSeaLevel()


def generate_tempera() -> None:
    """TODO: Write docstring"""
    generate_temp.generate(system)


def generate_sea() -> None:
    """TODO: Write docstring"""
    generate_station.generate(system)


def see_detail(station: str) -> None:
    """TODO: Write docstring"""
    go_plot(station)


def graph_data_set_up() -> tuple:
    """TODO: Write docstring"""
    generate_sea()
    dates = []
    x = []
    y = []
    color = []
    station_name = []

    num_station = len(system.get_station())
    date_list = sorted(system.get_dates())[-360:]
    print(len(date_list))
    for date in date_list:
        print(date)
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


def main() -> None:
    """TODO: Write docstring"""
    draw_figure(graph_data_set_up())
    print("Feel free to cal 'see_regression' if you want to see data about other stations.")
    see_regression()


def see_regression() -> None:
    """TODO: Write docstring"""
    all_station = system.get_station().keys()
    station = input('Please type in the station name that you want to see detailed report of. '
                    'Hover over it to see name.')
    while station not in all_station:
        print(f'The input station name {station} is invalid, please try again.')
        station = input('Please type in the station name that you want to see detailed report of. '
                        'Hover over it to see name.')
    see_detail(station)


if __name__ == '__main__':
    main()
