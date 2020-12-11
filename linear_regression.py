import random
import plotly.graph_objects as go
import datetime
from entities import Station, SeaLevel, Temperature
from typing import List, Callable
from generates import GenerateStationAndSeaLevel, GenerateTemperature
from climate_sea_level_system import ClimateSeaLevelSystem
import data_process

system = ClimateSeaLevelSystem()
generate_temp = GenerateTemperature()
generate_station = GenerateStationAndSeaLevel()


def generate_tempera():
    generate_temp.generate(system)


def generate_sea():
    generate_station.generate(system)


def get_compare(station=None) -> list:
    if station is None:
        new_lst = []
        lst_temp = system.get_temp()
        base_month = system.find_average_temp()
        for month in lst_temp:
            interval = (month - base_month).days
            new_lst.append((interval, lst_temp[month].temperature))
    else:
        dic = data_process.new_average(station)
        new_lst = []
        base_month = min(dic.keys())
        for month in dic:
            interval = (month - base_month).days
            new_lst.append((interval, dic[month]))

    return new_lst


def evaluate_line(a: float, b: float, error: float, x: float) -> float:
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

    >>> result = evaluate_line(5.0, 1.0, 0.5, 10.0)  # y = 5.0 + 1.0 * 10.0, with error 0.5
    >>> -0.5 <= result - 15.0 <= 0.5
    True
    """
    e = random.uniform(-error, error)
    return a + b * x + e
#
#
# # def generate_random_data(a: float, b: float, error: float, num_points: int,
# #                          x_max: float) -> list:
# #     """Return a list of num_points data points generated from the model y = a + bx,
# #     with the given error range for each point.
# #
# #     You may ASSUME that:
# #       - x_max > 0
# #       - error >= 0
# #
# #     Each x-coordinate is chosen randomly from 0 to x_max (again using
# #     random.uniform).
# #
# #     Implement this function in two steps:
# #       1. First, generate a list of random x values. You can do this using an expression
# #          of the form:
# #
# #              [ ... for _ in range(0, num_points) ]
# #
# #          See the handout for more help.
# #       2. Use those x values to generate a list of (x, y) points, using evaluate_line.
# #
# #     >>> points = generate_random_data(5.0, 1.0, 0.5, 10, 100.0)
# #     >>> len(points)
# #     10
# #     >>> first_point = points[0]
# #     >>> first_x = first_point[0]
# #     >>> first_y = first_point[1]
# #     >>> 0.0 <= first_x <= 100.0  # x-coordinate is in the right range
# #     True
# #     >>> -0.5 <= first_y - 5.0 - first_x <= 0.5
# #     True
# #     """
# #     x_values = [random.uniform(0, x_max) for _ in range(0, num_points)]
# #     return [(x, evaluate_line(a, b, error, x)) for x in x_values]


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


def calculate_r_squared(points: list, a: float, b: float) -> float:
    """Return the R squared value when the given points are modelled as the line y = a + bx.

    points is a list of pairs of numbers: [(x_1, y_1), (x_2, y_2), ...]

    Assume that:
        - points is not empty and contains tuples
        - each element of points is a tuple containing two floats

    Further reading: https://en.wikipedia.org/wiki/Coefficient_of_determination
    """
    converted_version = convert_points(points)
    average_y = find_average(converted_version[1])
    total_sum_of_squares = sum([(x[1] - average_y) ** 2 for x in points])
    residual_sum_of_squares = sum([(x[1] - (a + b * x[0])) ** 2 for x in points])
    return 1 - residual_sum_of_squares / total_sum_of_squares


def find_average(points: list) -> float:
    """Return the average of the elements in points

    >>> find_average([1, 2, 3, 4, 5])
    3.0
    >>> find_average([10, 3, 7, 6])
    6.5
    """
    return sum(points) / len(points)
#
#
# ###############################################################################
# # Helper functions for using plotly (don't change these!)
# ###############################################################################


def run_example_temp() -> tuple:
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
    points = get_compare()
    separated_coordinates = convert_points(points)
    x_coords = separated_coordinates[0]
    x_max = max(x_coords)
    y_coords = separated_coordinates[1]

    # Do a simple linear regression. Returns the (a, b) constants for
    # the line y = a + b * x.
    model = simple_linear_regression(points)
    a = model[0]
    b = model[1]

    # Plot all the data points that have been randomly generated
    plot_points(x_coords, y_coords)

    # Plot all the data points AND a line based on the regression
    plot_points_and_regression(x_coords, y_coords, a, b, x_max)

    # Calculate the r_squared value
    r_squared = calculate_r_squared(points, a, b)
    # r_squared = 0  # This is a dummy value to use until you complete calculate_r_squared
    return (a, b, r_squared)


def run_example_sea(station: str) -> tuple:
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
    generate_sea()
    points = get_compare(system.get_station()[station])
    separated_coordinates = convert_points(points)
    x_coords = separated_coordinates[0]
    x_max = max(x_coords)
    y_coords = separated_coordinates[1]

    # Do a simple linear regression. Returns the (a, b) constants for
    # the line y = a + b * x.
    model = simple_linear_regression(points)
    a = model[0]
    b = model[1]

    # Plot all the data points that have been randomly generated
    plot_points(x_coords, y_coords)

    # Plot all the data points AND a line based on the regression
    plot_points_and_regression(x_coords, y_coords, a, b, x_max)

    # Calculate the r_squared value
    r_squared = calculate_r_squared(points, a, b)
    # r_squared = 0  # This is a dummy value to use until you complete calculate_r_squared
    return (a, b, r_squared)


def plot_points(x_coords: list, y_coords: list) -> None:
    """Plot the given x- and y-coordinates using plotly. Display results in a web browser.

    x_coords is a list of floats representing the x-coordinates of the points,
    and y_coords is a list of float representing the y-coordinates of the points.
    These two lists must have the same length.

    We've provided this function for you, and you should not modify it!
    """
    # Create a blank figure
    fig = go.Figure()

    # Add the raw data
    fig.add_trace(go.Scatter(x=x_coords, y=y_coords, mode='markers', name='Data'))

    # Display the figure in a web browser.
    fig.show()


def plot_points_and_regression(x_coords: list, y_coords: list,
                               a: float, b: float, x_max: float) -> None:
    """Plot the given x- and y-coordinates and linear regression model using plotly.

    The linear regression model is the line y = a + bx.
    Like plot_points, this function displays the results in a web browser.

    Note: this function calls your evaluate_line function, so make sure that you've
    tested your evaluate_line function carefully before try to call this one.

    We've provided this function for you, and you should not modify it!
    """
    # Create a blank figure
    fig = go.Figure()

    # Add the raw data
    fig.add_trace(go.Scatter(x=x_coords, y=y_coords, mode='markers', name='Data'))

    # Add the regression line
    fig.add_trace(go.Scatter(x=[0, x_max], y=[evaluate_line(a, b, 0, 0),
                                              evaluate_line(a, b, 0, x_max)],
                             mode='lines', name='Regression line'))

    # Display the figure in a web browser
    fig.show()

