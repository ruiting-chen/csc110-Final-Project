from typing import Any, List, Dict, Tuple
from bs4 import BeautifulSoup
import requests
import csv
import urllib.request
import datetime
from statistics import mean

url = 'http://uhslc.soest.hawaii.edu/data/fd.html'


def get_sea_level_info(link: str) -> List[List[str]]:
    """Return a list of sea level information extracted from the given html"""
    r = requests.get(link).text
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


class InvalidStationError(Exception):
    """This exception will raise if the input station is not among the ones promoted."""

    def __str__(self):
        return 'The input station is not among the ones promoted.'


class SeaLevel:
    """Record the sea-level of a specific station at a specific date.

    Instance Variable:
        - date: The date at when the sea-level is recorded.
        - height: The recorded height of sea-level.

    Representation Invariance:
        - height > 0
    """
    date: datetime.date
    height: int

    def __init__(self, lst: List[int]):
        """Initialize a SeaLevel object"""
        if lst[3] < 0:
            return
        self.date = datetime.date(lst[0], lst[1], lst[2])
        self.height = lst[3]

    def __ge__(self, other):
        """Greater than or equal to."""
        return self.height >= other.height


class Station:
    """Record each station and its all sea-level data.

    Instance Variable:
        - sea_level: a list containing all its sea-level data at different time.
        - name: name of the station
        - location: location of the station, represented in (longitude, latitude)
    """
    sea_level: List[SeaLevel]
    # temperature
    name: str
    location: Tuple[float, float]

    def __init__(self, lst: List[List[Any]], name: str):
        self.sea_level = []
        for detail in lst:
            measure = SeaLevel(detail)
            self.sea_level.append(measure)
        self.name = name
        all_data = get_sea_level_info(url)
        for single in all_data:
            if single[2] == name:
                longitude = float(single[5])
                latitude = float(single[4])
                self.location = (longitude, latitude)

    def average(self) -> Dict[datetime.date, int]:
        """Return a dictionary containing each month of each year that have valid measurements and
         the average of all measurements during that month."""
        average = {}
        date = datetime.date(1000, 1, 1)
        height = 0
        for measure in self.sea_level:
            year_month = datetime.date(measure.date.year, measure.date.month, 1)
            if year_month not in average:
                average[year_month] = [measure.height]
            else:
                average[year_month].append(measure.height)

        for month in average:
            mean_height = mean(average[month])
            average[month] = mean_height

        return average
