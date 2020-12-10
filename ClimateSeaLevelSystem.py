<<<<<<< HEAD
from __future__ import annotations
=======
from typing import Any, List, Dict
from bs4 import BeautifulSoup
import requests
import csv
import urllib.request
import datetime
from statistics import mean

url = 'http://uhslc.soest.hawaii.edu/data/fd.html'

def get_sea_level_info() -> List[List[str]]:
    """Return a list of sea level information extracted from the website we found.
    The url of the website is 'http://uhslc.soest.hawaii.edu/data/fd.html'"""
    r = requests.get('http://uhslc.soest.hawaii.edu/data/fd.html').text
    soup = BeautifulSoup(r, features="html.parser")
    info = soup.find_all('td')
    try_lst = []
    for i in range(len(info) // 12):
        new_l = []
        for j in range(0, 8):
            new_l.append(info[i * 12 + j].text)
        new_l.append(info[i * 12 + 9].find_all('a')[0].get('href'))
        try_lst.append(new_l)
    return try_lst


def process_data() -> list:
    """This function will extract sea-level data from the internet.

    This function will promote the caller to type in a station that he want to check out.
    Base on the station the user typed in, this function will extract the corresponding
    sea-level data from the internet.

    If the input station is not among the ones promoted, an InvalidStationError will occur."""
    all_data = get_sea_level_info(url)
    all_station = {}
    for lst in all_data:
        all_station[lst[2]] = lst[-1]
    station = input(f'Which station do you want to see? Choose from {list(all_station.keys())}')
    if station not in all_station:
        raise InvalidStationError

    csv_web = all_station[station]
    csv_file = urllib.request.urlopen(csv_web)
    lst_line = [line.decode('utf-8') for line in csv_file.readlines()]
    read = csv.reader(lst_line)

    lst = []
    for row in read:
        lst.append(row)
    return lst
>>>>>>> adaf391604662107080ea2e09cf6133bcc573b80

import datetime
from typing import List, Dict, Optional

# This is the Python module containing the individual entity data classes.
from entities import Temperature, Station, SeaLevel


class ClimateSeaLevelSystem:
    """A system that maintains all entities (temperature, station, and sea-level).

    Representation Invariants:
        - all(name == self._stations[name].name for name in self._stations)
    """
    # Private Instance Attributes:
    #   - _temperatures: a mapping from the date when a measure of the global
    #       temperature is made to the measurement.
    #       This represents all the temperatures in the system.
    #   - _sea_levels: a mapping from the date when a measure of the sea_level
    #       of a certain station is made to SeaLevel object.
    #       This represents all the sea-levels in the system.
    #   - _stations: a mapping from station name to Station object.
    #       This represents all the stations in the system.

    _temperatures: Dict[datetime.date, Temperature]
    _sea_levels: Dict[(datetime.date, Station), SeaLevel]
    _stations: Dict[str, Station]

    def __init__(self) -> None:
        """Initialize a new food delivery system.

        The system starts with no entities.
        """
        self._temperatures = {}
        self._sea_levels = {}
        self._stations = {}

    def add_temperature(self, temperature: Temperature) -> bool:
        """Add the given temperature to this system.

        Do NOT add the temperature if one with the same date already exists.

        Return whether the temperature was successfully added to this system.
        """
        raise NotImplementedError

    def add_sea_level(self, sea_level: SeaLevel) -> bool:
        """Add the given SeaLevel to this system.

        Do NOT add the sea_level if one with the same date and station already exists.

        Return whether the SeaLevel was successfully added to this system.
        """
        identifier = (sea_level.date, sea_level.station)
        if identifier in self._sea_levels:
            return False
        self._sea_levels[identifier] = sea_level
        return True

    def add_station(self, station: Station) -> bool:
        """Add the given station to this system.

        Do NOT add the station if one with the same name already exists.

        Return whether the station was successfully added to this system.
        """
        identifier = station.name
        if identifier in self._stations:
            return False
        self._stations[identifier] = station
        return True


if __name__ == '__main__':
    import python_ta.contracts
    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest
    doctest.testmod(verbose=True)

    # import python_ta
    # python_ta.check_all(config={
    #     'extra-imports': ['dataclasses', 'datetime', 'python_ta.contracts', 'math', 'entities'],
    #     'allowed-io': ['run_example'],
    #     'max-line-length': 100,
    #     'disable': ['R1705', 'C0200', 'R0201']
    # })
