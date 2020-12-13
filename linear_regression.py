"""This python module contains all functions needed to draw the linear regression of a cretain station."""
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from entities import Station
from climate_sea_level_system import ClimateSeaLevelSystem


# When having trouble opening the graph, you can uncomment the following code and try again.
# import plotly.io as pio
# pio.renderers.default = "browser"


def get_compare(station: Station, system: ClimateSeaLevelSystem) -> list:
    """Return a list containing the temperature data and the sea level data at the input station (if any).

    The temperature data is universal, whereas the sea level data is for the input station."""
    sea_levels = station.sea_level
    temperatures = system.get_temp()

    base_month_sea = min(sea_levels.keys())
    base_month_temperature = min(temperatures.keys())

    new_lst_temp = []
    new_lst_sea = []
    for month in temperatures:
        interval_temp = (month - base_month_temperature).days
        if month in sea_levels:
            interval_sea = (month - base_month_sea).days
            new_lst_sea.append((interval_sea, sea_levels[month], month))
        new_lst_temp.append((interval_temp, temperatures[month].temperature, month))

    return [new_lst_temp, new_lst_sea]


def evaluate_line(a: float, b: float, x: float) -> float:
    """Evaluate the linear function y = a + bx for the given a, b, and x values.
    """
    return a + b * x


def convert_points(points: list) -> tuple:
    """Return a tuple of two lists, containing the x- and y-coordinates of the given points.

    Precondition:
        - points is a list of tuples, where each tuple is a list of floats.
    """
    list_of_x = [x[0] for x in points]
    list_of_y = [x[1] for x in points]
    return (list_of_x, list_of_y)


def simple_linear_regression(points: list) -> tuple:
    """Perform a linear regression on the given points.

    This function returns a pair of floats (a, b) such that the line
    y = a + bx is the approximation of this data.
    """
    converted_version = convert_points(points)
    average_x = find_average(converted_version[0])
    average_y = find_average(converted_version[1])
    b_numerator = sum([(x[0] - average_x) * (x[1] - average_y) for x in points])
    b_denominator = sum([(x[0] - average_x) ** 2 for x in points])
    b = b_numerator / b_denominator
    a = average_y - b * average_x
    return (a, b)


def calculate_r_squared(converted_version: tuple, a: float, b: float) -> float:
    """Return the R squared value when the given points are modelled as the line y = a + bx.
    """
    average_y = find_average(converted_version[1])
    total_sum_of_squares = sum([(converted_version[1][i] - average_y) ** 2
                                for i in range(len(converted_version[0]))])
    residual_sum_of_squares = sum([(converted_version[1][i] - (a + b * converted_version[0][i])) ** 2
                                   for i in range(len(converted_version[0]))])
    r = 1 - residual_sum_of_squares / total_sum_of_squares
    return float(str(r)[:5])


def find_average(points: list) -> float:
    """Return the average of the elements in points

    >>> find_average([1, 2, 3, 4, 5])
    3.0
    >>> find_average([10, 3, 7, 6])
    6.5
    """
    return sum(points) / len(points)


def extract_data(station: str, system: ClimateSeaLevelSystem) -> list:
    """Extract and process data from the input station and return a tuple containing the processed data to be used
    when drawing the linear regression.
    """
    points_list = get_compare(system.get_station()[station], system)
    graphing_data = []
    for points in points_list:
        new_points = [(tup[2], tup[1]) for tup in points]
        separated_coordinates = convert_points(new_points)
        x_coords = separated_coordinates[0]
        x_min = min(x_coords)
        x_max = max(x_coords)
        num_tup = convert_points(points)
        y_max = max(num_tup[0])
        y_coords = separated_coordinates[1]

        # Do a simple linear regression. Returns the (a, b) constants for
        # the line y = a + b * x.
        model = simple_linear_regression(points)
        a = model[0]
        b = model[1]

        # Plot all the data points AND a line based on the regression
        graphing_data.append((x_coords, y_coords, a, b, x_min, x_max, y_max, num_tup))
    return graphing_data


def plot(tmp: tuple, sea: tuple, station: str) -> None:
    """Plot the temperature and sea level data of the input station and linear regression model using plotly.

    The linear regression model is the line y = a + bx and displays the results in a web browser.
    """
    # Create a blank figure
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add the temperature data
    fig.add_trace(go.Scatter(x=tmp[0], y=tmp[1], mode='markers', marker={'color': 'yellow'}, name='Temperature Data'),
                  secondary_y=False)

    # Add the sea level data
    fig.add_trace(go.Scatter(x=sea[0], y=sea[1], mode='markers', marker={'color': 'green'}, name='Sea Level Data'),
                  secondary_y=True)

    # Add the regression line for temperature data
    r = calculate_r_squared(tmp[-1], tmp[2], tmp[3])
    fig.add_trace(go.Scatter(x=[tmp[4], tmp[5]], y=[evaluate_line(tmp[2], tmp[3], 0),
                                                    evaluate_line(tmp[2], tmp[3], tmp[6])],
                             mode='lines', marker={'color': 'red'},
                             name=f'Temperature Anomalies Regression line R^2 = {r}'), secondary_y=False)

    # Add the regression line for sea level data
    r = calculate_r_squared(sea[-1], sea[2], sea[3])
    fig.add_trace(go.Scatter(x=[sea[4], sea[5]], y=[evaluate_line(sea[2], sea[3], 0),
                                                    evaluate_line(sea[2], sea[3], sea[6])],
                             mode='lines', marker={'color': 'DarkBlue'},
                             name=f'Sea Level Regression line R^2 = {r}'), secondary_y=True)

    fig.update_layout(
        title_text=f'Station {station} Sea Level And Temperature Data'
    )

    fig.update_xaxes(title_text="Year")

    fig.update_yaxes(title_text="Temperature Anomalies", secondary_y=False)
    fig.update_yaxes(title_text="Sea Level", secondary_y=True)

    # Display the figure in a web browser
    fig.show()


def go_plot(station: str, system: ClimateSeaLevelSystem) -> None:
    """It draw the linear regression of the input station.

    The function that integrate all functions in this python module.
    """
    data = extract_data(station, system)
    plot(data[0], data[1], station)
