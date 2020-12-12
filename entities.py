from __future__ import annotations

from dataclasses import dataclass
import datetime
from typing import Tuple, List


@dataclass
class Temperature:
    """Store the global temperature of each month of each year which has a valid measurement.

    There are two different temperatures as described in instance variables.

    Instance Variables:
        - date: The date at when the sea-level is recorded. (data is recorded each month
        - temperature: The Global temperature anomaly of a given month"""
    date: datetime.date
    temperature: float


@dataclass
class Station:
    """Record each station and its all sea-level data.

        Instance Variable:
            - name: name of the station
            - location: location of the station, represented in (longitude, latitude)
            - sea_level: a list containing all its sea-level data at different time.
        """
    name: str
    location: Tuple[float, float]
    sea_level: dict
    min_date: datetime.date
    max_date: datetime.date
    min_height: float
    max_height: float


@dataclass
class SeaLevel:
    """Record the sea-level of a specific station at a specific date.

        Instance Variable:
            - date: The date at when the sea-level is recorded.
            - height: The recorded height of sea-level.
            - station: The name of the station at where the sea-level is measured

        Representation Invariance:
            - height > 0
        """
    date: datetime.date
    height: float
    station: str


if __name__ == '__main__':
    import python_ta.contracts
    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest
    doctest.testmod(verbose=True)

    # import python_ta
    # python_ta.check_all(config={
    #     'extra-imports': ['dataclasses', 'datetime', 'python_ta.contracts'],
    #     'max-line-length': 100,
    #     'disable': ['R1705', 'C0200']
    # })
