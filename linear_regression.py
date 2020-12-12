import plotly.graph_objects as go
from plotly.subplots import make_subplots
from generates import GenerateTemperature, GenerateStationAndSeaLevel
from climate_sea_level_system import ClimateSeaLevelSystem

# import plotly.io as pio
# pio.renderers.default = "browser"

system = ClimateSeaLevelSystem()
generate_temp = GenerateTemperature()
generate_station = GenerateStationAndSeaLevel()


def generate_tempera():
    generate_temp.generate(system)


def generate_sea(station: str):
    generate_station.generate(system, station)


# def get_compare_old(station=None) -> list:
#     if station is None:
#         new_lst = []
#         lst_temp = system.get_temp()
#         base_month = system.find_min_temp()
#         for month in lst_temp:
#             interval = (month - base_month).days
#             new_lst.append((interval, lst_temp[month].temperature, month))
#     else:
#         dic = station.sea_level
#         new_lst = []
#         base_month = min(dic.keys())
#         for month in dic:
#             interval = (month - base_month).days
#             new_lst.append((interval, dic[month], month))
#
#     return new_lst


def get_compare(station=None) -> list:
    sea_levels = station.sea_level
    temperatures = system.get_temp()

    base_month_sea = min(sea_levels.keys())
    base_month_temperature = system.find_min_temp()

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
    """Evaluate the linear function y = a + bx for the given a, b, and x values
    with the given error term.

    More precisely, this function first calculates a random number e between
    -error and error, inclusive, and then returns a + bx + e. When error == 0,
    this function simply returns a + bx.

    You may ASSUME that:
        - error >= 0

    Hint: use the random.uniform function, which takes in two numbers and
    returns a random number between them, inclusive. For example,
    random.uniform(-10, 10) returns a random number between -10 and 10.
    random.uniform(0, 0) returns 0.

    Because of the randomness, we can't specify an exact doctest, but we can
    write a doctest based on the range of possible values:

    >>> result = evaluate_line(5.0, 1.0, 10.0)  # y = 5.0 + 1.0 * 10.0, with error 0.5
    >>> -0.5 <= result - 15.0 <= 0.5
    True
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

    points is a list of pairs of floats: [(x_1, y_1), (x_2, y_2), ...]
    This function returns a pair of floats (a, b) such that the line
    y = a + bx is the approximation of this data.

    Further reading: https://en.wikipedia.org/wiki/Simple_linear_regression

    You may ASSUME that:
        - len(points) > 0
        - each element of points is a tuple of two floats

    >>> simple_linear_regression([(1.0, 1.0), (2.0, 2.0), (3.0, 3.0)])
    (0.0, 1.0)

    Hint: you might want to define a separate function that calculates the average
    of a collection of numbers.
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

    points is a list of pairs of numbers: [(x_1, y_1), (x_2, y_2), ...]

    Assume that:
        - points is not empty and contains tuples
        - each element of points is a tuple containing two floats

    Further reading: https://en.wikipedia.org/wiki/Coefficient_of_determination
    """
    average_y = find_average(converted_version[1])
    total_sum_of_squares = sum([(converted_version[1][i] - average_y) ** 2 for i in range(len(converted_version[0]))])
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


# def run_example_temp_old() -> tuple:
#     """Run an example use of the functions in this file.
#
#     Follow these example steps :
#       1. Generates some random data points.
#       2. Converts the points into the format expected by plotly.
#       3. Performs a simple linear regression on the points.
#       4. Plots the points and the line based on the regression using plotly.
#       5. Calculates the R squared value for the regression model with this data.
#       6. Returns the linear regression model and the R squared value.
#     """
#     generate_tempera()
#     points = get_compare()
#     new_points = [(tup[2], tup[1]) for tup in points]
#     separated_coordinates = convert_points(new_points)
#     x_coords = separated_coordinates[0]
#     x_min = min(x_coords)
#     x_max = max(x_coords)
#     num_tup = convert_points(points)
#     y_max = max(num_tup[0])
#     y_coords = separated_coordinates[1]
#
#     # Do a simple linear regression. Returns the (a, b) constants for
#     # the line y = a + b * x.
#     model = simple_linear_regression(points)
#     a = model[0]
#     b = model[1]
#
#     # Plot all the data points AND a line based on the regression
#     return (x_coords, y_coords, a, b, x_min, x_max, y_max, num_tup)


def run_example(station: str) -> list:
    """Run an example use of the functions in this file.

    Follow these example steps :
      1. Generates some random data points.
      2. Converts the points into the format expected by plotly.
      3. Performs a simple linear regression on the points.
      4. Plots the points and the line based on the regression using plotly.
      5. Calculates the R squared value for the regression model with this data.
      6. Returns the linear regression model and the R squared value.
    """
    generate_tempera()
    generate_sea(station)
    points_list = get_compare(system.get_station()[station])
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
    """Plot the given x- and y-coordinates and linear regression model using plotly.

    The linear regression model is the line y = a + bx.
    Like plot_points, this function displays the results in a web browser.

    Note: this function calls your evaluate_line function, so make sure that you've
    tested your evaluate_line function carefully before try to call this one.
    """
    # Create a blank figure
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add the raw data
    fig.add_trace(go.Scatter(x=tmp[0], y=tmp[1], mode='markers', marker={'color': 'yellow'}, name='Temperature Data'),
                  secondary_y=False)

    # Add the raw data
    fig.add_trace(go.Scatter(x=sea[0], y=sea[1], mode='markers', marker={'color': 'green'}, name='Sea Level Data'),
                  secondary_y=True)

    # Add the regression line
    r = calculate_r_squared(tmp[-1], tmp[2], tmp[3])
    fig.add_trace(go.Scatter(x=[tmp[4], tmp[5]], y=[evaluate_line(tmp[2], tmp[3], 0),
                                                    evaluate_line(tmp[2], tmp[3], tmp[6])],
                             mode='lines', marker={'color': 'red'},
                             name=f'Temperature Anomalies Regression line R^2 = {r}'), secondary_y=False)

    # Add the regression line
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


def go_plot(station: str) -> None:
    # temp_tup = run_example_temp()
    data = run_example(station)
    plot(data[0], data[1], station)
