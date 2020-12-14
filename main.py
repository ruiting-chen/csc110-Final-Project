"""The main python module that integrate the whole projects can complete all its functions.
It generates data, draw animation graph and linear regression graph."""
from linear_regression import go_plot
from graph import go_figure
from climate_sea_level_system import ClimateSeaLevelSystem
from generates import GenerateTemperature, GenerateStationAndSeaLevel

# When having trouble opening the graph, you can uncomment the following code and try again.
# import plotly.io as pio
# pio.renderers.default = "browser"


def see_regression(system: ClimateSeaLevelSystem) -> None:
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
    # Created instances for the next two functions.
    system = ClimateSeaLevelSystem()

    GenerateTemperature().generate(system)
    GenerateStationAndSeaLevel().generate(system)
    go_figure(system)
    print("RED color on the graph means the current sea level/temperature anomaly value is "
          "ABOVE the original sea level/temperature")
    print("BLUE color on the graph means the current sea level/temperature anomaly value is "
          "BELOW or EQUAL to the original sea level/temperature")
    print()
    # run see_regression non-stop so you can see linear regressions as much as you would like.
    while True:
        see_regression(system)


if __name__ == '__main__':
    # Run the main function.
    # If yu don't see graphs showing, please close your browser and try again
    main()
